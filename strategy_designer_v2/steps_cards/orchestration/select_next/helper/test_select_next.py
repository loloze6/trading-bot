"""Tests of select_next: reading ids, records, candidates, duplicates, the ranking (on a hand-made run)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import select_next as s  # noqa: E402


def test_id_parts():
    assert s.id_parts("003-01_some-name") == ("step 2", "003", 1, 0)
    assert s.id_parts("003-01_some-name.b2_other") == ("7.b", "003-01_some-name", 2, 1)
    assert s.id_parts("001-01_x.a1_y.c1_z") == ("7.c", "001-01_x.a1_y", 1, 2)
    assert s.id_parts("N2-04_renamed-by-hand")[0] is None


def idea(path, iid, text, data=("BTC, ETH", "1d", "folds A, B, C, D")):
    path.mkdir(parents=True, exist_ok=True)
    (path / f"{iid}.md").write_text(f"---\nbrief: 003_b\ninstruments: {data[0]}\nbar: {data[1]}\nperiod: {data[2]}\n---\n"
                                    f"Idea: {text}\nConsequence: c.\n")


def mark_tested(root, run, iid, s5, s6):
    rid = f"{iid}_1d"
    (root / "03_test_plan" / run / "plans").mkdir(parents=True, exist_ok=True)
    (root / "03_test_plan" / run / "plans" / f"{rid}.md").write_text(f"---\nidea: {iid}\noutcome: plan\n---\n")
    for step, sub, st in (("05_verification", "verdicts", s5), ("06_profitability", "checks", s6)):
        d = root / step / run / sub / rid
        d.mkdir(parents=True, exist_ok=True)
        (d / "result.json").write_text(json.dumps({"status": st}))


def test_records_count_analyses_not_ideas(tmp_path):
    mark_tested(tmp_path, "a_run", "003-01_x.b1_p", "confirmed", "not profitable enough")
    mark_tested(tmp_path, "a_run", "003-01_x.b2_q", "confirmed", "profitable enough")    # same analysis: one success
    mark_tested(tmp_path, "a_run", "003-02_y.b1_r", "inconclusive", "not profitable enough")
    mark_tested(tmp_path, "a_run", "003-01_x", "inconclusive", "profitable enough")
    mark_tested(tmp_path, "a_run", "N2-04_hand", "confirmed", "profitable enough")         # left out
    r = s.records(tmp_path)
    assert r["7.b"] == (1, 2, 0.5) and r["step 2"] == (1, 1, 2 / 3) and len(r) == 2
    assert s.record_of("7.e", r) == 0.5                                                # no analysis yet


def test_ranking_candidates_duplicates_and_ties(tmp_path):
    run = "b_run"
    idea(tmp_path / "02_ideation" / run / "ideas", "003-01_x", "one")
    idea(tmp_path / "02_ideation" / run / "ideas", "003-02_y", "two")
    idea(tmp_path / "02_ideation" / run / "ideas", "003-03_z", "two")                 # same as 003-02: duplicate
    lines = tmp_path / "07b_inconclusive" / run / "003-01_x_1d" / "ideas"
    idea(lines, "003-01_x.b1_p", "three")
    idea(lines, "003-01_x.b2_q", "four")
    idea(lines, "003-01_x.b3_r", "four", data=("BTC, ETH, ADA", "1d", "folds A, B, C, D"))   # other data: not a duplicate
    mark_tested(tmp_path, run, "003-01_x", "inconclusive", "not profitable enough")
    rows = s.rank(run, tmp_path, exclude={"003-01_x.b3_r"})
    st = {r["idea"]: r["status"] for r in rows}
    assert st["003-01_x"] == "tested" and st["003-03_z"] == "duplicate of 003-02_y" and st["003-01_x.b3_r"] == "excluded"
    cands = [r["idea"] for r in rows if r["status"] == "candidate"]
    # records: step 2 (0 of 1) = 1/3, generation 0 -> 0.333; 7.b none yet = 0.5, generation 1 -> 0.25
    assert cands == ["003-02_y", "003-01_x.b1_p", "003-01_x.b2_q"]
    assert rows[0]["score"] == round(1 / 3, 4)
