import numpy as np
import pandas as pd
from scipy import stats

RAW_COL = "debug_info.components.rsi_low.last_history_value"
H = 5


def _rsi_wilder(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)
    avg_gain = gain.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - 100 / (1 + rs)
    rsi = rsi.where(avg_loss != 0, 100.0)
    rsi = rsi.where(~(avg_gain.isna() | avg_loss.isna()))
    return rsi


def _non_overlapping(mask, fwd):
    # Walk the bars in time order and take a case where the condition holds.
    # After each case, skip the next H-1 bars so the 5-bar returns do not overlap.
    out = []
    n = len(mask)
    i = 0
    while i < n:
        if mask[i] and np.isfinite(fwd[i]):
            out.append(float(fwd[i]))
            i += H
        else:
            i += 1
    return out


def _diff_t(ext, neu):
    if len(ext) == 0 or len(neu) == 0:
        return None, None
    d = float(np.mean(ext) - np.mean(neu))
    if len(ext) < 2 or len(neu) < 2:
        return d, None
    t = stats.ttest_ind(ext, neu, equal_var=False).statistic
    t = float(t) if np.isfinite(t) else None
    return d, t


def measure(bars):
    pooled_ext, pooled_neu = [], []
    coin_ext, coin_neu = {}, {}
    coin_excess = {}

    for coin in sorted(bars.keys()):
        coin_ext[coin], coin_neu[coin] = [], []
        strat_wins, gain_wins = [], []

        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if "timestamp" in df.columns:
                df = df.sort_values("timestamp")
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")

            # 5-bar forward return, inside this window only
            fwd = (close.shift(-H) / close - 1).to_numpy()

            # Extreme bars: raw component >= 8 (RSI <= 30)
            raw = pd.to_numeric(df[RAW_COL], errors="coerce").to_numpy()
            ext_mask = np.isfinite(raw) & (raw >= 8)

            # Neutral bars: RSI(14) between 40 and 60, recomputed from this window's closes
            rsi = _rsi_wilder(close).to_numpy()
            neu_mask = np.isfinite(rsi) & (rsi >= 40) & (rsi <= 60)

            e = _non_overlapping(ext_mask, fwd)
            n = _non_overlapping(neu_mask, fwd)
            coin_ext[coin] += e
            coin_neu[coin] += n
            pooled_ext += e
            pooled_neu += n

            # Data for the supporting check
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            r1 = close.shift(-1) / close - 1
            valid = alloc.notna() & r1.notna()
            strat_wins.append((alloc[valid].to_numpy(), r1[valid].to_numpy()))
            gain_wins.append(valid.sum())

        # Supporting check: compound within each window, then chain the window results.
        all_alloc = np.concatenate([a for a, _ in strat_wins]) if strat_wins else np.array([])
        if len(all_alloc) == 0:
            coin_excess[coin] = None
            continue
        avg_size = float(np.mean(all_alloc))
        strat_cum, bench_cum = 1.0, 1.0
        for a, r in strat_wins:
            if len(a) == 0:
                continue
            strat_cum *= float(np.prod(1 + a * r))
            bench_cum *= float(np.prod(1 + avg_size * r))
        coin_excess[coin] = (strat_cum - 1) - (bench_cum - 1)

    n_ext = len(pooled_ext)
    diff, t = _diff_t(pooled_ext, pooled_neu)

    coin_diffs = {c: _diff_t(coin_ext[c], coin_neu[c])[0] for c in coin_ext}
    n_neg = sum(1 for v in coin_diffs.values() if v is not None and v < 0)
    min_coin_ext = min((len(v) for v in coin_ext.values()), default=0)

    ex_vals = [v for v in coin_excess.values() if v is not None]
    sup_value = float(np.mean(ex_vals)) if ex_vals else None
    sup_passed = (all(v > 0 for v in ex_vals) if ex_vals and len(ex_vals) == len(coin_excess) else None)

    if n_ext < 30 or min_coin_ext < 8 or diff is None:
        status = "inconclusive"
        decided = ("Fewer than 30 non-overlapping extreme cases pooled, or fewer than 8 for a coin, "
                   "is inconclusive whatever the sign.")
    elif diff >= 0:
        status = "rejected"
        decided = "Pooled extreme-minus-neutral 5-bar return is >= 0 (no continuation)."
    elif t is not None and t <= -2 and n_neg >= 2:
        status = "confirmed"
        decided = ("Pooled extreme-minus-neutral 5-bar return is below 0 with t <= -2, "
                   "and is negative in at least 2 coins.")
    else:
        status = "inconclusive"
        decided = ("A negative pooled difference with t between -2 and 0, "
                   "or coins that disagree in sign.")

    return {
        "status": status,
        "main_measure": {
            "name": "pooled 5-bar forward return after extreme (raw >= 8) minus after neutral (RSI 40-60) bars",
            "value": diff,
            "threshold": "below 0 with t <= -2 to confirm; >= 0 rejects",
        },
        "supporting_check": {
            "name": "per-coin cumulative strategy return minus constant short of same average size (mean over coins)",
            "value": sup_value,
            "passed": sup_passed,
        },
        "cases": n_ext,
        "decided_by": decided,
        "reading": (
            "Neutral RSI is a Wilder RSI(14) recomputed within each window, with bounds 40 and 60 inclusive. "
            "Non-overlapping cases are taken greedily per window and group, skipping 4 bars after each case. "
            "t is a Welch two-sample t. "
            "Only 2 coins are in the record, so 'at least 2 of 3 coins negative' requires both to be negative. "
            "For the supporting check: the average size is the signed mean allocation, returns are compounded "
            "within each window and chained across windows, and the check passes if every coin's excess is > 0."
        ),
    }
