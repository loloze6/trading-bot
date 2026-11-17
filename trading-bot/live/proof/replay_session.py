"""Proof that a live session decided what the backtest decides on the same candles.

    python live/proof/replay_session.py live_runs/<run>/session_NN

Runs the backtest engine (BacktestEngine, the same one run_backtest uses) on the session's recorded candles with
the session's start value and warm-up cut-off, then compares its per-bar record with the session's local_book.csv,
file against file. The unfinished last bar (candles of a bar whose end had not come when the session stopped) is
left out of the replay: the backtest closes the last bar of its data, live never closes an unfinished one.
"""
import datetime
import json
import sys
import tempfile
from pathlib import Path

import pandas as pd

BOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BOT))


def replay(session_dir, out_dir):
    import logging
    from core.backtester import BacktestEngine
    from live.runner import build_book
    session_dir, out_dir = Path(session_dir), Path(out_dir)
    run_dir = session_dir.parent
    cfg = json.loads((run_dir / "live_config.json").read_text(encoding="utf-8"))
    info = json.loads((session_dir / "session.json").read_text(encoding="utf-8"))
    symbol, interval, fetch = cfg["symbol"], int(cfg["interval_seconds"]), int(cfg["fetch_interval_seconds"])
    candles = pd.read_csv(session_dir / "candles.csv", parse_dates=["timestamp"])
    bar_start = candles["timestamp"].dt.floor(f"{interval}s")
    last_bar = bar_start.iloc[-1]
    complete = candles["timestamp"].iloc[-1] + datetime.timedelta(seconds=fetch) >= last_bar + datetime.timedelta(seconds=interval)
    if not complete:
        candles = candles[bar_start < last_bar]
    parts = build_book(run_dir / "strategy_config.json", symbol, interval, fetch, float(info["start_value"]),
                       out_dir, mode="backtest")
    data_manager = parts.pop("data_manager")
    engine = BacktestEngine(data_manager=data_manager, logger=logging.getLogger("trading_bot"),
                            candle_interval_seconds=interval, test_mode=True, symbols=[symbol],
                            initial_capital=float(info["start_value"]), exchange="kraken",
                            warmup_cutoff_timestamp=pd.Timestamp(info["cutoff"]), **parts)
    engine.historical_data = {symbol: candles.reset_index(drop=True)}
    data_manager.historical_data = engine.historical_data
    data_manager.initialize()
    engine.simulate_on_loaded_data()
    tracker = parts["portfolio_state_tracker"]
    tracker.output_dir = str(out_dir)   # the engine moved it into its run folder
    tracker.to_csv("replay_book.csv")
    return out_dir / "replay_book.csv"


def compare(session_dir):
    with tempfile.TemporaryDirectory() as tmp:
        replayed = replay(session_dir, tmp)
        live_bytes = (Path(session_dir) / "local_book.csv").read_bytes()
        same = replayed.read_bytes() == live_bytes
        a, b = pd.read_csv(Path(session_dir) / "local_book.csv"), pd.read_csv(replayed)
    print(f"{'IDENTICAL' if same else 'DIFFERENT'}: live local_book.csv ({len(a)} rows) vs backtest replay "
          f"({len(b)} rows)")
    if not same:
        cols = [c for c in a.columns.union(b.columns) if c not in a.columns or c not in b.columns
                or not a[c].reset_index(drop=True).equals(b[c].reset_index(drop=True))]
        print(f"columns that differ: {cols}")
        for c in cols[:5]:
            if c in a.columns and c in b.columns:
                diff = a[c].ne(b[c]) & ~(a[c].isna() & b[c].isna())
                i = diff.idxmax() if diff.any() else None
                print(f"  {c}: first differing row {i}: live {a[c].get(i)!r} | replay {b[c].get(i)!r} "
                      f"(timestamp {a['timestamp'].get(i)})")
    return same


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(0 if compare(sys.argv[1]) else 1)
