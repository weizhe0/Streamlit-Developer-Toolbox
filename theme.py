import streamlit as st


def apply_theme():
    st.markdown(
        """
<style>
/* ---------- PAGE BACKGROUND ---------- */
.stApp {
    background:
        radial-gradient(
            ellipse at 12% 5%,
            rgba(129, 140, 248, 0.22),
            transparent 45%
        ),
        radial-gradient(
            ellipse at 95% 25%,
            rgba(56, 189, 248, 0.16),
            transparent 42%
        ),
        radial-gradient(
            ellipse at 65% 95%,
            rgba(192, 132, 252, 0.15),
            transparent 48%
        ),
        #F5F7FC;
    color: #17233D;
}

/* Leave space below Streamlit's top toolbar */
[data-testid="stMainBlockContainer"] {
    max-width: 1180px;
    padding-top: 5rem !important;
    padding-bottom: 4rem;
}

[data-testid="stHeader"] {
    background: #F5F7FC;
}

/* ---------- MAIN HEADINGS ---------- */
[data-testid="stMain"] h1 {
    color: #17233D;
    letter-spacing: -0.035em;
    font-weight: 750;
}

[data-testid="stMain"] h2,
[data-testid="stMain"] h3 {
    color: #253454;
    letter-spacing: -0.025em;
}

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {
    background: #111C35;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

/* Bright title on the dark sidebar */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] [data-testid="stIconMaterial"] {
    color: #E8EDF9 !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.15);
}

[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 0.4rem;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: 0.7rem 0.8rem;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.045);
    border: 1px solid rgba(255, 255, 255, 0.06);
    transition: background 0.15s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(129, 140, 248, 0.20);
}

[data-testid="stSidebar"] [role="radiogroup"]
label:has(input:checked) {
    background: rgba(129, 140, 248, 0.26);
    border-color: rgba(165, 180, 252, 0.55);
}

/* ---------- METRIC CARDS ---------- */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid #DDE4F2;
    border-radius: 18px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 8px 24px rgba(32, 50, 91, 0.045);
}

[data-testid="stMetricValue"] {
    color: #4F46E5;
}

/* ---------- FORMS AND FILE UPLOADS ---------- */
[data-testid="stForm"],
[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.90);
    border: 1px solid #DCE3F1;
    border-radius: 18px;
    padding: 1.2rem;
    box-shadow: 0 8px 24px rgba(32, 50, 91, 0.035);
}

[data-testid="stFileUploaderDropzone"] {
    background: #F0F3FC;
    border: 1px dashed #B9C5E3;
    border-radius: 12px;
}

/* ---------- TABLES AND EXPANDERS ---------- */
[data-testid="stDataFrame"] {
    border: 1px solid #DDE4F2;
    border-radius: 14px;
    overflow: hidden;
    background: #FFFFFF;
}

[data-testid="stExpander"] {
    border: 1px solid #DDE4F2;
    border-radius: 14px;
    background: #FFFFFF;
}

/* ---------- CHAT ---------- */
[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid #DDE4F2;
    border-radius: 18px;
    padding: 1.1rem;
}

[data-testid="stBottomBlockContainer"] {
    background: #F5F7FC;
}

/* ---------- BUTTONS ---------- */
[data-testid="stButton"] button,
[data-testid="stDownloadButton"] button,
[data-testid="stFormSubmitButton"] button {
    border-radius: 11px;
    border: 1px solid #CBD5E8;
    background: #FFFFFF;
    color: #263653;
    font-weight: 600;
    min-height: 2.7rem;
}

[data-testid="stButton"] button:hover,
[data-testid="stDownloadButton"] button:hover,
[data-testid="stFormSubmitButton"] button:hover {
    border-color: #6366F1;
    color: #4F46E5;
    background: #EEF2FF;
}

[data-testid="stFormSubmitButton"] button {
    background: #4F46E5;
    color: #FFFFFF;
    border-color: #4F46E5;
}

[data-testid="stFormSubmitButton"] button:hover {
    background: #4338CA;
    color: #FFFFFF;
    border-color: #4338CA;
}

/* Sidebar buttons need their own text colour */
[data-testid="stSidebar"] button p {
    color: #263653 !important;
}

/* Keep disabled buttons visibly disabled */
.stApp button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Keyboard focus */
.stApp button:focus-visible,
.stApp input:focus-visible {
    outline: 3px solid #A5B4FC;
    outline-offset: 2px;
}

/* ---------- TOP BANNER ---------- */
.toolbox-banner {
    background: linear-gradient(
        115deg,
        #25345F 0%,
        #4338A0 65%,
        #526AC2 100%
    );
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 22px;
    padding: 1.7rem 2rem;
    margin-bottom: 1.7rem;
    box-shadow: 0 14px 40px rgba(49, 46, 129, 0.14);
}

.toolbox-banner .eyebrow {
    font-size: 0.74rem;
    font-weight: 650;
    letter-spacing: 0.16em;
    color: #E0E7FF !important;
    margin-bottom: 0.5rem;
}

.toolbox-banner .heading {
    font-size: clamp(1.4rem, 3vw, 2rem);
    font-weight: 750;
    line-height: 1.25;
    letter-spacing: -0.025em;
    margin-bottom: 0.6rem;
    color: #FFFFFF !important;
}

.toolbox-banner .description {
    color: #E0E7FF !important;
    line-height: 1.6;
}

/* ---------- MOBILE ---------- */
@media (max-width: 640px) {
    [data-testid="stMainBlockContainer"] {
        padding-top: 4.5rem !important;
    }

    .toolbox-banner {
        padding: 1.3rem;
        border-radius: 16px;
    }
}

/* Respect reduced-motion settings */
@media (prefers-reduced-motion: reduce) {
    .stApp * {
        transition: none !important;
    }
}
</style>

<div class="toolbox-banner">
    <div class="eyebrow">MY DEVELOPER TOOLBOX</div>
    <div class="heading">Ideas into useful tools.</div>
    <div class="description">
        Explore AI, documents, data, and your personal workspace.
    </div>
</div>
        """,
        unsafe_allow_html=True,
    )