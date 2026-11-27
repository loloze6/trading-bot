"""Build B10: how exact the replay's rebuilt queues are. At every turn night 9's loop logged ("select_next rank 1"), the
queue rebuilt at the turn's time (replay.py's Tree) and ranked by select_next as it was that night (this build's base, 7b7f0e8bbd8,
before B10); its first idea compared with the one the loop chose.
  python3 runs/build_b10/fidelity.py OUT_DIR       (from steps_cards; reads files only, writes OUT_DIR/fidelity.json)"""
import importlib.util, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import replay  # noqa: E402

STEPS = replay.STEPS


def old_select_next(out_dir):
    src = subprocess.run(["git", "show", "7b7f0e8bbd8:strategy_designer_v2/steps_cards/orchestration/select_next/helper/select_next.py"],
                         cwd=STEPS.parents[1], capture_output=True, text=True, check=True).stdout
    f = out_dir / "select_next_before_b10.py"
    f.write_text(src.replace("HERE = Path(__file__).resolve().parent", f"HERE = Path({str(STEPS / 'orchestration/select_next/helper')!r})"))
    spec = importlib.util.spec_from_file_location("select_next_before_b10", f)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def main():
    out_dir = Path(sys.argv[1]).resolve()
    old = old_select_next(out_dir)
    tree = replay.Tree(out_dir / "tree")
    turns = []
    for run in replay.RUNS:
        for x in replay.loop_lines(run):
            if "turn" in x and str(x.get("why", "")).startswith("select_next rank 1"):
                turns.append((replay.ts(x["at"]), run, x["idea"]))
    rows = []
    for T, run, chosen in sorted(turns):
        tree.at(T)
        failed = replay.loop.failed(run, tree.root / "orchestration")
        cands = [r for r in old.rank(run, tree.root, failed) if r["status"] == "candidate"]
        top = cands[0]["idea"] if cands else None
        rows.append({"at": T.strftime("%Y-%m-%dT%H:%M:%SZ"), "run": run, "chosen": chosen, "rebuilt_first": top,
                     "same": top == chosen, "chosen_rank": next((i + 1 for i, r in enumerate(cands) if r["idea"] == chosen), None)})
        print(rows[-1]["at"], run[7:], rows[-1]["same"], rows[-1]["chosen_rank"], flush=True)
    (out_dir / "fidelity.json").write_text(json.dumps(rows, indent=1) + "\n")
    same = sum(r["same"] for r in rows)
    print(f"turns: {len(rows)}; the rebuilt queue's first idea is the loop's choice: {same}; "
          f"its rank otherwise: {sorted(r['chosen_rank'] or 0 for r in rows if not r['same'])}")


if __name__ == "__main__":
    main()
