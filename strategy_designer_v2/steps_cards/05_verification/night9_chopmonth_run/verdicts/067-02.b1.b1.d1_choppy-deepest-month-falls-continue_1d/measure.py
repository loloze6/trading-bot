import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    FC = "forecast"
    MF = "debug_info.components.month_fall.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            # choppy regime: 60-day return in percent between -10 and +10, recomputed from prices
            trend60 = (close / close.shift(60) - 1.0) * 100.0
            chop_px = (trend60 >= -10.0) & (trend60 <= 10.0)
            chop_rec = d["regime"].astype(str).eq("chop") if "regime" in d.columns else pd.Series(False, index=d.index)
            chop = chop_px.where(trend60.notna(), chop_rec).astype(bool)
            # 30-day percent change: recorded raw value, else recomputed from prices
            ch30_px = (close / close.shift(30) - 1.0) * 100.0
            if MF in d.columns:
                ch30 = pd.to_numeric(d[MF], errors="coerce").where(
                    pd.to_numeric(d[MF], errors="coerce").notna(), ch30_px)
            else:
                ch30 = ch30_px
            fall = (ch30 < 0).fillna(False)
            active = fc != 0
            ok = active & chop & fall & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The 60-day choppy test is recomputed from closes inside each window (the recorded regime 'chop' is used "
               "on the first 60 bars where it cannot be); the cases of all coins are pooled and ranked by |forecast| "
               "(stable sort), the largest and smallest thirds being the top and bottom floor(n/3) cases; the coin's "
               "drift is the mean of its 7-bar returns on all its windows' non-overlapping grids; the day-clustered t "
               "sums the deviations per UTC day with a G/(G-1) correction.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean drift-adjusted 7-bar short return, largest third of |forecast|",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirms (with positive convexity), t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90 % of active bars are choppy (60-day return within +/-10 %) bars with the close "
                           "below its 30-day-earlier close held short."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    drift = {}
    for coin, wins in bars.items():
        allret = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d[FC], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allret.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    rows.append({"coin": coin, "day": ts.iloc[i].floor("D"), "fc": float(fc[i]), "r": r})
        drift[coin] = float(np.mean(allret)) if allret else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "day", "fc", "r"])
    if len(cases):
        cases["drift"] = cases["coin"].map(drift)
        cases["x"] = -(cases["r"] - cases["drift"])
        cases = cases.dropna(subset=["x"])
        cases["absf"] = cases["fc"].abs()
        cases = cases.sort_values(["absf", "coin", "day"], ascending=[False, True, True],
                                  kind="mergesort").reset_index(drop=True)
    n_all = len(cases)
    k = n_all // 3
    top = cases.iloc[:k] if k > 0 else cases.iloc[0:0]
    bot = cases.iloc[n_all - k:] if k > 0 else cases.iloc[0:0]
    n_top = int(len(top))
    days_top = int(top["day"].nunique()) if n_top else 0

    def clustered_t(df):
        if len(df) < 2:
            return np.nan
        x = df["x"].values
        m = x.mean()
        s = pd.Series(x - m).groupby(df["day"].values).sum().values
        G = len(s)
        if G < 2:
            return np.nan
        var = (s ** 2).sum() / (len(x) ** 2) * G / (G - 1)
        return float(m / np.sqrt(var)) if var > 0 else np.nan

    main_mean = float(top["x"].mean()) if n_top else None
    t_main = clustered_t(top) if n_top else np.nan
    diff = float(top["x"].mean() - bot["x"].mean()) if k > 0 else None
    sup_pass = (diff > 0) if diff is not None else None

    counts = {"negative-forecast cases": int(n_all),
              "cases in the largest third": n_top,
              "distinct days in the largest third": days_top,
              "cases in the smallest third": int(len(bot))}

    if n_top < 30 or days_top < 20:
        status = "not observable"
        decided = (f"The minimum of 30 cases in the largest third on at least 20 distinct days is not reached "
                   f"({n_top} cases, {days_top} days).")
    elif not np.isfinite(t_main):
        status = "inconclusive"
        decided = "The main t cannot be computed, so neither the confirm nor the reject rule is met."
    elif t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main mean has t >= 2 and the largest-minus-smallest third difference is above 0."
    elif t_main >= 2:
        status = "inconclusive"
        decided = "The main t is 2 or more but the supporting difference is 0 or below."
    elif t_main <= -2:
        status = "rejected"
        decided = "The main mean has t <= -2: the deepest falls are followed by rises beyond the coin's drift."
    else:
        status = "inconclusive"
        decided = "The main t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean drift-adjusted 7-bar short return, largest third of |forecast|",
                         "value": main_mean,
                         "statistic": {"name": "t of the mean, clustered by day",
                                       "value": float(t_main) if np.isfinite(t_main) else None},
                         "threshold": "t >= 2 confirms (with positive convexity), t <= -2 rejects"},
        "supporting_check": {"name": "largest-third mean minus smallest-third mean (convexity)",
                             "value": diff, "passed": (bool(sup_pass) if sup_pass is not None else None)},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
