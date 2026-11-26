import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    ER_N = 30
    ER_MAX = 0.3
    MIN_CASES = 100
    RAW = "debug_info.components.scaled_week.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            # 30-bar Kaufman efficiency ratio, unsmoothed, recomputed from prices inside the window
            net = (close - close.shift(ER_N)).abs()
            path = close.diff().abs().rolling(ER_N).sum()
            er = net / path.replace(0, np.nan)
            # fallback where ER cannot be computed inside the window: the detector's own decision
            choppy = er <= ER_MAX + 1e-12
            no_er = er.isna()
            reg_mr = df["regime"].astype(str) == "mean_reversion"
            choppy = choppy.where(~no_er, reg_mr)
            # raw scaled 7-day move: recorded raw value, else recomputed 7-day return from prices
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            ret7 = close / close.shift(H) - 1.0
            raw = raw.where(raw.notna(), ret7)
            exp_side = np.sign(raw)
            active = fc != 0
            agree = active & choppy & (np.sign(fc) == exp_side) & (exp_side != 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The 30-bar efficiency ratio is recomputed from closes inside each window, and on the first bars "
               "of a window where it cannot be, the recorded regime stands for the detector; the expected side is "
               "the sign of the recorded raw scaled 7-day move (the 7-day price return where not recorded); the "
               "coin's mean 7-bar return is taken on the non-overlapping 0,7,14,... grid of all its windows' bars; "
               "the slope's t is the ordinary least-squares slope over its standard error.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are choppy bars (30-day efficiency "
                           "ratio <= 0.3) with the forecast on the side of the scaled 7-day move, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    rets.append(c[i + H] / c[i] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    xs, ys = [], []
    for coin, wins in bars.items():
        m = coin_mean[coin]
        if not np.isfinite(m):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            reg = df["regime"].astype(str).to_numpy()
            for i in range(0, len(c) - H, H):
                if reg[i] != "mean_reversion" or not np.isfinite(fc[i]) or fc[i] == 0:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                xs.append(float(fc[i]))
                ys.append(c[i + H] / c[i] - 1.0 - m)

    n = len(xs)
    slope = None
    tval = None
    if n >= 3 and np.ptp(xs) > 0:
        lr = stats.linregress(np.array(xs), np.array(ys))
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    if n < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n} non-overlapping choppy cases with a non-zero forecast, under the plan's minimum of 100."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided_by = "The slope is positive with t >= 2 on at least 100 cases (confirm rule)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided_by = "The slope is negative with t <= -2 on at least 100 cases (reject rule)."
    else:
        status = "inconclusive"
        decided_by = "The t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "OLS slope of drift-removed 7-bar forward return on forecast, choppy grid bars",
            "value": slope,
            "statistic": {"name": "t of the OLS slope", "value": tval} if tval is not None else None,
            "threshold": "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 100 cases",
        },
        "supporting_check": None,
        "counts": {"non-overlapping cases on choppy bars": n},
        "decided_by": decided_by,
        "reading": reading,
    }
