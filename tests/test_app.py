from __future__ import annotations

import sqlite3
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from streamlit.testing.v1 import AppTest

import app


@pytest.fixture()
def isolated_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    db_path = tmp_path / "girl_math_test.db"
    monkeypatch.setattr(app, "DB_PATH", db_path)
    app.init_db()
    return db_path


def test_init_db_migrates_legacy_schema(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db_path = tmp_path / "legacy.db"
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE vip_passes (
            passcode TEXT PRIMARY KEY,
            member_name TEXT NOT NULL DEFAULT '',
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
    conn.execute(
        """
        INSERT INTO vip_passes (
            passcode, member_name, badge_name, badge_color, snack_json, spa_choice,
            merch_pick, extras_json, is_vip, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "LEGACY1",
            "Legacy Member",
            "Legacy Member",
            "#f598b8",
            "{}",
            "Comics corner",
            "Custom name tag",
            "[]",
            0,
            "2026-05-01T00:00:00+00:00",
            "2026-05-01T00:00:00+00:00",
        ),
    )
    conn.commit()
    conn.close()

    monkeypatch.setattr(app, "DB_PATH", db_path)
    app.init_db()

    conn = sqlite3.connect(db_path)
    columns = {row[1] for row in conn.execute("PRAGMA table_info(vip_passes)")}
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    migrated = conn.execute(
        "SELECT spa_choice, comic_choice, spa_add_on_json FROM vip_passes WHERE passcode = ?",
        ("LEGACY1",),
    ).fetchone()
    conn.close()

    assert "contact_email" in columns
    assert "vip_status" in columns
    assert "spa_add_on_json" in columns
    assert "comic_choice" in columns
    assert "pass_events" in tables
    assert migrated == ("Mini manicure", "Where did you get it?", "[]")


def test_create_recover_search_and_history(isolated_db: Path) -> None:
    created = app.create_pass(member_name="Mia", contact_email="MIA@Example.com ")

    fetched = app.get_pass(created["passcode"])
    assert fetched is not None
    assert fetched["member_name"] == "Mia"
    assert fetched["contact_email"] == "mia@example.com"
    assert fetched["vip_status"] == "not_requested"
    assert fetched["is_vip"] == 0
    assert fetched["comic_choice"] == app.DEFAULT_COMIC_CHOICES[0]
    assert fetched["spa_add_on_json"] == "[]"

    recovered = app.list_passes_for_email("mia@example.com")
    assert [row["passcode"] for row in recovered] == [created["passcode"]]

    history = app.recent_events(created["passcode"], limit=10)
    assert [event["event_type"] for event in history] == ["created"]

    search_hits = app.search_passes("mia@example.com")
    assert [row["passcode"] for row in search_hits] == [created["passcode"]]


def test_vip_requests_require_admin_approval(isolated_db: Path) -> None:
    created = app.create_pass(member_name="Luna", contact_email="luna@example.com")

    requested = app.request_vip_approval(created["passcode"])
    assert requested is not None
    assert requested["vip_status"] == "pending"
    assert requested["is_vip"] == 0

    approved = app.review_vip_pass(created["passcode"], "approved")
    assert approved is not None
    assert approved["vip_status"] == "approved"
    assert approved["is_vip"] == 1

    saved_payload = {
        "passcode": created["passcode"],
        "created_at": approved["created_at"],
        "member_name": approved["member_name"],
        "contact_email": approved["contact_email"],
        "badge_name": approved["badge_name"],
        "badge_color": approved["badge_color"],
        "snacks": app.parse_snacks(approved),
        "spa_choice": approved["spa_choice"],
        "spa_add_ons": ["Shampoo style reset"],
        "comic_choice": "Girl Math VIP!",
        "merch_pick": approved["merch_pick"],
        "extras": app.parse_extras(approved),
        "vip_status": "pending",
        "is_vip": False,
    }
    app.save_pass(saved_payload)

    still_approved = app.get_pass(created["passcode"])
    assert still_approved is not None
    assert still_approved["vip_status"] == "approved"
    assert still_approved["is_vip"] == 1

    rejected = app.review_vip_pass(created["passcode"], "rejected")
    assert rejected is not None
    assert rejected["vip_status"] == "rejected"
    assert rejected["is_vip"] == 0

    history = app.recent_events(created["passcode"], limit=10)
    assert [event["event_type"] for event in history[:5]] == [
        "vip_rejected",
        "updated",
        "vip_approved",
        "vip_requested",
        "created",
    ]


def test_load_logs_open_event_and_clear_resets_state(isolated_db: Path) -> None:
    created = app.create_pass(member_name="Ava", contact_email="ava@example.com")

    assert app.load_pass_into_state(created["passcode"]) is True
    assert app.st.session_state.current_passcode == created["passcode"]
    assert app.st.session_state.member_name == "Ava"
    assert app.st.session_state.contact_email == "ava@example.com"
    assert app.st.session_state.spa_add_ons == []
    assert app.st.session_state.comic_choice == app.DEFAULT_COMIC_CHOICES[0]

    history = app.recent_events(created["passcode"], limit=10)
    assert [event["event_type"] for event in history[:2]] == ["opened", "created"]

    app.clear_current_pass()
    assert app.st.session_state.current_passcode == ""
    assert app.st.session_state.member_name == ""
    assert app.st.session_state.contact_email == ""
    assert app.st.session_state.spa_add_ons == []
    assert app.st.session_state.comic_choice == app.DEFAULT_COMIC_CHOICES[0]


def test_streamlit_smoke_renders_without_exception(tmp_path: Path) -> None:
    at = AppTest.from_file("app.py")
    at.run(timeout=30)
    assert not at.exception
    assert any(button.label == "Create new pass" for button in at.button)
    assert any(field.label == "Recovery email" for field in at.text_input)
    assert not any(field.label == "Search passes" for field in at.text_input)

    admin_at = AppTest.from_file("app.py")
    admin_at.query_params["page"] = "admin"
    admin_at.run(timeout=30)
    assert not admin_at.exception
    assert any(field.label == "Search passes" for field in admin_at.text_input)
    assert any(button.label == "Approve" for button in admin_at.button)


def test_pricing_and_summary_rules() -> None:
    friday_pricing = app.current_pricing(date(2026, 5, 8))
    assert friday_pricing["is_friday"] is True
    assert friday_pricing["monthly_price"] == 5
    assert friday_pricing["discount"] == 3

    summary = app.build_pass_summary(
        {
            "snacks": {"Healthy Pack": True, "Sweet Tooth": False, "Lemonade": True, "Milkshakes": False},
            "spa_choice": "Hair sparkle",
            "spa_add_ons": ["Cream glow treatment"],
            "comic_choice": "Girl Math VIP!",
            "vip_status": "approved",
            "is_vip": True,
            "merch_pick": "Sticker pack",
        },
        on_date=date(2026, 5, 8),
    )
    assert summary["is_vip"] is True
    assert summary["pricing"]["monthly_price"] == 5
    assert summary["paid_add_ons"] == ["Cream glow treatment"]
    assert summary["comic_choice"] == "Girl Math VIP!"
    assert any("Snack bar picks" in item for item in summary["included_items"])


def test_streamlit_vip_request_button_updates_without_exception(tmp_path: Path) -> None:
    at = AppTest.from_file("app.py")
    at.run(timeout=30)

    at.text_input(key="new_member_name").input("Button Test")
    at.text_input(key="new_contact_email").input("button.test@example.com")
    at.button(key="create_pass_button").click()
    at.run(timeout=30)
    assert not at.exception

    at.button(key="vip_status_button").click()
    at.run(timeout=30)

    assert not at.exception
    assert any("pending admin approval" in info.value for info in at.info)
