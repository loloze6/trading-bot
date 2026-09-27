"""
The equal-weight portfolio's daily closes and daily returns -- ONE definition,
shared by the profit bars (run_phase1_research._portfolio_profit_metrics, the
branch-3 avg_daily_return / drawdown bars) and the composition's stand-alone
block returns (tools/composition.load_block_daily_returns, the vol_scaled
weights). E-060 S3b code review fix 9: extracted from run_phase1_research
(behaviour-preserving -- same readers, same messages, same floor) so the two
cannot drift.

Definition (mirrored in config/profitability_bars.yaml's header):
  * source: every (coin, window) backtest's portfolio_states.csv, column
    postRebalance_total_value, warm-up bars (regime NOT_READY) dropped;
  * daily close: the last bar of each UTC calendar day;
  * common days, per window: the UTC days on which every coin has a daily
    close; they must cover >= PORTFOLIO_MIN_COMMON_DAY_COVERAGE of the union
    of the coins' days, and there must be >= 2 of them;
  * each coin normalised at its close on the window's first common day; the
    portfolio is the arithmetic mean of the normalised coins;
  * daily return: V_d / V_(d-1) - 1 between CONSECUTIVE common days only.

Nothing here reads anything under local_data/holdout_sealed/: the paths come
from a protocol result's own window run ids under a run directory.
"""
from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path

# Coverage floor of the equal-weight portfolio (operator-changeable; mirrored in
# config/profitability_bars.yaml's header). Within EACH window, the UTC days on
# which every coin has a value (the intersection) must be at least this fraction
# of the days on which any coin has a value (the union). Below it the portfolio
# would be judged on a thinned-out sample (one coin's data gap, or a much longer
# warm-up on one coin, silently removes those days for all coins), so both
# portfolio bars read NOT_EVALUABLE instead.
PORTFOLIO_MIN_COMMON_DAY_COVERAGE = 0.9


class PortfolioNotEvaluable(ValueError):
    """The portfolio cannot be built from these (well-formed) inputs: a file is
    missing, the coin set differs, a window is too thin. The message is the
    reason; the profit bars read it as NOT_EVALUABLE, the composition raises."""


def find_window_equity_file(run_dir: Path, window_run_id: str) -> Path | None:
    """portfolio_states.csv of one (symbol, window) backtest. tools/run_protocol.py
    writes it under <out_dir>/results/<window run_id>/, with out_dir = RUN_DIR
    (variant loop off) or RUN_DIR/variants/<variant_id> (variant loop on). The
    window run_id is unique; more than one match raises."""
    run_dir = Path(run_dir)
    roots = [run_dir / "results"]
    vroot = run_dir / "variants"
    if vroot.exists():
        roots += [d / "results" for d in sorted(vroot.iterdir()) if d.is_dir()]
    hits = [r / window_run_id / "portfolio_states.csv" for r in roots
            if (r / window_run_id / "portfolio_states.csv").exists()]
    if len(hits) > 1:
        raise ValueError(f"equal-weight portfolio: window run {window_run_id!r} has more than one "
                         f"portfolio_states.csv: {hits}")
    return hits[0] if hits else None


def window_equity_bars(path: Path) -> dict:
    """{timestamp (naive UTC): equity} for one (coin, window) backtest:
    postRebalance_total_value of every bar, warm-up bars (regime NOT_READY)
    dropped. Fails loud on a missing column or a non-numeric / non-positive
    equity value."""
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        missing = {"timestamp", "regime", "postRebalance_total_value"} - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"equal-weight portfolio: {path} lacks column(s) {sorted(missing)}")
        rows = []
        for row in reader:
            if str(row["regime"]).strip().upper() == "NOT_READY":
                continue
            ts = datetime.fromisoformat(str(row["timestamp"]).strip())
            if ts.tzinfo is not None:  # an aware stamp is bucketed by its UTC date
                ts = ts.astimezone(timezone.utc).replace(tzinfo=None)
            try:
                equity = float(row["postRebalance_total_value"])
            except (TypeError, ValueError):
                raise ValueError(f"equal-weight portfolio: {path} has a non-numeric "
                                 f"postRebalance_total_value at {row['timestamp']!r}")
            if not math.isfinite(equity) or equity <= 0:
                raise ValueError(f"equal-weight portfolio: {path} has equity {equity!r} at "
                                 f"{row['timestamp']!r}")
            rows.append((ts, equity))
    rows.sort(key=lambda r: r[0])
    return dict(rows)


def daily_closes(bars: dict) -> dict:
    """{UTC date: (timestamp, equity)} -- the LAST bar of each UTC calendar day."""
    daily: dict = {}
    for ts in sorted(bars):
        daily[ts.date()] = (ts, bars[ts])
    return daily


def window_daily_closes(path: Path) -> dict:
    """{UTC date: equity}: postRebalance_total_value of the LAST bar of each UTC
    calendar day of one (coin, window) backtest, warm-up bars dropped."""
    return {d: eq for d, (_ts, eq) in daily_closes(window_equity_bars(path)).items()}


def load_windows(run_dir: Path, pr: dict) -> tuple:
    """(windows, coins): {window label: {coin: {timestamp: equity}}} in results
    order, and the sorted coin list. A malformed results entry or a duplicate
    (coin, window) raises ValueError; an empty result, a missing equity file or
    a coin set that differs between windows raises PortfolioNotEvaluable."""
    results = pr.get("results") or []
    if not results:
        raise PortfolioNotEvaluable("protocol_result has no per-window results")
    windows: dict = {}
    for r in results:
        if not isinstance(r, dict) or any(r.get(k) in (None, "")
                                          for k in ("symbol", "window", "run_id")):
            raise ValueError(f"equal-weight portfolio: protocol_result.results entry {r!r} "
                             f"lacks symbol/window/run_id")
        sym, win, wid = r["symbol"], r["window"], r["run_id"]
        if sym in windows.get(win, {}):
            raise ValueError(f"equal-weight portfolio: coin {sym!r} appears twice in window "
                             f"{win!r}")
        path = find_window_equity_file(run_dir, wid)
        if path is None:
            raise PortfolioNotEvaluable(f"no portfolio_states.csv for window {win!r} ({sym}, "
                                        f"run {wid!r})")
        windows.setdefault(win, {})[sym] = window_equity_bars(path)
    coin_sets = {w: frozenset(c) for w, c in windows.items()}
    if len(set(coin_sets.values())) > 1:
        raise PortfolioNotEvaluable("the coin set differs between windows "
                                    f"({ {w: sorted(c, key=str) for w, c in coin_sets.items()} })")
    return windows, sorted(next(iter(coin_sets.values())), key=str)


def window_common_curve(win, by_coin: dict, coins: list) -> dict:
    """One window's common days and normalised portfolio curve:
    {daily, union, common, anchor, curve}. Too few common days or coverage
    below the floor raises PortfolioNotEvaluable."""
    daily = {c: daily_closes(by_coin[c]) for c in coins}
    union = set().union(*(set(d) for d in daily.values()))
    common = sorted(set.intersection(*(set(d) for d in daily.values())))
    coverage = len(common) / len(union) if union else 0.0
    if len(common) < 2:
        raise PortfolioNotEvaluable(f"window {win!r} has {len(common)} UTC day(s) on which every "
                                    f"coin has a value; at least 2 are needed")
    if coverage < PORTFOLIO_MIN_COMMON_DAY_COVERAGE:
        raise PortfolioNotEvaluable(
            f"window {win!r}: the {len(common)} common day(s) cover {coverage:.1%} of the "
            f"{len(union)} day(s) any coin has, below "
            f"PORTFOLIO_MIN_COMMON_DAY_COVERAGE={PORTFOLIO_MIN_COMMON_DAY_COVERAGE}")
    anchor = {c: daily[c][common[0]][1] for c in coins}
    curve = [sum(daily[c][d][1] / anchor[c] for c in coins) / len(coins) for d in common]
    return {"daily": daily, "union": union, "common": common, "anchor": anchor, "curve": curve}


def consecutive_daily_returns(common: list, curve: list) -> tuple:
    """([(date, simple return)], n_gap_steps): returns between consecutive
    common days only; a step across a gap is not a daily return."""
    out, gaps = [], 0
    for i in range(1, len(common)):
        if (common[i] - common[i - 1]).days == 1:
            out.append((common[i], curve[i] / curve[i - 1] - 1.0))
        else:
            gaps += 1
    return out, gaps


def portfolio_daily_returns(run_dir: Path, pr: dict) -> list:
    """[(UTC date, return)] of the equal-weight portfolio over every window of
    `pr` (results order). Raises PortfolioNotEvaluable / ValueError."""
    windows, coins = load_windows(run_dir, pr)
    out = []
    for win, by_coin in windows.items():
        wc = window_common_curve(win, by_coin, coins)
        out.extend(consecutive_daily_returns(wc["common"], wc["curve"])[0])
    return out
