import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    DEPTH = "debug_info.components.depth.last_history_value"
    EPS = 1e-12

    def recompute_depth(df):
        c = df["close"].astype(float)
        hi = c.rolling(14, min_periods=14).max()
        vol = c.pct_change().rolling(30, min_periods=30).std()
        return (c - hi) / hi / vol

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = df["forecast"].astype(float)
            raw = df[DEPTH].astype(float) if DEPTH in df.columns else pd.Series(np.nan, index=df.index)
            raw = raw.where(raw.notna(), recompute_depth(df))
            active = f.notna() & (f.abs() > EPS)
            n_active += int(active.sum())
            ok = active & raw.notna() & (raw < -EPS) & (f < 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the active bars are short bars with the close below its 14-day closing high (negative swing-scaled depth), as the Fidelity's situation and falling outcome require.",
            "reading": "Situation = raw depth below 0 with a negative forecast; missing raw values recomputed from closes inside the window.",
        }

    # ---------- 2. grid returns and coin drift ----------
    grid_rows = []   # coin, ret, forecast, in_profile
    case_rows = []   # coin, ret, timestamp (bets)
    coin_grid_rets = {}
    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).fillna(0.0).values
            reg = df["regime"].astype(str).values
            n = len(df)
            for g in range(0, n - H, H):
                r = c[g + H] / c[g] - 1.0
                if not np.isfinite(r):
                    continue
                rets_all.append(r)
                grid_rows.append((coin, r, f[g], reg[g] == "unknown"))
            # bets on the short side (forecast.md 7)
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                if f[i] < -EPS:
                    m = -f[i]
                    if m - ref >= BAND - 1e-9:
                        bet[i] = True
                        ref = m
                    else:
                        ref = min(ref, m)
                else:
                    ref = 0.0
            for g in range(0, n, H):
                idx = np.where(bet[g:min(g + H, n)])[0]
                if len(idx) == 0:
                    continue
                t = g + int(idx[0])
                if t + H >= n:
                    continue
                r = c[t + H] / c[t] - 1.0
                if np.isfinite(r):
                    case_rows.append((coin, r))
        coin_grid_rets[coin] = float(np.mean(rets_all)) if rets_all else np.nan

    G = pd.DataFrame(grid_rows, columns=["coin", "ret", "forecast", "inprof"])
    G["drift"] = G["coin"].map(coin_grid_rets)
    G["excess"] = G["ret"] - G["drift"]
    P = G[G["inprof"]].dropna(subset=["excess", "forecast"])
    n_inprof = int(len(P))
    n_nonzero = int((P["forecast"].abs() > EPS).sum())

    slope = None
    tval = None
    if n_inprof >= 3 and P["forecast"].std() > 0:
        lr = stats.linregress(P["forecast"].values, P["excess"].values)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    # supporting check
    C = pd.DataFrame(case_rows, columns=["coin", "ret"])
    if len(C):
        C["drift"] = C["coin"].map(coin_grid_rets)
        C["unusual"] = -(C["ret"] - C["drift"])
        C = C.dropna(subset=["unusual"])
    n_cases = int(len(C))
    sup_val = float(C["unusual"].mean()) if n_cases > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    counts = {
        "grid cases in profile with a non-zero forecast": n_nonzero,
        "grid cases in profile": n_inprof,
        "supporting cases (short-side forecast rises of at least 2 points)": n_cases,
    }

    if n_nonzero < 150:
        status = "not observable"
        decided = f"Only {n_nonzero} grid cases in profile with a non-zero forecast, fewer than the plan's minimum of 150."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the mean unusual move of the cases is positive in the short direction."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check is not positive, which the plan calls inconclusive."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: deeper declines are followed by rebounds against the drift."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of 5-bar excess return on forecast, in-profile grid bars",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": "confirm: slope > 0 with t >= 2 (and supporting check positive); reject: slope < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "mean unusual 5-bar move of short-side cases, short direction",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "In-profile means regime 'unknown' (the calm regime with the strategy), the regression uses all in-profile grid bars including forecast 0, the coin's drift is its mean non-overlapping 5-bar grid return over all windows, and supporting cases are short-side bets (forecast.md 7) taken once per grid cell at their first bar; a short count below the minimum is reported as not observable per the workflow.",
    }
