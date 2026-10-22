"""D-178 (operator item D, 2026-10-22): the answer checks D-178 added to analyst_session
(the next-steps ledger, completeness, the mechanism query) refuse every answer written before
them. The older analyst test modules test what they always tested -- the checks that existed --
so they switch the three new checks off with this fixture; tests/test_d178_analyst_method.py
tests the three on, with real fixtures."""
import pytest

import analyst_session as asm


@pytest.fixture()
def d178_checks_off(monkeypatch):
    monkeypatch.setattr(asm, "next_steps_errors", lambda *a, **k: [])
    monkeypatch.setattr(asm, "completeness_errors", lambda *a, **k: [])
    monkeypatch.setattr(asm, "_mechanism_errors", lambda *a, **k: [])
