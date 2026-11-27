"""B2.1's proof that a run without a target box is unchanged: select_next's ranking of every named run with the code
before B2.1 (7b7f0e8bbd8) and with B2.1's, compared row by row. Reads only.  python3 runs/build_b2_1/select_next_all_runs.py"""
import subprocess, sys, types
from pathlib import Path
STEPS = Path(__file__).resolve().parents[2]
REPO = STEPS.parents[1]
f = STEPS / "orchestration" / "select_next" / "helper" / "select_next.py"
sys.path.insert(0, str(f.parent))
import select_next as new
old = types.ModuleType("select_next_old"); old.__file__ = str(f)
src = subprocess.run(["git", "show", f"7b7f0e8bbd8:{f.relative_to(REPO)}"], cwd=REPO, capture_output=True, text=True, check=True).stdout
exec(compile(src, str(f), "exec"), old.__dict__)
runs = sorted({p.parent.name for p in STEPS.glob("02_ideation/*_run/ideas")} | {p.parents[1].name for p in STEPS.glob("07?_*/*_run/*/ideas")})
same = rows = 0; diff = []
for run in runs:
    a, b = new.rank(run), old.rank(run)
    rows += len(a)
    if a == b: same += 1
    else: diff.append(run)
print(f"runs: {len(runs)}; ranking identical: {same}; different: {len(diff)} {diff}; rows compared: {rows}")
