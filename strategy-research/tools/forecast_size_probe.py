"""
forecast_size_probe -- is this config's forecast broken in size? (O-10, D-056)

C4 run_061 (2026-10-01): step 1b followed a MovingAverageDistanceComponent
(percent output) with the `vol_adjusted` transform, which divides by
stddev_24 x close (~1e6 for BTC). Every forecast stayed ~1e-5, every
allocation change failed min_allocation_change, and the variant made 0 trades
in 95 windows. The validator, step 5a, the data gate and the engine all
accepted it; the result looked like an ordinary "0 trades".

BUG DETECTION ONLY (operator, 2026-10-02). How often a strategy trades is the
backtest's question, never this tool's: a deliberately quiet strategy (rare
events, small forecasts most of the time) must pass. The tool refuses only a
forecast that is broken in SIZE:
  * every forecast is NaN, or
  * the forecast is nonzero somewhere but its LARGEST magnitude stays below
    BUG_FACTOR x the size a forecast needs to move the position from flat
    (10 x min_allocation_change; forecast / 10 is the allocation) -- a
    units/scale mistake, orders of magnitude off (run_061: 7e-6 vs 2.0).
A forecast that is exactly 0 on every bar passes: a rare-event strategy can
be silent on any sample.

INVENTED DATA ONLY (operator, 2026-10-02): no real market bar is ever read.
The strategy (the real AdvancedStrategy, fed bar by bar as the engine feeds
it) runs on a synthetic series with a fixed seed: a geometric random walk at
a crypto-like price level and volatility (constants below, not fitted to any
real period), plus synthetic values for every live aux feed (funding_rate,
fear_greed). Timestamps are an invented calendar (year 2000). A scale bug
depends on the price level and the units, not on what the market did, so it
shows on invented data; nothing about real market behaviour is measured.
Not a trial: no data, PnL, trade or metric of any real market is touched.

Used by run_phase1_research under orchestrator.forecast_size_probe.enabled
(off by default): after 1b on the base config and in step 5a on every
variant. Run as a subprocess, so strategy state never leaks into the
orchestrator.

CLI:  python forecast_size_probe.py --config <cfg.json> --protocol <protocol.json>
                                    --json-out <result.json>
The protocol is read only for its timeframe. Exit 0 with the assessment
written (status "ok" or "refuse"); non-zero only on an engineering failure.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent.parent
_TBOT = _REPO / "trading-bot"
CONFIG_JSON = _TBOT / "config.json"

# Pre-registered (operator, 2026-10-02): refuse only when the largest
# |forecast| is below 1/100 of the size needed to trade -- a bug, not a style.
BUG_FACTOR = 0.01

# Invented series (fixed; never fitted to a real period).
SYNTH_SEED = 20261002
SYNTH_BARS = 2000             # scored bars, after 2 x required_bars of warmup
START_PRICE = 30000.0         # crypto-like level (a scale bug depends on it)
HOURLY_VOL = 0.007            # per-bar log-return std at 1h, scaled by sqrt(interval)
SYNTH_START = "2000-01-01"    # invented calendar, far from any real or sealed date
_TIMEFRAME_SECONDS = {"1m": 60, "5m": 300, "15m": 900, "30m": 1800, "1h": 3600,
                      "2h": 7200, "4h": 14400, "6h": 21600, "12h": 43200, "1d": 86400}


def forecast_threshold(config_json: Path = CONFIG_JSON,
                       strategy_config: dict | None = None) -> float:
    """10 x the rebalance floor the engine will actually apply: the strategy
    config's own `strategies.min_allocation_change` when set (the engine's
    override, main_strategy.py / launcher.py), else trading-bot/config.json's
    risk_management.controls.min_allocation_change.threshold. 0 is allowed
    (every nonzero forecast trades). Fail loud when the floor is missing or
    not a non-negative number: the probe must not guess it."""
    override = ((strategy_config or {}).get("strategies") or {}).get("min_allocation_change")
    if override is not None:
        floor, where = override, "strategies.min_allocation_change"
    else:
        cfg = json.loads(Path(config_json).read_text(encoding="utf-8"))
        try:
            floor = cfg["risk_management"]["controls"]["min_allocation_change"]["threshold"]
        except (KeyError, TypeError) as exc:
            raise ValueError(f"{config_json}: risk_management.controls.min_allocation_change."
                             f"threshold is missing -- cannot size the probe") from exc
        where = f"{config_json}: min_allocation_change.threshold"
    if isinstance(floor, bool) or not isinstance(floor, (int, float)) or floor < 0:
        raise ValueError(f"{where}={floor!r} is not a non-negative number")
    return 10.0 * float(floor)


def assess(forecasts: list, threshold: float) -> dict:
    """Pure: the size verdict. Refuses only all-NaN, or a nonzero forecast
    whose largest magnitude is below BUG_FACTOR x threshold."""
    finite = [abs(float(f)) for f in forecasts
              if f is not None and isinstance(f, (int, float)) and math.isfinite(f)]
    n, n_nan = len(finite), len(forecasts) - len(finite)
    if n == 0:
        return {"status": "refuse", "n_bars": 0, "n_nan": n_nan, "threshold": threshold,
                "message": (f"every forecast is NaN or missing ({n_nan} bars) on the invented "
                            f"series: the config never produces a usable forecast")}
    max_abs = max(finite)
    out = {"status": "ok", "n_bars": n, "n_nan": n_nan, "threshold": threshold,
           "bug_limit": BUG_FACTOR * threshold, "max_abs": max_abs,
           "share_nonzero": sum(1 for v in finite if v > 0) / n}
    if max_abs == 0:
        out["note"] = ("silent: every forecast is exactly 0 on the invented series -- not a "
                       "refusal (a rare-event strategy can be silent on any sample)")
    elif threshold > 0 and max_abs < BUG_FACTOR * threshold:
        out["status"] = "refuse"
        out["message"] = (
            f"forecast broken in size: its largest |forecast| on the invented series is "
            f"{max_abs:.3g}, below 1/{int(1 / BUG_FACTOR)} of the {threshold:g} needed to move "
            f"the position (10 x min_allocation_change) -- a units/scale mistake, e.g. "
            f"vol_adjusted or vol_normalize used in `transforms` without a ratio_to_mean "
            f"rescale (they divide by stddev_24 x close, ~price^2), or price_normalized on a "
            f"percent output. Rescale so a typical signal is a few forecast units")
    return out


def synthetic_bars(n: int, interval_seconds: int, seed: int = SYNTH_SEED):
    """The invented series: OHLCV + every live aux feed column, as the engine's
    get_data_history rows carry them. Deterministic for a seed."""
    import numpy as np
    import pandas as pd
    rng = np.random.default_rng(seed)
    vol = HOURLY_VOL * math.sqrt(interval_seconds / 3600.0)
    close = START_PRICE * np.exp(np.cumsum(rng.normal(0.0, vol, n)))
    open_ = np.concatenate(([START_PRICE], close[:-1]))
    wick = np.abs(rng.normal(0.0, vol / 2.0, n))
    ts = pd.date_range(SYNTH_START, periods=int(n), freq=f"{int(interval_seconds)}s")
    # funding: an 8h print carried forward; fear & greed: a daily 0..100 walk carried forward
    hours = (np.arange(n) * interval_seconds) // 3600
    funding_prints = rng.normal(1e-4, 2e-4, int(hours[-1] // 8) + 1)
    fg_daily = np.clip(50 + np.cumsum(rng.normal(0, 4, int(hours[-1] // 24) + 1)), 0, 100).round()
    return pd.DataFrame({
        "timestamp": ts, "open": open_,
        "high": np.maximum(open_, close) * (1 + wick),
        "low": np.minimum(open_, close) * (1 - wick),
        "close": close, "volume": rng.lognormal(6.0, 0.5, n),
        "funding_rate": funding_prints[hours // 8],
        "fear_greed": fg_daily[hours // 24],
    })


def _forecasts_on_invented_series(config_path: Path, interval_seconds: int) -> list:
    """The real AdvancedStrategy, fed bar by bar exactly as TradingBot feeds it
    (strategy.update(one-row frame) then generate_signals())."""
    if str(_TBOT) not in sys.path:
        sys.path.insert(0, str(_TBOT))
    from strategies.main_strategy import AdvancedStrategy  # noqa: E402
    strategy = AdvancedStrategy(str(config_path))
    bars = synthetic_bars(2 * strategy.required_bars + SYNTH_BARS, interval_seconds)
    warmup = 2 * strategy.required_bars
    forecasts = []
    for i in range(len(bars)):
        strategy.update(bars.iloc[i:i + 1])
        signal = strategy.generate_signals()
        if i >= warmup:
            forecasts.append(signal.forecast)
    return forecasts


def probe(config_path: Path, protocol: dict) -> dict:
    timeframe = str(protocol.get("timeframe", "1h"))
    if timeframe not in _TIMEFRAME_SECONDS:
        raise ValueError(f"protocol timeframe {timeframe!r} is not one of "
                         f"{sorted(_TIMEFRAME_SECONDS)}")
    threshold = forecast_threshold(
        strategy_config=json.loads(Path(config_path).read_text(encoding="utf-8")))
    result = assess(_forecasts_on_invented_series(Path(config_path),
                                                  _TIMEFRAME_SECONDS[timeframe]), threshold)
    result.update({"data": "invented", "seed": SYNTH_SEED, "timeframe": timeframe})
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
