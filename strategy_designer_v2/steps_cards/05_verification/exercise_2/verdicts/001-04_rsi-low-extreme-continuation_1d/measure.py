import numpy as np
import pandas as pd
from scipy import stats

RAW_COL = "debug_info.components.rsi_low.last_history_value"
H = 5
EXTREME_RAW = 8.0
NEUTRAL_LO, NEUTRAL_HI = 40.0, 60.0
RSI_PERIOD = 14


def _wilder_rsi(close, period=RSI_PERIOD):
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = (-delta).clip(lower=0.0)
    avg_gain = gain.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100.0 - 100.0 / (1.0 + rs)
    rsi = rsi.where(avg_loss != 0, 100.0)
    rsi = rsi.where(avg_gain.notna() & avg_loss.notna())
    return rsi


def _non_overlapping(idx_positions, h=H):
    chosen, last = [], -10**9
    for p in idx_positions:
        if p - last >= h:
            chosen.append(p)
            last = p
    return chosen


def measure(bars):
    ext_all, neu_all = [], []
    per_coin = {}
    support = {}

    for coin in sorted(bars.keys()):
        ext_c, neu_c = [], []
        strat_cum, bench_cum = 1.0, 1.0
        gains_alloc, gains_ret = [], []
        windows = bars[coin]
        for w in sorted(windows.keys()):
            df = windows[w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            raw = pd.to_numeric(df[RAW_COL], errors="coerce") if RAW_COL in df.columns else pd.Series(np.nan, index=df.index)
            rsi = _wilder_rsi(close)
            fwd = close.shift(-H) / close - 1.0
            n = len(df)

            ext_pos = [i for i in range(n)
                       if pd.notna(raw.iloc[i]) and raw.iloc[i] >= EXTREME_RAW - 1e-9 and pd.notna(fwd.iloc[i])]
            neu_pos = [i for i in range(n)
                       if pd.notna(rsi.iloc[i]) and NEUTRAL_LO <= rsi.iloc[i] <= NEUTRAL_HI and pd.notna(fwd.iloc[i])]
            for p in _non_overlapping(ext_pos):
                ext_c.append(float(fwd.iloc[p]))
            for p in _non_overlapping(neu_pos):
                neu_c.append(float(fwd.iloc[p]))

            # supporting check data (per window, no cross-window returns)
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            r1 = close.shift(-1) / close - 1.0
            for i in range(n):
                if pd.notna(alloc.iloc[i]) and pd.notna(r1.iloc[i]):
                    gains_alloc.append(float(alloc.iloc[i]))
                    gains_ret.append(float(r1.iloc[i]))

        ext_all.extend(ext_c)
        neu_all.extend(neu_c)
        diff_c = (np.mean(ext_c) - np.mean(neu_c)) if (len(ext_c) > 0 and len(neu_c) > 0) else None
        per_coin[coin] = {"n_extreme": len(ext_c), "n_neutral": len(neu_c),
                          "diff": None if diff_c is None else float(diff_c)}

        if gains_alloc:
            a = np.array(gains_alloc)
            r = np.array(gains_ret)
            avg_size = a.mean()
            strat_cum = float(np.prod(1.0 + a * r) - 1.0)
            bench_cum = float(np.prod(1.0 + avg_size * r) - 1.0)
            support[coin] = strat_cum - bench_cum

    n_ext = len(ext_all)
    n_neu = len(neu_all)
    diff = None
    t = None
    if n_ext >= 2 and n_neu >= 2:
        diff = float(np.mean(ext_all) - np.mean(neu_all))
        tt = stats.ttest_ind(ext_all, neu_all, equal_var=False)
        t = float(tt.statistic) if np.isfinite(tt.statistic) else None
    elif n_ext >= 1 and n_neu >= 1:
        diff = float(np.mean(ext_all) - np.mean(neu_all))

    coin_diffs = [v["diff"] for v in per_coin.values()]
    n_neg = sum(1 for d in coin_diffs if d is not None and d < 0)
    n_pos = sum(1 for d in coin_diffs if d is not None and d >= 0)
    min_coin_ext = min((v["n_extreme"] for v in per_coin.values()), default=0)

    if support:
        sup_val = float(min(support.values()))
        sup_pass = bool(all(v > 0 for v in support.values()))
    else:
        sup_val, sup_pass = None, None

    if n_ext < 30 or min_coin_ext < 8 or diff is None:
        status = "inconclusive"
        decided = (f"Fewer than 30 pooled non-overlapping extreme cases ({n_ext}) or fewer than 8 for a coin "
                   f"(min {min_coin_ext}) is inconclusive whatever the sign.")
    elif diff >= 0:
        status = "rejected"
        decided = (f"Pooled extreme-minus-neutral 5-bar return is >= 0 ({diff:.5f}, t={t}), "
                   "so continuation is rejected.")
    elif t is not None and t <= -2 and n_neg >= 2 and n_pos == 0:
        status = "confirmed"
        decided = (f"Pooled difference {diff:.5f} is below 0 with t={t:.2f} <= -2 and negative in "
                   f"{n_neg} coins (at least 2).")
    else:
        status = "inconclusive"
        decided = (f"Negative pooled difference {diff:.5f} with t={t} not <= -2, or coins disagree in sign "
                   f"({n_neg} negative, {n_pos} non-negative), is inconclusive.")

    return {
        "status": status,
        "main_measure": {
            "name": "pooled 5-bar forward return after extreme (raw>=8) minus after neutral (RSI 40-60) bars",
            "value": diff,
            "threshold": "below 0 with t <= -2 to confirm; >= 0 to reject",
        },
        "supporting_check": {
            "name": "per-coin strategy cumulative return before costs minus same-average-size short hold (min over coins)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "cases": int(n_ext),
        "decided_by": decided,
        "reading": ("Neutral RSI is recomputed as Wilder RSI(14) on each window's closes (first bars without RSI dropped), "
                    "extreme bars use the recorded raw component >= 8, non-overlap is enforced per group per window by "
                    "taking a case then skipping the next 4 bars, the t is Welch's two-sample t, and with only 2 coins in "
                    "the record 'negative in at least 2 of 3 coins' requires both coins negative; the supporting check "
                    "compounds per-bar gains within windows, uses the coin's mean signed allocation as the short size, "
                    "and passes only if the strategy beats it in every coin."),
    }
