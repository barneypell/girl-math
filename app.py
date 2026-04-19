import html

import streamlit as st

st.set_page_config(
    page_title="Girl Math VIP Pass",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        :root {
            --paper: #fffafc;
            --pink: #f6a9c0;
            --pink-strong: #ef7fa8;
            --pink-soft: #ffdbe8;
            --green: #a9c44a;
            --pencil: #6c6872;
            --border: #c8c1c8;
        }

        .stApp {
            background: linear-gradient(180deg, #fffdfd 0%, #fff7fb 100%);
        }

        .block-container {
            max-width: 860px;
            padding-top: 1rem;
            padding-bottom: 2rem;
            padding-left: 0.9rem;
            padding-right: 0.9rem;
        }

        .main * {
            font-family: "Comic Sans MS", "Trebuchet MS", "Marker Felt", cursive, sans-serif;
        }

        h1, h2, h3 {
            color: var(--pencil);
            letter-spacing: 0.02em;
        }

        .poster {
            background: white;
            border: 1.5px solid #eee4ea;
            border-radius: 22px;
            padding: 1rem 0.95rem 1.15rem;
            box-shadow: 0 10px 30px rgba(239, 127, 168, 0.08);
        }

        .vine-row {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            margin-bottom: 0.35rem;
        }

        .vine {
            flex: 1;
            height: 7px;
            border-radius: 999px;
            background: linear-gradient(90deg, #b6d14f 0%, #9dc03d 100%);
            position: relative;
        }

        .flower {
            font-size: 1.2rem;
            line-height: 1;
        }

        .title {
            text-align: center;
            font-size: clamp(2.4rem, 9vw, 4.7rem);
            line-height: 0.95;
            font-weight: 900;
            color: #f4a9bf;
            letter-spacing: 0.08em;
            text-shadow:
                1px 1px 0 #c77c95,
                -1px 1px 0 #c77c95,
                1px -1px 0 #c77c95,
                -1px -1px 0 #c77c95;
            margin: 0.15rem 0;
        }

        .subtitle {
            text-align: center;
            color: #9d8893;
            font-size: 1.1rem;
            margin-bottom: 0.7rem;
        }

        .pearl-line {
            display: flex;
            justify-content: space-between;
            gap: 0.4rem;
            margin: 0.6rem 0 1rem;
        }

        .pearl {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: radial-gradient(circle at 35% 35%, #fff 0%, #fff 32%, #f5d8e4 65%, #ead2db 100%);
            box-shadow: 0 0 0 1px rgba(232, 194, 210, 0.45);
            flex: 1 1 auto;
            max-width: 10px;
        }

        .hero-heart {
            text-align: center;
            font-size: 2.6rem;
            margin: -0.15rem 0 0.65rem;
        }

        .paper-card {
            background: var(--paper);
            border: 1.5px solid #d8d0d7;
            border-radius: 18px;
            padding: 0.9rem;
            margin-bottom: 0.9rem;
        }

        .section-title {
            color: #6f6771;
            font-size: 1.8rem;
            margin: 0 0 0.35rem 0;
        }

        .hand-copy {
            color: var(--pencil);
            font-size: 1.05rem;
            line-height: 1.35;
        }

        .tiny-note {
            color: #8f8692;
            font-size: 0.98rem;
        }

        .comic-strip {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.45rem;
            margin-top: 0.55rem;
        }

        .comic-panel {
            min-height: 116px;
            border: 1.5px solid #cfc8cf;
            border-radius: 12px;
            padding: 0.45rem;
            background: #fff;
            color: var(--pencil);
            font-size: 0.9rem;
        }

        .comic-head {
            font-size: 1.35rem;
            text-align: center;
            margin-bottom: 0.2rem;
        }

        .gift-sticker {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 118px;
            height: 118px;
            margin: 0.35rem auto 0.5rem;
            background: radial-gradient(circle at 35% 35%, #ffbed2 0%, #f891b1 100%);
            color: white;
            font-weight: 800;
            text-align: center;
            line-height: 1.1;
            clip-path: path('M59 107 C52 98,18 84,11 58 C5 35,20 16,42 18 C52 19,58 27,59 31 C60 27,66 19,76 18 C98 16,113 35,107 58 C100 84,66 98,59 107 Z');
            filter: drop-shadow(0 3px 8px rgba(0,0,0,0.12));
        }

        .gift-caption {
            text-align: center;
            color: var(--pencil);
            font-size: 0.98rem;
        }

        .access-title {
            margin-top: 0.2rem;
            margin-bottom: 0.6rem;
            color: #6a6570;
            font-size: 1.8rem;
        }

        .section-card {
            background: white;
            border: 2px solid #ddd3da;
            border-radius: 20px;
            padding: 0.95rem;
            margin-bottom: 0.95rem;
            box-shadow: 0 6px 18px rgba(244, 169, 191, 0.08);
        }

        .section-label {
            color: #6a6570;
            font-size: 1.5rem;
            margin-bottom: 0.2rem;
        }

        .stButton > button {
            width: 100%;
            border-radius: 999px;
            border: 2px solid #e68aa9;
            background: linear-gradient(180deg, #ffb7cc 0%, #f48fb2 100%);
            color: white;
            font-weight: 800;
            padding: 0.78rem 1rem;
        }

        .stCheckbox label, .stRadio label, .stSelectbox label, .stTextInput label, .stColorPicker label {
            color: #6f6872 !important;
            font-weight: 700;
        }

        .preview-tag {
            border: 2px solid rgba(0,0,0,0.08);
            border-radius: 18px;
            padding: 1rem;
            text-align: center;
            color: white;
            font-weight: 800;
            box-shadow: 0 8px 18px rgba(0,0,0,0.1);
            margin-top: 0.4rem;
        }

        .ribbon {
            margin-top: 1rem;
            text-align: center;
            font-size: 2rem;
            color: #f39ab8;
        }

        .footer-note {
            text-align: center;
            color: #8e8691;
            margin-top: 0.15rem;
        }

        @media (max-width: 640px) {
            .block-container {
                padding-left: 0.7rem;
                padding-right: 0.7rem;
            }

            .comic-strip {
                grid-template-columns: 1fr;
            }

            .gift-sticker {
                width: 104px;
                height: 104px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if "is_vip" not in st.session_state:
    st.session_state.is_vip = False

if "snack_choices" not in st.session_state:
    st.session_state.snack_choices = {
        "Healthy Pack": False,
        "Sweet Tooth": False,
        "Lemonade": False,
        "Milkshakes": False,
    }

st.markdown("<div class='poster'>", unsafe_allow_html=True)
st.markdown(
    """
    <div class='vine-row'>
        <span class='flower'>🌸</span><div class='vine'></div><span class='flower'>🌸</span>
    </div>
    <div class='title'>VIP PASS</div>
    <div class='subtitle'>AT: Girl Math</div>
    <div class='vine-row' style='margin-top:-0.15rem;'>
        <span class='flower'>🌸</span><div class='vine'></div><span class='flower'>🌸</span>
    </div>
    <div class='pearl-line'>
        <span class='pearl'></span><span class='pearl'></span><span class='pearl'></span><span class='pearl'></span>
        <span class='pearl'></span><span class='pearl'></span><span class='pearl'></span><span class='pearl'></span>
        <span class='pearl'></span><span class='pearl'></span><span class='pearl'></span><span class='pearl'></span>
    </div>
    <div class='hero-heart'>💎💖💎</div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='paper-card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>How to get V.I.P.</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='hand-copy'>A worker will tell you how to get V.I.P. <br><span class='tiny-note'>Just ask. ☺️</span></div>",
    unsafe_allow_html=True,
)
button_text = "ASK FOR VIP STATUS" if not st.session_state.is_vip else "✨ YOU ARE NOW VIP ✨"
if st.button(button_text, use_container_width=True):
    if not st.session_state.is_vip:
        st.session_state.is_vip = True
        st.balloons()

if st.session_state.is_vip:
    st.success("VIP unlocked.")
else:
    st.info("Tap when a worker says you're ready.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='paper-card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Comic Scene</div>", unsafe_allow_html=True)
st.markdown("<div class='tiny-note'>(No one specific)</div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class='comic-strip'>
        <div class='comic-panel'>
            <div class='comic-head'>👧</div>
            That makeover is so good.<br>Where did you get it?
        </div>
        <div class='comic-panel'>
            <div class='comic-head'>💅✨</div>
            Girl Math VIP.<br>nails VIP!
        </div>
        <div class='comic-panel'>
            <div class='comic-head'>🎀💖</div>
            1 second later...<br>A VIP! wowww dress...<br>white curled hair + smile + tiara
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='paper-card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Early Gift: Sticker</div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align:center;'>
        <div class='gift-sticker'>Girl Math<br>💗</div>
        <div class='gift-caption'>To. Look. At.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='access-title'>Access To:</div>", unsafe_allow_html=True)

st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.markdown("<div class='section-label'>🥤 Snack Bar</div>", unsafe_allow_html=True)
updated_choices = {}
for label, selected in st.session_state.snack_choices.items():
    updated_choices[label] = st.checkbox(label, value=selected)
st.session_state.snack_choices = updated_choices
picked = [label for label, selected in st.session_state.snack_choices.items() if selected]
if picked:
    st.caption("Picked today: " + ", ".join(picked))
else:
    st.caption("Pick your favorites.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.markdown("<div class='section-label'>💅 Spa Treatments</div>", unsafe_allow_html=True)
spa_choice = st.radio(
    "Choose a spa moment:",
    ["Mini manicure", "Hair sparkle", "Dress-up glam", "Comics corner"],
)
st.caption(f"Today’s choice: {spa_choice}")
st.markdown("<div class='section-label' style='font-size:1.25rem; margin-top:0.6rem;'>📚 And more daily / weekly comics</div>", unsafe_allow_html=True)
st.caption("New comic scenes can be added anytime.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.markdown("<div class='section-label'>🛍️ Merch + Name Tag</div>", unsafe_allow_html=True)
merch_pick = st.selectbox(
    "Schedule in advance:",
    ["Custom name tag", "Sticker pack", "Bow accessory", "Surprise merch"],
)
name = st.text_input("Name tag name:", placeholder="Type your VIP name")
color = st.color_picker("Name tag color:", "#f48fb2")
extras = st.multiselect("Customize options:", ["Pink", "Orange", "Gems", "Hearts", "Sparkles"])
preview_name = html.escape(name.strip()) if name.strip() else "Your Name"
preview_extras = " • ".join(extras) if extras else "VIP MEMBER"
st.markdown(
    f"<div class='preview-tag' style='background:{color};'><div style='font-size:1.5rem'>{preview_name}</div><div style='margin-top:0.25rem; font-size:1rem'>{preview_extras}</div></div>",
    unsafe_allow_html=True,
)
st.caption(f"Selected merch item: {merch_pick}")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='ribbon'>💗🎀💗</div>", unsafe_allow_html=True)
st.markdown("<div class='footer-note'>Hand-drawn VIP pass style, tuned for mobile.</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
