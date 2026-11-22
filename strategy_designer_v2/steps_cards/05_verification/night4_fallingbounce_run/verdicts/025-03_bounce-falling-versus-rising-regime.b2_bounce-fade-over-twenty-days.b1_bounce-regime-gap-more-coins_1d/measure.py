import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    BAND = 2.0
    RU = "debug_info.components.rise_up.last_history_value"
    RD = "debug_info.components.rise_down.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            # raw rise: recorded component value, else recomputed from prices
            raw = pd.Series(np.nan, index=df.index, dtype=float)
            for col in (RU, RD):
                if col in df.columns:
                    v = pd.to_numeric(df[col], errors="coerce")
                    raw = raw.fillna(v)
            r1 = pd.Series(close).pct_change()
            vol = r1.rolling(20, min_periods=20).std()
            raw_px = r1 / vol
            raw = raw.fillna(raw_px)
            # 90-day return: from prices when 90 bars exist in the window, else the detector's regime
            reg = df["regime"].astype(str).values
            for t in range(n):
                if f[t] == 0:
                    continue
                n_active += 1
                if t >= 90 and close[t - 90] > 0:
                    r90 = close[t] / close[t - 90] - 1.0
                    side = 1 if r90 >= 0 else -1
                else:
                    if reg[t] == "trending":
                        side = 1
                    elif reg[t] == "mean_reversion":
                        side = -1
                    else:
                        side = 0
                rv = raw.iloc[t]
                rise = (not pd.isna(rv)) and rv > 0
                if rise and side != 0 and np.sign(f[t]) == side:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active forecast bars are one-day rises signed long when the 90-day return is >= 0 and short when it is < 0, as the Fidelity's situation and outcome require.",
            "reading": "The 90-day return is recomputed from closes where 90 prior bars exist in the window, else taken from the recorded regime; the rise is the recorded raw component value, else recomputed from prices.",
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean non-overlapping 20-bar return over all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if c[p] > 0 and np.isfinite(c[p]) and np.isfinite(c[p + H]):
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (regime, |forecast|, unusual move)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values
            n = len(df)
            side = 0
            ref = 0.0
            bets = []
            for t in range(n):
                s = int(np.sign(f[t]))
                a = abs(f[t])
                if s == 0:
                    side, ref = 0, 0.0
                    continue
                if s != side:
                    side, ref = s, 0.0
                if a - ref >= BAND:
                    bets.append(t)
                    ref = a
                else:
                    ref = min(ref, a)
            seen = set()
            for t in bets:
                cell = t // H
                if cell in seen:
                    continue
                seen.add(cell)
                if t + H >= n or not (c[t] > 0) or not np.isfinite(c[t + H]):
                    continue
                if reg[t] not in ("trending", "mean_reversion"):
                    continue
                um = c[t + H] / c[t] - 1.0 - drift[coin]
                cases.append((reg[t], abs(f[t]), um))

    tr = np.array([u for r, a, u in cases if r == "trending"])
    mr = np.array([u for r, a, u in cases if r == "mean_reversion"])
    counts = {"trending cases": int(len(tr)), "mean_reversion cases": int(len(mr))}
    reading = ("A case is the first bet (forecast rise of >= 2 points on its side from its lowest level since the last bet) "
               "in each 20-bar cell of a window counted from its first row, grouped by the bar's recorded regime, its move is the raw "
               "20-bar return minus the coin's drift (not signed by direction, as the main measure states), and the median split puts "
               "cases with |forecast| above the median in the larger-rise half.")
    thr = "gap > 0 with Welch t >= 2 (confirm, with supporting check); gap < 0 with Welch t <= -2 (reject)"

    gap = float(tr.mean() - mr.mean()) if len(tr) and len(mr) else None
    tstat = None
    if len(tr) >= 2 and len(mr) >= 2:
        tv = stats.ttest_ind(tr, mr, equal_var=False).statistic
        tstat = float(tv) if np.isfinite(tv) else None

    # supporting check
    sup_val, sup_pass = None, None
    if cases:
        absf = np.array([a for r, a, u in cases])
        med = float(np.median(absf))
        def g(sel):
            t_ = [u for (r, a, u) in sel if r == "trending"]
            m_ = [u for (r, a, u) in sel if r == "mean_reversion"]
            if not t_ or not m_:
                return None
            return float(np.mean(t_) - np.mean(m_))
        big = [x for x in cases if x[1] > med]
        small = [x for x in cases if x[1] <= med]
        gb, gs = g(big), g(small)
        if gb is not None and gs is not None:
            sup_val = float(gb - gs)
            sup_pass = bool(gb > gs)
            counts["larger-rise cases"] = int(len(big))
            counts["smaller-rise cases"] = int(len(small))

    main = {"name": "mean unusual 20-bar move, trending minus mean_reversion",
            "value": gap,
            "statistic": {"name": "Welch t", "value": tstat} if tstat is not None else None,
            "threshold": thr}
    sup = {"name": "gap among larger-rise minus gap among smaller-rise cases (median |forecast| split)",
           "value": sup_val, "passed": sup_pass}
    sc = {"agreement": agreement, "passed": True}

    if len(tr) < 30 or len(mr) < 30:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": sup, "counts": counts,
                "decided_by": "Fewer than 30 cases in at least one group (trending or mean_reversion).",
                "reading": reading}

    if tstat is None or gap is None:
        status, dec = "inconclusive", "The Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif gap > 0 and tstat >= 2 and sup_pass is True:
        status, dec = "confirmed", "The gap is positive with Welch t >= 2 and the larger-rise gap exceeds the smaller-rise gap."
    elif tstat >= 2:
        status, dec = "inconclusive", "Welch t >= 2 but the supporting check fails (the larger-rise gap does not exceed the smaller-rise gap)."
    elif gap < 0 and tstat <= -2:
        status, dec = "rejected", "The gap is negative with Welch t <= -2: after sharp rises, coins down over 90 days do better."
    else:
        status, dec = "inconclusive", "Welch t lies between -2 and 2."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": sup, "counts": counts, "decided_by": dec, "reading": reading}
