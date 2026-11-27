"""Build A12, proof: the prompts of steps 1, 2 and 7 without a box and without data_use.json, before and after.

  python3 runs/build_a12/prompts_before_after.py BASE_COMMIT

Composes each step's system prompt from the files at BASE_COMMIT and from the working files, the way the helpers do
(common/lib.py, with_common), and prints the difference. Step 1: also its request and the files it writes, with the
model call replaced by a fixed answer (no model call anywhere here).
"""
import contextlib, difflib, importlib.util, io, re, subprocess, sys, tempfile
from pathlib import Path

STEPS = Path(__file__).resolve().parents[2]
BASE = sys.argv[1]


def old(rel):
    return subprocess.run(["git", "show", f"{BASE}:strategy_designer_v2/steps_cards/{rel}"], cwd=STEPS, capture_output=True,
                          text=True, check=True).stdout


def new(rel):
    return (STEPS / rel).read_text()


def filled(text, read):
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: read(f"common/{m.group(1).lower()}.md"), text)


def diff(name, a, b):
    d = [l for l in difflib.unified_diff(a.splitlines(), b.splitlines(), "before", "after", lineterm="", n=0)
         if not l.startswith(("---", "+++", "@@"))]
    print(f"\n## {name}: {len(a.splitlines())} lines before, {len(b.splitlines())} after; "
          f"{sum(l.startswith('+') for l in d)} added, {sum(l.startswith('-') for l in d)} removed")
    print("\n".join(d) or "(identical)")


def step2(read):
    return filled(read("02_ideation/helper/system_prompt.md"), read)


def step7(read, line):
    """analyse.py's system prompt: the common rules, the measures, the line's prompt, the output format (the profile
    map is the same file on both sides)."""
    s = (read("07_common/helper/common_rules.md") + "\n[HOW THE WORKFLOW MEASURES]\n" + read("common/measures.md") + "\n"
         + filled(read(f"{line}/helper/line_prompt.md").replace("{{PROFILE_MAP}}", "(the profile map)"), read)
         + "\n" + read("07_common/helper/output_one_call.md")
         ).replace("{{IDEA_DEFINITION}}", read("common/idea_definition.md"))
    return filled(s, read)


def step1(source):
    """Step 1's call (system, request) and the files it writes, the model's answer fixed; `source`: make_brief.py's text."""
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "make_brief.py"
        f.write_text(source.replace("HERE = Path(__file__).resolve().parent", f"HERE = Path({str(STEPS / '01_brief' / 'helper')!r})")
                     .replace('sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))',
                              f"sys.path.insert(0, {str(STEPS / 'common')!r})"))
        spec = importlib.util.spec_from_file_location("mb", f)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        seen = []
        m.call = lambda model, system, request: seen.append((system, request)) or (
            "---\ninstruments: LINK, UNI, SOL\nbar: 1d\n---\nA theory.\n\nshort-name: a b c\nindex-line: a theory [bar: 1d]\n", 0.0)
        out = {}
        for label, extra in (("no --run", []), ("--run of a run without a box or data_use.json", ["--run", "a12_no_such_run"])):
            d = Path(tmp) / label.replace(" ", "_")
            sys.argv = ["make_brief.py", "--theme", "calm declines", "--briefs-dir", str(d)] + extra
            with contextlib.redirect_stdout(io.StringIO()):
                m.main()
            out[label] = (seen[-1], {p.name: p.read_text() for p in sorted(d.iterdir())})
        return out


print(f"Base: {BASE}")
diff("step 2, system prompt", step2(old), step2(new))
for line in sorted(p.name for p in STEPS.glob("07?_*") if (p / "helper" / "line_prompt.md").exists()):
    diff(f"step {line[:3]}, system prompt", step7(old, line), step7(new, line))
for f in ("02_ideation/helper/make_ideas.py", "07_common/helper/analyse.py"):
    a, b = old(f), new(f)
    req = lambda t: [l.strip() for l in t.splitlines() if "request = " in l or "context = " in l or "theme_note" in l or l.strip().startswith('f"Write the ideas')]
    print(f"\n## {f}: the lines that build the request: {'identical' if req(a) == req(b) else 'DIFFERENT'}")
a, b = step1(old("01_brief/helper/make_brief.py")), step1(new("01_brief/helper/make_brief.py"))
print("\n## step 1 (system prompt, request and files written, a fixed answer in place of the model)")
for label in a:
    (sa, ra), fa = a[label]; (sb, rb), fb = b[label]
    print(f"- {label}: system prompt {'identical' if sa == sb else 'DIFFERENT'} ({len(sa)} characters); request "
          f"{'identical' if ra == rb else 'DIFFERENT'}; files {'identical' if fa == fb else 'DIFFERENT'} ({', '.join(fa)})")
