from __future__ import annotations

import sqlite3
from pathlib import Path

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
    conn.commit()
    conn.close()

    monkeypatch.setattr(app, "DB_PATH", db_path)
    app.init_db()

    conn = sqlite3.connect(db_path)
    columns = {row[1] for row in conn.execute("PRAGMA table_info(vip_passes)")}
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()

    assert "contact_email" in columns
    assert "pass_events" in tables


def test_create_recover_search_and_history(isolated_db: Path) -> None:
    created = app.create_pass(member_name="Mia", contact_email="MIA@Example.com ")

    fetched = app.get_pass(created["passcode"])
    assert fetched is not None
    assert fetched["member_name"] == "Mia"
    assert fetched["contact_email"] == "mia@example.com"

    recovered = app.list_passes_for_email("mia@example.com")
    assert [row["passcode"] for row in recovered] == [created["passcode"]]

    history = app.recent_events(created["passcode"], limit=10)
    assert [event["event_type"] for event in history] == ["created"]

    search_hits = app.search_passes("mia@example.com")
    assert [row["passcode"] for row in search_hits] == [created["passcode"]]


def test_load_logs_open_event_and_clear_resets_state(isolated_db: Path) -> None:
    created = app.create_pass(member_name="Ava", contact_email="ava@example.com")

    assert app.load_pass_into_state(created["passcode"]) is True
    assert app.st.session_state.current_passcode == created["passcode"]
    assert app.st.session_state.member_name == "Ava"
    assert app.st.session_state.contact_email == "ava@example.com"

    history = app.recent_events(created["passcode"], limit=10)
    assert [event["event_type"] for event in history[:2]] == ["opened", "created"]

    app.clear_current_pass()
    assert app.st.session_state.current_passcode == ""
    assert app.st.session_state.member_name == ""
    assert app.st.session_state.contact_email == ""


def test_streamlit_smoke_renders_without_exception(tmp_path: Path) -> None:
    at = AppTest.from_file("app.py")
    at.run(timeout=30)
    assert not at.exception
    assert any(button.label == "Create new pass" for button in at.button)
    assert any(field.label == "Recovery email" for field in at.text_input)
