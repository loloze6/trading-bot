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
    mark_tested(tmp_path, "c_run", "003-01_x.b1_s", "confirmed", "not profitable enough")  # same idea read in another run
    (tmp_path / "03_test_plan" / "c_run" / "plans" / "003-01_x.b2_t_1d.md").write_text(          # no plan built: not counted
        "---\nidea: 003-01_x.b2_t\noutcome: missing-components\n---\n")
    (tmp_path / "03_test_plan" / "c_run" / "plans" / "004-01_z_1d.md").write_text(
        "---\nidea: 004-01_z\noutcome: missing-components\n---\n")
    r = s.records(tmp_path)
    # a success is a profitable book (2026-11-19): a_run 003-01_x's 7.b analysis has one (b2_q); c_run's only confirms
    assert r["7.b"] == (1, 3, 0.4) and r["step 2"] == (1, 1, 2 / 3) and len(r) == 2
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


def test_an_unblocked_refusal_is_a_candidate_again(tmp_path, monkeypatch):
    run = "u_run"
    idea(tmp_path / "02_ideation" / run / "ideas", "003-01_x", "one")
    plans = tmp_path / "03_test_plan" / run / "plans"
    plans.mkdir(parents=True)
    (plans / "003-01_x_1d.md").write_text("---\nidea: 003-01_x\noutcome: missing-components\n---\n")
    assert [r["status"] for r in s.rank(run, tmp_path)] == ["tested"]
    monkeypatch.setattr(s.wishes, "unblocked", lambda plan, root=None: plan.name == "003-01_x_1d.md")
    assert [r["status"] for r in s.rank(run, tmp_path)] == ["candidate"]


def test_a_brief_s_own_ideas_come_first(tmp_path):
    run = "o_run"
    idea(tmp_path / "02_ideation" / run / "ideas", "003-01_x", "one")
    idea(tmp_path / "02_ideation" / run / "ideas", "003-02_y", "two")
    mark_tested(tmp_path, run, "003-01_x", "confirmed", "profitable enough")
    mark_tested(tmp_path, "p_run", "009-01_q.g1_w", "confirmed", "profitable enough")      # 7.g gets a high record
    lines = tmp_path / "07g_patterns" / run / "003-01_x_1d" / "ideas"
    idea(lines, "003-01_x.g1_child", "three")
    cands = [r["idea"] for r in s.rank(run, tmp_path) if r["status"] == "candidate"]
    assert cands == ["003-02_y", "003-01_x.g1_child"]                       # the brief's idea before a better-scored child


def register_book(root, run, iid, kind, share):
    reg = root / "orchestration" / "ideas_similarities_check" / "register"
    (reg / "comparisons").mkdir(parents=True, exist_ok=True)
    f = reg / "books.json"; rows = json.loads(f.read_text()) if f.exists() else []
    key = f"{run}__{iid}_1d"; rows.append({"key": key, "run": run, "id": f"{iid}_1d", "kind": kind})
    f.write_text(json.dumps(rows))
    (reg / "comparisons" / f"{key}.json").write_text(json.dumps({"nearest_relative": {"share_explained": share}}))


def test_real_ideas_unlike_what_we_earn_come_first_and_those_we_already_earn_last(tmp_path):
    """Operator, 2026-11-22: after a brief's own ideas, the ideas written from a confirmed idea whose book the paying books
    explain little; then the unproven ones; an idea written from a confirmed idea we already earn after them."""
    run = "t_run"; ideas = tmp_path / "02_ideation" / run / "ideas"
    for iid in ("003-01_unrelated", "003-02_earned", "003-03_unclear"):
        idea(ideas, iid, f"parent {iid}")
    mark_tested(tmp_path, run, "003-01_unrelated", "confirmed", "not profitable enough")
    mark_tested(tmp_path, run, "003-02_earned", "confirmed", "profitable enough")
    mark_tested(tmp_path, run, "003-03_unclear", "inconclusive", "not profitable enough")
    register_book(tmp_path, run, "003-01_unrelated", "confirmed", 0.05)       # difference 0.95
    register_book(tmp_path, run, "003-02_earned", "paying", 0.90)             # difference 0.10
    idea(ideas, "003-04_brief-idea", "a brief idea not yet tested")
    for parent in ("003-01_unrelated", "003-02_earned", "003-03_unclear"):
        idea(ideas, f"{parent}.g1_child", f"a child of {parent}")
    order = [r["idea"] for r in s.rank(run, root=tmp_path) if r["status"] == "candidate"]
    assert order == ["003-04_brief-idea", "003-01_unrelated.g1_child", "003-03_unclear.g1_child", "003-02_earned.g1_child"]
    rows = {r["idea"]: r for r in s.rank(run, root=tmp_path)}
    assert rows["003-01_unrelated.g1_child"]["group"] == 2 and rows["003-02_earned.g1_child"]["group"] == 3
    assert rows["003-03_unclear.g1_child"]["difference"] is None                # no evidence: w 0.5
