import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    rows_check = []
    case_frames = []

    for coin, windows in bars.items():
        coin_rets = []
        per_window = []
        for wname, df in windows.items():
            d = df.copy()
            d = d.sort_values("timestamp").reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            # next-bar return inside the window only
            d["_r1"] = close.shift(-1) / close - 1.0
            coin_rets.append(d["_r1"].dropna().values)
            # 20-day close-to-close return recomputed from prices, inside the window
            ret20 = close / close.shift(20) - 1.0
            regime_tr = (d["regime"].astype(str) == "trending")
            situ = pd.Series(np.where(ret20.notna(), ret20 < 0.0, regime_tr), index=d.index).astype(bool)
            f = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            active = f != 0
            rows_check.append(pd.DataFrame({
                "active": active.values,
                "ok": (active & situ & (f < 0)).values,
            }))
            d["_f"] = f
            d["_coin"] = coin
            per_window.append(d)
        all_r = np.concatenate(coin_rets) if coin_rets else np.array([])
        mu = float(np.mean(all_r)) if all_r.size else np.nan
        for d in per_window:
            sel = (d["regime"].astype(str) == "trending") & (d["_f"] != 0) & d["_r1"].notna()
            c = d.loc[sel, ["timestamp", "_coin", "_f", "_r1"]].copy()
            c["v"] = -(c["_r1"] - mu)
            c["w"] = c["_f"].abs()
            case_frames.append(c)

    chk = pd.concat(rows_check, ignore_index=True) if rows_check else pd.DataFrame({"active": [], "ok": []})
    n_active = int(chk["active"].sum())
    agreement = float(chk["ok"].sum() / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "|forecast|-weighted mean next-day excess fall (short side) on regime bars"
    threshold = "confirm: > 0 with t >= 2; reject: < 0 with t <= -2; else inconclusive; at least 100 case-days"
    reading = ("The situation is the 20-day return below 0 recomputed from closes inside each window "
               "(the recorded regime where fewer than 20 prior bars exist in the window) with a short forecast; "
               "case-days are counted as the (coin, day) cases with a non-zero forecast in the trending regime and a next-day return; "
               "the day-pooled t sums each day's weighted deviations into one cluster with a D/(D-1) correction; "
               "the plan's fewer-than-100 case-days rule is applied as the minimum count giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with a negative 20-day return, "
                           "so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    cases = pd.concat(case_frames, ignore_index=True) if case_frames else pd.DataFrame(columns=["timestamp", "v", "w"])
    cases = cases.dropna(subset=["v", "w"])
    n_cases = int(len(cases))
    cases["day"] = cases["timestamp"].dt.floor("D") if n_cases else []
    n_days = int(cases["day"].nunique()) if n_cases else 0

    value, tstat = None, None
    if n_cases > 0 and cases["w"].sum() > 0:
        W = float(cases["w"].sum())
        m = float((cases["w"] * cases["v"]).sum() / W)
        value = m
        dev = cases["w"] * (cases["v"] - m)
        g = dev.groupby(cases["day"]).sum().values
        D = len(g)
        if D > 1:
            var = (D / (D - 1.0)) * float(np.sum(g ** 2)) / (W ** 2)
            se = np.sqrt(var)
            tstat = float(m / se) if se > 0 else None

    counts = {"case-days": n_cases, "distinct days": n_days, "active bars": n_active}
    stat = {"name": "t of the weighted mean, cases of one day pooled", "value": tstat} if tstat is not None else None
    mm = {"name": main_name, "value": value, "statistic": stat, "threshold": threshold}

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} case-days across all coins and windows, below the plan's minimum of 100."
    elif value is None or tstat is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif value > 0 and tstat >= 2:
        status = "confirmed"
        decided = "The |forecast|-weighted mean excess fall is above 0 with t >= 2 (confirm rule)."
    elif value < 0 and tstat <= -2:
        status = "rejected"
        decided = "The |forecast|-weighted mean excess fall is below 0 with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": mm,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
