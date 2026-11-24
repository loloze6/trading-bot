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
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "common"))
from lib import call, write_atomic, header, idea_fields, common_text, catalogue_version, profile_name, PROFILE_TREND, PROFILE_AGITATION  # noqa: E402  (shared helpers, common/lib.py)

import yaml

HERE = Path(__file__).resolve().parent
REF = HERE / "reference"   # the two references: the strategy config guide and the component catalogue
DEFAULT_DATA = {"instruments": "BTC, ETH, LTC, XMR, XRP, ZEC", "bar": "1d", "period": "folds A, B, C, D"}   # the cached coins with data in all four folds
FOLDS = HERE.parents[3] / "trading-bot" / "config" / "folds.yaml"
UNIT_SECONDS = {"m": 60, "h": 3600, "d": 86400, "w": 604800}


def bars_per_day(bar):
    """Bars in a day for a bar size ('1d' 1, '4h' 6, '1h' 24, '15m' 96); None when the bar does not divide a day."""
    if len(bar) < 2 or bar[-1] not in UNIT_SECONDS or not bar[:-1].isdigit() or not int(bar[:-1]):
        return None
    seconds = int(bar[:-1]) * UNIT_SECONDS[bar[-1]]
    return 86400 // seconds if 86400 % seconds == 0 else None
ATTEMPTS, MAX_FIELD_WORDS = 3, 300   # 300 words: a guard against a runaway answer, not a length rule
def windows(period, bar):
    """'N separate windows of about M bars each' for a fold id; no date is returned or printed."""
    m = re.fullmatch(r"folds? ([A-Z](?:, [A-Z])*)", period.strip())   # "fold A", or "folds A, B, C, D"
    if not m or not bars_per_day(bar):
        return f"period {period}"
    folds = yaml.safe_load(FOLDS.read_text())["folds"]
    fold = [w for f in m.group(1).split(", ") for w in folds[f]]
    days = [(datetime.date.fromisoformat(str(w["end"])) - datetime.date.fromisoformat(str(w["start"]))).days + 1 for w in fold]
    return (f"{len(days)} separate windows of about {round(sum(days) / len(days)) * bars_per_day(bar)} bars each, per coin; "
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
# forecast / 10 x target / the coin's realised volatility over the last 60 days (in bars of the bar size, so the
# same in real time on any bar size), capped at 2: a more volatile coin gets a smaller position, each coin aiming
# at a 2 % daily move at a forecast of 10.
DAILY_VOL_TARGET, SIZING_DAYS, MAX_ALLOCATION = 0.02, 60, 2


def add_sizing(config, bar):
    config.setdefault("strategies", {})["sizing"] = {
        "kind": "vol_target", "window": SIZING_DAYS * bars_per_day(bar),
        "target_annual_vol": round(DAILY_VOL_TARGET * 365 ** 0.5, 6),
        "periods_per_year": 365 * bars_per_day(bar), "max_allocation": MAX_ALLOCATION}
    return config


# The holding period (operator, 2026-11-19; common/forecast.md, 7): the book holds what it takes for the idea's horizon.
# Added by code from the plan's horizon line, never by the model, like the sizing.
def add_holding(config, horizon):
    m = re.search(r"\d+", horizon or "")
    if not m or int(m.group()) < 1:
        raise ValueError(f"the horizon line gives no number of bars: {horizon!r}")
    config.setdefault("strategies", {})["min_holding_bars"] = int(m.group())
    return config


# The brief's side (operator, 2026-11-22; topic 45, runs/SHORT_1D_RUN.md): enforced by code, never left to the model. Each
# strategy component's forecast is capped at 0 from below ("long only") or from above ("short only"); the combined forecast
# is a weighted mean of the components (common/forecast.md), so it keeps the side too. Any other side: nothing added.
SIDE_CLIP = {"long only": {"op": "clip", "params": {"min": 0}}, "short only": {"op": "clip", "params": {"max": 0}}}


def add_side(config, side):
    clip = SIDE_CLIP.get((side or "").strip().lower())
    if not clip:
        return config
    for reg in (config.get("strategies", {}).get("regimes") or {}).values():
        if isinstance(reg, dict):
            for c in reg.get("components", []):
                t = c.setdefault("transforms", [])
                if not t or t[-1] != clip:
                    t.append(dict(clip, params=dict(clip["params"])))
    return config


# The idea's market profile (operator, 2026-11-24; topic 49, common/market_profile.md): built by code from the idea's
# `profile:` line, never by the model, like the side. The book holds nothing outside the profile: one veto per condition
# the profile does not meet sends the bar to a flat regime (the guide's vetoes, evaluated before the model's own rules);
# inside the profile the model's regimes and forecast are unchanged. Settings in days, converted to bars.
PROFILE_DAYS = {"trend": 60, "swing": 30, "year": 365}
OPPOSITE = {"gt": "lte", "gte": "lt", "lt": "gte", "lte": "gt"}
PROFILE_CLASS = "strategies.strategy_components."


def add_profile(config, profile, bar):
    name = profile_name(profile)
    if not name:
        return config
    rd = config.setdefault("regime_detector", {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"})
    regimes = config.get("strategies", {}).get("regimes") or {}
    flat = next((r for r in ("chop", "mean_reversion", "trending", "unknown") if regimes.get(r) is None), None)
    if flat is None:
        raise ValueError("the config uses all four regimes: none is left flat for the bars outside the idea's profile")
    n = bars_per_day(bar)
    words = name.split()                                  # its trend, its agitation, or both
    parts = [("profile_trend", PROFILE_TREND[w]) for w in words if w in PROFILE_TREND] \
        + [("profile_swing", PROFILE_AGITATION[w]) for w in words if w in PROFILE_AGITATION]
    built = {"profile_trend": {"id": "profile_trend", "class": PROFILE_CLASS + "PriceEvolutionComponent",
                               "params": {"period": PROFILE_DAYS["trend"] * n, "scaling_factor": 1.0}},
             "profile_swing": {"id": "profile_swing", "class": PROFILE_CLASS + "VolatilityPercentileRegimeComponent",
                               "params": {"vol_period": PROFILE_DAYS["swing"] * n, "lookback_period": PROFILE_DAYS["year"] * n,
                                          "smooth_period": 1}}}
    rd.setdefault("components", []).extend(built[cid] for cid, _ in parts)
    vetoes = [{"id": cid, "transforms": [{"op": "identity"}], "rules": [{"op": OPPOSITE[op], "value": v}], "result": flat}
              for cid, conds in parts for op, v in conds]
    rd["vetoes"] = vetoes + rd.get("vetoes", [])
    return config


def brief_side(brief_text):
    """The brief's `side:` header line, or None."""
    head, _ = header(brief_text)
    return next((l.split(":", 1)[1].strip() for l in head if l.split(":", 1)[0].strip() == "side"), None)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("idea", type=Path)
    a.add_argument("--briefs-dir", type=Path, required=True)
    a.add_argument("--plans-dir", type=Path, default=HERE.parent / "plans")
    a.add_argument("--model", default="claude-opus-5-5")
    a.add_argument("--bar", default=None, help="bar size to test on (e.g. 1h), overriding the header and the default")
    args = a.parse_args()

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
              + f"\n[WHAT A BACKTEST RECORDS]\n{common_text("backtest_record")}"
              + f"\n[HOW A FORECAST IS BUILT]\n{common_text("forecast")}"
              + f"\n[HOW THE WORKFLOW MEASURES]\n{common_text("measures")}"
              + f"\n[MARKET PROFILES]\n{common_text("market_profile")}")
    request = (f"[DATA THE TEST RUNS ON]\ncoins: {data['instruments']}\nbar size: {data['bar']}\n"
               f"windows: {windows(data['period'], data['bar'])}\n\n"
               f"[IDEA]\n{idea_fields(idea_text)}\n[BRIEF]\n{brief_text}\n"
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
            + (f"fit: {fit}\n" if fit else "") + f"catalogue: {catalogue_version(REF / 'component_catalogue.md')}\n" + "---\n")
    fid = result["fidelity"]
    body = ("Fidelity:\n" + "".join(f"- {p.capitalize()}: {fid[p]}\n" for p in PARTS)
            + f"- Verdict transfer: {fid['verdict-transfer']}\n")
    bracket = f"[{data['instruments']}, {data['bar']}, {data['period']}]"
    stale = args.plans_dir / f"{plan_id}_config.json"
    if out == "plan":
        side, profile = brief_side(brief_text), profile_name(fields.get("profile"))
        config = add_profile(add_side(add_holding(add_sizing(result["config"], data["bar"]), result["horizon"]), side), profile, data["bar"])
        write_atomic(stale, json.dumps(config, indent=2) + "\n")
        body += (f"Forecast: {result['forecast']}\nConfig: {plan_id}_config.json\n"
                 + (f"Side: {side} (the brief): each component's forecast capped at 0 by step 3's code\n" if side in SIDE_CLIP else "")
                 + (f"Profile: {profile} (the idea): no position outside it, by step 3's code (common/market_profile.md)\n" if profile else "")
                 + "Criterion:\n"
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
