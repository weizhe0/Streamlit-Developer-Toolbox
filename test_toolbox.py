import os
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

os.environ['TOOLBOX_DB_PATH'] = tempfile.mktemp(suffix='.db')
import core
import pandas as pd
from streamlit.testing.v1 import AppTest
from pathlib import Path

APP = str(Path(__file__).parent / 'streamlit_app.py')

class Tests(unittest.TestCase):
    def test_records(self):
        a = core.register('alice','a secure password')
        b = core.register('bobby','another secure password')
        self.assertEqual(core.authenticate(a,'a secure password'),a)
        self.assertIsNone(core.authenticate(a,'wrong'))
        core.save_record(a,'Private','Note',10)
        rid = int(core.records(a).iloc[0].id)
        core.save_record(b,'Attack','',0,rid)
        core.delete_record(b,rid)
        self.assertEqual(len(core.records(b)),0)
        self.assertEqual(core.records(a).iloc[0].title,'Private')
        core.delete_record(a,rid)
        self.assertEqual(len(core.records(a)),0)

    def test_comparison(self):
        po = pd.DataFrame({'item_code':['A','B','C'],'quantity':[2,1,1],'unit_price':[10,20,30]})
        inv = pd.DataFrame({'item_code':[' a ','B','D'],'quantity':[2,2,1],'unit_price':[10,25,40]})
        result = core.compare(po,inv).set_index('item_code')
        self.assertEqual(result.loc['A','status'],'Match')
        self.assertIn('Quantity mismatch',result.loc['B','status'])
        self.assertIn('Price mismatch',result.loc['B','status'])
        self.assertEqual(result.loc['C','status'],'Missing from invoice')
        self.assertEqual(result.loc['D','status'],'Not on PO')
        with self.assertRaises(ValueError):
            core.compare(pd.concat([po,po]),inv)
        po.loc[0,'quantity'] = float('inf')
        with self.assertRaises(ValueError):
            core.compare(po,inv)

    def test_pages(self):
        for page in ['Home','AI Chatbot','PDF Q&A','Invoice vs PO','Dashboard','Login & Records','Image Text Extractor','Database Manager']:
            app = AppTest.from_file(APP).run(timeout=20)
            app.sidebar.radio[0].set_value(page).run(timeout=20)
            self.assertEqual(len(app.exception),0,page)
        app = AppTest.from_file(APP).run()
        app.session_state['user'] = core.register('tester','testing password')
        app.sidebar.radio[0].set_value('Login & Records').run()
        app.text_input[0].set_value('Test record')
        next(b for b in app.button if b.label == 'Save record').click().run()
        self.assertEqual(len(core.records('tester')),1)
        app.sidebar.radio[0].set_value('Database Manager').run()
        self.assertEqual(len(app.exception),0)

    def test_mock_chat(self):
        reply = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content='Test response'))])
        with patch.dict(os.environ,{'GROQ_API_KEY':'fake-test-key'}), patch('groq.Groq') as mock:
            mock.return_value.chat.completions.create.return_value = reply
            app = AppTest.from_file(APP).run()
            app.sidebar.radio[0].set_value('AI Chatbot').run()
            app.chat_input[0].set_value('Hello').run()
            self.assertEqual(len(app.exception),0)
            self.assertEqual(app.session_state['chat'][-1]['content'],'Test response')
            args = mock.return_value.chat.completions.create.call_args.kwargs
            self.assertEqual(args['messages'][-1]['content'],'Hello')

if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        Path(os.environ['TOOLBOX_DB_PATH']).unlink(missing_ok=True)
