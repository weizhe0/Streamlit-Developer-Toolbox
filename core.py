import hashlib
import hmac
import math
import os
import re
import secrets
import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path(os.environ.get('TOOLBOX_DB_PATH', str(Path(__file__).parent / 'data' / 'toolbox.db')))


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH, timeout=20)
    db.execute('PRAGMA foreign_keys=ON')
    db.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, salt TEXT NOT NULL, digest TEXT NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, owner TEXT NOT NULL REFERENCES users(username), title TEXT NOT NULL, note TEXT NOT NULL, amount REAL NOT NULL, created TEXT DEFAULT CURRENT_TIMESTAMP)')
    return db


def register(username, password):
    username = username.strip().lower()
    if not re.fullmatch(r'[a-z0-9_]{3,30}', username):
        raise ValueError('Username: 3–30 letters, numbers, or underscores.')
    if len(password) < 12 or len(password) > 200:
        raise ValueError('Use a password between 12 and 200 characters.')
    salt = secrets.token_hex(16)
    digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=16384, r=8, p=1).hex()
    with connect() as db:
        db.execute('INSERT INTO users VALUES (?,?,?)', (username, salt, digest))
    return username


def authenticate(username, password):
    username = username.strip().lower()
    with connect() as db:
        row = db.execute('SELECT salt,digest FROM users WHERE username=?', (username,)).fetchone()
    salt, expected = row if row else ('00' * 16, '00' * 64)
    actual = hashlib.scrypt(password[:200].encode(), salt=bytes.fromhex(salt), n=16384, r=8, p=1).hex()
    return username if row and hmac.compare_digest(actual, expected) else None


def records(owner):
    with connect() as db:
        return pd.read_sql_query('SELECT id,title,note,amount,created FROM records WHERE owner=? ORDER BY id DESC', db, params=(owner,))


def save_record(owner, title, note, amount, record_id=None):
    if not title.strip() or len(title) > 200 or len(note) > 5000:
        raise ValueError('Enter a title (up to 200 characters) and a note (up to 5,000).')
    if not math.isfinite(float(amount)):
        raise ValueError('Amount must be finite.')
    with connect() as db:
        if record_id is None:
            db.execute('INSERT INTO records(owner,title,note,amount) VALUES (?,?,?,?)', (owner,title.strip(),note,amount))
        else:
            db.execute('UPDATE records SET title=?,note=?,amount=? WHERE id=? AND owner=?', (title.strip(),note,amount,record_id,owner))


def delete_record(owner, record_id):
    with connect() as db:
        db.execute('DELETE FROM records WHERE id=? AND owner=?', (record_id,owner))


def compare(po, invoice, tolerance=0.01):
    needed = ['item_code','quantity','unit_price']
    frames = []
    for label, original in [('PO',po),('Invoice',invoice)]:
        df = original.copy()
        df.columns = df.columns.astype(str).str.strip().str.lower()
        if df.columns.duplicated().any():
            raise ValueError(f'{label}: duplicate column names.')
        if not set(needed).issubset(df.columns):
            raise ValueError(f'{label} needs columns: {", ".join(needed)}')
        if df.empty:
            raise ValueError(f'{label} has no items.')
        if df['item_code'].isna().any():
            raise ValueError(f'{label}: missing item code.')
        df['item_code'] = df['item_code'].astype(str).str.strip().str.upper()
        if df['item_code'].eq('').any() or df['item_code'].duplicated().any():
            raise ValueError(f'{label}: item codes must be nonempty and unique. Combine duplicate lines before comparing.')
        for col in needed[1:]:
            df[col] = pd.to_numeric(df[col], errors='raise')
            if not df[col].map(lambda x: math.isfinite(x) and x >= 0).all():
                raise ValueError(f'{label}: {col} must contain finite, nonnegative numbers.')
        frames.append(df[needed])
    merged = frames[0].merge(frames[1], on='item_code', how='outer', suffixes=('_po','_invoice'), indicator=True)
    def status(row):
        if row['_merge'] == 'left_only':
            return 'Missing from invoice'
        if row['_merge'] == 'right_only':
            return 'Not on PO'
        issues = []
        if abs(row.quantity_po-row.quantity_invoice) > 0.000001:
            issues.append('Quantity mismatch')
        if abs(row.unit_price_po-row.unit_price_invoice) > tolerance + 1e-9:
            issues.append('Price mismatch')
        return '; '.join(issues) or 'Match'
    merged['status'] = merged.apply(status, axis=1)
    for side in ['po','invoice']:
        merged[f'total_{side}'] = merged[f'quantity_{side}'] * merged[f'unit_price_{side}']
    return merged.drop(columns='_merge')


def retrieve(pages, question, limit=6):
    terms = set(re.findall(r'\w+', question.lower()))
    chunks = []
    for page, text in pages:
        for start in range(0, len(text), 1800):
            chunk = text[start:start+2200]
            score = len(terms & set(re.findall(r'\w+', chunk.lower())))
            chunks.append((score, page, chunk))
    return sorted(chunks, key=lambda x: x[0], reverse=True)[:limit]
