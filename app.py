import os
import re
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ==================================================
# 1. CONFIGURATION
# ==================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

st.set_page_config(
    page_title="Marketing Email Generator",
    page_icon="📧",
    layout="centered"
)


# ==================================================
# 2. PREMIUM UI DESIGN
# ==================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #f4f7fb;
    --surface: #ffffff;
    --ink: #0f172a;
    --text: #334155;
    --muted: #64748b;
    --faint: #94a3b8;
    --border: #e2e8f0;
    --border-strong: #cbd5e1;

    --teal: #0f766e;
    --teal-dark: #115e59;
    --teal-soft: #f0fdfa;
    --teal-line: #99f6e4;

    --indigo: #4f46e5;
    --indigo-dark: #4338ca;
    --indigo-soft: #eef2ff;
    --indigo-line: #c7d2fe;

    --amber: #b45309;
    --amber-soft: #fffbeb;
    --amber-line: #fde68a;

    --radius: 14px;
    --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.04), 0 2px 8px rgba(15, 23, 42, 0.04);
    --shadow-md: 0 1px 3px rgba(15, 23, 42, 0.05), 0 12px 32px rgba(15, 23, 42, 0.08);
}

/* GLOBAL THEME */
html, body, .stApp, .stApp * {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* RICH BACKGROUND: colour glows + subtle dot grid */
.stApp {
    background-color: var(--bg);
    background-image:
        /* fine dot grid */
        radial-gradient(rgba(79, 70, 229, 0.16) 1px, transparent 1.2px),
        /* colour glows */
        radial-gradient(700px 520px at 0% 0%, rgba(20, 184, 166, 0.20), transparent 65%),
        radial-gradient(760px 560px at 100% 0%, rgba(99, 102, 241, 0.20), transparent 65%),
        radial-gradient(640px 480px at 0% 100%, rgba(245, 158, 11, 0.12), transparent 65%),
        radial-gradient(760px 560px at 100% 100%, rgba(20, 184, 166, 0.16), transparent 65%),
        linear-gradient(180deg, #f3f8fb 0%, #f3f4fc 100%);
    background-size: 26px 26px, auto, auto, auto, auto, auto;
    background-attachment: fixed;
    color: var(--text);
}

/* Thin accent line across the top of the page */
.stApp:before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #0f766e, #14b8a6, #6366f1, #4f46e5);
    z-index: 999991;
}

/* Keep icon fonts intact */
.stApp [data-testid="stIconMaterial"],
.stApp .material-icons,
.stApp span[class*="material"] {
    font-family: 'Material Symbols Rounded', 'Material Icons' !important;
}

.block-container {
    max-width: 920px;
    padding-top: 3.5rem;
    padding-bottom: 3rem;
}

/* STREAMLIT CHROME */
header[data-testid="stHeader"] {
    background: transparent;
}

.stDeployButton,
div[data-testid="stToolbar"] {
    display: none;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Hide the little link icon Streamlit adds next to headings */
[data-testid="stHeaderActionElements"],
a.anchor-link,
.hero h1 a {
    display: none !important;
}

/* HERO SECTION */
.hero {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(135deg, rgba(240, 253, 250, 0.97) 0%, rgba(255, 255, 255, 1) 50%, rgba(238, 242, 255, 0.97) 100%);
    border: 1px solid var(--border);
    padding: 36px 40px 34px 44px;
    border-radius: 16px;
    margin-bottom: 40px;
    box-shadow: var(--shadow-md);
}

.hero:before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 5px;
    background: linear-gradient(180deg, #0f766e, #14b8a6 45%, #4f46e5);
}

.hero:after {
    content: "✉";
    position: absolute;
    right: 36px;
    top: 10px;
    font-size: 130px;
    color: rgba(79, 70, 229, 0.08);
    transform: rotate(-10deg);
}

.hero-tag {
    display: inline-block;
    background: var(--teal-soft);
    border: 1px solid var(--teal-line);
    border-radius: 30px;
    padding: 5px 13px;
    color: var(--teal-dark);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.3px;
    margin-bottom: 18px;
    position: relative;
    z-index: 1;
}

.hero h1 {
    color: var(--ink) !important;
    font-size: 36px !important;
    font-weight: 700 !important;
    letter-spacing: -1px;
    line-height: 1.15;
    margin: 0 0 12px 0;
    padding: 0;
    position: relative;
    z-index: 1;
}

.hero p {
    color: var(--muted) !important;
    font-size: 15.5px;
    line-height: 1.7;
    max-width: 580px;
    margin: 0;
    position: relative;
    z-index: 1;
}

.hero-chips {
    margin-top: 22px;
    position: relative;
    z-index: 1;
}

.hero-chip {
    display: inline-block;
    border-radius: 7px;
    padding: 5px 11px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 8px;
    margin-bottom: 4px;
    border: 1px solid transparent;
}

.hero-chip.c1 {
    background: var(--teal-soft);
    color: var(--teal-dark);
    border-color: var(--teal-line);
}

.hero-chip.c2 {
    background: var(--indigo-soft);
    color: var(--indigo-dark);
    border-color: var(--indigo-line);
}

.hero-chip.c3 {
    background: var(--amber-soft);
    color: var(--amber);
    border-color: var(--amber-line);
}

/* SECTION HEADINGS */
.section-heading {
    color: var(--ink);
    font-size: 21px;
    font-weight: 700;
    letter-spacing: -0.4px;
    margin-top: 4px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 11px;
}

.section-heading:before {
    content: "";
    display: inline-block;
    width: 5px;
    height: 22px;
    border-radius: 4px;
    background: linear-gradient(180deg, #14b8a6, #4f46e5);
}

.section-subtitle {
    color: var(--muted);
    font-size: 14px;
    margin-bottom: 18px;
}

/* FORM CONTAINER (single clean card) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow-md);
    padding: 14px 16px;
}

div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}

/* INPUT LABELS */
.stTextInput label,
.stSelectbox label,
.stTextInput label p,
.stSelectbox label p {
    color: var(--ink) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

/* INPUT FIELDS */
.stTextInput input {
    background: #ffffff !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 9px !important;
    color: var(--ink) !important;
    font-size: 14.5px !important;
    min-height: 44px;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.stTextInput input::placeholder {
    color: var(--faint) !important;
}

.stTextInput input:hover {
    border-color: #94a3b8 !important;
}

.stTextInput input:focus {
    border-color: var(--indigo) !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.14) !important;
}

.stTextInput div[data-baseweb="input"],
.stTextInput div[data-baseweb="base-input"] {
    background: transparent !important;
    border: none !important;
}

/* SELECT BOX */
.stSelectbox div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 9px !important;
    min-height: 44px;
    color: var(--ink) !important;
    font-size: 14.5px;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.stSelectbox div[data-baseweb="select"] > div:hover {
    border-color: #94a3b8 !important;
}

.stSelectbox div[data-baseweb="select"] > div:focus-within {
    border-color: var(--indigo) !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.14) !important;
}

/* GENERATE BUTTON */
.stFormSubmitButton button {
    background: linear-gradient(100deg, #0f766e 0%, #4f46e5 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    min-height: 50px;
    font-size: 15px !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.15), 0 8px 20px rgba(79, 70, 229, 0.20);
    transition: filter 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease;
}

.stFormSubmitButton button:hover {
    filter: brightness(1.08);
    box-shadow: 0 2px 4px rgba(15, 23, 42, 0.18), 0 12px 26px rgba(79, 70, 229, 0.28);
    transform: translateY(-1px);
}

.stFormSubmitButton button:active {
    transform: translateY(0);
}

/* EMAIL RESULTS */
.email-label {
    display: inline-block;
    padding: 4px 11px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.2px;
    margin-bottom: 16px;
    color: var(--teal-dark);
    background: var(--teal-soft);
    border: 1px solid var(--teal-line);
}

.email-label.v2 {
    color: var(--indigo-dark);
    background: var(--indigo-soft);
    border-color: var(--indigo-line);
}

.subject-box {
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
    color: var(--ink);
    font-size: 15.5px;
    font-weight: 600;
    line-height: 1.55;
    margin-bottom: 20px;
}

.subject-box:before {
    content: "SUBJECT";
    display: block;
    color: var(--teal);
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 1.3px;
    margin-bottom: 3px;
}

.subject-box.v2:before {
    color: var(--indigo);
}

/* RESULT CONTAINERS */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.email-label) {
    border: 1px solid var(--border);
    border-top: 3px solid var(--teal);
    border-radius: var(--radius);
    box-shadow: var(--shadow-md);
    padding: 22px 26px;
    margin-top: 10px;
    margin-bottom: 18px;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.email-label.v2) {
    border-top-color: var(--indigo);
}

/* EMAIL BODY TEXT */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.email-label) p {
    line-height: 1.85;
    color: var(--text);
    font-size: 14.5px;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.email-label) p strong {
    color: var(--faint);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.3px;
    text-transform: uppercase;
}

/* DOWNLOAD BUTTON */
.stDownloadButton button {
    background: var(--surface) !important;
    color: var(--indigo-dark) !important;
    border: 1px solid var(--indigo-line) !important;
    border-radius: 10px !important;
    min-height: 48px;
    font-weight: 600 !important;
    box-shadow: var(--shadow-sm);
    transition: background 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
}

.stDownloadButton button:hover {
    background: var(--indigo-soft) !important;
    border-color: var(--indigo) !important;
    transform: translateY(-1px);
}

/* DIVIDER */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 2.2rem 0 1.6rem 0 !important;
}

/* ALERTS */
div[data-testid="stAlert"] {
    border-radius: 10px;
    border: 1px solid var(--border);
}

/* SPINNER */
div[data-testid="stSpinner"] p {
    color: var(--indigo-dark) !important;
    font-weight: 500;
}

/* FOOTER */
.footer {
    text-align: center;
    border-top: 1px solid var(--border);
    padding-top: 24px;
    margin-top: 44px;
    color: var(--muted);
    font-size: 12.5px;
    line-height: 1.9;
}

.footer strong {
    letter-spacing: 1.6px;
    font-size: 12px;
    background: linear-gradient(90deg, #0f766e, #4f46e5);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
}

/* RESPONSIVE DESIGN */
@media (max-width: 700px) {
    .block-container {
        padding: 3rem 1rem 2rem;
    }

    .hero {
        padding: 26px 22px 26px 26px;
        border-radius: 14px;
    }

    .hero h1 {
        font-size: 27px !important;
    }

    .hero p {
        font-size: 14.5px;
    }

    .hero:after {
        right: 8px;
        font-size: 70px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.email-label) {
        padding: 16px;
    }
}

</style>
""", unsafe_allow_html=True)




# ==================================================
# 3. HEADER
# ==================================================

st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ AI-POWERED MARKETING TOOL</div>
    <h1>Marketing Email Studio</h1>
    <p>
        Turn your promotions into powerful customer connections.
        Create engaging, professional marketing emails for every
        festival, celebration and special offer.
    </p>
    <div class="hero-chips">
        <span class="hero-chip c1">Unique drafts</span>
        <span class="hero-chip c2">6 tone options</span>
        <span class="hero-chip c3">Ready to send</span>
    </div>
</div>
""", unsafe_allow_html=True)



# ==================================================
# 4. CHECK API KEY
# ==================================================

if not API_KEY:
    st.error("Gemini API key not found. Please check your .env file.")
    st.stop()


# ==================================================
# 5. GEMINI CLIENT
# ==================================================

@st.cache_resource
def get_client(api_key):
    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=60000,
            retry_options=types.HttpRetryOptions(
                attempts=1
            )
        )
    )


client = get_client(API_KEY)


# ==================================================
# 6. EMAIL PARSER
# ==================================================

def parse_emails(text):

    emails = []

    for number in [1, 2]:

        pattern = (
            rf"===\s*VARIANT\s+{number}\s*===\s*"
            rf"SUBJECT:\s*(.*?)\s*"
            rf"EMAIL BODY:\s*(.*?)\s*"
            rf"===\s*END VARIANT\s+{number}\s*==="
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.DOTALL
        )

        if match:
            emails.append({
                "subject": match.group(1).strip(),
                "body": match.group(2).strip()
            })

    return emails


# ==================================================
# 7. INPUT FORM
# ==================================================

st.markdown(
    '<div class="section-heading">Create Your Campaign</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    '✦ Enter your business details and let AI craft unique email campaigns.'
    '</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    with st.form("email_form"):

        col1, col2 = st.columns(2)

        with col1:
            shop_name = st.text_input(
                "Shop / Business Name",
                placeholder="Example: Fashion Hub"
            )

        with col2:
            festival = st.text_input(
                "Festival or Occasion",
                placeholder="Example: Diwali"
            )

        offer = st.text_input(
            "Promotional Offer",
            placeholder="Example: 30% discount on all products"
        )

        tone = st.selectbox(
            "Choose Your Email Tone",
            [
                "Friendly",
                "Professional",
                "Exciting",
                "Creative",
                "Persuasive",
                "Festive"
            ]
        )

        st.markdown("")

        submitted = st.form_submit_button(
            "✨ Generate My Marketing Emails",
            use_container_width=True
        )


# ==================================================
# 8. GENERATE EMAILS
# ==================================================

if submitted:

    if (
        not shop_name.strip()
        or not festival.strip()
        or not offer.strip()
    ):

        st.warning("Please complete all fields before generating emails.")

    else:

        prompt = f"""
You are an experienced professional email marketing copywriter.

Create EXACTLY TWO different, polished promotional marketing emails.

BUSINESS INFORMATION:
Business name: {shop_name}
Festival or occasion: {festival}
Promotional offer: {offer}
Required tone: {tone}

EMAIL WRITING REQUIREMENTS:

1. Write emails that look like real business marketing emails,
   not short promotional paragraphs or advertisements.

2. Each email must contain:
   - An attractive and relevant subject line.
   - A suitable customer greeting.
   - A warm, engaging opening connected to the occasion.
   - A clear explanation of the promotional offer.
   - Persuasive but natural marketing language.
   - A separate and noticeable call to action.
   - A professional closing.
   - A signature using the actual business name.

3. Keep each email approximately 100-140 words.

4. Make the two emails genuinely different in their opening,
   writing style and presentation.

5. Follow the selected tone throughout.

6. Mention the exact business name, occasion and offer.

7. Never invent additional discounts, deadlines, coupon codes,
   contact details, website links or conditions.

8. Use correct grammar, professional formatting and natural language.

9. Do not include explanations or commentary outside the emails.

FOLLOW THIS EXACT OUTPUT STRUCTURE:

===VARIANT 1===
SUBJECT:
[Write subject line]

EMAIL BODY:
Dear Valued Customer,

[Engaging opening paragraph]

[Offer and promotional details]

[Call to action]

Warm regards,
{shop_name} Team

===END VARIANT 1===

===VARIANT 2===
SUBJECT:
[Write a different subject line]

EMAIL BODY:
Dear Valued Customer,

[Different engaging opening paragraph]

[Offer and promotional details]

[Call to action]

Warm regards,
{shop_name} Team

===END VARIANT 2===
"""

        try:

            st.session_state.pop("generated_emails", None)

            with st.spinner("✨ Crafting your professional marketing emails..."):

                response_parts = []

                stream = client.models.generate_content_stream(
                    model=MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=1200
                    )
                )

                for chunk in stream:

                    if chunk.text:
                        response_parts.append(chunk.text)

                generated_text = "".join(response_parts)

            if generated_text.strip():

                st.session_state["generated_emails"] = generated_text

            else:

                st.warning("Gemini returned an empty response.")

        except Exception as e:

            error_message = str(e)

            if "503" in error_message or "UNAVAILABLE" in error_message:
                st.error(
                    "Gemini is temporarily unavailable. Please try again."
                )

            elif "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                st.error(
                    "Gemini API usage limit reached. Please try again later."
                )

            else:
                st.error("Unable to generate emails.")

            st.caption(f"Technical details: {error_message}")


# ==================================================
# 9. DISPLAY GENERATED EMAILS
# ==================================================

if st.session_state.get("generated_emails"):

    generated_text = st.session_state["generated_emails"]

    emails = parse_emails(generated_text)

    st.markdown("---")

    st.markdown(
        '<div class="section-heading">✨ Your Generated Emails</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Review your two personalized email drafts below."
    )

    if len(emails) == 2:

        for index, email in enumerate(emails, start=1):

            with st.container(border=True):

                st.markdown(
                    f'<div class="email-label v{index}">EMAIL VARIATION 0{index}</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="subject-box v{index}">{email["subject"]}</div>',
                    unsafe_allow_html=True
                )

                st.markdown("**Email Preview**")

                st.markdown(email["body"].replace("\n", "  \n"))

    else:

        st.warning(
            "The generated response could not be separated into "
            "two email cards. Showing the original AI response below."
        )

        st.markdown(generated_text)

    st.download_button(
        label="📥 Download Both Marketing Emails",
        data=generated_text,
        file_name="marketing_emails.txt",
        mime="text/plain",
        use_container_width=True
    )


# ==================================================
# 10. FOOTER
# ==================================================

st.markdown("""
<div class="footer">
    <strong>MARKETING EMAIL STUDIO</strong>
    <br>
    Intelligent email creation for modern businesses.
    <br>
    Powered by Python · Streamlit · Google Gemini AI
</div>
""", unsafe_allow_html=True)