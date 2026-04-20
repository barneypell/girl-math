from __future__ import annotations

import html
import json
import secrets
import sqlite3
import string
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Girl Math VIP Pass",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed",
)


DB_PATH = Path(__file__).with_name("girl_math.db")
DEFAULT_SNACK_CHOICES = ["Healthy Pack", "Sweet Tooth", "Lemonade", "Milkshakes"]
DEFAULT_SPA_CHOICES = ["Mini manicure", "Hair sparkle", "Dress-up glam", "Comics corner"]
DEFAULT_MERCH_CHOICES = ["Custom name tag", "Sticker pack", "Bow accessory", "Surprise merch"]
DEFAULT_EXTRA_CHOICES = ["Pink", "Orange", "Gems", "Hearts", "Sparkles"]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS vip_passes (
                passcode TEXT PRIMARY KEY,
                member_name TEXT NOT NULL DEFAULT '',
                contact_email TEXT NOT NULL DEFAULT '',
                badge_name TEXT NOT NULL DEFAULT '',
                badge_color TEXT NOT NULL DEFAULT '#f598b8',
                snack_json TEXT NOT NULL DEFAULT '{}',
                spa_choice TEXT NOT NULL DEFAULT 'Mini manicure',
                merch_pick TEXT NOT NULL DEFAULT 'Custom name tag',
                extras_json TEXT NOT NULL DEFAULT '[]',
                is_vip INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        columns = {row[1] for row in conn.execute("PRAGMA table_info(vip_passes)")}
        if "contact_email" not in columns:
            conn.execute("ALTER TABLE vip_passes ADD COLUMN contact_email TEXT NOT NULL DEFAULT ''")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS pass_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                passcode TEXT NOT NULL,
                event_type TEXT NOT NULL,
                details TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL
            )
            """
        )


init_db()


def normalize_passcode(value: str) -> str:
    return "".join(ch for ch in value.upper().strip() if ch.isalnum())[:8]


def normalize_email(value: str) -> str:
    return value.strip().lower()


def generate_passcode(length: int = 6) -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    while True:
        passcode = "".join(secrets.choice(alphabet) for _ in range(length))
        if not get_pass(passcode):
            return passcode



def default_pass_record(member_name: str = "") -> dict:
    return {
        "passcode": "",
        "member_name": member_name,
        "contact_email": "",
        "badge_name": member_name,
        "badge_color": "#f598b8",
        "snack_json": json.dumps({label: False for label in DEFAULT_SNACK_CHOICES}),
        "spa_choice": DEFAULT_SPA_CHOICES[0],
        "merch_pick": DEFAULT_MERCH_CHOICES[0],
        "extras_json": json.dumps([]),
        "is_vip": 0,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }



def log_event(passcode: str, event_type: str, details: str = "") -> None:
    code = normalize_passcode(passcode)
    if not code:
        return
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO pass_events (passcode, event_type, details, created_at) VALUES (?, ?, ?, ?)",
            (code, event_type, details.strip(), utc_now_iso()),
        )



def create_pass(member_name: str = "", contact_email: str = "") -> dict:
    record = default_pass_record(member_name=member_name.strip())
    record["passcode"] = generate_passcode()
    record["contact_email"] = normalize_email(contact_email)
    record["badge_name"] = record["member_name"]
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO vip_passes (
                passcode, member_name, contact_email, badge_name, badge_color,
                snack_json, spa_choice, merch_pick, extras_json,
                is_vip, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["passcode"],
                record["member_name"],
                record["contact_email"],
                record["badge_name"],
                record["badge_color"],
                record["snack_json"],
                record["spa_choice"],
                record["merch_pick"],
                record["extras_json"],
                record["is_vip"],
                record["created_at"],
                record["updated_at"],
            ),
        )
    log_event(record["passcode"], "created", f"Created pass for {record['member_name'] or 'VIP member'}")
    return get_pass(record["passcode"])



def get_pass(passcode: str) -> dict | None:
    code = normalize_passcode(passcode)
    if not code:
        return None
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM vip_passes WHERE passcode = ?", (code,)).fetchone()
    return dict(row) if row else None



def save_pass(record: dict) -> None:
    payload = {
        "passcode": normalize_passcode(record.get("passcode", "")),
        "member_name": record.get("member_name", "").strip(),
        "contact_email": normalize_email(record.get("contact_email", "")),
        "badge_name": record.get("badge_name", "").strip(),
        "badge_color": record.get("badge_color", "#f598b8"),
        "snack_json": json.dumps(record.get("snacks", {})),
        "spa_choice": record.get("spa_choice", DEFAULT_SPA_CHOICES[0]),
        "merch_pick": record.get("merch_pick", DEFAULT_MERCH_CHOICES[0]),
        "extras_json": json.dumps(record.get("extras", [])),
        "is_vip": 1 if record.get("is_vip") else 0,
        "created_at": record.get("created_at") or utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    existing = get_pass(payload["passcode"])
    tracked_fields = [
        "member_name",
        "contact_email",
        "badge_name",
        "badge_color",
        "snack_json",
        "spa_choice",
        "merch_pick",
        "extras_json",
        "is_vip",
    ]
    changed_fields = [field for field in tracked_fields if str((existing or {}).get(field, "")) != str(payload[field])]
    if existing and not changed_fields:
        return
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO vip_passes (
                passcode, member_name, contact_email, badge_name, badge_color,
                snack_json, spa_choice, merch_pick, extras_json,
                is_vip, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(passcode) DO UPDATE SET
                member_name = excluded.member_name,
                contact_email = excluded.contact_email,
                badge_name = excluded.badge_name,
                badge_color = excluded.badge_color,
                snack_json = excluded.snack_json,
                spa_choice = excluded.spa_choice,
                merch_pick = excluded.merch_pick,
                extras_json = excluded.extras_json,
                is_vip = excluded.is_vip,
                updated_at = excluded.updated_at
            """,
            (
                payload["passcode"],
                payload["member_name"],
                payload["contact_email"],
                payload["badge_name"],
                payload["badge_color"],
                payload["snack_json"],
                payload["spa_choice"],
                payload["merch_pick"],
                payload["extras_json"],
                payload["is_vip"],
                payload["created_at"],
                payload["updated_at"],
            ),
        )
    event_type = "updated" if existing else "created"
    detail_text = ", ".join(changed_fields) if changed_fields else "initial save"
    log_event(payload["passcode"], event_type, detail_text)



def stats() -> dict:
    today = datetime.now(timezone.utc).date().isoformat()
    with get_conn() as conn:
        total_passes = conn.execute("SELECT COUNT(*) FROM vip_passes").fetchone()[0]
        vip_count = conn.execute("SELECT COUNT(*) FROM vip_passes WHERE is_vip = 1").fetchone()[0]
        today_count = conn.execute(
            "SELECT COUNT(*) FROM vip_passes WHERE substr(created_at, 1, 10) = ?",
            (today,),
        ).fetchone()[0]
    return {"total_passes": total_passes, "vip_count": vip_count, "today_count": today_count}



def list_passes_for_email(email: str) -> list[dict]:
    normalized = normalize_email(email)
    if not normalized:
        return []
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM vip_passes
            WHERE contact_email = ?
            ORDER BY updated_at DESC
            """,
            (normalized,),
        ).fetchall()
    return [dict(row) for row in rows]



def recent_events(passcode: str | None = None, limit: int = 12) -> list[dict]:
    with get_conn() as conn:
        if passcode:
            rows = conn.execute(
                """
                SELECT *
                FROM pass_events
                WHERE passcode = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (normalize_passcode(passcode), limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT *
                FROM pass_events
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
    return [dict(row) for row in rows]



def search_passes(query: str = "", limit: int = 20) -> list[dict]:
    cleaned = query.strip()
    with get_conn() as conn:
        if cleaned:
            like = f"%{cleaned.lower()}%"
            rows = conn.execute(
                """
                SELECT *
                FROM vip_passes
                WHERE lower(passcode) LIKE ?
                   OR lower(member_name) LIKE ?
                   OR lower(contact_email) LIKE ?
                ORDER BY updated_at DESC
                LIMIT ?
                """,
                (like, like, like, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM vip_passes ORDER BY updated_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
    return [dict(row) for row in rows]



def parse_snacks(record: dict | None) -> dict[str, bool]:
    base = {label: False for label in DEFAULT_SNACK_CHOICES}
    if not record:
        return base
    try:
        loaded = json.loads(record.get("snack_json", "{}"))
    except (TypeError, json.JSONDecodeError):
        loaded = {}
    for label in DEFAULT_SNACK_CHOICES:
        base[label] = bool(loaded.get(label, False))
    return base



def parse_extras(record: dict | None) -> list[str]:
    if not record:
        return []
    try:
        loaded = json.loads(record.get("extras_json", "[]"))
    except (TypeError, json.JSONDecodeError):
        loaded = []
    return [item for item in loaded if item in DEFAULT_EXTRA_CHOICES]



def human_time(iso_value: str | None) -> str:
    if not iso_value:
        return "just now"
    try:
        dt = datetime.fromisoformat(iso_value.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    except ValueError:
        return iso_value



def apply_record_to_state(record: dict) -> None:
    st.session_state.current_passcode = record["passcode"]
    st.session_state.record_created_at = record.get("created_at", utc_now_iso())
    st.session_state.record_updated_at = record.get("updated_at", utc_now_iso())
    st.session_state.member_name = record.get("member_name", "")
    st.session_state.contact_email = record.get("contact_email", "")
    st.session_state.badge_name = record.get("badge_name", record.get("member_name", ""))
    st.session_state.badge_color = record.get("badge_color", "#f598b8")
    st.session_state.is_vip = bool(record.get("is_vip", 0))
    st.session_state.spa_choice = record.get("spa_choice", DEFAULT_SPA_CHOICES[0])
    st.session_state.merch_pick = record.get("merch_pick", DEFAULT_MERCH_CHOICES[0])
    st.session_state.badge_extras = parse_extras(record)
    for label, selected in parse_snacks(record).items():
        st.session_state[f"snack::{label}"] = selected
    try:
        st.query_params["pass"] = record["passcode"]
    except Exception:
        pass



def load_pass_into_state(passcode: str) -> bool:
    record = get_pass(passcode)
    if not record:
        return False
    apply_record_to_state(record)
    log_event(record["passcode"], "opened", "Pass opened from app")
    return True



def clear_current_pass() -> None:
    st.session_state.current_passcode = ""
    st.session_state.record_created_at = ""
    st.session_state.record_updated_at = ""
    st.session_state.member_name = ""
    st.session_state.contact_email = ""
    st.session_state.badge_name = ""
    st.session_state.badge_color = "#f598b8"
    st.session_state.is_vip = False
    st.session_state.spa_choice = DEFAULT_SPA_CHOICES[0]
    st.session_state.merch_pick = DEFAULT_MERCH_CHOICES[0]
    st.session_state.badge_extras = []
    for label in DEFAULT_SNACK_CHOICES:
        st.session_state[f"snack::{label}"] = False
    try:
        if "pass" in st.query_params:
            del st.query_params["pass"]
    except Exception:
        pass



def current_record_payload() -> dict:
    return {
        "passcode": st.session_state.get("current_passcode", ""),
        "created_at": st.session_state.get("record_created_at", utc_now_iso()),
        "member_name": st.session_state.get("member_name", "").strip(),
        "contact_email": normalize_email(st.session_state.get("contact_email", "")),
        "badge_name": st.session_state.get("badge_name", "").strip(),
        "badge_color": st.session_state.get("badge_color", "#f598b8"),
        "snacks": {label: bool(st.session_state.get(f"snack::{label}", False)) for label in DEFAULT_SNACK_CHOICES},
        "spa_choice": st.session_state.get("spa_choice", DEFAULT_SPA_CHOICES[0]),
        "merch_pick": st.session_state.get("merch_pick", DEFAULT_MERCH_CHOICES[0]),
        "extras": st.session_state.get("badge_extras", []),
        "is_vip": bool(st.session_state.get("is_vip", False)),
    }



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
      <path d="M120 16 L139 38 L168 23 L177 51 L209 46 L205 78 L232 92 L216 119 L236 144 L210 159 L219 189 L188 193 L183 223 L154 213 L136 238 L112 217 L86 233 L72 205 L42 212 L39 181 L11 171 L23 142 L7 118 L31 98 L20 70 L51 64 L54 33 L84 42 L103 18 Z"
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
    ''')}" alt="comic panel 1"/></div>
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
    ''')}" alt="comic panel 2"/></div>
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
    ''')}" alt="comic panel 3"/></div>
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


for key, default_value in {
    "current_passcode": "",
    "record_created_at": "",
    "record_updated_at": "",
    "member_name": "",
    "contact_email": "",
    "badge_name": "",
    "badge_color": "#f598b8",
    "is_vip": False,
    "spa_choice": DEFAULT_SPA_CHOICES[0],
    "merch_pick": DEFAULT_MERCH_CHOICES[0],
    "badge_extras": [],
    "recover_email_input": "",
    "admin_search": "",
}.items():
    st.session_state.setdefault(key, default_value)

for label in DEFAULT_SNACK_CHOICES:
    st.session_state.setdefault(f"snack::{label}", False)

query_pass = normalize_passcode(st.query_params.get("pass", "")) if hasattr(st, "query_params") else ""
if query_pass and query_pass != st.session_state.get("current_passcode"):
    load_pass_into_state(query_pass)


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
        --line: #d8cfd7;
      }
      .stApp { background: linear-gradient(180deg, #fffdfd 0%, #fff8fb 100%); }
      .block-container { max-width: 860px; padding-top: 0.85rem; padding-bottom: 2rem; padding-left: 0.75rem; padding-right: 0.75rem; }
      .main * { color: var(--ink); }
      .poster-wrap { background: linear-gradient(180deg, #ffffff 0%, #fffafd 100%); border: 2px solid #f1e7ee; border-radius: 28px; padding: 0.9rem 0.8rem 1rem; box-shadow: 0 16px 40px rgba(223, 156, 183, 0.12); }
      .doodle-vine { width: 100%; margin: 0.1rem auto 0.25rem; }
      .wobble-title { display: flex; justify-content: center; align-items: flex-end; flex-wrap: wrap; gap: 0.05rem; margin-top: 0.1rem; margin-bottom: 0.15rem; }
      .wobble-letter { display: inline-block; font-family: 'Bubblegum Sans', 'Comic Sans MS', sans-serif; font-size: clamp(2.6rem, 10vw, 5rem); line-height: 0.9; color: var(--pink); text-shadow: -2px -2px 0 var(--pink-dark), 2px -2px 0 var(--pink-dark), -2px 2px 0 var(--pink-dark), 2px 2px 0 var(--pink-dark), 0 5px 0 rgba(255,255,255,0.65); }
      .space { width: 0.7rem; }
      .subtitle { text-align: center; font-family: 'Patrick Hand', 'Comic Sans MS', cursive; font-size: 1.38rem; letter-spacing: 0.03em; color: #918792; margin-bottom: 0.45rem; }
      .pearl-row { display: flex; justify-content: center; flex-wrap: nowrap; gap: 0.32rem; margin: 0.55rem 0 0.65rem; }
      .pearl { width: 11px; height: 11px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #fff 0%, #fff 32%, #f9e7ef 65%, #ebd1dc 100%); box-shadow: 0 0 0 1px rgba(218, 190, 204, 0.55); }
      .tiny-doodles { display: flex; justify-content: center; margin-bottom: 0.25rem; }
      .paper-card, .section-card, .status-card { background: linear-gradient(180deg, var(--paper) 0%, var(--paper-2) 100%); border: 2px solid var(--line); border-radius: 22px; padding: 1rem 0.9rem; box-shadow: 0 10px 24px rgba(228, 174, 196, 0.08); margin-bottom: 0.95rem; }
      .paper-card { transform: rotate(-0.35deg); }
      .section-card:nth-of-type(odd) { transform: rotate(0.2deg); }
      .section-card:nth-of-type(even) { transform: rotate(-0.15deg); }
      .card-title { font-family: 'Bubblegum Sans', 'Comic Sans MS', sans-serif; font-size: 1.95rem; line-height: 1; color: #7a7078; margin-bottom: 0.35rem; }
      .hand-copy, .comic-caption, .mini-note, .footer-note, .field-caption { font-family: 'Patrick Hand', 'Comic Sans MS', cursive; font-size: 1.18rem; line-height: 1.2; }
      .mini-note { color: #978d97; }
      .status-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.65rem; margin-top: 0.6rem; }
      .status-pill { background: #fff; border: 2px dashed #e7c8d5; border-radius: 18px; padding: 0.7rem; text-align: center; }
      .status-number { font-family: 'Bubblegum Sans', 'Comic Sans MS', sans-serif; font-size: 2rem; color: #d57b9d; }
      .comic-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.7rem; margin-top: 0.65rem; }
      .comic-panel { background: #fffefe; border: 2px solid #d5ccd4; border-radius: 18px; padding: 0.45rem 0.45rem 0.55rem; }
      .tilt-a { transform: rotate(-1.2deg); } .tilt-b { transform: rotate(0.9deg); } .tilt-c { transform: rotate(-0.75deg); }
      .comic-art img, .sticker-wrap img, .bow-row img, .gem-row img, .badge-image img { width: 100%; display: block; border-radius: 12px; }
      .comic-caption { text-align: center; margin-top: 0.2rem; }
      .sticker-wrap { display: grid; grid-template-columns: 180px 1fr; gap: 0.75rem; align-items: center; }
      .access-title { font-family: 'Bubblegum Sans', 'Comic Sans MS', sans-serif; font-size: 2.25rem; color: #7a7078; text-align: center; margin: 0.25rem 0 0.7rem; }
      .decor-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.65rem; margin: 0.15rem 0 0.65rem; }
      .bow-row, .gem-row { background: #fff; border: 2px dashed #e7c8d5; border-radius: 18px; padding: 0.35rem 0.7rem; }
      .field-caption { color: #938892; margin-bottom: 0.25rem; }
      .code-box { background: #fff; border: 2px dashed #e6c5d3; border-radius: 16px; padding: 0.7rem; text-align: center; font-family: 'Bubblegum Sans', 'Comic Sans MS', sans-serif; font-size: 2rem; letter-spacing: 0.08em; color: #d57b9d; }
      .stButton > button { width: 100%; border-radius: 999px; border: 2px solid #df84a5; background: linear-gradient(180deg, #ffc1d3 0%, #f598b8 100%); color: white !important; font-family: 'Bubblegum Sans', 'Comic Sans MS', sans-serif; font-size: 1.05rem; letter-spacing: 0.03em; padding: 0.78rem 1rem; box-shadow: 0 8px 16px rgba(230, 137, 171, 0.25); }
      .stTextInput label, .stColorPicker label, .stSelectbox label, .stMultiSelect label, .stCheckbox label, .stRadio label { font-family: 'Patrick Hand', 'Comic Sans MS', cursive !important; font-size: 1.08rem !important; color: #756c76 !important; }
      .badge-shell { background: #fff; border: 2px dashed #e4c5d4; border-radius: 20px; padding: 0.7rem; }
      .footer-note { text-align: center; color: #8f8590; margin-top: 0.2rem; }
      @media (max-width: 680px) { .comic-grid, .decor-row, .sticker-wrap, .status-grid { grid-template-columns: 1fr; } .poster-wrap { padding-left: 0.7rem; padding-right: 0.7rem; } .subtitle { font-size: 1.2rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown("<div class='poster-wrap'>", unsafe_allow_html=True)
st.markdown(f"<img class='doodle-vine' src='{FLOWER_VINE}' alt='flower vine divider' />", unsafe_allow_html=True)
st.markdown(f"<div class='wobble-title'>{wobble_word_html('VIP PASS')}</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AT: Girl Math Hair Salon</div>", unsafe_allow_html=True)
st.markdown(f"<img class='doodle-vine' src='{FLOWER_VINE}' alt='flower vine divider' />", unsafe_allow_html=True)
st.markdown("<div class='pearl-row'>" + "".join("<span class='pearl'></span>" for _ in range(19)) + "</div>", unsafe_allow_html=True)
st.markdown(f"<div class='tiny-doodles'><img src='{GEM_CLUSTER_SVG}' alt='gems' style='max-width:220px;'/></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

app_stats = stats()
st.markdown("<div class='status-card'>", unsafe_allow_html=True)
st.markdown("<div class='card-title'>Shared VIP Passes</div>", unsafe_allow_html=True)
st.markdown("<div class='hand-copy'>This app now stores each VIP pass in a shared backend. Create a pass once, then reopen it from another phone or browser with the same pass code.</div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div class='status-grid'>
      <div class='status-pill'><div class='status-number'>{app_stats['total_passes']}</div><div class='mini-note'>total passes</div></div>
      <div class='status-pill'><div class='status-number'>{app_stats['vip_count']}</div><div class='mini-note'>VIP unlocked</div></div>
      <div class='status-pill'><div class='status-number'>{app_stats['today_count']}</div><div class='mini-note'>created today</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='status-card'>", unsafe_allow_html=True)
st.markdown("<div class='card-title'>Create, open, or recover a pass</div>", unsafe_allow_html=True)
create_col, open_col = st.columns(2)
with create_col:
    new_member_name = st.text_input("VIP member name", key="new_member_name", placeholder="Type the name for a new pass")
    new_contact_email = st.text_input("Recovery email", key="new_contact_email", placeholder="name@example.com")
    if st.button("Create new pass", use_container_width=True, key="create_pass_button"):
        record = create_pass(new_member_name, new_contact_email)
        apply_record_to_state(record)
        st.success(f"Created pass {record['passcode']}")
with open_col:
    existing_code = st.text_input("Open existing pass", key="existing_pass_code", placeholder="Enter pass code")
    if st.button("Open pass", use_container_width=True, key="open_pass_button"):
        if load_pass_into_state(existing_code):
            st.success(f"Loaded pass {normalize_passcode(existing_code)}")
        else:
            st.error("That pass code was not found.")

recover_email = st.text_input("Recover with email", key="recover_email_input", placeholder="Use the saved email to find your pass")
if recover_email:
    recover_matches = list_passes_for_email(recover_email)
    if recover_matches:
        st.caption(f"Found {len(recover_matches)} pass{'es' if len(recover_matches) != 1 else ''} for {normalize_email(recover_email)}")
        for match in recover_matches[:5]:
            row_col_1, row_col_2, row_col_3 = st.columns([2.4, 1.2, 1])
            with row_col_1:
                st.write(f"**{match['member_name'] or 'VIP member'}**")
                st.caption(match.get("contact_email") or "No recovery email")
            with row_col_2:
                st.caption(f"Code {match['passcode']}")
                st.caption(f"Saved {human_time(match.get('updated_at'))}")
            with row_col_3:
                if st.button("Open", key=f"recover_open_{match['passcode']}", use_container_width=True):
                    apply_record_to_state(match)
                    log_event(match["passcode"], "recovered", f"Recovered with {normalize_email(recover_email)}")
                    st.rerun()
    else:
        st.info("No passes match that email yet.")

if st.session_state.current_passcode:
    st.markdown("<div class='mini-note' style='margin-top:0.65rem;'>Current pass code</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='code-box'>{st.session_state.current_passcode}</div>", unsafe_allow_html=True)
    st.caption(
        f"Created {human_time(st.session_state.record_created_at)} • Last saved {human_time(st.session_state.record_updated_at)}"
    )
    if st.button("Start a different pass", use_container_width=True, key="clear_pass_button"):
        clear_current_pass()
        st.rerun()
else:
    st.info("Create a pass, open one by code, or recover it by email to start editing shared data.")
st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.current_passcode:
    st.markdown("<div class='paper-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>How to get V.I.P.</div>", unsafe_allow_html=True)
    st.markdown("<div class='hand-copy'>A worker will tell you how to get V.I.P.<br><span class='mini-note'>This status now saves across devices for the same pass code.</span></div>", unsafe_allow_html=True)
    st.text_input("VIP member name", key="member_name", placeholder="Type the VIP member name")
    st.text_input("Recovery email", key="contact_email", placeholder="name@example.com")
    if not st.session_state.get("badge_name") and st.session_state.get("member_name"):
        st.session_state.badge_name = st.session_state.member_name
    button_text = "ASK FOR VIP STATUS" if not st.session_state.is_vip else "YOU ARE NOW VIP"
    if st.button(button_text, use_container_width=True, key="vip_status_button"):
        st.session_state.is_vip = True
        st.balloons()
    if st.session_state.is_vip:
        st.success("VIP unlocked.")
    else:
        st.info("Tap when a worker says you're ready.")
    if st.session_state.get("contact_email"):
        st.caption(f"Recovery email on file: {normalize_email(st.session_state.contact_email)}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>Request History</div>", unsafe_allow_html=True)
    pass_history = recent_events(st.session_state.current_passcode, limit=12)
    if pass_history:
        for event in pass_history:
            detail = event.get("details", "").strip() or "No extra detail"
            event_type = event.get("event_type", "updated").replace("_", " ").title()
            st.markdown(
                f"**{event_type}** · {human_time(event.get('created_at'))}<br><span class='mini-note'>{detail}</span>",
                unsafe_allow_html=True,
            )
    else:
        st.info("No saved history for this pass yet.")
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
    for label in DEFAULT_SNACK_CHOICES:
        st.checkbox(label, key=f"snack::{label}")
    picked = [label for label in DEFAULT_SNACK_CHOICES if st.session_state.get(f"snack::{label}")]
    st.caption("Picked today: " + ", ".join(picked) if picked else "Picked today: none yet")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>Spa Treatments + Weekly Comics</div>", unsafe_allow_html=True)
    st.markdown("<div class='field-caption'>Choose a spa moment.</div>", unsafe_allow_html=True)
    st.radio("Choose a spa moment:", DEFAULT_SPA_CHOICES, key="spa_choice")
    st.caption(f"Today’s choice: {st.session_state.spa_choice}")
    st.markdown("<div class='mini-note'>New comic scenes can be dropped in daily or weekly.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>Merch + Name Tag</div>", unsafe_allow_html=True)
    st.selectbox("Schedule in advance:", DEFAULT_MERCH_CHOICES, key="merch_pick")
    st.text_input("Name tag name:", key="badge_name", placeholder="Type your VIP name")
    st.color_picker("Name tag color:", key="badge_color")
    st.multiselect("Customize options:", DEFAULT_EXTRA_CHOICES, key="badge_extras")
    st.markdown(
        f"<div class='badge-shell'><div class='badge-image'><img src='{badge_svg(st.session_state.badge_name.strip(), st.session_state.badge_color, st.session_state.badge_extras)}' alt='custom badge preview' /></div></div>",
        unsafe_allow_html=True,
    )
    st.caption(f"Selected merch item: {st.session_state.merch_pick}")
    st.markdown("</div>", unsafe_allow_html=True)

    payload = current_record_payload()
    save_pass(payload)
    refreshed = get_pass(st.session_state.current_passcode)
    if refreshed:
        st.session_state.record_updated_at = refreshed.get("updated_at", utc_now_iso())
        if refreshed.get("member_name") and not st.session_state.badge_name.strip():
            st.session_state.badge_name = refreshed["member_name"]
    st.markdown(f"<div class='footer-note'>Shared pass saved. Reopen with code {st.session_state.current_passcode} from another device.</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='footer-note'>Create or open a shared pass to start the multi-user experience.</div>", unsafe_allow_html=True)

st.markdown("<div class='status-card'>", unsafe_allow_html=True)
st.markdown("<div class='card-title'>Worker / Admin Tools</div>", unsafe_allow_html=True)
st.markdown("<div class='mini-note'>Search by pass code, member name, or recovery email. Open a pass and review the latest shared activity.</div>", unsafe_allow_html=True)
admin_query = st.text_input("Search passes", key="admin_search", placeholder="Search by code, name, or email")
admin_results = search_passes(admin_query, limit=10)
if admin_results:
    for result in admin_results:
        summary_col, detail_col, action_col = st.columns([2.2, 1.4, 1])
        with summary_col:
            st.write(f"**{result.get('member_name') or 'VIP member'}**")
            st.caption(result.get("contact_email") or "No recovery email")
        with detail_col:
            vip_label = "VIP unlocked" if result.get("is_vip") else "Standard pass"
            st.caption(f"Code {result['passcode']} · {vip_label}")
            st.caption(f"Saved {human_time(result.get('updated_at'))}")
        with action_col:
            if st.button("Load", key=f"admin_load_{result['passcode']}", use_container_width=True):
                apply_record_to_state(result)
                log_event(result["passcode"], "admin_opened", "Opened from worker/admin tools")
                st.rerun()
else:
    st.info("No passes found yet.")

global_history = recent_events(limit=10)
if global_history:
    st.markdown("<div class='mini-note' style='margin-top:0.65rem;'>Latest activity across passes</div>", unsafe_allow_html=True)
    for event in global_history:
        detail = event.get("details", "").strip() or "No extra detail"
        event_type = event.get("event_type", "updated").replace("_", " ").title()
        st.markdown(
            f"**{event.get('passcode', '')}** · {event_type} · {human_time(event.get('created_at'))}<br><span class='mini-note'>{detail}</span>",
            unsafe_allow_html=True,
        )
st.markdown("</div>", unsafe_allow_html=True)
