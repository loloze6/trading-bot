"""Tests of step 1's own code (no model call): the header lines it accepts; the brief's instruments in the new data
use (common/data_use.md, A12)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))
import make_brief as M  # noqa: E402

RESEARCH = ["BTC", "ATOM", "XMR", "CRV", "GRT", "DOGE", "XRP", "ADA"]
ANSWER = ("---\ninstruments: LINK, UNI, SOL\nbar: 1d\n---\nIn a calm decline a short rebound keeps going, because sellers "
          "are slow.\n\nshort-name: calm decline rebound\nindex-line: a rebound in a calm decline continues [instruments: "
          "LINK, UNI, SOL, bar: 1d]\n")


def run(monkeypatch, tmp_path, answer, run_name=None, du=None):
    seen = []
    monkeypatch.setattr(M, "call", lambda model, system, request: seen.append((system, request)) or (answer, 0.0))
    monkeypatch.setattr(M.coins, "data_use", lambda r: du)
    monkeypatch.setattr(M.target_box, "theme_note", lambda r: "")
    monkeypatch.setattr(sys, "argv", ["make_brief.py", "--theme", "calm declines", "--briefs-dir", str(tmp_path / "briefs")]
                        + (["--run", run_name] if run_name else []))
    M.main()
    return seen, {f.name: f.read_text() for f in sorted((tmp_path / "briefs").iterdir())}


def test_in_the_new_data_use_the_instruments_are_the_runs_research_coins_written_by_code(monkeypatch, tmp_path):
    seen, files = run(monkeypatch, tmp_path, ANSWER, "du_run", {"version": 2, "research_coins": RESEARCH})
    system, request = seen[0]
    assert M.INSTRUMENTS_KEY not in system and "- bar: the bar size" in system        # not asked for instruments
    assert "write no `instruments:` line" in request
    brief = files["001_calm-decline-rebound.md"]
    assert brief.startswith("---\ninstruments: BTC, ATOM, XMR, CRV, GRT, DOGE, XRP, ADA\nbar: 1d\n---\n")
    assert files["INDEX.md"].endswith("[instruments: BTC, ATOM, XMR, CRV, GRT, DOGE, XRP, ADA, bar: 1d]\n")
    for text in files.values():                    # no final-group coin in any file step 1 wrote
        assert M.final_coins_named(text) == []


def test_in_the_new_data_use_a_theory_naming_a_final_coin_is_refused(monkeypatch, tmp_path):
    for coin in M.coins.FINAL:
        answer = ANSWER.replace("In a calm decline", f"On {coin}, in a calm decline")
        with pytest.raises(SystemExit):            # every attempt names it: no brief
            run(monkeypatch, tmp_path / coin, answer, "du_run", {"version": 2, "research_coins": RESEARCH})
        assert not list((tmp_path / coin / "briefs").glob("0*.md")) and not (tmp_path / coin / "briefs" / "INDEX.md").exists()


def test_without_a_data_use_step_1_is_as_before(monkeypatch, tmp_path):
    seen, files = run(monkeypatch, tmp_path / "plain", ANSWER)                         # no --run
    seen2, files2 = run(monkeypatch, tmp_path / "old", ANSWER, "old_run", None)        # a run in the old data use
    assert seen == seen2 and files == files2
    system, request = seen[0]
    assert M.INSTRUMENTS_KEY in system and "[THE COINS OF THIS RESEARCH]" not in request
    assert files["001_calm-decline-rebound.md"].startswith("---\ninstruments: LINK, UNI, SOL\nbar: 1d\n---\n")


def test_a_boxed_run_s_brief_may_carry_its_profile_line():
    """B2.1 (common/target_box.md): in a boxed run the brief's header names the box's profile and side."""
    text = "---\nbar: 1d\nprofile: falling calm\nside: long only\n---\nIn a falling, calm market, a theory.\nshort-name: calm fall rebound\n"
    header, body, short, *_ = M.parse(text, False)
    assert header == ["bar: 1d", "profile: falling calm", "side: long only"] and short == "calm-fall-rebound"
    with pytest.raises(ValueError, match="outside the list"):
        M.parse("---\nregime: calm\n---\nA theory.\n", False)

