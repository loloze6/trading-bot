"""B13's proof that run_brief's `ideas_of` (a brief's own ideas: its number and, now, its header) gives the same ideas
as before (7b7f0e8bbd8's: the number alone) for every brief of every run. Reads only.
  python3 runs/build_b2_1/ideas_of_all_runs.py"""
import re, subprocess, sys, types
from pathlib import Path
STEPS = Path(__file__).resolve().parents[2]; REPO = STEPS.parents[1]
f = STEPS / "orchestration" / "run_brief" / "helper" / "run_brief.py"
sys.path.insert(0, str(f.parent))
import run_brief as new
src = subprocess.run(["git", "show", f"7b7f0e8bbd8:{f.relative_to(REPO)}"], cwd=REPO, capture_output=True, text=True, check=True).stdout
old = types.ModuleType("run_brief_old"); old.__file__ = str(f); exec(compile(src, str(f), "exec"), old.__dict__)
pairs = same = ideas = 0; diff = []
for b in sorted(STEPS.glob("01_brief/*_run/briefs/[0-9][0-9][0-9]_*.md")):
    d = STEPS / "02_ideation" / b.parents[1].name / "ideas"
    a, o = new.ideas_of(b, d), old.ideas_of(b, d)
    pairs += 1; ideas += len(o); same += a == o
    if a != o: diff.append((str(b.relative_to(STEPS)), [p.name for p in o if p not in a]))
print(f"briefs in runs: {pairs}; the same ideas: {same}; different: {len(diff)}; ideas compared: {ideas}")
for x in diff: print(" ", x)
