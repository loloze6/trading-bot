import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    BAND = 2.0
    ER_P, ER_S, ER_MAX = 60, 5, 0.3
    LOW_P = 60
    MIN_CASES = 30
    DEPTH_COL = "debug_info.components.depth.last_history_value"

    def er_series(close):
        c = close.astype(float)
        change = (c - c.shift(ER_P)).abs()
        vol = c.diff().abs().rolling(ER_P, min_periods=ER_P).sum()
        er = change / vol.replace(0.0, np.nan)
        return er.rolling(ER_S, min_periods=ER_S).mean()

    def depth_from_prices(df):
        prior_low = df["low"].astype(float).shift(1).rolling(LOW_P, min_periods=LOW_P).min()
        return (df["close"].astype(float) / prior_low - 1.0) * 100.0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = f != 0
            if not active.any():
                continue
            er = er_series(df["close"])
            depth = pd.to_numeric(df[DEPTH_COL], errors="coerce") if DEPTH_COL in df.columns \
                else pd.Series(np.nan, index=df.index)
            depth = depth.where(depth.notna(), depth_from_prices(df))
            regime_mr = df["regime"].astype(str) == "mean_reversion"
            er_ok = (er <= ER_MAX) | (er.isna() & regime_mr)
            situ = er_ok & (depth < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean excess 10-bar return of long bets over the coin's mean 10-bar return"
    main_thr = "confirm: mean > 0 with day-clustered t >= 2 over >= 30 cases; reject: t <= -2"
    sup_name = "OLS slope of recovered share (excess / depth) on depth"
    reading = ("A case is the first long bet (forecast rise >= 2 points from its lowest long level since the last bet, "
               "reset to 0 when flat) in each non-overlapping 10-bar grid cell from each window's first row, kept only "
               "when 10 bars remain in the window; the coin's mean 10-bar return is taken on the same grid over all its "
               "windows; the day-clustered t sums deviations per UTC day with a G/(G-1) correction; the slope t is OLS; "
               "situation bars use the 60-bar ER recomputed from closes (SMA-5 smoothing), falling back on the recorded "
               "regime where the window is too short, and the recorded depth (else recomputed from prior 60-bar lows); "
               "fewer than 30 cases is reported 'not observable' per the workflow's minimum-count rule.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the 60-day "
                           "efficiency ratio is <= 0.3 and the close is below the prior 60-day low."),
            "reading": reading,
        }

    # ---------- 2. coin mean 10-bar return ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            for t in range(0, len(c) - H, H):
                if c[t] > 0 and np.isfinite(c[t]) and np.isfinite(c[t + H]):
                    rets.append(c[t + H] / c[t] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            c = df["close"].astype(float).to_numpy()
            depth = pd.to_numeric(df[DEPTH_COL], errors="coerce").to_numpy() if DEPTH_COL in df.columns \
                else np.full(len(df), np.nan)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            base = 0.0
            bets = []
            for i in range(len(f)):
                if f[i] <= 0:
                    base = 0.0
                    continue
                if f[i] - base >= BAND:
                    bets.append(i)
                    base = f[i]
                else:
                    base = min(base, f[i])
            seen = set()
            for i in bets:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= len(c) or not (c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                ex = r - coin_mean[coin]
                if not np.isfinite(ex):
                    continue
                rows.append({"day": ts.iloc[i].floor("D"), "excess": ex,
                             "depth": -depth[i] / 100.0 if np.isfinite(depth[i]) else np.nan})
    cases = pd.DataFrame(rows, columns=["day", "excess", "depth"])
    n = len(cases)
    n_days = int(cases["day"].nunique()) if n else 0

    mean_ex = float(cases["excess"].mean()) if n else None
    t_main = None
    if n >= 2:
        dev = cases["excess"] - mean_ex
        g = dev.groupby(cases["day"]).sum()
        G = len(g)
        if G > 1:
            se = np.sqrt((g ** 2).sum() * G / (G - 1)) / n
            t_main = float(mean_ex / se) if se > 0 else None

    slope = None
    t_slope = None
    sub = cases.dropna(subset=["depth"])
    sub = sub[sub["depth"] > 0]
    if len(sub) >= 3 and sub["depth"].nunique() > 1:
        share = sub["excess"] / sub["depth"]
        lr = stats.linregress(sub["depth"].to_numpy(), share.to_numpy())
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    sup_passed = None if t_slope is None else bool(t_slope >= 2)

    counts = {"cases": int(n), "days": n_days, "cases with depth": int(len(sub))}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 30 cases."
    elif t_main is not None and t_main <= -2:
        status = "rejected"
        decided = "Reject rule: the mean excess return has t <= -2 (breakdowns keep going)."
    elif t_slope is not None and t_slope <= -2:
        status = "rejected"
        decided = "Reject rule: the slope of the share on the depth has t <= -2 (bigger breaks are recovered less)."
    elif t_main is not None and mean_ex > 0 and t_main >= 2 and slope is not None and slope > 0 \
            and t_slope is not None and t_slope >= 2:
        status = "confirmed"
        decided = "Confirm rule: mean excess return positive with t >= 2 over >= 30 cases, and slope positive with t >= 2."
    elif t_main is not None and mean_ex > 0 and t_main >= 2:
        status = "inconclusive"
        decided = "Inconclusive rule: the main measure meets the confirm rule but the slope t is between -2 and 2."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the main t is between -2 and 2 and no reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_ex,
                         "statistic": None if t_main is None else {"name": "day-clustered t", "value": t_main},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name + " (t)", "value": t_slope, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
