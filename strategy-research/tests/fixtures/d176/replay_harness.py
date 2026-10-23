"""
D-176 byte-identity replay harness (used by the recorder AND the test).

One function, `replay(trading_bot_root, config_path, ohlcv_csv, work_dir)`, drives the REAL
backtest entry point `core.launcher.run_backtest` over a synthetic OHLCV CSV and returns the
produced `bars.csv` path. The only thing substituted is the data source: the
`DataManager.fetch_historical_data` call (cache / network) is replaced by a read of the CSV,
so the strategy, buffer, forecast manager, risk manager, execution mock, tracker and the
bars.csv writer are all the real code of whichever checkout `trading_bot_root` names.

Recording (once, on master's code, NOT part of the test):
    python -I replay_harness.py <master trading-bot root> <config.json> <ohlcv.csv> <out_bars.csv>
Synthetic series (deterministic):
    python -I replay_harness.py --make-series <out.csv>

The test imports `replay` by path and passes the BRANCH's trading-bot root. Nothing here
imports from, or points at, the master checkout.
"""
import contextlib
import shutil
import sys
from pathlib import Path

SEED = 176
N_BARS = 700
START = "2019-01-01"
SYMBOL = "BTCUSDT"
INTERVAL_SECONDS = 86400


def make_series(path, seed=SEED, n=N_BARS):
    """Seeded geometric random walk, ~3% daily vol, positive prices, volume > 0."""
    import numpy as np
    import pandas as pd

    rng = np.random.default_rng(seed)
    ret = rng.normal(0.0004, 0.03, n)
    close = 10000.0 * np.exp(np.cumsum(ret))
    open_ = np.concatenate([[10000.0], close[:-1]])
    wiggle_hi = np.abs(rng.normal(0.0, 0.01, n))
    wiggle_lo = np.abs(rng.normal(0.0, 0.01, n))
    high = np.maximum(open_, close) * (1.0 + wiggle_hi)
    low = np.minimum(open_, close) * (1.0 - wiggle_lo)
    volume = rng.uniform(100.0, 1000.0, n)
    df = pd.DataFrame({
        "timestamp": pd.date_range(START, periods=n, freq="D"),
        "open": open_, "high": high, "low": low, "close": close, "volume": volume,
    })
    df.to_csv(path, index=False)
    return df


def assert_traded(bars_csv):
    """Generation-step guard: the recorded book is not flat (>= 1 executed rebalance and a
    nonzero position). Never fix a failure by editing a config: change SEED / the vol."""
    import pandas as pd

    d = pd.read_csv(bars_csv)
    executed = int((d["succcess_execute_portfolio_rebalance"] == True).sum())  # noqa: E712
    assert executed >= 1, f"{bars_csv}: no executed rebalance"
    assert (d["postRebalance_current_allocation"].abs() > 0).any(), f"{bars_csv}: book always flat"
    return executed


def replay(trading_bot_root, config_path, ohlcv_csv, work_dir):
    """Run core.launcher.run_backtest from `trading_bot_root` over `ohlcv_csv`; return bars.csv Path."""
    import pandas as pd

    root = str(Path(trading_bot_root).resolve())
    if root not in sys.path:
        sys.path.insert(0, root)
    from core.launcher import run_backtest
    from data.data_manager import DataManager

    df = pd.read_csv(ohlcv_csv, parse_dates=["timestamp"])
    work = Path(work_dir)
    results_root = work / "results"
    runs_root = work / "runs"
    results_root.mkdir(parents=True, exist_ok=True)
    runs_root.mkdir(parents=True, exist_ok=True)

    def _fetch(self, symbol, start_date, end_date, *a, **k):
        return df.copy()

    original = DataManager.fetch_historical_data
    DataManager.fetch_historical_data = _fetch
    try:
        run_dir = run_backtest(
            config_path=str(config_path), symbol=SYMBOL,
            start=START, end="2020-12-31",
            results_root=str(results_root), runs_root=str(runs_root),
            interval_seconds=INTERVAL_SECONDS,
            trades_log_file=str(work / "trades.json"),
            feed_local_storage=False,
        )
    finally:
        DataManager.fetch_historical_data = original
    return Path(run_dir) / "bars.csv"


if __name__ == "__main__":
    if sys.argv[1] == "--make-series":
        make_series(sys.argv[2])
    else:
        root, cfg, csv, out = sys.argv[1:5]
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            bars = replay(root, cfg, csv, td)
            assert_traded(bars)
            shutil.copyfile(bars, out)
        print("wrote", out)
