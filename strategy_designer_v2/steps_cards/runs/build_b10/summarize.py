"""Build B10: the replay's counts (replay.py's replay.json), per run, for the rule and for the variant rejected.
  python3 runs/build_b10/summarize.py OUT_DIR/replay.json > runs/build_b10/replay_result.txt   (from steps_cards)
For each of night 9's profitable strategies (confirmed by step 5, profitable enough by step 6): the 7.g calls on its path
(a discovery its brief came from, an on-theme idea of 7.g it descends from), and whether the rule would have skipped one.
The replay is not a simulation: a skipped call's later turns are those that happened, not those that would have."""
import json, re, sys, collections, glob
from pathlib import Path

STEPS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(STEPS / "common"))
from lib import idea_code  # noqa: E402

rows = json.loads(Path(sys.argv[1]).read_text())
print("| Run | Tests | 7.g calls made | Their USD | Calls the rule skips | Their USD | Of which behind a brief's own idea | "
      "Variant (w and groups): skips | Its USD |\n|---|---|---|---|---|---|---|---|---|")
tot = collections.Counter()
for run in sorted({r["run"] for r in rows}):
    R = [r for r in rows if r["run"] == run]
    made = [r for r in R if r["action"].startswith("called")]
    sk = [r for r in made if not r["call"]]
    fv = [r for r in made if not r["call_full_rank"]]
    c = collections.Counter(tests=len(R), made=len(made), usd=sum(r["usd"] for r in made), skip=len(sk),
                            skip_usd=sum(r["usd"] for r in sk), g1=sum("brief's own idea" in r["why"] for r in sk),
                            full=len(fv), full_usd=sum(r["usd"] for r in fv))
    tot.update(c)
    print(f"| {run} | {c['tests']} | {c['made']} | {c['usd']:.2f} | {c['skip']} | {c['skip_usd']:.2f} | {c['g1']} | {c['full']} | {c['full_usd']:.2f} |")
c = tot
print(f"| all | {c['tests']} | {c['made']} | {c['usd']:.2f} | {c['skip']} | {c['skip_usd']:.2f} | {c['g1']} | {c['full']} | {c['full_usd']:.2f} |")
print(f"\nCalls kept by the rule: {c['made'] - c['skip']}, of which with nothing waiting: "
      f"{sum(r['call'] and 'nothing waits' in r['why'] for r in rows)}. 7.g calls whose helper failed: "
      f"{sum('failed' in r['action'] for r in rows)} (counted as made).")

# night 9's profitable strategies and the 7.g calls on their path
briefs = {}
for f in glob.glob(str(STEPS / "orchestration/loop/night9_*_run/loop.jsonl")):
    run = Path(f).parent.name
    for x in (json.loads(l) for l in open(f) if l.strip()):
        if x.get("brief") and x.get("discovery"):
            briefs[(run, x["brief"].split("_")[0])] = re.sub(r"_\d+[mhdw]$", "", x["discovery"].split("/")[2])
by = {(r["run"], idea_code(r["idea"])): r for r in rows}
print("\nNight 9's profitable strategies (confirmed, profitable enough) and the 7.g calls on their path:\n")
print("| Run | Strategy | 7.g calls on its path (the tested idea read) | Rule | Variant |\n|---|---|---|---|---|")
lost = collections.Counter()
for t in sorted(glob.glob(str(STEPS / "orchestration/run_idea/night9_*_run/table.json"))):
    run = Path(t).parent.name
    for r in json.loads(Path(t).read_text()):
        if not (str(r.get("step5", "")).startswith("confirmed") and str(r.get("step6", "")).startswith("profitable")):
            continue
        path, cur = [], r["idea"]
        while True:
            parts = idea_code(cur).split(".")
            path += [".".join(parts[:k]) for k in range(len(parts) - 1, 0, -1) if parts[k][0] == "g"]
            src = briefs.get((run, parts[0].split("-")[0]))
            if not src:
                break
            path.append(idea_code(src))
            cur = src
        calls = [by[(run, p)] for p in path if (run, p) in by]
        rule = "skipped: " + ", ".join(idea_code(x["idea"]) for x in calls if not x["call"]) if any(not x["call"] for x in calls) else "all called"
        var = "skipped: " + ", ".join(idea_code(x["idea"]) for x in calls if not x["call_full_rank"]) if any(not x["call_full_rank"] for x in calls) else "all called"
        lost["rule"] += rule != "all called"; lost["variant"] += var != "all called"; lost["all"] += 1
        print(f"| {run} | {idea_code(r['idea'])} | {', '.join(path) or '-'} | {rule} | {var} |")
print(f"\nProfitable strategies with a skipped 7.g call on their path: the rule {lost['rule']} of {lost['all']}; "
      f"the variant {lost['variant']} of {lost['all']}.")
