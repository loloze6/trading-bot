import numpy as np
import pandas as pd


def measure(bars):
    FL = "debug_info.components.fall_low.last_history_value"
    RS = "debug_info.components.rise.last_history_value"

    # ---------- per coin drift: mean daily return over all its windows ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            r = (c.shift(-1) / c - 1.0).dropna()
            rets.append(r.values)
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    case_rows = []
    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            fc = d["forecast"].astype(float)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            sma = close.rolling(50, min_periods=50).mean()
            dist = close / sma - 1.0
            prev_ret = close / close.shift(1) - 1.0
            fl = d[FL].astype(float) if FL in d.columns else pd.Series(np.nan, index=d.index)
            rs = d[RS].astype(float) if RS in d.columns else pd.Series(np.nan, index=d.index)

            # side of the 50-day average: recomputed where 50 bars of the window exist, else the detector's decision
            above = pd.Series(np.where(dist.notna(), dist > 0, regime == "mean_reversion"), index=d.index)
            below = pd.Series(np.where(dist.notna(), dist < 0, regime == "chop"), index=d.index)

            # fall reading: recorded raw value > 0, else recomputed sign of the day's fall
            fall_on = pd.Series(np.where(fl.notna(), fl > 0,
                                         np.where(prev_ret.notna(), prev_ret < 0, False)), index=d.index)
            rise_on = pd.Series(np.where(rs.notna(), rs > 0,
                                         np.where(prev_ret.notna(), prev_ret > 0, False)), index=d.index)

            long_sit = above & fall_on & (fc > 0)
            short_sit = below & rise_on & (fc < 0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (long_sit | short_sit)).sum())

            # cases for the criterion
            nxt = close.shift(-1) / close - 1.0
            pos = d["postRebalance_current_allocation"].astype(float)
            for i in np.where(active.values)[0]:
                if pd.isna(nxt.iloc[i]) or pd.isna(pos.iloc[i]) or pd.isna(mu):
                    continue
                adj = float(nxt.iloc[i]) - mu
                case_rows.append((float(pos.iloc[i]) * adj,
                                  float(np.sign(fc.iloc[i])) * adj,
                                  abs(float(fc.iloc[i]))))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    threshold = "confirm if t >= 2 with top-minus-bottom third > 0; reject if t <= -2; else inconclusive; at least 100 cases"
    mm_name = "mean of position held x (next-day return - coin mean daily return), forecast != 0 bars"
    reading = ("Position held is postRebalance_current_allocation; the directional return for the thirds is "
               "sign(forecast) x drift-adjusted next-day return; thirds are equal-count splits of cases ranked by "
               "|forecast| (ties by order); the pool of fewer than 100 cases is treated as the plan's minimum count; "
               "the 50-day side is recomputed within a window where 50 bars exist, otherwise read from the recorded regime.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": len(case_rows)},
            "decided_by": ("Fewer than 90% of bars with forecast != 0 are a fall bar above the 50-day SMA with a long "
                           "forecast or a rise bar below it with a short forecast."),
            "reading": reading,
        }

    n = len(case_rows)
    vals = np.array([r[0] for r in case_rows]) if n else np.array([])
    dirr = np.array([r[1] for r in case_rows]) if n else np.array([])
    absf = np.array([r[2] for r in case_rows]) if n else np.array([])

    mean_v = float(np.mean(vals)) if n else None
    t = None
    if n >= 2:
        sd = float(np.std(vals, ddof=1))
        t = float(mean_v / (sd / np.sqrt(n))) if sd > 0 else 0.0

    diff = None
    sup_pass = None
    if n >= 3:
        order = np.argsort(absf, kind="mergesort")
        parts = np.array_split(order, 3)
        diff = float(np.mean(dirr[parts[2]]) - np.mean(dirr[parts[0]]))
        sup_pass = bool(diff > 0)

    counts = {"cases": int(n)}
    main = {"name": mm_name, "value": mean_v,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": threshold}
    sup = {"name": "top-minus-bottom third of |forecast|, drift-adjusted directional next-day return",
           "value": diff, "passed": sup_pass}

    if n < 100:
        status = "not observable"
        decided = "The pool has fewer than 100 cases, the plan's minimum."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main measure's t is 2 or more and the top-minus-bottom third difference is above 0."
    elif t >= 2:
        status = "inconclusive"
        decided = "The main measure's t is 2 or more but the supporting check fails."
    elif t <= -2:
        status = "rejected"
        decided = "The main measure's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The main measure's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
