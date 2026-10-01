"""
forecast_size_probe -- can this config's forecast ever move the position? (O-10, D-056)

C4 run_061 (2026-10-01): step 1b followed a MovingAverageDistanceComponent
(percent output) with the `vol_adjusted` transform, which divides by
stddev_24 x close (~1e6 for BTC). Every forecast stayed ~1e-5, every
allocation change failed min_allocation_change, and the variant made 0 trades
in 95 windows. The validator, step 5a, the data gate and the engine all
accepted it; the result looked like an ordinary "0 trades".

This tool runs the REAL engine (trading-bot run_backtest -- the same data
merge, aux feeds, gap rule and warmup prefetch run_protocol.py uses) on a few
training-era windows of the run's own protocol and reads ONLY the `forecast`
column of bars.csv. It refuses a config when fewer than MIN_TRADABLE_SHARE of
the bars have |forecast| >= 10 x min_allocation_change (the size a forecast
needs, from flat, to pass the risk layer's rebalance floor; forecast / 10 is
the allocation), or when every forecast is NaN.

Not a trial (D-056): no PnL, trade, return or metric is read or recorded --
only the forecast's size. Why it cannot leak: the sample is limited to windows
that END before PROBE_CUTOFF (2024-01-01, the start of the validation era), so
no validation or holdout bar is ever loaded, and the holdout guard is
run_protocol.py's own (_training_holdout_start + _preflight_training_windows).
The check is about scale, never about direction or performance.

Used by run_phase1_research under orchestrator.forecast_size_probe.enabled
(off by default): after 1b on the base config and in step 5a on every
variant. Run as a subprocess (like run_protocol.py), so engine state never
leaks into the orchestrator.

CLI:  python forecast_size_probe.py --config <cfg.json> --protocol <protocol.json>
                                    --json-out <result.json>
Exit 0 with the assessment written (status "ok", "refuse" or "skipped");
non-zero only on an engineering failure.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent.parent
CONFIG_JSON = _REPO / "trading-bot" / "config.json"

# Training eras (CLAUDE.fork.md era-stability bar). One sample window per era.
ERAS = (("2018-01-01", "2021-01-01"), ("2021-01-01", "2023-01-01"),
        ("2023-01-01", "2024-01-01"))
PROBE_CUTOFF = "2024-01-01"   # a sample window must END strictly before this
MIN_TRADABLE_SHARE = 0.01     # pre-registered (operator, 2026-10-01)


def forecast_threshold(config_json: Path = CONFIG_JSON) -> float:
    """10 x risk_management.controls.min_allocation_change.threshold. Fail
    loud when the key is missing: the probe must not guess the floor."""
    cfg = json.loads(Path(config_json).read_text(encoding="utf-8"))
    try:
        floor = cfg["risk_management"]["controls"]["min_allocation_change"]["threshold"]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"{config_json}: risk_management.controls.min_allocation_change."
                         f"threshold is missing -- cannot size the probe") from exc
    if isinstance(floor, bool) or not isinstance(floor, (int, float)) or floor <= 0:
        raise ValueError(f"{config_json}: min_allocation_change.threshold={floor!r} is not a "
                         f"positive number")
    return 10.0 * float(floor)


def sample_windows(protocol: dict) -> list:
    """The first protocol window of each training era that ends strictly
    before PROBE_CUTOFF. Window dates are ISO strings (lexical = chronological)."""
    picked = []
    for era_start, era_end in ERAS:
        limit = min(era_end, PROBE_CUTOFF)
        for w in protocol.get("windows") or []:
            test = w.get("test") or {}
            start, end = str(test.get("start", "")), str(test.get("end", ""))
            if start >= era_start and end < limit and start < end:
                picked.append(w)
                break
    return picked


def assess(forecasts: list, threshold: float) -> dict:
    """Pure: the size verdict for one config. `forecasts` = every bar's
    forecast across the sample windows (NaN allowed)."""
    finite = [abs(float(f)) for f in forecasts
              if f is not None and isinstance(f, (int, float)) and math.isfinite(f)]
    n, n_nan = len(finite), len(forecasts) - len(finite)
    if n == 0:
        return {"status": "refuse", "n_bars": 0, "n_nan": n_nan, "threshold": threshold,
                "message": (f"every forecast is NaN or missing ({n_nan} bars): the config "
                            f"never produces a usable forecast")}
    s = sorted(finite)
    pct = lambda q: s[min(n - 1, int(q * (n - 1) + 0.5))]  # noqa: E731
    share = sum(1 for v in finite if v >= threshold) / n
    out = {"status": "ok" if share >= MIN_TRADABLE_SHARE else "refuse",
           "n_bars": n, "n_nan": n_nan, "threshold": threshold,
           "max_abs": s[-1], "p50_abs": pct(0.5), "p95_abs": pct(0.95),
           "share_tradable": share}
    if out["status"] == "refuse":
        out["message"] = (
            f"forecast too small to ever trade: only {share:.2%} of {n} sample bars reach "
            f"|forecast| >= {threshold:g} (10 x min_allocation_change; needed: "
            f">= {MIN_TRADABLE_SHARE:.0%}); max |forecast| {s[-1]:.3g}, median {pct(0.5):.3g}. "
            f"Likely a units/scale mistake -- e.g. vol_adjusted or vol_normalize used in "
            f"`transforms` without a ratio_to_mean rescale (they divide by stddev_24 x close, "
            f"~price^2), or price_normalized on a percent output. Rescale so a typical "
            f"signal is a few forecast units (forecast / 10 is the allocation)")
    return out


def _run_sample(config_path: Path, protocol: dict, windows: list, out_root: Path) -> list:
    """Real engine on the sample windows; returns the forecast column only."""
    import pandas as pd
    sys.path.insert(0, str(_HERE))
    import run_protocol as rp  # noqa: E402 -- also puts trading-bot on sys.path
    from core.launcher import run_backtest, parse_interval_seconds  # noqa: E402

    policy = rp._load_policy_or_refuse()
    holdout_start = rp._training_holdout_start(protocol, policy)
    rp._preflight_training_windows({**protocol, "windows": windows}, holdout_start)
    exchange = protocol.get("exchange")
    if exchange is None:
        exchange = "binance"
    timeframe = protocol.get("timeframe", "1h")
    interval_seconds = parse_interval_seconds(timeframe) if timeframe != "1h" else None
    symbol = protocol["symbols"][0]
    forecasts = []
    for w in windows:
        rd = run_backtest(str(config_path), symbol, w["test"]["start"], w["test"]["end"],
                          str(out_root), runs_root=str(out_root),
                          interval_seconds=interval_seconds, warmup_prefetch=True,
                          holdout_start=holdout_start, exchange=exchange,
                          drop_feeds=protocol.get("drop_feeds"))
        bars = pd.read_csv(Path(rd) / "bars.csv", usecols=["forecast"])
        forecasts.extend(bars["forecast"].tolist())
    return forecasts


def probe(config_path: Path, protocol: dict) -> dict:
    windows = sample_windows(protocol)
    if not windows:
        return {"status": "skipped", "message": (
            f"no protocol window ends before {PROBE_CUTOFF} in a training era -- nothing "
            f"safe to probe; the size check is skipped")}
    threshold = forecast_threshold()
    with tempfile.TemporaryDirectory(prefix="forecast_probe_") as tmp:
        forecasts = _run_sample(Path(config_path), protocol, windows, Path(tmp))
    result = assess(forecasts, threshold)
    result["symbol"] = protocol["symbols"][0]
    result["windows"] = [w.get("label") for w in windows]
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--config", required=True)
    ap.add_argument("--protocol", required=True)
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args()
    protocol = json.loads(Path(args.protocol).read_text(encoding="utf-8"))
    result = probe(Path(args.config), protocol)
    Path(args.json_out).write_text(json.dumps(result, indent=2, default=float), encoding="utf-8")
    print(f"forecast_size_probe: {result['status']}"
          + (f" -- {result['message']}" if result.get("message") else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
