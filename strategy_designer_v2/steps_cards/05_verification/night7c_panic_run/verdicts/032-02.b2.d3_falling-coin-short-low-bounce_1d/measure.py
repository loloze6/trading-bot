import numpy as np
import pandas as pd


def measure(bars):
    LH = "debug_info.components.break_depth.last_history_value"
    PP = "debug_info.components.break_depth.post_pipeline_value"
    POS = "postRebalance_current_allocation"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_unchecked = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            low = d["low"].astype(float)
            ret30 = close / close.shift(30) - 1.0
            prior_low10 = low.shift(1).rolling(10, min_periods=10).min()
            low10 = close / prior_low10 - 1.0
            if LH in d.columns:
                low10 = low10.fillna(pd.to_numeric(d[LH], errors="coerce"))
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            known = ret30.notna() & low10.notna()
            sit = (ret30 < 0) & (low10 < 0)
            ok = active & known & sit & (fc > 0)
            n_active += int((active & known).sum())
            n_agree += int(ok.sum())
            n_active_unchecked += int((active & ~known).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation recomputed from prices inside each window (30-bar close-to-close return < 0, close below "
               "the minimum low of the 10 prior bars, falling back to the recorded break_depth raw value), active "
               "bars whose 30-bar return cannot be computed inside the window are left out of the agreement; cases "
               "are bars with a held position > 0, the coin's mean is the mean next-bar return over all its windows, "
               "the weighted mean's t clusters cases by UTC day (weighted deviations summed per day), and the slope is "
               "an unweighted least-squares fit over cases with a recorded post_pipeline_value.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active},
            "decided_by": ("Fewer than 90% of the active bars are long bars where the 30-day return is below 0 and "
                           "the close is below the prior 10-day low, as the plan's Fidelity states."
                           if agreement is not None else "No active bar could be checked against the situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        per_win = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            r = close.shift(-1) / close - 1.0
            coin_rets.append(r.dropna())
            per_win.append((d, r))
        allr = pd.concat(coin_rets) if coin_rets else pd.Series(dtype=float)
        if len(allr) == 0:
            continue
        mu = float(allr.mean())
        for d, r in per_win:
            pos = pd.to_numeric(d[POS], errors="coerce")
            pp = pd.to_numeric(d[PP], errors="coerce") if PP in d.columns else pd.Series(np.nan, index=d.index)
            m = (pos > 0) & r.notna()
            for i in np.where(m.values)[0]:
                rows.append({
                    "day": pd.Timestamp(d["timestamp"].iloc[i]).floor("D") if not isinstance(d["timestamp"].iloc[i], (int, float, np.integer, np.floating))
                    else pd.to_datetime(d["timestamp"].iloc[i], unit="ms" if d["timestamp"].iloc[i] > 1e11 else "s").floor("D"),
                    "w": float(pos.iloc[i]),
                    "e": float(r.iloc[i] - mu),
                    "pp": float(pp.iloc[i]) if pd.notna(pp.iloc[i]) else np.nan,
                })
    cases = pd.DataFrame(rows, columns=["day", "w", "e", "pp"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    wmean = None
    t = None
    if n_cases > 0 and cases["w"].sum() > 0:
        W = cases["w"].sum()
        wmean = float((cases["w"] * cases["e"]).sum() / W)
        dev = cases["w"] * (cases["e"] - wmean)
        s = dev.groupby(cases["day"]).sum()
        D = len(s)
        if D > 1:
            var = (D / (D - 1)) * float((s ** 2).sum()) / (W ** 2)
            se = np.sqrt(var)
            t = float(wmean / se) if se > 0 else None

    slope = None
    sc = cases.dropna(subset=["pp"])
    if len(sc) >= 2 and sc["pp"].var() > 0:
        x = sc["pp"].values
        y = sc["e"].values
        slope = float(np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2))
    slope_pass = None if slope is None else bool(slope > 0)

    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases (distinct days) across all coins and windows: {n_days}."
    elif wmean is None or t is None:
        status = "inconclusive"
        decided = "The weighted mean excess or its t could not be computed."
    elif wmean > 0 and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "The weighted mean excess is above 0 with t >= 2 and the slope on break depth is positive."
    elif wmean < 0 and t <= -2:
        status = "rejected"
        decided = "The weighted mean excess is below 0 with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope on break depth is at or below 0 (or not computable): inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the weighted mean excess lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "position-weighted mean next-day excess return over the coin's mean",
            "value": wmean,
            "statistic": {"name": "t of weighted mean, cases clustered by day", "value": t} if t is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "OLS slope of next-day excess on break_depth post_pipeline_value > 0",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": {"cases (distinct days)": n_days, "cases (bars)": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
