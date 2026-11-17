"""run_brief: one trading theory researched from end to end: step 1 (theme or source only), step 2, then loop.

  python3 orchestration/run_brief/helper/run_brief.py --run NAME_run --python VENV_PYTHON
      (BRIEF_FILE | --theme "TEXT" | --source FILE) [--budget USD] [--model M]

It adds no rule of its own: steps 1 and 2 as validated, the next idea by select_next, the stop rules of loop. Its state
is the run's files, so a second call resumes. Visibility only: orchestration/run_brief/<run>/journal.jsonl (one line
per call of step 1 or 2) and logs/<brief>/<step>.txt. Card: ../card.md.
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORCH = HERE.parents[1]
STEPS = ORCH.parent
sys.path.insert(0, str(ORCH / "run_idea" / "helper"))
sys.path.insert(0, str(STEPS / "common"))
from run_idea import Journal, copy_into  # noqa: E402  (one journal for every orchestration function)

BRIEFS = STEPS / "01_brief" / "briefs"          # step 1's list of every brief: one number per theory
LOOP = ORCH / "loop" / "helper" / "loop.py"
BRIEF_LINE = re.compile(r"^brief:\s*(\S+\.md)\s*$", re.M)
NOT_RESEARCHABLE = re.compile(r"^not researchable:\s*(.+)$", re.M)


def brief_number(brief):
    m = re.match(r"(\d{3})_", Path(brief).name)
    if not m:
        sys.exit(f"{Path(brief).name}: a brief's file name starts with its number (NNN_)")
    return m.group(1)


def ideas_of(brief, ideas_dir):
    """The run's ideas created from this brief by step 2: ids NNN-KK_name (an id with a line's .<letter><n>_ part is
    an idea a line created, even when a run copied it here as its starting idea)."""
    num = brief_number(brief)
    return sorted(p for p in Path(ideas_dir).glob(f"{num}-*.md") if re.fullmatch(rf"{num}-\d{{2}}_[^.]+", p.stem))


def spent(table_dir):
    """USD of the run's step 1 and step 2 calls, from this function's journal."""
    p = Path(table_dir) / "journal.jsonl"
    return round(sum(json.loads(l).get("usd", 0.0) for l in p.read_text().splitlines()), 4) if p.exists() else 0.0


def loop_budget(budget, brief_usd):
    """The budget is the run's total; the loop counts only the tested ideas, so it gets what steps 1 and 2 left."""
    return None if budget is None else round(budget - brief_usd, 4)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("brief", type=Path, nargs="?", help="a brief file (step 1's format)")
    a.add_argument("--theme", help="a theme in the operator's words: step 1 writes the brief")
    a.add_argument("--source", type=Path, help="a source the operator pastes: step 1 writes the brief")
    a.add_argument("--run", required=True)
    a.add_argument("--python", required=True)
    a.add_argument("--budget", type=float, help="the run's total USD, steps 1 and 2 included (optional; no limit otherwise)")
    a.add_argument("--model")
    args = a.parse_args()
    if not args.run.endswith("_run"):
        sys.exit("a run name ends in _run")
    if sum(x is not None for x in (args.brief, args.theme, args.source)) != 1:
        sys.exit("give exactly one of: a brief file, --theme, --source")
    if args.brief is not None and not args.brief.exists():
        sys.exit(f"no brief file {args.brief}")
    if args.source is not None and not args.source.exists():
        sys.exit(f"no source file {args.source}")
    if args.budget is not None and args.budget <= 0:
        sys.exit("a budget is a positive number of USD")

    table_dir = ORCH / "run_brief" / args.run
    run_briefs = STEPS / "01_brief" / args.run / "briefs"
    ideas_dir = STEPS / "02_ideation" / args.run / "ideas"
    model = ["--model", args.model] if args.model else []

    brief = args.brief
    if brief is None:                                   # step 1: a theme or a source becomes a brief
        what = ["--theme", args.theme] if args.theme else ["--source", args.source]
        j = Journal(table_dir, args.run, "step1_" + re.sub(r"\W+", "-", (args.theme or args.source.stem))[:40].strip("-"))
        out, _ = j.step("step1_brief", [STEPS / "01_brief/helper/make_brief.py", *what, "--briefs-dir", BRIEFS] + model,
                        [BRIEFS / "INDEX.md"])
        nr, b = NOT_RESEARCHABLE.search(out), BRIEF_LINE.search(out)
        if nr:
            print(f"{args.run}: step 1: not researchable: {nr.group(1)}")
            return
        if not b:
            sys.exit(f"step 1 wrote no brief:\n{out[-800:]}")
        brief = Path(b.group(1))

    run_briefs.mkdir(parents=True, exist_ok=True)
    copy_into(brief, run_briefs / brief.name)           # where the run's ideas find their brief
    j = Journal(table_dir, args.run, brief.stem)
    out, _ = j.step("step2_ideas", [STEPS / "02_ideation/helper/make_ideas.py", run_briefs / brief.name,
                                    "--ideas-dir", ideas_dir] + model,
                    [ideas_dir / "INDEX.md"], done=bool(ideas_of(brief, ideas_dir)))
    ideas = ideas_of(brief, ideas_dir)
    if not ideas:
        why = re.search(r"^no-ideas:\s*(.+)$", out, re.M)
        sys.exit(f"{args.run}: step 2 wrote no idea for {brief.stem}" + (f": {why.group(1)}" if why else f":\n{out[-800:]}"))
    print(f"{args.run}: {brief.stem}: {len(ideas)} ideas in the run")

    budget = loop_budget(args.budget, spent(table_dir))
    if budget is not None and budget <= 0:
        print(f"{args.run}: stopped: budget reached by steps 1 and 2 ({spent(table_dir):.2f} USD)")
        return
    cmd = [sys.executable, str(LOOP), "--run", args.run, "--python", args.python] + model
    if budget is not None:
        cmd += ["--budget", str(budget)]
    sys.exit(subprocess.run(cmd).returncode)


if __name__ == "__main__":
    main()
