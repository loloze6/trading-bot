import json
import numpy as np
import pandas as pd


def _component_series(df, comp_id, field="last_history_value"):
    """Read a strategy component's recorded value, flattened or nested; NaN where it is missing."""
    flat = "debug_info.components." + comp_id + "." + field
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        vals = []
        for v in df["debug_info.components"].values:
            out = np.nan
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get(comp_id)
                if isinstance(c, dict):
                    x = c.get(field)
                    try:
                        out = float(x) if x is not None else np.nan
                    except Exception:
                        out = np.nan
            vals.append(out)
        return pd.Series(vals, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def _day_clustered_t(values, days):
    values = np.asarray(values, dtype=float)
    n = len(values)
    if n < 2:
        return None
    m = values.mean()
    dev = pd.Series(values - m).groupby(np.asarray(days)).sum().values
    D = len(dev)
    if D < 2:
        return None
    var = (dev ** 2).sum() * D / (D - 1)
    se = np.sqrt(var) / n
    if not np.isfinite(se) or se == 0:
        return None
    return float(m / se)


def measure(bars):
    total_active = 0
    agree = 0
    cases = []  # (excess_short, loc, day)

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        frames = []
        for w in sorted(wins.keys()):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.copy()
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
                df = df.sort_values("timestamp").reset_index(drop=True)
            frames.append(df)

        # coin's mean daily return over all windows together
        all_r = []
        for df in frames:
            c = pd.to_numeric(df["close"], errors="coerce")
            r = (c.shift(-1) / c - 1.0).dropna()
            all_r.append(r.values)
        allr = np.concatenate(all_r) if all_r else np.array([])
        mu = float(np.mean(allr)) if len(allr) > 0 else np.nan

        for df in frames:
            o = pd.to_numeric(df["open"], errors="coerce")
            h = pd.to_numeric(df["high"], errors="coerce")
            l = pd.to_numeric(df["low"], errors="coerce")
            c = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)

            rng = h - l
            loc_calc = ((c - l) / rng).where(rng > 0)
            loc_rec = _component_series(df, "high_close", "last_history_value")
            loc = loc_rec.where(loc_rec.notna(), loc_calc)

            ret = c / c.shift(1) - 1.0
            sd = ret.rolling(30, min_periods=30).std(ddof=1)
            width = ((h - l) / c) / sd.where(sd > 0)

            in_regime = regime == "mean_reversion"
            width_ok = (width >= 2.0) | width.isna()
            situation = in_regime & (loc >= 0.75) & width_ok

            active = fc != 0
            total_active += int(active.sum())
            agree += int((active & situation & (fc < 0)).sum())

            fwd = c.shift(-1) / c - 1.0
            if "timestamp" in df.columns:
                days = df["timestamp"].dt.floor("D").astype(str)
            else:
                days = pd.Series(np.arange(len(df)).astype(str), index=df.index)
            mask = (fc < 0) & fwd.notna()
            for i in df.index[mask]:
                if not np.isfinite(mu):
                    continue
                ex = -(float(fwd[i]) - mu)
                cases.append((ex, float(loc[i]) if pd.notna(loc[i]) else np.nan, days[i]))

    agreement = float(agree) / total_active if total_active > 0 else 0.0
    passed = total_active > 0 and agreement >= 0.9
    sit = {"agreement": agreement, "passed": bool(passed)}
    main_name = "next-day short-direction return minus the coin's mean daily return, over cases with forecast below 0"
    thr = "confirm: mean above 0 with day-grouped t >= 2 and check passes; reject: mean below 0 with t <= -2"
    reading = ("The profile (60-bar fall and 365-bar volatility percentile, unrecorded and needing history before each window) "
               "is read from regime == mean_reversion, width is recomputed from prices where 30 past returns exist in the window "
               "(else taken as met by the regime), the t sums case deviations per UTC day, and the median split puts locations "
               "above the median in the upper half; fewer than 50 cases or days gives not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(total_active), "active bars in situation on short side": int(agree)},
            "decided_by": ("Fewer than 90 percent of active bars are falling-calm days with range at least 2 usual moves "
                           "and close in the top quarter, forecast short: agreement " + str(round(agreement, 4)) + "."),
            "reading": reading,
        }

    ex = np.array([x[0] for x in cases], dtype=float)
    locs = np.array([x[1] for x in cases], dtype=float)
    days = [x[2] for x in cases]
    n_cases = int(len(ex))
    n_days = int(len(set(days)))
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_ex = float(ex.mean()) if n_cases > 0 else None
    t = _day_clustered_t(ex, days) if n_cases > 1 else None

    sup_val = None
    sup_pass = None
    ok = ~np.isnan(locs)
    if ok.sum() >= 2:
        med = float(np.median(locs[ok]))
        up = ex[ok][locs[ok] > med]
        lo = ex[ok][locs[ok] <= med]
        if len(up) > 0 and len(lo) > 0:
            sup_val = float(up.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)

    main = {"name": main_name, "value": mean_ex,
            "statistic": ({"name": "t of the mean, cases grouped by day", "value": t} if t is not None else None),
            "threshold": thr}
    sup = {"name": "upper-half minus lower-half excess return, split at median close location",
           "value": sup_val, "passed": sup_pass}

    if n_cases < 50 or n_days < 50:
        status = "not observable"
        decided = ("The plan's minimum of 50 cases on 50 distinct days is not reached (" + str(n_cases) +
                   " cases, " + str(n_days) + " days).")
    elif t is None or mean_ex is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_ex > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean is above 0 with t >= 2 and the upper half beats the lower half: confirm rule."
        else:
            status = "inconclusive"
            decided = "A confirming t with a failed supporting check is inconclusive by the plan."
    elif mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "The mean is below 0 with t <= -2: reject rule."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2: inconclusive rule."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
