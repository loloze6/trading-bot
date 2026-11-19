"""components step: answer the open wishes of runs, one model call each: exists, built, or cannot build.

  python3 components/helper/build_component.py --runs NAME_run [NAME_run ...] --python VENV_PYTHON [--model M]
  python3 components/helper/build_component.py --runs NAME_run [NAME_run ...] --list

For each open wish (a line of a run's COMPONENT_WISHLIST.md with no line in components/INDEX.md), one closed-book call
reads it against the component catalogue as it stands (with what this call built before it). The answer:
- exists: the class and settings are checked against the catalogue; nothing is written but the index line;
- built: the class is written in trading-bot/strategies/strategy_components.py (appended, or replacing the class it
  gives a new setting), its row in step 3's catalogue, its spec (settings and hand computation) in
  trading-bot/tests/built_components/; then the standard checks (trading-bot/tests/component_harness.py, on real data;
  for a class given a new setting, its output at the old defaults unchanged) and the bot's suite. A failure undoes the
  files and goes back to the model with its output; after three attempts: cannot build;
- cannot build: the reason, in the index line.
Every answer is one line in components/INDEX.md, so a wish is not asked twice. Visibility: components/journal.jsonl (one
line per wish: run, plan, wish, answer, USD, seconds, attempts) and components/builds/<class>/ (the answers, the checks'
output; a build undone: components/builds/not_built/<run>/<plan>/<wish>/). Card: ../card.md.
A build in progress keeps the three files as they were in components/build_in_progress.json (not committed): a build cut
short (a restart) is undone at the step's next start, from that note, with one journal line; its wish is asked again.
"""
import argparse, json, re, subprocess, sys, tempfile, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = HERE.parents[1]
REPO = STEPS.parents[1]
TBOT = REPO / "trading-bot"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(STEPS / "common"))
from lib import call, write_atomic, CATALOGUE, utc_now  # noqa: E402  (shared helpers, common/lib.py)
import wishes as W  # noqa: E402

COMPONENTS_FILE = TBOT / "strategies" / "strategy_components.py"
BASE_FILE = TBOT / "strategies" / "strategy_base.py"
SPECS = TBOT / "tests" / "built_components"
HARNESS = TBOT / "tests" / "component_harness.py"
EXAMPLE = "VolumeRatioComponent"     # the worked example pasted into the call: its class and its spec
TABLES = ("Regime measures", "Directional components", "Hedges and filters")
ATTEMPTS = 3
ROOT = HERE.parent
PENDING = ROOT / "build_in_progress.json"   # the files as they were, while a build runs (not committed)


# ---- the files a build changes ----------------------------------------------------------------------------------

def class_source(text, name):
    """The source of one class in a module's text, from its `class` line to the next top-level class (or the end)."""
    m = re.search(rf"^class {re.escape(name)}\(.*?(?=^class |\Z)", text, re.S | re.M)
    return m.group(0).rstrip() + "\n" if m else None


def classes_in(text):
    return re.findall(r"^class (\w+)\(", text, re.M)


def catalogue_rows(cat):
    """{class: its params} from the catalogue's component rows."""
    rows = cat[cat.index("## Component rows"):cat.index("## Variant patterns")]
    return {n: set(re.findall(r"`(\w+)` \(", p)) for n, p in re.findall(r"^\| `(\w+)` \| ([^|]*) \|", rows, re.M)}


def with_class(module, name, source):
    """The module's text with the class replaced (same name) or appended."""
    old = class_source(module, name)
    if old:
        return module.replace(old.rstrip() + "\n", source.rstrip() + "\n", 1)
    return module.rstrip() + "\n\n\n" + source.rstrip() + "\n"


def with_row(cat, name, table, row):
    """The catalogue with the class's row replaced, or inserted at the end of its table; the class count updated."""
    row = row.strip()
    lines = cat.split("\n")
    at = next((i for i, l in enumerate(lines) if l.startswith(f"| `{name}` |")), None)
    if at is not None:
        lines[at] = row
    else:
        start = next(i for i, l in enumerate(lines) if l.strip() == f"### {table}")
        i = start + 1
        while i < len(lines) and not lines[i].startswith("|"):
            i += 1
        while i < len(lines) and lines[i].startswith("|"):
            i += 1
        lines.insert(i, row)
    return "\n".join(lines)


def with_count(cat, n):
    return re.sub(r"There are \d+ classes", f"There are {n} classes", cat, count=1)


def spec_settings(text):
    """The SETTINGS list of a spec file, read as a Python literal (a spec written by hand may carry comments)."""
    import ast
    for node in ast.parse(text).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "SETTINGS" for t in node.targets):
            return ast.literal_eval(node.value)
    return []


def spec_text(name, settings, hand, before=None):
    """The spec: the defaults first, then the settings checked before (a class given a new setting keeps them), then
    this wish's."""
    first = [{}]
    for s_ in (before or []) + [settings]:
        if s_ not in first:
            first.append(s_)
    return (f'"""Spec of {name} for the standard checks (component_harness.py), written by the components step: its '
            f'settings (the defaults first) and a hand computation that uses only the rows up to bar t."""\n'
            f"CLASS = {name!r}\nSETTINGS = {json.dumps(first)}\n\n\n{hand.strip()}\n")


# ---- the call ---------------------------------------------------------------------------------------------------

def system_prompt():
    base = class_source(BASE_FILE.read_text(encoding="utf-8"), "SubStrategyComponent")
    example = class_source(COMPONENTS_FILE.read_text(encoding="utf-8"), EXAMPLE)
    spec = (SPECS / f"{EXAMPLE}.py").read_text(encoding="utf-8")
    return ((HERE / "system_prompt.md").read_text(encoding="utf-8")
            + f"\n\n[COMPONENT CATALOGUE]\n{CATALOGUE.read_text(encoding="utf-8")}"
            + f"\n[THE BASE CLASS]\n{base}"
            + f"\n[A WORKED EXAMPLE: A CLASS]\n{example}"
            + f"\n[A WORKED EXAMPLE: ITS SETTINGS AND HAND COMPUTATION]\n{spec}")


def field(text, key):
    m = re.search(rf"^\s*{key}:\s*(.+)$", text, re.M | re.I)
    return m.group(1).strip() if m else ""


def block(text, tag):
    m = re.search(rf"```python {tag}\s*\n(.*?)```", text, re.S)
    return m.group(1) if m else ""


def parse(text, catalogue_text):
    """The answer's fields; refuse only what cannot be used (a missing field, a class the catalogue does not list for
    exists, unreadable settings, a class block that is not one class of the given name)."""
    code = {tag: block(text, tag) for tag in ("class", "hand")}            # the code as written (** is Python's power)
    text = text.replace("**", "")                                         # markdown bold, in the fields only
    kind = field(text, "answer").lower().strip(".")
    if kind not in W.ANSWERS:
        raise ValueError("the answer line must be exists, built or cannot build")
    reason = field(text, "reason")
    if not reason:
        raise ValueError("the reason line is missing")
    out = {"answer": kind, "reason": reason}
    if kind == "cannot build":
        return out
    name = field(text, "class").strip("`")
    try:
        settings = json.loads(field(text, "settings") or "{}")
    except json.JSONDecodeError:
        raise ValueError("the settings line must be a JSON object")
    if not isinstance(settings, dict):
        raise ValueError("the settings line must be a JSON object")
    out.update(name=name, settings=settings)
    known = catalogue_rows(catalogue_text)
    if kind == "exists":
        if name not in known:
            raise ValueError(f"{name} is not a class of the catalogue")
        if set(settings) - known[name]:
            raise ValueError(f"{name} does not take the settings {sorted(set(settings) - known[name])}")
        return out
    if not re.fullmatch(r"[A-Z]\w*Component", name):
        raise ValueError("a new class is named <Measure>Component")
    table = field(text, "table")
    if table not in TABLES:
        raise ValueError(f"the table line must be one of: {', '.join(TABLES)}")
    row = field(text, "row")
    if not row.startswith(f"| `{name}` |") or row.count("|") != 10:
        raise ValueError(f"the row must start with | `{name}` | and have the catalogue's nine columns")
    src, hand = code["class"], code["hand"]
    if classes_in(src) != [name] or f"class {name}(SubStrategyComponent)" not in src:
        raise ValueError(f"the class block must hold exactly one class, {name}(SubStrategyComponent)")
    if "def hand(df, params)" not in hand:
        raise ValueError("the hand block must define hand(df, params)")
    if re.search(r"^\s*(import|from)\s", src, re.M):
        raise ValueError("the class must not import anything")
    out.update(table=table, row=row, source=src, hand=hand)
    return out


# ---- the checks -------------------------------------------------------------------------------------------------

def run(cmd, cwd=None, timeout=1800):
    p = subprocess.run([str(c) for c in cmd], cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout + p.stderr)


def suite(python):
    """The bot's suite, after the standard checks: every existing component's and the engine's tests still pass."""
    code, out = run([python, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider"], cwd=TBOT, timeout=3600)
    if code:
        return False, f"the bot's suite fails:\n{out[-1500:]}"
    return True, f"the bot's suite: {out.strip().splitlines()[-1]}"


def restore(saved):
    """The files as they were: {path: text, or None for a file that did not exist}."""
    for p, text in saved.items():
        if text is None:
            p.unlink(missing_ok=True)
        else:
            write_atomic(p, text)


def undo_cut_build():
    """A build cut short (the process stopped between writing the files and keeping or undoing them) left its note:
    the files are put back from it, one journal line says so, and the note is removed. Returns the journal line."""
    if not PENDING.exists():
        return None
    note = json.loads(PENDING.read_text(encoding="utf-8"))
    restore({REPO / k: v for k, v in note["files"].items()})
    line = {"at": utc_now(), "run": note["run"], "plan": note["plan"], "wish": note["wish"],
            "answer": f"a build cut short: undone ({note['class']}, started {note['started']})", "usd": note["usd"]}
    with open(ROOT / "journal.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(line) + "\n")
    PENDING.unlink()
    return line


# ---- one wish ---------------------------------------------------------------------------------------------------

def answer_wish(wish, python, model):
    """One wish answered: (answer line, USD, attempts, the build folder's texts)."""
    run_name, pid, name, text = wish
    request = f"[WISH]\nrun: {run_name}\nplan: {pid}\n{text}\n\nGive your answer for this wish."
    cost, note, log = 0.0, "", []
    for attempt in range(1, ATTEMPTS + 1):
        catalogue_text = CATALOGUE.read_text(encoding="utf-8")
        reply, c = call(model, system_prompt(), request + note)
        cost += c
        log.append(f"## attempt {attempt}\n\n{reply}\n")
        try:
            a = parse(reply, catalogue_text)
        except ValueError as e:
            note = f"\n\nYour previous answer was refused: {e}. Give your answer again."
            log.append(f"refused: {e}\n")
            continue
        if a["answer"] == "cannot build":
            return f"cannot build: {a['reason']}", cost, attempt, log, None
        settings = json.dumps(a["settings"], sort_keys=True)
        if a["answer"] == "exists":
            return f"exists: {a['name']} {settings}", cost, attempt, log, None
        ok, checks = build(a, python, {"run": run_name, "plan": pid, "wish": name, "usd": round(cost, 4)})
        log.append(f"checks:\n{checks}\n")
        if ok:
            return f"built: {a['name']} {settings}", cost, attempt, log, a["name"]
        note = f"\n\nYour class failed the checks; nothing was kept. Their output:\n{checks[-2000:]}\nGive your answer again."
    return f"cannot build: no answer passed the checks after {ATTEMPTS} attempts", cost, ATTEMPTS, log, None


def build(a, python, wish):
    """Write the class, its row and its spec; run the checks and the bot's suite; undo every file on a failure. While it
    runs, the files as they were are in PENDING, so a build cut short is undone at the next start (undo_cut_build)."""
    name = a["name"]
    saved = {p: (p.read_text(encoding="utf-8") if p.exists() else None) for p in (COMPONENTS_FILE, CATALOGUE, SPECS / f"{name}.py")}
    replaced = class_source(saved[COMPONENTS_FILE], name) is not None
    write_atomic(PENDING, json.dumps({**wish, "class": name, "started": utc_now(),
                                      "files": {p.relative_to(REPO).as_posix(): v for p, v in saved.items()}}))
    try:
        module = with_class(saved[COMPONENTS_FILE], name, a["source"])
        write_atomic(COMPONENTS_FILE, module)
        write_atomic(CATALOGUE, with_count(with_row(saved[CATALOGUE], name, a["table"], a["row"]), len(classes_in(module))))
        SPECS.mkdir(parents=True, exist_ok=True)
        before = spec_settings(saved[SPECS / f"{name}.py"]) if saved[SPECS / f"{name}.py"] else []
        write_atomic(SPECS / f"{name}.py", spec_text(name, a["settings"], a["hand"], before))
        cmd = [python, HARNESS, SPECS / f"{name}.py", "--real-data", "--catalogue", CATALOGUE]
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as old:
            old.write(saved[COMPONENTS_FILE])
        if replaced:
            cmd += ["--old-source", old.name]
        code, out = run(cmd, cwd=TBOT)
        Path(old.name).unlink()
        if code:
            raise RuntimeError(f"the standard checks:\n{out.strip()}")
        ok, text = suite(python)
        if not ok:
            raise RuntimeError(text)
    except Exception as e:                       # undo: the files as they were
        restore(saved)
        PENDING.unlink(missing_ok=True)
        return False, str(e)
    PENDING.unlink(missing_ok=True)              # kept: the files are final (an interruption leaves the note)
    return True, out.strip() + "\n" + text


def record(wish, line, usd, seconds, attempts, log, built):
    run_name, pid, name, _ = wish
    idx = W.index_path(ROOT.parent)
    idx.parent.mkdir(parents=True, exist_ok=True)
    head = "" if idx.exists() else "# Components: one line per wish answered (run | plan id | wish | answer)\n\n"
    with open(idx, "a", encoding="utf-8") as fh:
        fh.write(head + f"{run_name} | {pid} | {name} | {line}\n")
    with open(ROOT / "journal.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"at": utc_now(), "run": run_name, "plan": pid, "wish": name, "answer": line,
                             "usd": round(usd, 4), "seconds": round(seconds, 1), "attempts": attempts}) + "\n")
    if built or any(l.startswith("checks:") for l in log):      # every build tried, kept or undone: its answers and checks
        d = ROOT / "builds" / (built or f"not_built/{run_name}/{pid}/{re.sub(r'[^A-Za-z0-9_-]', '_', name)}")
        d.mkdir(parents=True, exist_ok=True)
        write_atomic(d / "answer.md", f"# {built or 'not built'}: {run_name} | {pid} | {name}\n\n" + "\n".join(log))


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--runs", nargs="+", required=True)
    a.add_argument("--python", help="the interpreter of a venv with trading-bot/requirements.txt (for the checks)")
    a.add_argument("--model", default="claude-opus-5-5")
    a.add_argument("--list", action="store_true", help="print the open wishes and the answered ones; no call")
    args = a.parse_args()
    for r in args.runs:
        if not r.endswith("_run"):
            sys.exit(f"{r}: a run name ends in _run")
    todo = W.open_wishes(args.runs)
    if args.list:
        for run_name, pid, name, _ in todo:
            print(f"open: {run_name} | {pid} | {name}")
        for run_name, pid, name, ans in W.answered(args.runs):
            print(f"answered: {run_name} | {pid} | {name} | {ans}")
        print(f"{len(todo)} open wishes")
        return
    if not args.python:
        sys.exit("--python is needed to answer wishes (the checks run in the venv)")
    cut = undo_cut_build()
    if cut:
        print(f"{cut['run']} | {cut['plan']} | {cut['wish']} | {cut['answer']}")
        todo = W.open_wishes(args.runs)
    total = 0.0
    for wish in todo:
        if wish[:3] not in {w[:3] for w in W.open_wishes([wish[0]])}:
            continue                              # answered meanwhile (the same wish found twice)
        t0 = time.time()
        line, usd, attempts, log, built = answer_wish(wish, args.python, args.model)
        record(wish, line, usd, time.time() - t0, attempts, log, built)
        total += usd
        print(f"{wish[0]} | {wish[1]} | {wish[2]} | {line}")
    print(f"components: {len(todo)} wishes answered; {total:.2f} USD")


if __name__ == "__main__":
    main()
