"""Test plan helper, step 3. One closed-book model call reads one idea, its brief and the two reference
documents (reference/), and writes the idea's test plan: the fidelity of the test to the idea, then
either a plan (forecast, config, criterion) or a refusal (untestable or missing-components) with its reason.
This script saves the plan as <idea id>_<bar>.md (and, for a plan, its config as <idea id>_<bar>_config.json) in the
plans folder, writes its line in the folder's INDEX.md, and, for missing-components, its block in COMPONENT_WISHLIST.md.

  python make_test_plan.py path/to/NNN-KK_idea.md --briefs-dir path/to/briefs
Options: --plans-dir (default: ../plans next to this folder), --model (default: the strongest),
--bar (a bar size, such as 1h, overriding the idea's header and the default).

The data (coins, bar size, period) is taken from the idea's header when it sets them; otherwise the default
below. The model is told the coins and bar size; it does not choose them.

The model sees only the system prompt and the request: no tools, no files, no web, no repository, an empty
working folder. This script reads no market data and runs no backtest.
"""
import argparse, datetime, json, os, re, subprocess, sys, tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REF = HERE / "reference"   # set from --reference-dir in main()
DEFAULT_DATA = {"instruments": "BTC, ETH, LTC, XMR, XRP, ZEC", "bar": "1d", "period": "folds A, B, C, D"}   # the cached coins with data in all four folds
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
    m = re.fullmatch(r"folds? ([A-Z](?:, [A-Z])*)", period.strip())   # "fold A", or "folds A, B, C, D"
    if not m or bar not in BARS_PER_DAY:
        return f"period {period}"
    folds = yaml.safe_load(FOLDS.read_text())["folds"]
    fold = [w for f in m.group(1).split(", ") for w in folds[f]]
    days = [(datetime.date.fromisoformat(str(w["end"])) - datetime.date.fromisoformat(str(w["start"]))).days + 1 for w in fold]
    return (f"{len(days)} separate windows of about {round(sum(days) / len(days)) * BARS_PER_DAY[bar]} bars each, per coin; "
            "the bars a config needs for its warm-up are loaded before each window, so every bar of the window is tested")


def catalogue_params():
    """Class name to its accepted params, read from the catalogue rows."""
    cat = (REF / "component_catalogue.md").read_text()
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


# What step 3 reads of an idea file (operator, 2026-11-14): the same subset whatever step wrote it (step 2 or step 7).
# Anything else (a step 7 idea's "Why", with numbers measured on the data; a source line) never reaches the model,
# so the plan is written closed book.
IDEA_HEADER_FIELDS = ("brief", "instruments", "bar", "period")
IDEA_BODY_FIELDS = ("Idea", "Consequence")


def idea_for_step3(text):
    """The idea file reduced to the fields step 3 reads: its brief and data lines, then Idea and Consequence."""
    head, body = header(text)
    kept = [l for l in head if l.split(":", 1)[0].strip() in IDEA_HEADER_FIELDS]
    lines = []
    for f in IDEA_BODY_FIELDS:
        m = re.search(rf"^{f}:\s*(.+)$", body, re.M)
        if not m:
            sys.exit(f"the idea file has no '{f}:' line")
        lines.append(f"{f}: {m.group(1).strip()}")
    return "---\n" + "".join(l + "\n" for l in kept) + "---\n" + "".join(l + "\n" for l in lines)


PARTS = ("situation", "comparison", "outcome")
OUTCOMES = ("plan", "untestable", "missing-components")
PLAN_FIELDS = ("forecast", "horizon", "main-measure", "supporting-check", "confirm", "reject", "inconclusive")
KEYS = PLAN_FIELDS + ("outcome", "reason", "config", "fidelity", "component")


def fields_of(text):
    """Single-line-or-more fields 'key: value', each running to the next known key."""
    keys = "|".join(re.escape(k) for k in KEYS)
    return dict((k, " ".join(v.split())) for k, v in
                re.findall(rf"^({keys}):[ \t]*(.*?)(?=^(?:{keys}):|\Z)", text, re.M | re.S) if k not in ("config", "fidelity", "component"))


def parse(text):
    """Split the answer into its fidelity, its outcome, and the fields that outcome needs.
    Refuse only a major deviation: a missing or unreadable field the outcome needs, a fidelity that contradicts the
    outcome, an unreadable config, a class or param the catalogue does not list, or a runaway field.
    Markup and code fences are stripped."""
    text = re.sub(r"```(?:json)?", "", text).replace("**", "")
    fid = {}
    for part in PARTS + ("verdict-transfer",):
        m = re.search(rf"^\s*-\s*{part}:\s*(.+)$", text, re.M | re.I)
        if not m:
            raise ValueError(f"the fidelity line '- {part}:' is missing")
        fid[part] = " ".join(m.group(1).split())
    status = {}
    for part in PARTS:
        what, _, how = fid[part].partition("->")
        word = (how.strip().split(":")[0].split() or [""])[0].lower().strip(".,")
        if not how and what.strip().lower().strip('".') == "none":
            word = "kept"
        if word not in ("kept", "adapted", "replaced"):
            raise ValueError(f"the fidelity line for {part} must end with '-> kept', '-> adapted: ...' or '-> replaced: ...'")
        status[part] = word
    transfer = fid["verdict-transfer"].split(":")[0].split()[0].lower().strip(".,")
    if transfer not in ("yes", "no"):
        raise ValueError("the verdict-transfer line must start with yes or no")
    f = fields_of(text)
    outcome = f.get("outcome", "").split()[0].lower().strip(".,") if f.get("outcome") else ""
    if outcome not in OUTCOMES:
        raise ValueError("the outcome line must be plan, untestable or missing-components")
    replaced = "replaced" in status.values()
    if outcome == "plan" and (replaced or transfer == "no"):
        raise ValueError("the fidelity has a replaced part or a 'no' verdict transfer, so the outcome cannot be plan")
    if outcome != "plan" and not replaced and transfer == "yes":
        raise ValueError("the outcome is a refusal, but the fidelity has no replaced part and a 'yes' verdict transfer")
    for k, v in f.items():
        if len(v.split()) > MAX_FIELD_WORDS:
            raise ValueError(f"the {k} field has {len(v.split())} words; write one or two sentences")
    result = {"fidelity": fid, "status": status, "transfer": transfer, "outcome": outcome}
    if outcome != "plan":
        if not f.get("reason"):
            raise ValueError("the reason line is missing")
        result["reason"] = f["reason"]
        if outcome == "missing-components":
            comps = [" ".join(c.split()) for c in re.findall(r"^component:\s*(.+)$", text, re.M)]
            if not comps:
                raise ValueError("missing-components needs at least one 'component:' line")
            result["components"] = comps
        return result
    m = re.search(r"^config:\s*(\{.*\})\s*^horizon:", text, re.M | re.S)
    if not m:
        raise ValueError("no config: line followed by one JSON object and a horizon: line")
    try:
        config = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        raise ValueError(f"the config is not valid JSON: {e}")
    for key in ("regime_detector", "strategies"):
        if key not in config:
            raise ValueError(f"the config has no {key} key")
    check_names(config)
    for k in ("forecast", "horizon", "main-measure", "confirm", "reject"):
        if not f.get(k):
            raise ValueError(f"the {k}: line is missing")
    result["config"] = config
    result.update({k: f.get(k, "not given") for k in PLAN_FIELDS})
    return result


# Sizing (operator, 2026-11-13; the engine's strategies.sizing block, as in v1's D-176/D-181): the same for every plan,
# added by code, never by the model. The forecast stays the signal (-20 to +20); the allocation is
# forecast / 10 x target / the coin's realised volatility, capped at 2: a more volatile coin gets a smaller position,
# each coin aiming at a 2 % daily move at a forecast of 10.
DAILY_VOL_TARGET, SIZING_WINDOW, MAX_ALLOCATION = 0.02, 60, 2
PERIODS_PER_YEAR = {"1d": 365, "4h": 2190, "1h": 8760}


def add_sizing(config, bar):
    config.setdefault("strategies", {})["sizing"] = {
        "kind": "vol_target", "window": SIZING_WINDOW,
        "target_annual_vol": round(DAILY_VOL_TARGET * 365 ** 0.5, 6),
        "periods_per_year": PERIODS_PER_YEAR[bar], "max_allocation": MAX_ALLOCATION}
    return config


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
    a.add_argument("--bar", default=None, help="bar size to test on (e.g. 1h), overriding the header and the default")
    a.add_argument("--reference-dir", type=Path, default=HERE / "reference",
                   help="the folder of the two references (overnight test: reference_overnight, with two more components)")
    args = a.parse_args()
    global REF
    REF = args.reference_dir.resolve()

    idea_text, idea_id = args.idea.read_text(), args.idea.stem
    idea_header, _ = header(idea_text)
    fields = dict(l.split(":", 1) for l in idea_header)
    fields = {k.strip(): v.strip() for k, v in fields.items()}
    brief_path = args.briefs_dir / f"{fields['brief']}.md"
    brief_text = brief_path.read_text()
    data = {k: fields.get(k, DEFAULT_DATA[k]) for k in DEFAULT_DATA}
    if args.bar:
        data["bar"] = args.bar
    plan_id = f"{idea_id}_{data['bar']}"   # the plan's id: one plan per idea and bar size

    ref = REF
    # The two references go in the system prompt: they are the same in every call, so from the second idea on
    # they come from the model's cache (exercise 8 probe: 0.26 USD for the first idea, about 0.07 after).
    system = ((HERE / "system_prompt.md").read_text()
              + f"\n\n[STRATEGY CONFIG GUIDE]\n{(ref / 'strategy_config_guide.md').read_text()}"
              + f"\n[COMPONENT CATALOGUE]\n{(ref / 'component_catalogue.md').read_text()}"
              + f"\n[HOW THE WORKFLOW MEASURES]\n{(HERE.parents[1] / 'common' / 'measures.md').read_text()}")
    request = (f"[DATA THE TEST RUNS ON]\ncoins: {data['instruments']}\nbar size: {data['bar']}\n"
               f"windows: {windows(data['period'], data['bar'])}\n\n"
               f"[IDEA]\n{idea_for_step3(idea_text)}\n[BRIEF]\n{brief_text}\n"
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
    out = result["outcome"]
    fit = ("exact" if all(v == "kept" for v in result["status"].values()) else "adapted") if out == "plan" else None
    head = ("---\n" + f"idea: {idea_id}\n" + f"brief: {fields['brief']}\n"
            + "".join(f"data-{k}: {v}\n" for k, v in data.items()) + f"outcome: {out}\n"
            + (f"fit: {fit}\n" if fit else "") + "---\n")
    fid = result["fidelity"]
    body = ("Fidelity:\n" + "".join(f"- {p.capitalize()}: {fid[p]}\n" for p in PARTS)
            + f"- Verdict transfer: {fid['verdict-transfer']}\n")
    bracket = f"[{data['instruments']}, {data['bar']}, {data['period']}]"
    stale = args.plans_dir / f"{plan_id}_config.json"
    if out == "plan":
        write_atomic(stale, json.dumps(add_sizing(result["config"], data["bar"]), indent=2) + "\n")
        body += (f"Forecast: {result['forecast']}\nConfig: {plan_id}_config.json\nCriterion:\n"
                 + "".join(f"- {k.replace('-', ' ').capitalize()}: {result[k]}\n" for k in PLAN_FIELDS[1:]))
        line = f"{plan_id}: plan (fit: {fit}) {bracket}"
        print(f"plan ({fit}): {args.plans_dir / (plan_id + '.md')}")
    else:
        if stale.exists():
            stale.unlink()   # a rerun that refuses leaves no config behind
        body += f"Reason: {result['reason']}\n"
        line = f"{plan_id}: {out}: {' '.join(result['reason'].split()[:20])} {bracket}"
        print(f"{out}: {result['reason']}")
    write_atomic(args.plans_dir / f"{plan_id}.md", head + body)
    # The component wish list: one block per plan id; a rerun replaces it, a rerun with another outcome removes it.
    wish_path = args.plans_dir / "COMPONENT_WISHLIST.md"
    wish = wish_path.read_text() if wish_path.exists() else "# Component wish list\n\nOne block per idea that needs components the catalogue does not have.\n"
    wish = re.sub(rf"\n## {re.escape(plan_id)}\n.*?(?=\n## |\Z)", "", wish, flags=re.S).rstrip("\n") + "\n"
    if out == "missing-components":
        wish += f"\n## {plan_id}\n" + "".join(f"- Component: {c}\n" for c in result["components"])
    write_atomic(wish_path, wish)
    # One line per plan; a rerun of the same idea and bar replaces its line.
    index_path = args.plans_dir / "INDEX.md"
    lines = [l for l in (index_path.read_text().splitlines() if index_path.exists() else []) if not l.startswith(plan_id + ":")]
    write_atomic(index_path, "".join(l + "\n" for l in sorted(lines + [line])))
    print(f"cost: {cost:.4f} USD, attempts: {attempt}")


if __name__ == "__main__":
    main()
