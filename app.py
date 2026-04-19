import html
import urllib.parse

import streamlit as st


st.set_page_config(
    page_title="Girl Math VIP Pass",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed",
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


if "spa_choice" not in st.session_state:
    st.session_state.spa_choice = "Mini manicure"


def svg_data_uri(svg: str) -> str:
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)


def wobble_word_html(text: str) -> str:
    rotations = [-6, 4, -3, 5, -4, 3, -5, 4, -2, 5, -4, 3]
    lifts = [0, -5, 2, -4, 1, -3, 2, -4, 1, -2, 1, -3]
    letters = []
    i = 0
    for ch in text:
        if ch == " ":
            letters.append("<span class='space'></span>")
            continue
        letters.append(
            f"<span class='wobble-letter' style='transform: rotate({rotations[i % len(rotations)]}deg) translateY({lifts[i % len(lifts)]}px);'>{html.escape(ch)}</span>"
        )
        i += 1
    return "".join(letters)


def flower_vine_svg() -> str:
    svg = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 140" width="900" height="140">
      <defs>
        <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#dca7b8" flood-opacity="0.35"/>
        </filter>
      </defs>
      <rect width="900" height="140" fill="none"/>
      <path d="M10 70 C80 35, 150 105, 220 70 S360 40, 430 70 S570 100, 640 70 S780 35, 890 70"
            fill="none" stroke="#9fbe54" stroke-width="9" stroke-linecap="round"/>
      <path d="M110 75 C120 60, 125 50, 130 38" fill="none" stroke="#9fbe54" stroke-width="5" stroke-linecap="round"/>
      <path d="M295 68 C305 52, 307 42, 304 26" fill="none" stroke="#9fbe54" stroke-width="5" stroke-linecap="round"/>
      <path d="M495 73 C505 57, 510 44, 516 28" fill="none" stroke="#9fbe54" stroke-width="5" stroke-linecap="round"/>
      <path d="M708 72 C718 57, 724 42, 728 28" fill="none" stroke="#9fbe54" stroke-width="5" stroke-linecap="round"/>

      <ellipse cx="120" cy="48" rx="16" ry="9" fill="#b4d46a" transform="rotate(-22 120 48)"/>
      <ellipse cx="139" cy="41" rx="16" ry="9" fill="#b4d46a" transform="rotate(28 139 41)"/>
      <ellipse cx="292" cy="34" rx="16" ry="9" fill="#b4d46a" transform="rotate(-35 292 34)"/>
      <ellipse cx="313" cy="28" rx="16" ry="9" fill="#b4d46a" transform="rotate(25 313 28)"/>
      <ellipse cx="502" cy="39" rx="16" ry="9" fill="#b4d46a" transform="rotate(-25 502 39)"/>
      <ellipse cx="522" cy="31" rx="16" ry="9" fill="#b4d46a" transform="rotate(30 522 31)"/>
      <ellipse cx="717" cy="38" rx="16" ry="9" fill="#b4d46a" transform="rotate(-28 717 38)"/>
      <ellipse cx="738" cy="31" rx="16" ry="9" fill="#b4d46a" transform="rotate(24 738 31)"/>

      <g filter="url(#softShadow)">
        <g transform="translate(82 28)">
          <ellipse cx="20" cy="20" rx="13" ry="18" fill="#f7bad0"/>
          <ellipse cx="20" cy="20" rx="13" ry="18" fill="#f7bad0" transform="rotate(72 20 20)"/>
          <ellipse cx="20" cy="20" rx="13" ry="18" fill="#f7bad0" transform="rotate(144 20 20)"/>
          <ellipse cx="20" cy="20" rx="13" ry="18" fill="#f7bad0" transform="rotate(216 20 20)"/>
          <ellipse cx="20" cy="20" rx="13" ry="18" fill="#f7bad0" transform="rotate(288 20 20)"/>
          <circle cx="20" cy="20" r="8" fill="#fee7ef" stroke="#d98faa" stroke-width="1.5"/>
        </g>
        <g transform="translate(408 14)">
          <ellipse cx="20" cy="20" rx="13" ry="18" fill="#f7bad0"/>
          <ellipse cx="20" cy="20" rx="13" ry="18" fill="#f7bad0" transform="rotate(72 20 20)"/>
          <ellipse cx="20" cy="20" rx="13" ry="18" fill="#f7bad0" transform="rotate(144 20 20)"/>
          <ellipse cx="20" cy="20" rx="13" ry="18" fill="#f7bad0" transform="rotate(216 20 20)"/>
          <ellipse cx="20" cy="20" rx="13" ry="18" fill="#f7bad0" transform="rotate(288 20 20)"/>
          <circle cx="20" cy="20" r="8" fill="#fee7ef" stroke="#d98faa" stroke-width="1.5"/>
        </g>
        <g transform="translate(774 26)">
          <ellipse cx="20" cy="20" rx="13" ry="18" fill="#f7bad0"/>
          <ellipse cx="20" cy="20" rx="13" ry="18" fill="#f7bad0" transform="rotate(72 20 20)"/>
          <ellipse cx="20" cy="20" rx="13" ry="18" fill="#f7bad0" transform="rotate(144 20 20)"/>
          <ellipse cx="20" cy="20" rx="13" ry="18" fill="#f7bad0" transform="rotate(216 20 20)"/>
          <ellipse cx="20" cy="20" rx="13" ry="18" fill="#f7bad0" transform="rotate(288 20 20)"/>
          <circle cx="20" cy="20" r="8" fill="#fee7ef" stroke="#d98faa" stroke-width="1.5"/>
        </g>
      </g>
    </svg>
    """
    return svg_data_uri(svg)


FLOWER_VINE = flower_vine_svg()


STICKER_SVG = svg_data_uri(
    """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240">
      <defs>
        <radialGradient id="g" cx="35%" cy="30%" r="70%">
          <stop offset="0%" stop-color="#ffd6e5"/>
          <stop offset="100%" stop-color="#f48fb2"/>
        </radialGradient>
      </defs>
      <path d="M120 16
               L139 38 L168 23 L177 51 L209 46 L205 78 L232 92 L216 119 L236 144 L210 159
               L219 189 L188 193 L183 223 L154 213 L136 238 L112 217 L86 233 L72 205
               L42 212 L39 181 L11 171 L23 142 L7 118 L31 98 L20 70 L51 64 L54 33 L84 42 L103 18 Z"
            fill="url(#g)" stroke="#d46f95" stroke-width="6" stroke-linejoin="round"/>
      <path d="M87 104 C87 86, 102 72, 120 72 C138 72, 153 86, 153 104 C153 128, 120 149, 120 149 C120 149, 87 128, 87 104 Z"
            fill="#fff4f8" stroke="#d46f95" stroke-width="4"/>
      <text x="120" y="172" text-anchor="middle" font-size="28" font-family="Bubblegum Sans, Comic Sans MS, sans-serif" fill="#ffffff">GIRL</text>
      <text x="120" y="198" text-anchor="middle" font-size="28" font-family="Bubblegum Sans, Comic Sans MS, sans-serif" fill="#ffffff">MATH</text>
    </svg>
    """
)


GEM_CLUSTER_SVG = svg_data_uri(
    """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 120" width="300" height="120">
      <g opacity="0.96">
        <path d="M70 20 L98 48 L70 97 L42 48 Z" fill="#d8f4ff" stroke="#7bb5c9" stroke-width="4"/>
        <path d="M70 20 L42 48 L58 48 L70 34 L82 48 L98 48 Z" fill="#f6feff" stroke="#7bb5c9" stroke-width="4"/>
        <path d="M150 10 L182 42 L150 102 L118 42 Z" fill="#ffe1ee" stroke="#d98fab" stroke-width="4"/>
        <path d="M150 10 L118 42 L136 42 L150 26 L164 42 L182 42 Z" fill="#fff7fb" stroke="#d98fab" stroke-width="4"/>
        <path d="M232 26 L256 50 L232 90 L208 50 Z" fill="#fff2bb" stroke="#d1b25a" stroke-width="4"/>
        <path d="M232 26 L208 50 L220 50 L232 36 L244 50 L256 50 Z" fill="#fff9df" stroke="#d1b25a" stroke-width="4"/>
      </g>
    </svg>
    """
)


BOW_SVG = svg_data_uri(
    """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 120" width="220" height="120">
      <path d="M111 55 C90 33, 52 25, 34 36 C15 48, 25 80, 55 82 C74 83, 90 73, 111 55 Z" fill="#f5a3bf" stroke="#cf6e92" stroke-width="5"/>
      <path d="M109 55 C130 33, 168 25, 186 36 C205 48, 195 80, 165 82 C146 83, 130 73, 109 55 Z" fill="#f5a3bf" stroke="#cf6e92" stroke-width="5"/>
      <ellipse cx="110" cy="58" rx="20" ry="17" fill="#ffd8e5" stroke="#cf6e92" stroke-width="5"/>
      <path d="M97 68 L81 95" stroke="#cf6e92" stroke-width="5" stroke-linecap="round"/>
      <path d="M123 68 L139 95" stroke="#cf6e92" stroke-width="5" stroke-linecap="round"/>
    </svg>
    """
)


COMIC_STRIP_HTML = f"""
<div class='comic-grid'>
  <div class='comic-panel tilt-a'>
    <div class='comic-art'><img src="{svg_data_uri('''
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 230 140" width="230" height="140">
        <rect width="230" height="140" fill="#fffdfd"/>
        <path d="M36 38 C46 22, 84 18, 103 32 C115 40, 117 59, 105 71 C93 83, 58 82, 42 70 C30 61, 27 49, 36 38 Z" fill="#ffffff" stroke="#9b94a0" stroke-width="3"/>
        <text x="67" y="49" text-anchor="middle" font-size="14" font-family="Patrick Hand, Comic Sans MS, sans-serif" fill="#655f68">That</text>
        <text x="67" y="64" text-anchor="middle" font-size="14" font-family="Patrick Hand, Comic Sans MS, sans-serif" fill="#655f68">makeover</text>
        <text x="67" y="79" text-anchor="middle" font-size="14" font-family="Patrick Hand, Comic Sans MS, sans-serif" fill="#655f68">is so good</text>
        <circle cx="145" cy="73" r="22" fill="#ffe2b8" stroke="#887c7b" stroke-width="3"/>
        <path d="M122 68 C123 44, 170 42, 168 71" fill="#3e2a20" stroke="#3e2a20" stroke-width="3"/>
        <path d="M130 98 C136 121, 160 121, 166 98" fill="none" stroke="#887c7b" stroke-width="3"/>
        <path d="M145 95 L145 121" stroke="#887c7b" stroke-width="3"/>
        <path d="M145 110 L128 126" stroke="#887c7b" stroke-width="3"/>
        <path d="M145 110 L162 126" stroke="#887c7b" stroke-width="3"/>
      </svg>
    ''')}" alt="comic panel 1"/>
    </div>
    <div class='comic-caption'>“Where did you get it?”</div>
  </div>
  <div class='comic-panel tilt-b'>
    <div class='comic-art'><img src="{svg_data_uri('''
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 230 140" width="230" height="140">
        <rect width="230" height="140" fill="#fffdfd"/>
        <rect x="28" y="26" width="70" height="90" rx="18" fill="#ffdbe8" stroke="#d98fab" stroke-width="3"/>
        <path d="M45 42 L82 42" stroke="#d98fab" stroke-width="3" stroke-linecap="round"/>
        <path d="M45 56 L82 56" stroke="#d98fab" stroke-width="3" stroke-linecap="round"/>
        <path d="M45 70 L82 70" stroke="#d98fab" stroke-width="3" stroke-linecap="round"/>
        <path d="M45 84 L82 84" stroke="#d98fab" stroke-width="3" stroke-linecap="round"/>
        <circle cx="154" cy="73" r="22" fill="#ffe2b8" stroke="#887c7b" stroke-width="3"/>
        <path d="M132 67 C132 43, 178 45, 176 72" fill="#f0cce0" stroke="#9e8faa" stroke-width="3"/>
        <path d="M140 98 C146 121, 170 121, 176 98" fill="none" stroke="#887c7b" stroke-width="3"/>
        <path d="M154 95 L154 121" stroke="#887c7b" stroke-width="3"/>
        <path d="M154 110 L137 126" stroke="#887c7b" stroke-width="3"/>
        <path d="M154 110 L171 126" stroke="#887c7b" stroke-width="3"/>
        <path d="M119 40 C136 25, 169 21, 194 31 C208 37, 211 57, 197 65 C182 73, 146 69, 127 58 C116 51, 111 46, 119 40 Z" fill="#ffffff" stroke="#9b94a0" stroke-width="3"/>
        <text x="160" y="46" text-anchor="middle" font-size="14" font-family="Patrick Hand, Comic Sans MS, sans-serif" fill="#655f68">Girl Math</text>
        <text x="160" y="61" text-anchor="middle" font-size="14" font-family="Patrick Hand, Comic Sans MS, sans-serif" fill="#655f68">VIP!</text>
      </svg>
    ''')}" alt="comic panel 2"/>
    </div>
    <div class='comic-caption'>VIP nails and sparkle time</div>
  </div>
  <div class='comic-panel tilt-c'>
    <div class='comic-art'><img src="{svg_data_uri('''
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 230 140" width="230" height="140">
        <rect width="230" height="140" fill="#fffdfd"/>
        <circle cx="116" cy="68" r="24" fill="#ffe2b8" stroke="#887c7b" stroke-width="3"/>
        <path d="M92 66 C93 31, 141 28, 142 68" fill="#fff7b8" stroke="#cfb85c" stroke-width="3"/>
        <path d="M99 34 L104 16" stroke="#cfb85c" stroke-width="3" stroke-linecap="round"/>
        <path d="M132 34 L137 16" stroke="#cfb85c" stroke-width="3" stroke-linecap="round"/>
        <path d="M116 30 L116 12" stroke="#cfb85c" stroke-width="3" stroke-linecap="round"/>
        <path d="M101 95 C106 122, 126 122, 131 95" fill="none" stroke="#887c7b" stroke-width="3"/>
        <path d="M116 92 L116 121" stroke="#887c7b" stroke-width="3"/>
        <path d="M116 110 L99 127" stroke="#887c7b" stroke-width="3"/>
        <path d="M116 110 L133 127" stroke="#887c7b" stroke-width="3"/>
        <path d="M34 35 C51 17, 92 18, 106 32 C112 38, 108 50, 98 54 C87 59, 50 59, 36 49 C28 44, 27 39, 34 35 Z" fill="#ffffff" stroke="#9b94a0" stroke-width="3"/>
        <text x="71" y="41" text-anchor="middle" font-size="14" font-family="Patrick Hand, Comic Sans MS, sans-serif" fill="#655f68">1 second</text>
        <text x="71" y="57" text-anchor="middle" font-size="14" font-family="Patrick Hand, Comic Sans MS, sans-serif" fill="#655f68">later...</text>
        <circle cx="183" cy="38" r="12" fill="#ffdbe8" stroke="#d98fab" stroke-width="3"/>
        <circle cx="171" cy="54" r="9" fill="#d8f4ff" stroke="#7bb5c9" stroke-width="3"/>
        <circle cx="197" cy="58" r="8" fill="#fff2bb" stroke="#d1b25a" stroke-width="3"/>
      </svg>
    ''')}" alt="comic panel 3"/>
    </div>
    <div class='comic-caption'>Instant princess mode</div>
  </div>
</div>
"""


def badge_svg(name: str, color: str, extras: list[str]) -> str:
    safe_name = html.escape(name) if name else "Your Name"
    safe_line = html.escape(" • ".join(extras) if extras else "VIP MEMBER")
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 220" width="460" height="220">
      <defs>
        <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
          <feDropShadow dx="0" dy="7" stdDeviation="10" flood-color="#c97b97" flood-opacity="0.25"/>
        </filter>
      </defs>
      <g filter="url(#shadow)">
        <rect x="26" y="34" width="408" height="152" rx="28" fill="{color}" stroke="#ffffff" stroke-width="7"/>
        <rect x="38" y="46" width="384" height="128" rx="22" fill="none" stroke="rgba(255,255,255,0.55)" stroke-width="4"/>
      </g>
      <path d="M84 64 L108 88 L84 112 L60 88 Z" fill="#d8f4ff" stroke="#7bb5c9" stroke-width="4"/>
      <path d="M380 64 L404 88 L380 112 L356 88 Z" fill="#fff2bb" stroke="#d1b25a" stroke-width="4"/>
      <path d="M124 66 C124 54, 134 44, 146 44 C158 44, 168 54, 168 66 C168 84, 146 98, 146 98 C146 98, 124 84, 124 66 Z" fill="#ffdbe8" stroke="#d98fab" stroke-width="4"/>
      <path d="M292 66 C292 54, 302 44, 314 44 C326 44, 336 54, 336 66 C336 84, 314 98, 314 98 C314 98, 292 84, 292 66 Z" fill="#ffdbe8" stroke="#d98fab" stroke-width="4"/>
      <text x="230" y="114" text-anchor="middle" font-size="42" font-family="Bubblegum Sans, Comic Sans MS, sans-serif" fill="#ffffff">{safe_name}</text>
      <text x="230" y="148" text-anchor="middle" font-size="24" font-family="Patrick Hand, Comic Sans MS, sans-serif" fill="#fff7fb">{safe_line}</text>
    </svg>
    """
    return svg_data_uri(svg)


st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Bubblegum+Sans&family=Patrick+Hand&display=swap');

      :root {
        --paper: #fffafc;
        --paper-2: #fff5f9;
        --ink: #6e6670;
        --pink: #f4a9bf;
        --pink-dark: #ce7897;
        --pink-soft: #ffdbe8;
        --mint: #dff6f5;
        --green: #a7c64c;
        --line: #d8cfd7;
      }

      .stApp {
        background: linear-gradient(180deg, #fffdfd 0%, #fff8fb 100%);
      }

      .block-container {
        max-width: 820px;
        padding-top: 0.85rem;
        padding-bottom: 2rem;
        padding-left: 0.75rem;
        padding-right: 0.75rem;
      }

      .main * {
        color: var(--ink);
      }

      .poster-wrap {
        background: linear-gradient(180deg, #ffffff 0%, #fffafd 100%);
        border: 2px solid #f1e7ee;
        border-radius: 28px;
        padding: 0.9rem 0.8rem 1rem;
        box-shadow: 0 16px 40px rgba(223, 156, 183, 0.12);
      }

      .doodle-vine {
        width: 100%;
        margin: 0.1rem auto 0.25rem;
      }

      .wobble-title {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        flex-wrap: wrap;
        gap: 0.05rem;
        margin-top: 0.1rem;
        margin-bottom: 0.15rem;
      }

      .wobble-letter {
        display: inline-block;
        font-family: 'Bubblegum Sans', 'Comic Sans MS', sans-serif;
        font-size: clamp(2.6rem, 10vw, 5rem);
        line-height: 0.9;
        color: var(--pink);
        text-shadow:
          -2px -2px 0 var(--pink-dark),
           2px -2px 0 var(--pink-dark),
          -2px  2px 0 var(--pink-dark),
           2px  2px 0 var(--pink-dark),
           0    5px 0 rgba(255,255,255,0.65);
      }

      .space {
        width: 0.7rem;
      }

      .subtitle {
        text-align: center;
        font-family: 'Patrick Hand', 'Comic Sans MS', cursive;
        font-size: 1.38rem;
        letter-spacing: 0.03em;
        color: #918792;
        margin-bottom: 0.45rem;
      }

      .pearl-row {
        display: flex;
        justify-content: center;
        flex-wrap: nowrap;
        gap: 0.32rem;
        margin: 0.55rem 0 0.65rem;
      }

      .pearl {
        width: 11px;
        height: 11px;
        border-radius: 50%;
        background: radial-gradient(circle at 35% 35%, #fff 0%, #fff 32%, #f9e7ef 65%, #ebd1dc 100%);
        box-shadow: 0 0 0 1px rgba(218, 190, 204, 0.55);
      }

      .tiny-doodles {
        display: flex;
        justify-content: center;
        margin-bottom: 0.25rem;
      }

      .paper-card, .section-card {
        background: linear-gradient(180deg, var(--paper) 0%, var(--paper-2) 100%);
        border: 2px solid var(--line);
        border-radius: 22px;
        padding: 1rem 0.9rem;
        box-shadow: 0 10px 24px rgba(228, 174, 196, 0.08);
        margin-bottom: 0.95rem;
      }

      .paper-card {
        transform: rotate(-0.35deg);
      }

      .section-card:nth-of-type(odd) {
        transform: rotate(0.2deg);
      }

      .section-card:nth-of-type(even) {
        transform: rotate(-0.15deg);
      }

      .card-title {
        font-family: 'Bubblegum Sans', 'Comic Sans MS', sans-serif;
        font-size: 1.95rem;
        line-height: 1;
        color: #7a7078;
        margin-bottom: 0.35rem;
      }

      .hand-copy, .comic-caption, .mini-note, .footer-note {
        font-family: 'Patrick Hand', 'Comic Sans MS', cursive;
        font-size: 1.18rem;
        line-height: 1.2;
      }

      .mini-note {
        color: #978d97;
      }

      .comic-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.7rem;
        margin-top: 0.65rem;
      }

      .comic-panel {
        background: #fffefe;
        border: 2px solid #d5ccd4;
        border-radius: 18px;
        padding: 0.45rem 0.45rem 0.55rem;
      }

      .tilt-a { transform: rotate(-1.2deg); }
      .tilt-b { transform: rotate(0.9deg); }
      .tilt-c { transform: rotate(-0.75deg); }

      .comic-art img {
        width: 100%;
        display: block;
        border-radius: 12px;
      }

      .comic-caption {
        text-align: center;
        margin-top: 0.2rem;
      }

      .sticker-wrap {
        display: grid;
        grid-template-columns: 180px 1fr;
        gap: 0.75rem;
        align-items: center;
      }

      .sticker-wrap img, .bow-row img, .gem-row img, .badge-image img {
        width: 100%;
        display: block;
      }

      .access-title {
        font-family: 'Bubblegum Sans', 'Comic Sans MS', sans-serif;
        font-size: 2.25rem;
        color: #7a7078;
        text-align: center;
        margin: 0.25rem 0 0.7rem;
      }

      .decor-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.65rem;
        margin: 0.15rem 0 0.65rem;
      }

      .bow-row, .gem-row {
        background: #fff;
        border: 2px dashed #e7c8d5;
        border-radius: 18px;
        padding: 0.35rem 0.7rem;
      }

      .field-caption {
        font-family: 'Patrick Hand', 'Comic Sans MS', cursive;
        font-size: 1.1rem;
        color: #938892;
      }

      .stButton > button {
        width: 100%;
        border-radius: 999px;
        border: 2px solid #df84a5;
        background: linear-gradient(180deg, #ffc1d3 0%, #f598b8 100%);
        color: white !important;
        font-family: 'Bubblegum Sans', 'Comic Sans MS', sans-serif;
        font-size: 1.12rem;
        letter-spacing: 0.03em;
        padding: 0.78rem 1rem;
        box-shadow: 0 8px 16px rgba(230, 137, 171, 0.25);
      }

      .stTextInput label, .stColorPicker label, .stSelectbox label,
      .stMultiSelect label, .stCheckbox label, .stRadio label {
        font-family: 'Patrick Hand', 'Comic Sans MS', cursive !important;
        font-size: 1.08rem !important;
        color: #756c76 !important;
      }

      .badge-shell {
        background: #fff;
        border: 2px dashed #e4c5d4;
        border-radius: 20px;
        padding: 0.7rem;
      }

      .badge-image {
        max-width: 100%;
      }

      .footer-note {
        text-align: center;
        color: #8f8590;
        margin-top: 0.2rem;
      }

      @media (max-width: 680px) {
        .comic-grid,
        .decor-row,
        .sticker-wrap {
          grid-template-columns: 1fr;
        }

        .poster-wrap {
          padding-left: 0.7rem;
          padding-right: 0.7rem;
        }

        .subtitle {
          font-size: 1.2rem;
        }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown("<div class='poster-wrap'>", unsafe_allow_html=True)
st.markdown(f"<img class='doodle-vine' src='{FLOWER_VINE}' alt='flower vine divider' />", unsafe_allow_html=True)
st.markdown(
    f"<div class='wobble-title'>{wobble_word_html('VIP PASS')}</div>",
    unsafe_allow_html=True,
)
st.markdown("<div class='subtitle'>AT: Girl Math Hair Salon</div>", unsafe_allow_html=True)
st.markdown(f"<img class='doodle-vine' src='{FLOWER_VINE}' alt='flower vine divider' />", unsafe_allow_html=True)
st.markdown(
    "<div class='pearl-row'>" + "".join("<span class='pearl'></span>" for _ in range(19)) + "</div>",
    unsafe_allow_html=True,
)
st.markdown(f"<div class='tiny-doodles'><img src='{GEM_CLUSTER_SVG}' alt='gems' style='max-width:220px;'/></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<div class='paper-card'>", unsafe_allow_html=True)
st.markdown("<div class='card-title'>How to get V.I.P.</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='hand-copy'>A worker will tell you how to get V.I.P.<br><span class='mini-note'>Just ask and they can upgrade you.</span></div>",
    unsafe_allow_html=True,
)
button_text = "ASK FOR VIP STATUS" if not st.session_state.is_vip else "YOU ARE NOW VIP"
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
st.markdown("<div class='card-title'>Comic Scene</div>", unsafe_allow_html=True)
st.markdown("<div class='mini-note'>(No one specific)</div>", unsafe_allow_html=True)
st.markdown(COMIC_STRIP_HTML, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<div class='paper-card'>", unsafe_allow_html=True)
st.markdown("<div class='card-title'>Early Gift: Sticker</div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div class='sticker-wrap'>
      <div><img src='{STICKER_SVG}' alt='girl math sticker'/></div>
      <div>
        <div class='hand-copy'>A handmade-style sticker, just like the drawing.</div>
        <div class='mini-note'>To. Look. At.</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<div class='access-title'>Access To:</div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div class='decor-row'>
      <div class='bow-row'><img src='{BOW_SVG}' alt='pink bow'/></div>
      <div class='gem-row'><img src='{GEM_CLUSTER_SVG}' alt='gem cluster'/></div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.markdown("<div class='card-title'>Snack Bar</div>", unsafe_allow_html=True)
st.markdown("<div class='field-caption'>Pick today’s favorites.</div>", unsafe_allow_html=True)
updated_choices = {}
for label, selected in st.session_state.snack_choices.items():
    updated_choices[label] = st.checkbox(label, value=selected)
st.session_state.snack_choices = updated_choices
picked = [label for label, selected in st.session_state.snack_choices.items() if selected]
st.caption("Picked today: " + ", ".join(picked) if picked else "Picked today: none yet")
st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.markdown("<div class='card-title'>Spa Treatments + Weekly Comics</div>", unsafe_allow_html=True)
st.markdown("<div class='field-caption'>Choose a spa moment.</div>", unsafe_allow_html=True)
st.session_state.spa_choice = st.radio(
    "Choose a spa moment:",
    ["Mini manicure", "Hair sparkle", "Dress-up glam", "Comics corner"],
    index=["Mini manicure", "Hair sparkle", "Dress-up glam", "Comics corner"].index(st.session_state.spa_choice),
)
st.caption(f"Today’s choice: {st.session_state.spa_choice}")
st.markdown("<div class='mini-note'>New comic scenes can be dropped in daily or weekly.</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)


st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.markdown("<div class='card-title'>Merch + Name Tag</div>", unsafe_allow_html=True)
merch_pick = st.selectbox(
    "Schedule in advance:",
    ["Custom name tag", "Sticker pack", "Bow accessory", "Surprise merch"],
)
name = st.text_input("Name tag name:", placeholder="Type your VIP name")
color = st.color_picker("Name tag color:", "#f598b8")
extras = st.multiselect("Customize options:", ["Pink", "Orange", "Gems", "Hearts", "Sparkles"])
st.markdown(
    f"<div class='badge-shell'><div class='badge-image'><img src='{badge_svg(name.strip(), color, extras)}' alt='custom badge preview' /></div></div>",
    unsafe_allow_html=True,
)
st.caption(f"Selected merch item: {merch_pick}")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='footer-note'>Hand-drawn VIP pass look, tuned for phones and ready to deploy.</div>", unsafe_allow_html=True)
