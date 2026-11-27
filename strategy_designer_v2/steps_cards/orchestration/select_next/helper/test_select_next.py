"""Tests of select_next: reading ids, records, candidates, duplicates, the ranking (on a hand-made run)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import select_next as s  # noqa: E402


def test_id_parts():
    assert s.id_parts("003-01_some-name") == ("step 2", "003", 1, 0)
    # created_from is the parent's lineage code, the same in both id conventions (topic 46)
    assert s.id_parts("003-01_some-name.b2_other") == ("7.b", "003-01", 2, 1)
    assert s.id_parts("001-01_x.a1_y.c1_z") == ("7.c", "001-01.a1", 1, 2)
    assert s.id_parts("001-01.a1.c1_z") == ("7.c", "001-01.a1", 1, 2)
    assert s.id_parts("001-01.a1.c12_z") == ("7.c", "001-01.a1", 12, 2)
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


def test_an_idea_whose_files_cannot_be_written_is_not_a_candidate(tmp_path):
    """Topic 46 (2026-11-23): an id plus its plan's longest file suffix over 255 bytes is not offered (step 3 would fail)."""
    run = "t_run"; ideas = tmp_path / "02_ideation" / run / "ideas"
    long_id = ("003-01_x" + "".join(f".g{i}_" + "a-long-short-name-of-an-idea" for i in range(1, 9)))[:245]
    assert len(long_id) == 245            # its idea file fits (245 + ".md"); its plan's config (245 + 15) does not
    idea(ideas, "003-01_x", "a brief idea"); idea(ideas, long_id, "a very deep idea")
    rows = {r["idea"]: r["status"] for r in s.rank(run, root=tmp_path)}
    assert rows["003-01_x"] == "candidate" and rows[long_id].startswith("not testable")


def test_the_register_s_longer_names_count_too():
    """Night 5: the similarity register names a book <run>__<id>_<bar>, longer than a plan's files: an id that fits step 3
    but not the register is not offered either."""
    iid = "x" * 228                                   # 228 + "_4h_config.json" = 243: fits step 3
    assert not s.too_long(iid) and s.too_long(iid, "brief_absorption_run")    # 20 + 2 + 228 + 10 = 260: does not


def test_the_parents_difference_reads_its_nearest_held_book(tmp_path):
    import json
    import select_next as SN
    reg = tmp_path / "orchestration" / "ideas_similarities_check" / "register"
    (reg / "comparisons").mkdir(parents=True)
    (reg / "books.json").write_text(json.dumps([
        {"key": "r__001-01.b1_x_1d", "run": "r", "id": "001-01.b1_x_1d", "kind": "confirmed"},
        {"key": "r__002-01_y_1d", "run": "r", "id": "002-01_y_1d", "kind": "confirmed"}]))
    (reg / "comparisons" / "r__001-01.b1_x_1d.json").write_text(json.dumps(
        {"nearest_relative": {"share_explained": 0.1}, "nearest_held": {"share_explained": 0.8}}))
    (reg / "comparisons" / "r__002-01_y_1d.json").write_text(json.dumps({"nearest_relative": {"share_explained": 0.3}}))
    ev = SN.parent_evidence(tmp_path)
    assert abs(ev[("r", "001-01.b1_x")][1] - 0.2) < 1e-9      # close to a portfolio book: little difference
    assert abs(ev[("r", "002-01_y")][1] - 0.7) < 1e-9         # an older comparison: its nearest paying book


def test_a_discovery_s_brief_ideas_rank_as_follow_ups(tmp_path):
    """Next steps 1n (the operator, 2026-11-25): a brief written from a discovery does not put its ideas first; they rank
    as the discovery would, a follow-up of the idea it was found in, after the theme's own ideas."""
    run = "d_run"; ideas = tmp_path / "02_ideation" / run / "ideas"
    idea(ideas, "003-01_x", "one"); idea(ideas, "003-02_y", "two")
    mark_tested(tmp_path, run, "003-01_x", "inconclusive", "not profitable enough")
    idea(tmp_path / "07b_inconclusive" / run / "003-01_x_1d" / "ideas", "003-01_x.b1_on-theme", "three")
    briefs = tmp_path / "01_brief" / run / "briefs"; briefs.mkdir(parents=True)
    (briefs / "004_found.md").write_text("---\nbar: 1d\ndiscovery: 003-01.g1_a-pattern\n---\nA theory.\n")
    (ideas / "004-01_from-discovery.md").write_text("---\nbrief: 004_found\ninstruments: BTC\nbar: 1d\nperiod: folds A, B, C, D\n---\n"
                                                   "Idea: four\nConsequence: c.\n")
    mark_tested(tmp_path, run, "004-02_tested", "inconclusive", "not profitable enough")
    (tmp_path / "07b_inconclusive" / run / "004-02_tested_1d" / "ideas").mkdir(parents=True)
    (tmp_path / "07b_inconclusive" / run / "004-02_tested_1d" / "ideas" / "004-02.b1_child.md").write_text(
        "---\nbrief: 004_found\ninstruments: BTC\nbar: 1d\nperiod: folds A, B, C, D\n---\nIdea: five\nConsequence: c.\n")
    rows = {r["idea"]: r for r in s.rank(run, tmp_path)}
    order = [r["idea"] for r in s.rank(run, tmp_path) if r["status"] == "candidate"]
    assert order[0] == "003-02_y"
    assert rows["004-02.b1_child"]["generation"] == 2                # its follow-ups count from the discovery's level                                   # the theme's own idea first
    d = rows["004-01_from-discovery"]
    assert (d["line"], d["generation"], d["group"], d["discovery"]) == ("7.g discovery", 1, 3, "003-01.g1_a-pattern")
    assert rows["003-02_y"]["group"] == 1


def test_with_header_field():
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "common"))
    from lib import with_header_field, header_fields
    t = with_header_field("---\nbar: 1d\nsource: x\n---\nBody.\n", "discovery", "003-01.g1_p")
    assert header_fields(t) == {"bar": "1d", "source": "x", "discovery": "003-01.g1_p"} and t.endswith("---\nBody.\n")
    assert header_fields(with_header_field(t, "discovery", "z"))["discovery"] == "z"


def test_a_discovery_s_brief_counts_as_its_own_line(tmp_path):
    """Next steps B10 (the operator, 2026-11-27): a tested idea of a brief written from a discovery counts as an analysis
    of "7.g discovery", one per brief in a run, not of step 2; a brief written before the field (night 8) is known by the
    loop's line that wrote it from the discovery; a follow-up keeps its own line's record."""
    run = "e_run"
    briefs = tmp_path / "01_brief" / run / "briefs"; briefs.mkdir(parents=True)
    (briefs / "004_found.md").write_text("---\nbar: 1d\ndiscovery: 003-01.g1_a-pattern\n---\nA theory.\n")
    (briefs / "005_older.md").write_text("---\nbar: 1d\nsource: line 7.g patterns, backtest 003-01.g1_x_1d\n---\nA theory.\n")
    (briefs / "003_b.md").write_text("---\nbar: 1d\n---\nThe run's own theory.\n")
    loop = tmp_path / "orchestration" / "loop" / run; loop.mkdir(parents=True)
    (loop / "loop.jsonl").write_text(json.dumps({"discovery": f"07g_patterns/{run}/003-01.g1_x_1d/discoveries/003-01.g1.g1_older.md",
                                                 "brief": "005_older", "ideas": 1, "outcome": "ok"}) + "\n")
    for iid, brief, s5, s6 in (("004-01_a", "004_found", "confirmed", "profitable enough"),
                               ("004-02_b", "004_found", "inconclusive", "not profitable enough"),   # same analysis
                               ("005-01_c", "005_older", "inconclusive", "not profitable enough"),
                               ("003-01_d", "003_b", "inconclusive", "not profitable enough"),
                               ("004-01.b1_e", "004_found", "confirmed", "profitable enough")):       # a follow-up: 7.b
        mark_tested(tmp_path, run, iid, s5, s6)
        p = tmp_path / "03_test_plan" / run / "plans" / f"{iid}_1d.md"
        p.write_text(p.read_text().replace("outcome: plan", f"brief: {brief}\noutcome: plan"))
    r = s.records(tmp_path)
    assert r[s.DISCOVERY] == (1, 2, 0.5) and r["step 2"] == (0, 1, 1 / 3) and r["7.b"] == (1, 1, 2 / 3)
    # the ranking scores the brief's own ideas with that record, and names it
    ideas = tmp_path / "02_ideation" / run / "ideas"
    (ideas).mkdir(parents=True)
    (ideas / "004-03_f.md").write_text("---\nbrief: 004_found\ninstruments: BTC\nbar: 1d\nperiod: folds A, B, C, D\n---\n"
                                       "Idea: six\nConsequence: c.\n")
    row = next(x for x in s.rank(run, tmp_path) if x["idea"] == "004-03_f")
    assert (row["line"], row["record"], row["generation"]) == (s.DISCOVERY, 0.5, 1)


def test_line_7g_is_called_only_when_its_idea_would_rank_first(tmp_path):
    """Next steps B10: after a test, 7.g's idea scores the higher of the records "7.g" and "7.g discovery" over 1 plus its
    generation; called when that is at least the best waiting idea's priority, or when nothing waits; never while a
    brief's own idea waits."""
    run = "f_run"; ideas = tmp_path / "02_ideation" / run / "ideas"
    idea(ideas, "003-01_x", "one")
    mark_tested(tmp_path, run, "003-01_x", "inconclusive", "not profitable enough")
    call, why = s.discovery_call(run, "003-01_x", tmp_path)
    assert call and "nothing waits" in why and "score 0.25" in why          # (0 + 1) / (0 + 2) / (1 + 1)
    idea(ideas, "003-02_y", "two")                                          # a brief's own idea waits: it goes first
    call, why = s.discovery_call(run, "003-01_x", tmp_path)
    assert not call and "brief's own idea" in why
    mark_tested(tmp_path, run, "003-02_y", "inconclusive", "not profitable enough")
    idea(tmp_path / "07b_inconclusive" / run / "003-01_x_1d" / "ideas", "003-01_x.b1_p", "three")
    call, why = s.discovery_call(run, "003-02_y", tmp_path)                 # 7.b's idea: 0.5 / 2 x w 0.5 = 0.125
    assert call and "priority 0.125" in why
    for k in range(1, 5):                                                   # 7.b succeeds in 4 other runs
        mark_tested(tmp_path, f"g{k}_run", f"009-0{k}_z.b1_q", "confirmed", "profitable enough")
    idea(tmp_path / "07b_inconclusive" / run / "003-01_x_1d" / "ideas", "003-01_x.b2_r", "four")
    mark_tested(tmp_path, run, "003-01_x.b1_p", "inconclusive", "not profitable enough")
    # 7.b: 4 of 5 analyses, (4 + 1) / (5 + 2) = 0.7143; its waiting 003-01_x.b2_r: 0.7143 / 2 = 0.3571, x 0.5 = 0.1785; 7.g's idea
    # after 003-01_x.b1_p, a generation deeper: 0.5 / 3 = 0.1667: not called
    call, why = s.discovery_call(run, "003-01_x.b1_p", tmp_path)
    assert not call and "score 0.1667" in why and "priority 0.1785" in why
