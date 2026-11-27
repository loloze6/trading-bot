"""Build B10's replay of night 9 (2026-11-27): for each idea night 9's loop tested, in the loop's order, the run's queue
rebuilt as it stood when step 7 started on it, and whether line 7.g would have been called under B10's rule
(select_next.discovery_call, the code run_idea calls).

  python3 runs/build_b10/replay.py OUT_DIR          (from steps_cards; reads files only, writes OUT_DIR/replay.json)

How the state at a time T is rebuilt: a tree of symbolic links (OUT_DIR/tree) holding only the files that existed at T,
every named run included (the records are read over every run, and night 9's six ran side by side). A file's time is read
from the journals the runs committed: a plan at its step3_plan line, a verdict at step5_verdict, a check at step6_check,
a line's ideas at its step7_<line> line, a discovery's brief and its ideas at the loop's line that wrote them, a register
book at its `added_utc`; the loop's lines up to T (its failed ideas). A file no journal dates (older runs) is there from
the start. T is the start of the idea's first step 7 line (its journal time minus its seconds).
The briefs of night 9's runs are taken as git has them at T (the last commit at or before T touching the file; its
first version before that): the designer removed the `discovery:` line of some starting briefs during the night, and
put one back, which changed how their ideas ranked.
Not rebuilt (today's state used): the register's comparisons' contents (a comparison redone later keeps its new
nearest book), the components step's answers, the plans' COMPONENT_WISHLIST.md.
"""
import json, os, re, shutil, subprocess, sys, collections
from datetime import datetime, timedelta
from pathlib import Path

STEPS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(STEPS / "orchestration" / "select_next" / "helper"))
sys.path.insert(0, str(STEPS / "orchestration" / "loop" / "helper"))
sys.path.insert(0, str(STEPS / "common"))
import select_next as sn  # noqa: E402
import loop  # noqa: E402
from lib import idea_code  # noqa: E402

RUNS = ["night9_chopagishort_run", "night9_chopdeep_run", "night9_chopmonth_run", "night9_chopstretch_run",
        "night9_fallcalmfade_run", "night9_fallcalmwide_run"]
EARLY = datetime(2000, 1, 1)
BAR = re.compile(r"_\d+[mhdw]$")


def ts(s):
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    except (TypeError, ValueError):
        return None


def journal_times():
    """{(run, backtest, step): the time of the step's first line}, every run with a journal."""
    out = {}
    for j in STEPS.glob("orchestration/run_idea/*_run/journal.jsonl"):
        for l in j.read_text().splitlines():
            e = json.loads(l) if l.strip() else {}
            t = ts(e.get("at"))
            k = (j.parent.name, e.get("backtest"), e.get("step"))
            if t and k[1] and k not in out:
                out[k] = t
    return out


def loop_lines(run):
    p = STEPS / "orchestration" / "loop" / run / "loop.jsonl"
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def dated_files():
    """[(time, relative path)] for every file select_next reads; EARLY for those no journal dates."""
    J = journal_times()
    first_step = collections.defaultdict(lambda: None)        # (run, idea id): its first journal time, any bar
    for (run, rid, _), t in J.items():
        k = (run, BAR.sub("", rid or ""))
        first_step[k] = min(t, first_step[k]) if first_step[k] else t
    briefs_at = {}                                             # (run, brief stem): the loop line that wrote it
    for lj in STEPS.glob("orchestration/loop/*_run/loop.jsonl"):
        for x in loop_lines(lj.parent.name):
            if x.get("brief") and x.get("discovery") and ts(x.get("at")):
                briefs_at[(lj.parent.name, x["brief"])] = ts(x["at"])
    out = []
    for f in STEPS.glob("03_test_plan/*_run/plans/*.md"):
        out.append((J.get((f.parents[1].name, f.stem, "step3_plan"), EARLY), f))
    for f in STEPS.glob("05_verification/*_run/verdicts/*/result.json"):
        out.append((J.get((f.parents[2].name, f.parent.name, "step5_verdict"), EARLY), f))
    for f in STEPS.glob("06_profitability/*_run/checks/*/result.json"):
        out.append((J.get((f.parents[2].name, f.parent.name, "step6_check"), EARLY), f))
    for f in STEPS.glob("01_brief/*_run/briefs/*.md"):
        out.append((briefs_at.get((f.parents[1].name, f.stem), EARLY), f))
    for f in STEPS.glob("02_ideation/*_run/ideas/*.md"):
        run = f.parents[1].name
        if "." in f.stem.split("_")[0]:                       # a line's idea copied in by run_idea when it was turned
            out.append((first_step[(run, f.stem)] or EARLY, f))
        else:
            n = f.stem.split("-")[0]
            b = [t for (r, s), t in briefs_at.items() if r == run and s.split("_")[0] == n]
            out.append((min(b) if b else EARLY, f))
    for f in STEPS.glob("07?_*/*_run/*/ideas/*.md"):
        line = "7." + f.parents[3].name[2]
        out.append((J.get((f.parents[2].name, f.parents[1].name, f"step7_{line}"), EARLY), f))
    return [(t, f.relative_to(STEPS)) for t, f in out]


def git_versions(rel):
    """[(commit time, content)] of a file in git, oldest first."""
    path = f"strategy_designer_v2/steps_cards/{rel}"
    log = subprocess.run(["git", "log", "--format=%H %cI", "--", path], cwd=STEPS.parents[1], capture_output=True, text=True).stdout
    out = []
    for l in reversed(log.split("\n")):
        if l.strip():
            h, t = l.split()
            when = datetime.strptime(t[:19], "%Y-%m-%dT%H:%M:%S")
            out.append((when, subprocess.run(["git", "show", f"{h}:{path}"], cwd=STEPS.parents[1], capture_output=True, text=True).stdout))
    return out


class Tree:
    """The files as they stood at a time: links added as the time moves on; the loop's lines and the register written."""

    def __init__(self, root):
        self.root = root
        shutil.rmtree(root, ignore_errors=True)
        root.mkdir(parents=True)
        (root / "components").symlink_to(STEPS / "components")
        self.files = sorted(dated_files(), key=lambda x: x[0])
        self.i = 0
        self.when = {rel: t for t, rel in self.files}
        self.files_at = lambda rel: self.when.get(rel, EARLY)
        self.books = json.loads((sn.REGISTER / "books.json").read_text())
        reg = root / "orchestration" / "ideas_similarities_check" / "register"
        reg.mkdir(parents=True)
        (reg / "comparisons").symlink_to(sn.REGISTER / "comparisons")
        (reg / "held.json").symlink_to(sn.REGISTER / "held.json")
        self.loops = [p.parent.name for p in STEPS.glob("orchestration/loop/*_run/loop.jsonl")]
        self.versioned = {f.relative_to(STEPS): git_versions(f.relative_to(STEPS))
                          for run in RUNS for f in (STEPS / "01_brief" / run / "briefs").glob("*.md")}
        assert all(self.versioned.values()), "a brief of night 9 with no version in git"

    def at(self, T):
        while self.i < len(self.files) and self.files[self.i][0] <= T:
            rel = self.files[self.i][1]
            (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
            if not (self.root / rel).exists() and rel not in self.versioned:
                (self.root / rel).symlink_to(STEPS / rel)
            self.i += 1
        for rel, vs in self.versioned.items():                 # a brief there at T: as git had it at T
            if self.files_at(rel) <= T and vs:
                (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
                (self.root / rel).write_text(([c for t, c in vs if t <= T] or [vs[0][1]])[-1])
        reg = self.root / "orchestration" / "ideas_similarities_check" / "register"
        (reg / "books.json").write_text(json.dumps([b for b in self.books if (ts(b.get("added_utc")) or EARLY) <= T]))
        for run in self.loops:
            d = self.root / "orchestration" / "loop" / run
            d.mkdir(parents=True, exist_ok=True)
            lines = [x for x in loop_lines(run) if (ts(x.get("at")) or EARLY) <= T]
            (d / "loop.jsonl").write_text("".join(json.dumps(x) + "\n" for x in lines))


def decisions():
    """[(T, run, idea, backtest, 7.g's journal action, its USD)] for every idea night 9's loop tested, in time order."""
    out = []
    for run in RUNS:
        jl = [json.loads(l) for l in (STEPS / "orchestration" / "run_idea" / run / "journal.jsonl").read_text().splitlines() if l.strip()]
        tab = {r["backtest"]: r for r in json.loads((STEPS / "orchestration" / "run_idea" / run / "table.json").read_text())}
        order = []
        for x in loop_lines(run):
            if x.get("idea") and ("turn" in x or "resumed" in x) and x["idea"] not in order:
                order.append(x["idea"])
        for idea in order:
            for rid in sorted({e["backtest"] for e in jl if BAR.sub("", e["backtest"]) == idea}):
                s7 = [e for e in jl if e["backtest"] == rid and e["step"].startswith("step7_")]
                if not s7:
                    continue                                  # stopped before step 7 (no plan, a failure)
                T = min(ts(e["at"]) - timedelta(seconds=e["seconds"]) for e in s7)
                g = [e for e in s7 if e["step"] == "step7_7.g"]
                usd = tab.get(rid, {}).get("consumption", {}).get("step7_7.g", {}).get("usd", 0.0)
                out.append((T, run, idea, rid, g[0]["action"] if g else "no line", usd))
    return sorted(out)


def paying(run, keep):
    """The ideas of the run's table that keep() selects, confirmed by step 5 and profitable enough by step 6."""
    tab = json.loads((STEPS / "orchestration" / "run_idea" / run / "table.json").read_text())
    return [r["idea"] for r in tab if keep(r["idea"]) and str(r.get("step5", "")).startswith("confirmed")
            and str(r.get("step6", "")).startswith("profitable")]


def what_it_gave(run, rid):
    """What 7.g's analysis of this backtest led to: each discovery's brief, with the strategies of the brief's lineage
    (its ideas and their follow-ups) that are confirmed and profitable enough; each on-theme idea, with its lineage's."""
    d = STEPS / "07g_patterns" / run / rid
    briefs = {Path(x["discovery"]).stem: x.get("brief") for x in loop_lines(run) if x.get("discovery")}
    disc = {}
    for f in sorted((d / "discoveries").glob("*.md")):
        b = briefs.get(f.stem)
        n = b.split("_")[0] + "-" if b else None
        disc[f.stem] = {"brief": b, "pays": paying(run, lambda i: i.startswith(n)) if n else []}
    on = {}
    for f in sorted((d / "ideas").glob("*.md")):
        c = idea_code(f.stem)
        on[f.stem] = paying(run, lambda i: (idea_code(i) + ".").startswith(c + "."))
    return disc, on


def full_rank(run, idea, root, failed):
    """The variant first built and rejected (2026-11-27): 7.g's idea given the group and the priority of any follow-up of
    the tested idea (its difference w), compared by (group, priority) with the best waiting idea. (call, its, the best's)."""
    ranking = sn.rank(run, root, failed)
    recs = sn.records(root)
    me = next((r for r in ranking if r["idea"] == idea), None)
    gen = (me["generation"] if me else sn.id_parts(idea)[3]) + 1
    score = round(max(sn.record_of("7.g", recs), sn.record_of(sn.DISCOVERY, recs)) / (1 + gen), 4)
    ev = sn.parent_evidence(root)
    d = ev.get((run, idea), ev.get((run, idea_code(idea)), (None, None)))[1] if sn.parent_confirmed(run, idea, root) else None
    w = d if d is not None else 0.5
    mine = (2 if w > 0.5 else 3, round(score * w, 4))
    cands = [r for r in ranking if r["status"] == "candidate"]
    if not cands:
        return True, mine, None
    best = (cands[0]["group"], cands[0]["priority"])
    return (mine[0], -mine[1]) <= (best[0], -best[1]), mine, best


def main():
    out_dir = Path(sys.argv[1]).resolve()
    tree = Tree(out_dir / "tree")
    rows = []
    for T, run, idea, rid, action, usd in decisions():
        tree.at(T)
        failed = loop.failed(run, tree.root / "orchestration")
        call, why = sn.discovery_call(run, idea, tree.root, exclude=failed)
        full, mine, best = full_rank(run, idea, tree.root, failed)
        row = {"at": T.strftime("%Y-%m-%dT%H:%M:%SZ"), "run": run, "idea": idea, "backtest": rid, "action": action,
               "usd": usd, "call": call, "why": why, "call_full_rank": full, "full_rank_new": mine, "full_rank_best": best}
        if action.startswith("called"):
            row["discoveries"], row["on_theme"] = what_it_gave(run, rid)
        rows.append(row)
        print(f"{row['at']} {run[7:]} {idea[:40]:40} {action[:16]:16} {usd:5.2f} rule={'call' if call else 'skip'} "
              f"full-rank={'call' if full else 'skip'}", flush=True)
    (out_dir / "replay.json").write_text(json.dumps(rows, indent=1) + "\n")


if __name__ == "__main__":
    main()
