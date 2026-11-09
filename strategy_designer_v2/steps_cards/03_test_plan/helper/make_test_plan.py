"""Test plan helper, step 3. One closed-book model call reads one idea, its brief and the two reference
documents (reference/), and writes the idea's test plan: a strategy config, the result that would confirm
the idea, the result that would reject it, and the deviation; or "untestable", with the reason.
This script saves the plan as <idea id>.md and the config as <idea id>_config.json in the plans folder.

  python make_test_plan.py path/to/NNN-KK_idea.md --briefs-dir path/to/briefs
Options: --plans-dir (default: ../plans next to this folder), --model (default: the strongest).

The data (coins, bar size, period) is taken from the idea's header when it sets them; otherwise the default
below. The model is told the coins and bar size; it does not choose them.

The model sees only the system prompt and the request: no tools, no files, no web, no repository, an empty
working folder. This script reads no market data and runs no backtest.
"""
import argparse, datetime, json, os, re, subprocess, sys, tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
DEFAULT_DATA = {"instruments": "BTC/USDT", "bar": "1d", "period": "fold A"}
FOLDS = HERE.parents[3] / "strategy-research" / "config" / "folds.yaml"
BARS_PER_DAY = {"1d": 1, "4h": 6, "1h": 24}
ATTEMPTS, MAX_FIELD_WORDS = 3, 300   # 300 words: a guard against a runaway answer, not a length rule
DROP_ENV = {"CLAUDE_ADDITIONAL_DIRECTORIES", "CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD", "CLAUDE_EFFORT",
            "CLAUDE_CODE_USER_EMAIL", "CLAUDE_CODE_REMOTE_SESSION_ID", "CLAUDE_CODE_SESSION_ID"}


def call(model, system, request):
    """One model call, closed book. Returns (text, cost in USD)."""
    cmd = ["claude", "-p", "--model", model, "--system-prompt", system, "--tools", "",
           "--strict-mcp-config", "--disable-slash-commands", "--no-session-persistence", "--setting-sources", "",
           "--settings", '{"attribution":{"commit":"","pr":""},"includeCoAuthoredBy":false}', "--output-format", "json"]
    env = {k: v for k, v in os.environ.items() if k not in DROP_ENV}
    with tempfile.TemporaryDirectory() as empty:
        p = subprocess.run(cmd, input=request, cwd=empty, env=env, capture_output=True, text=True, timeout=900)
    d = json.loads(p.stdout)
    if d.get("is_error"):
        sys.exit(f"model call failed: {d.get('result')}")
    return d["result"], d["total_cost_usd"]


def windows(period, bar):
    """'N separate windows of about M bars each' for a fold id; no date is returned or printed."""
    m = re.fullmatch(r"fold ([A-Z])", period.strip())
    if not m or bar not in BARS_PER_DAY:
        return f"period {period}"
    fold = yaml.safe_load(FOLDS.read_text())["folds"][m.group(1)]
    days = [(datetime.date.fromisoformat(str(w["end"])) - datetime.date.fromisoformat(str(w["start"]))).days + 1 for w in fold]
    return (f"{len(days)} separate windows of about {round(sum(days) / len(days)) * BARS_PER_DAY[bar]} bars each, per coin; "
            "the bars a config needs for its warm-up are loaded before each window, so every bar of the window is tested")


def catalogue_params():
    """Class name to its accepted params, read from the catalogue rows."""
    cat = (HERE / "reference" / "component_catalogue.md").read_text()
    rows = cat[cat.index("### Regime measures"):]
    return {n: set(re.findall(r"`(\w+)` \(", p)) for n, p in re.findall(r"^\| `(\w+)` \| ([^|]*) \|", rows, re.M)}


def check_names(config):
    """Refuse a class or a param the catalogue does not list: the engine would ignore it silently."""
    known = catalogue_params()
    comps = config["regime_detector"].get("components", []) + [
        c for v in config["strategies"].get("regimes", {}).values() if v for c in v.get("components", [])]
    for c in comps:
        cls = str(c.get("class", "")).split(".")[-1]
        if cls not in known:
            raise ValueError(f"class {cls} is not in the catalogue")
        bad = set(c.get("params", {})) - known[cls]
        if bad:
            raise ValueError(f"{cls} has params the catalogue does not list (the engine would ignore them): {sorted(bad)}")


def header(text):
    """The --- header lines of a Markdown file, word for word, and the body."""
    m = re.match(r"\s*---\n(.*?)---\n(.*)", text, re.S)
    if not m:
        sys.exit("the file does not start with a --- header")
    return [l.strip() for l in m.group(1).splitlines() if l.strip()], m.group(2)


def parse(text):
    """Return ("untestable", reason) or ("plan", config, confirm, reject, inconclusive, deviation).
    Refuse only a major deviation: no untestable line and no readable config, a config without its two
    top-level keys, a missing confirm or reject, or a runaway field. Markup and code fences are stripped."""
    text = re.sub(r"```(?:json)?", "", text).replace("**", "")
    u = re.search(r"^untestable:\s*(.+)", text, re.M | re.S)
    if u and "config:" not in text:
        return ("untestable", " ".join(u.group(1).split()))
    m = re.search(r"^config:\s*(\{.*\})\s*^confirm:", text, re.M | re.S)
    if not m:
        raise ValueError("no config: line followed by one JSON object and a confirm: line")
    try:
        config = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        raise ValueError(f"the config is not valid JSON: {e}")
    for key in ("regime_detector", "strategies"):
        if key not in config:
            raise ValueError(f"the config has no {key} key")
    check_names(config)
    fields = dict((k, " ".join(v.split())) for k, v in
                  re.findall(r"^(forecast|confirm|reject|inconclusive|deviation):\s*(.*?)(?=^(?:forecast|config|confirm|reject|inconclusive|deviation):|\Z)", text, re.M | re.S))
    for k in ("confirm", "reject"):
        if not fields.get(k):
            raise ValueError(f"the {k}: line is missing")
    for k, v in fields.items():
        if len(v.split()) > MAX_FIELD_WORDS:
            raise ValueError(f"the {k} field has {len(v.split())} words; write one or two sentences")
    return ("plan", config, fields["confirm"], fields["reject"], fields.get("inconclusive", "not given"),
            fields.get("deviation", "not given"), fields.get("forecast", "not given"))


def write_atomic(path, text):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("idea", type=Path)
    a.add_argument("--briefs-dir", type=Path, required=True)
    a.add_argument("--plans-dir", type=Path, default=HERE.parent / "plans")
    a.add_argument("--model", default="claude-opus-5-5")
    args = a.parse_args()

    idea_text, idea_id = args.idea.read_text(), args.idea.stem
    idea_header, _ = header(idea_text)
    fields = dict(l.split(":", 1) for l in idea_header)
    fields = {k.strip(): v.strip() for k, v in fields.items()}
    brief_path = args.briefs_dir / f"{fields['brief']}.md"
    brief_text = brief_path.read_text()
    data = {k: fields.get(k, DEFAULT_DATA[k]) for k in DEFAULT_DATA}

    ref = HERE / "reference"
    system = (HERE / "system_prompt.md").read_text()
    request = (f"[DATA THE TEST RUNS ON]\ncoins: {data['instruments']}\nbar size: {data['bar']}\n"
               f"windows: {windows(data['period'], data['bar'])}\n\n"
               f"[IDEA]\n{idea_text}\n[BRIEF]\n{brief_text}\n"
               f"[STRATEGY CONFIG GUIDE]\n{(ref / 'strategy_config_guide.md').read_text()}\n"
               f"[COMPONENT CATALOGUE]\n{(ref / 'component_catalogue.md').read_text()}\n"
               f"Write the test plan for this idea.")

    cost, refusal = 0.0, ""
    for attempt in range(1, ATTEMPTS + 1):
        text, c = call(args.model, system, request + refusal)
        cost += c
        try:
            result = parse(text)
            break
        except ValueError as e:
            print(f"attempt {attempt} refused: {e}")
            refusal = f"\n\nYour previous answer was refused: {e}. Write the test plan again."
    else:
        sys.exit(f"no valid answer after {ATTEMPTS} attempts; cost {cost:.4f} USD")

    args.plans_dir.mkdir(parents=True, exist_ok=True)
    head = ("---\n" + f"idea: {idea_id}\n" + f"brief: {fields['brief']}\n"
            + "".join(f"data-{k}: {v}\n" for k, v in data.items()) + "---\n")
    if result[0] == "untestable":
        write_atomic(args.plans_dir / f"{idea_id}.md", head + f"Untestable: {result[1]}\n")
        print(f"untestable: {result[1]}")
    else:
        _, config, confirm, reject, inconclusive, deviation, forecast = result
        write_atomic(args.plans_dir / f"{idea_id}_config.json", json.dumps(config, indent=2) + "\n")
        write_atomic(args.plans_dir / f"{idea_id}.md", head + f"Forecast: {forecast}\nConfig: {idea_id}_config.json\n"
                     f"Confirm: {confirm}\nReject: {reject}\nInconclusive: {inconclusive}\nDeviation: {deviation}\n")
        print(f"plan: {args.plans_dir / (idea_id + '.md')}")
    print(f"cost: {cost:.4f} USD, attempts: {attempt}")


if __name__ == "__main__":
    main()
