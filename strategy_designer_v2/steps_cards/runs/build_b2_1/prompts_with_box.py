"""B2.1's proof of the theme note (common/target_box.md): the prompts steps 1 and 2 and line 7.g would send, captured at the
model call (no call is made), with the code before B2.1 (7b7f0e8bbd8) and with B2.1's, without a box and with one.
  python3 runs/build_b2_1/prompts_with_box.py OUT_DIR
Inputs (read only): night 9 E's 074-01.b1.g1 (its record, plan, verdict, check, brief). The outputs go to OUT_DIR."""
import subprocess, sys, types
from pathlib import Path
STEPS = Path(__file__).resolve().parents[2]; REPO = STEPS.parents[1]
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
S, R = "night9_fallcalmfade_run", "074-01.b1.g1_convex-deep-run-fade_1d"
sys.path.insert(0, str(STEPS / "common"))
import target_box
BOX = {"profile": "falling calm", "side": "long"}


class Captured(Exception):
    pass


def load(rel, version):
    f = STEPS / rel
    sys.path.insert(0, str(f.parent))
    m = types.ModuleType(f.stem + "_" + version); m.__file__ = str(f)
    src = f.read_text() if version == "new" else subprocess.run(["git", "show", f"7b7f0e8bbd8:{f.relative_to(REPO)}"],
                                                                 cwd=REPO, capture_output=True, text=True, check=True).stdout
    exec(compile(src, str(f), "exec"), m.__dict__)
    return m


def capture(m, argv):
    got = {}
    def call(model, system, user, *a, **k):
        got["system"], got["user"] = system, user
        raise Captured
    m.call = call
    old, sys.argv = sys.argv, argv
    try:
        m.main()
    except Captured:
        pass
    finally:
        sys.argv = old
    return got["system"] + "\n=====USER=====\n" + got["user"]


tmp = OUT / "scratch"; (tmp / "ideas").mkdir(parents=True, exist_ok=True)
cases = {"step1": ("01_brief/helper/make_brief.py",
                   ["make_brief.py", "--theme", "a strong daily fall is followed by a rebound",
                    "--briefs-dir", str(STEPS / "01_brief" / "briefs")]),
         "step2": ("02_ideation/helper/make_ideas.py",
                   ["make_ideas.py", str(STEPS / "01_brief" / S / "briefs" / "074_falling-market-run-break-fade.md"),
                    "--ideas-dir", str(STEPS / "02_ideation" / S / "ideas")]),
         "7g": ("07_common/helper/analyse.py",
                ["analyse.py", str(STEPS / "07g_patterns"), str(STEPS / "04_backtest" / S / "backtests" / R),
                 "--plan", str(STEPS / "03_test_plan" / S / "plans" / f"{R}.md"), "--briefs-dir", str(STEPS / "01_brief" / S / "briefs"),
                 "--verdicts-dir", str(STEPS / "05_verification" / S / "verdicts"), "--checks-dir", str(STEPS / "06_profitability" / S / "checks"),
                 "--python", sys.executable, "--out-dir", str(tmp / "7g")])}
real_run_box = target_box.run_box
for name, (rel, argv) in cases.items():
    target_box.run_box = real_run_box                                   # night 9 E has no box
    old = capture(load(rel, "old"), argv)
    new = capture(load(rel, "new"), argv)
    target_box.run_box = lambda run, steps=None: BOX if run == S else None
    boxed = capture(load(rel, "new"), argv + (["--run", S] if name == "step1" else []))   # run_brief adds it for a boxed run
    for k, v in (("old", old), ("new", new), ("boxed", boxed)):
        (OUT / f"{name}_{k}.txt").write_text(v)
    print(f"{name}: without a box, new == old byte for byte: {new == old} ({len(new)} characters); "
          f"with a box: +{len(boxed) - len(new)} characters, the note after the brief: {(target_box.theme_note(S) in boxed)}")
print("\nThe note, as it appears for line 7.g (after the brief):\n" + target_box.theme_note(S))
