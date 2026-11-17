"""The standard checks of a strategy component (strategy_designer_v2 components step, 2026-11-17).

The same checks for every component, written once; the model that writes a component never writes the test that
judges it. Each check returns a list of failures (empty when it passes).

  check_warmup     not ready before get_required_periods() rows, ready at it
  check_hand       the class matches an independent hand computation that uses only the rows up to bar t
  check_engine     the engine runs it as a forecast source; the config validator accepts it in a strategy and in a
                   regime rule
  check_real_data  on every cached coin's daily bars, a finite value on every bar once warm
  check_defaults   (a class given a new setting) its output at the old defaults is unchanged on real data
  check_catalogue  every class in strategy_components.py has one row in step 3's component catalogue

No lookahead by construction: the engine hands a component the rows up to bar t only, so a component cannot read a
later bar; check_hand checks it reads the right ones.

CLI (the components step calls it with the venv's python):
  python component_harness.py SPEC.py [--real-data] [--old-source FILE] [--catalogue FILE]
SPEC.py holds CLASS (the class name), SETTINGS (a list of params dicts, the first being the defaults) and
hand(df, params) -> float. Exit 0 when every check passes; one line per failure otherwise.
"""
import argparse, importlib.util, math, re, sys
from pathlib import Path

import numpy as np
import pandas as pd

TBOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TBOT))

from strategies.strategy_base import MarketRegime  # noqa: E402
from strategies.strategy_engine import ConfigDrivenStrategyEngine  # noqa: E402
from tools.validate_config import validate  # noqa: E402
import strategies.strategy_components as SC  # noqa: E402

PREFIX = "strategies.strategy_components."
DATA = TBOT / "local_data"
COMPONENTS_FILE = TBOT / "strategies" / "strategy_components.py"


def synthetic_bars(n=400, seed=7):
    """Daily OHLCV bars, a random walk with positive volume and a consistent high-low range."""
    rng = np.random.default_rng(seed)
    close = 100.0 * np.exp(np.cumsum(rng.normal(0.0, 0.02, n)))
    open_ = np.r_[close[0], close[:-1]] * np.exp(rng.normal(0.0, 0.005, n))
    high = np.maximum(open_, close) * np.exp(np.abs(rng.normal(0.0, 0.01, n)))
    low = np.minimum(open_, close) * np.exp(-np.abs(rng.normal(0.0, 0.01, n)))
    return pd.DataFrame({"timestamp": pd.date_range("2021-03-01", periods=n, freq="D"), "open": open_, "high": high,
                         "low": low, "close": close, "volume": rng.lognormal(10.0, 0.5, n)})


def value(cls, params, df):
    c = cls(parameters=dict(params))
    c.update(df)
    return float(c.raw_value()), c


def same(a, b):
    if math.isnan(a) or math.isnan(b):
        return math.isnan(a) and math.isnan(b)
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)


def check_warmup(cls, params, df=None):
    df = synthetic_bars() if df is None else df
    req = cls(parameters=dict(params)).get_required_periods()
    out = []
    if req > 1 and value(cls, params, df.iloc[:req - 1])[1].is_ready():
        out.append(f"warm-up {params}: ready with {req - 1} rows, before get_required_periods() = {req}")
    if not value(cls, params, df.iloc[:req])[1].is_ready():
        out.append(f"warm-up {params}: not ready with {req} rows = get_required_periods()")
    return out


def check_hand(cls, settings, hand, df=None):
    df = synthetic_bars() if df is None else df
    out = []
    for params in settings:
        req = cls(parameters=dict(params)).get_required_periods()
        for t in sorted({req - 1, req + 36, len(df) - 1}):
            if t < 0 or t >= len(df):
                continue
            rows = df.iloc[: t + 1]
            got, _ = value(cls, params, rows)
            want = float(hand(rows.copy(), dict(params)))
            if not same(got, want):
                out.append(f"hand computation {params} at bar {t}: class {got!r}, hand {want!r}")
    return out


def _strategy(cls_name, params):
    return {"warmup": 5, "regimes": {
        "unknown": {"components": [{"id": "c", "class": PREFIX + cls_name, "params": params, "weight": 1.0,
                                    "transforms": [{"op": "identity"}, {"op": "clip", "params": {"min": -20, "max": 20}}]}]},
        "trending": None, "mean_reversion": None, "chop": None}}


def check_engine(cls, params, df=None):
    df = synthetic_bars() if df is None else df
    name, out = cls.__name__, []
    req = cls(parameters=dict(params)).get_required_periods()
    eng = ConfigDrivenStrategyEngine(_strategy(name, params))
    start = max(2 * req, req + 20)
    for i in range(2, len(df) + 1):
        eng.update(df.iloc[:i])
        if i >= start:
            fc, dbg = eng.forecast(MarketRegime.UNKNOWN)
            if "not_ready_component" in dbg or not np.isfinite(fc):
                out.append(f"engine {params}: no finite forecast at row {i} ({dbg})")
                break
    flat = {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"}
    errs = validate({"regime_detector": flat, "strategies": {**_strategy(name, params), "warmup": 2 * req + 5}})
    if errs:
        out.append(f"validator, as a forecast source: {errs}")
    detector = {"mode": "threshold_rules", "components": [{"id": "x", "class": PREFIX + name, "params": params}],
                "rules": [{"regime": "trending", "any_of": [[{"id": "x", "op": "gt", "value": 0.0}]]}],
                "default_regime": "unknown"}
    errs = validate({"regime_detector": detector, "strategies": {**_strategy("PriceEvolutionComponent", {"period": 5}),
                                                                 "warmup": 2 * req + 5}})
    if errs:
        out.append(f"validator, in a regime rule: {errs}")
    return out


def real_data(bar="1d"):
    """Every cached Kraken coin's bars, by coin."""
    out = {}
    for f in sorted(DATA.glob(f"kraken_*_{bar}.csv")):
        d = pd.read_csv(f)
        d["timestamp"] = pd.to_datetime(d["timestamp"])
        out[f.stem.split("_")[1]] = d.reset_index(drop=True)
    return out


def values_on(cls, params, d):
    """The component's value on every bar of d once warm (each computed from the rows up to that bar)."""
    c = cls(parameters=dict(params))
    req = c.get_required_periods()
    vals = []
    for t in range(max(req, 1) - 1, len(d)):
        c.update(d.iloc[: t + 1])
        vals.append(float(c.raw_value()) if c.is_ready() else float("nan"))
    return np.array(vals)


def check_real_data(cls, params, data=None):
    data = real_data() if data is None else data
    out = []
    for coin, d in data.items():
        v = values_on(cls, params, d)
        bad = int((~np.isfinite(v)).sum())
        if bad:
            out.append(f"real data {params}: {coin}: {bad} of {len(v)} bars without a finite value once warm")
    return out


def check_defaults(old_cls, new_cls, params, data=None):
    data = real_data() if data is None else data
    out = []
    for coin, d in list(data.items())[:3]:
        a, b = values_on(old_cls, params, d), values_on(new_cls, params, d)
        if len(a) != len(b) or not all(same(x, y) for x, y in zip(a, b)):
            out.append(f"defaults {params}: {coin}: output changed")
    return out


def check_catalogue(catalogue, components_file=COMPONENTS_FILE):
    classes = re.findall(r"^class (\w+)\(", Path(components_file).read_text(), re.M)
    cat = Path(catalogue).read_text()
    rows = cat[cat.index("## Component rows"):cat.index("## Variant patterns")]
    listed = re.findall(r"^\| `(\w+)` \|", rows, re.M)
    out = [f"catalogue: no row for {c}" for c in classes if c not in listed]
    out += [f"catalogue: {c} has {listed.count(c)} rows" for c in set(listed) if listed.count(c) > 1]
    out += [f"catalogue: a row for {c}, which is not a class" for c in set(listed) if c not in classes]
    m = re.search(r"There are (\d+) classes", cat)
    if not m or int(m.group(1)) != len(classes):
        out.append(f"catalogue: its class count says {m.group(1) if m else 'nothing'}, the file has {len(classes)}")
    return out


def load_spec(path):
    spec = importlib.util.spec_from_file_location(Path(path).stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_class_from_source(source, name):
    """A class from another version of strategy_components.py (the old defaults' check)."""
    ns = {"__name__": "old_strategy_components"}
    exec(compile(source, "old_strategy_components.py", "exec"), ns)
    return ns[name]


def main():
    a = argparse.ArgumentParser()
    a.add_argument("spec", type=Path)
    a.add_argument("--real-data", action="store_true")
    a.add_argument("--old-source", type=Path, help="strategy_components.py before the change, for a replaced class")
    a.add_argument("--catalogue", type=Path)
    args = a.parse_args()
    spec = load_spec(args.spec)
    cls = getattr(SC, spec.CLASS)
    fails = []
    for p in spec.SETTINGS:
        fails += check_warmup(cls, p) + check_engine(cls, p)
    fails += check_hand(cls, spec.SETTINGS, spec.hand)
    if args.real_data:
        for p in spec.SETTINGS:
            fails += check_real_data(cls, p)
    if args.old_source:
        old = load_class_from_source(args.old_source.read_text(), spec.CLASS)
        fails += check_defaults(old, cls, spec.SETTINGS[0])
    if args.catalogue:
        fails += check_catalogue(args.catalogue)
    for f in fails:
        print("FAIL " + f)
    print(f"{spec.CLASS}: {'every check passed' if not fails else f'{len(fails)} failure(s)'}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
