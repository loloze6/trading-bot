import json
import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    WIDE_MIN, LOC_MIN, MIN_CASES, MIN_DAYS = 2.0, 0.75, 30, 30

    def comp_raw(df, cid):
        col = f"debug_info.components.{cid}.last_history_value"
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        out = pd.Series(np.nan, index=df.index, dtype=float)
        if "debug_info.components" in df.columns:
            vals = []
            for v in df["debug_info.components"].values:
                x = np.nan
                try:
                    d = v
                    if isinstance(d, str):
                        d = json.loads(d)
                    if isinstance(d, dict) and cid in d:
                        e = d[cid]
                        if isinstance(e, dict):
                            x = float(e.get("last_history_value", np.nan))
                except Exception:
                    x = np.nan
                vals.append(x)
            out = pd.Series(vals, index=df.index, dtype=float)
        return out

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    rows = []
    for coin in sorted(bars.keys()):
        wins = bars[coin]
        coin_rets = []
        coin_rows = []
        for w in sorted(wins.keys()):
            df = wins[w].copy().reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ret = close.pct_change()
            std30 = ret.rolling(30).std()
            rng = (high - low)
            wide_px = (rng / close) / std30
            loc_px = (close - low) / rng.replace(0, np.nan)
            wide = comp_raw(df, "width")
            loc = comp_raw(df, "high_close")
            wide = wide.where(wide.notna(), wide_px)
            loc = loc.where(loc.notna(), loc_px)
            situ = (wide >= WIDE_MIN) & (loc >= LOC_MIN)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())

            fwd = close.shift(-1) / close - 1.0
            coin_rets.append(fwd.dropna().values)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            sel = (fc < 0) & fwd.notna()
            for i in np.where(sel.values)[0]:
                coin_rows.append((coin, ts.iloc[i].normalize(), float(fwd.iloc[i]), abs(float(fc.iloc[i]))))
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        mu = float(np.mean(allr)) if allr.size else np.nan
        for (c, d, r, a) in coin_rows:
            rows.append({"coin": c, "day": d, "unusual": -(r - mu), "absf": a})

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)
    reading = ("Situation taken as raw width >= 2.0 and close location >= 0.75 (recorded raw values, recomputed from prices "
               "where missing) with a short forecast; the falling calm profile is added by code and not recomputed (its 365-day "
               "lookback exceeds a window); cases are all bars with forecast < 0 and a next bar in the same window; t of the mean "
               "uses deviations summed per UTC day; the slope's t is the ordinary least-squares t.")
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2, or slope t <= -2"
    mm_name = "mean next-day unusual move, short direction"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of the {n_active} active bars are short bars of the plan's situation "
                           "(range >= 2 return std and close in the top quarter), below 90%."),
            "reading": reading,
        }

    cases = pd.DataFrame(rows)
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_u = float(cases["unusual"].mean()) if n_cases else None
    t_mean = None
    slope = None
    slope_t = None
    if n_cases >= 2:
        dev = cases["unusual"] - mean_u
        g = dev.groupby(cases["day"]).sum()
        G = len(g)
        if G > 1:
            var_mean = float((g ** 2).sum()) / (n_cases ** 2) * G / (G - 1)
            if var_mean > 0:
                t_mean = mean_u / np.sqrt(var_mean)
        if cases["absf"].nunique() > 1 and n_cases >= 3:
            lr = stats.linregress(cases["absf"].values, cases["unusual"].values)
            slope = float(lr.slope)
            slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    main = {"name": mm_name, "value": mean_u,
            "statistic": ({"name": "t of the mean, same-day cases summed", "value": float(t_mean)} if t_mean is not None else None),
            "threshold": threshold}
    supp = {"name": "OLS slope of unusual move on |forecast|", "value": slope,
            "passed": (bool(slope > 0) if slope is not None else None)}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Minimum count not reached: {n_cases} cases and {n_days} distinct days, the plan needs at least 30 of each."
    else:
        conf = (mean_u is not None and t_mean is not None and mean_u > 0 and t_mean >= 2 and slope is not None and slope > 0)
        rej_mean = (mean_u is not None and t_mean is not None and mean_u < 0 and t_mean <= -2)
        rej_slope = (slope_t is not None and slope_t <= -2)
        if conf:
            status = "confirmed"
            decided = "Confirm rule met: mean unusual move above 0 with t >= 2 and the slope on |forecast| above 0."
        elif rej_mean or rej_slope:
            status = "rejected"
            decided = ("Reject rule met: " +
                       ("mean unusual move below 0 with t <= -2" if rej_mean else "") +
                       (" and " if (rej_mean and rej_slope) else "") +
                       ("slope of the unusual move on |forecast| with t <= -2" if rej_slope else "") + ".")
        else:
            status = "inconclusive"
            if mean_u is not None and t_mean is not None and mean_u > 0 and t_mean >= 2:
                decided = "Mean meets the confirm rule but the slope is not above 0, and no reject rule is met: inconclusive."
            else:
                decided = "Neither the confirm rule nor a reject rule is met: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": {**supp, "slope_t": slope_t} if False else supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
