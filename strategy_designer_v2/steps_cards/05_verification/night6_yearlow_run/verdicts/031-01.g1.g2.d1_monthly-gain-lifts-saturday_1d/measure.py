import numpy as np
import pandas as pd


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype("float64")
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0.0
        if med > 1e17:
            unit = "ns"
        elif med > 1e14:
            unit = "us"
        elif med > 1e11:
            unit = "ms"
        else:
            unit = "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    LHV = "debug_info.components.gain20.last_history_value"
    PPV = "debug_info.components.gain20.post_pipeline_value"

    n_active = 0
    n_agree = 0
    coin_rets = {}
    case_rows = []

    for coin, wins in bars.items():
        all_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = _to_utc(d["timestamp"]).reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).astype(float)

            # 1-bar return inside the window (next row)
            ret1 = close.shift(-1) / close - 1.0
            all_rets.append(ret1.dropna().values)

            # raw 20-day return: recorded value, else recomputed from prices
            gain_rec = pd.to_numeric(d[LHV], errors="coerce") if LHV in d.columns else pd.Series(np.nan, index=d.index)
            gain_calc = close / close.shift(20) - 1.0
            gain = gain_rec.where(gain_rec.notna(), gain_calc)
            ppv = pd.to_numeric(d[PPV], errors="coerce") if PPV in d.columns else pd.Series(np.nan, index=d.index)

            # bar whose coming bar is a Saturday (UTC): bar opening on Friday
            next_wd = (ts + pd.Timedelta(days=1)).dt.weekday
            situation = (next_wd == 5) & (gain > 0)

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            cases = (next_wd == 5) & (fc > 0) & ret1.notna()
            for i in np.where(cases.values)[0]:
                coin_cases.append({
                    "coin": coin,
                    "day": ts.iloc[i].strftime("%Y-%m-%d"),
                    "f": float(fc.iloc[i]),
                    "ppv": float(ppv.iloc[i]) if pd.notna(ppv.iloc[i]) else np.nan,
                    "ret": float(ret1.iloc[i]),
                })
        allr = np.concatenate(all_rets) if all_rets else np.array([])
        coin_rets[coin] = float(np.mean(allr)) if len(allr) else np.nan
        case_rows.extend(coin_cases)

    threshold = "confirm: weighted mean excess > 0 with t >= 2 and slope > 0; reject: weighted mean excess < 0 with t <= -2; at least 100 cases"
    reading = ("A Friday-close bar is a bar opening on a Friday UTC (its next bar is Saturday); the situation's gain is the recorded "
               "gain20 last_history_value (recomputed from closes if missing) > 0; Saturday's return is the next row's close over this close "
               "inside the window; the coin's mean daily return is the mean of all 1-bar returns over all its windows; the t of the "
               "forecast-weighted mean uses a day-clustered standard error (per day, the sum of forecast x (excess - weighted mean)); "
               "the 100-case minimum counts all cases with a positive forecast and a valid Saturday return across all coins.")

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "forecast-weighted mean Saturday excess return", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Friday-close bars after a positive 20-day return "
                           "with a long forecast, so the config does not do what the plan's Fidelity says."),
            "reading": reading,
        }

    cdf = pd.DataFrame(case_rows, columns=["coin", "day", "f", "ppv", "ret"])
    if len(cdf):
        cdf["mu"] = cdf["coin"].map(coin_rets)
        cdf["x"] = cdf["ret"] - cdf["mu"]
        cdf = cdf[cdf["x"].notna()]
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    m = None
    t = None
    if n_cases > 0 and cdf["f"].sum() > 0:
        W = float(cdf["f"].sum())
        m = float((cdf["f"] * cdf["x"]).sum() / W)
        dev = cdf["f"] * (cdf["x"] - m)
        dsum = dev.groupby(cdf["day"]).sum().values
        G = len(dsum)
        if G > 1:
            var = (G / (G - 1.0)) * float(np.sum(dsum ** 2)) / (W ** 2)
            se = np.sqrt(var)
            t = float(m / se) if se > 0 else None

    slope = None
    sub = cdf[cdf["ppv"].notna()] if n_cases else cdf
    if n_cases and len(sub) >= 2 and np.var(sub["ppv"].values) > 0:
        xv = sub["ppv"].values.astype(float)
        yv = sub["x"].values.astype(float)
        slope = float(np.sum((xv - xv.mean()) * (yv - yv.mean())) / np.sum((xv - xv.mean()) ** 2))
    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < 100:
        status = "not observable"
        decided = f"The plan's minimum of 100 cases (Friday closes after a 20-day gain, all coins together) is not reached: {n_cases} cases."
    elif m is None or t is None:
        status = "inconclusive"
        decided = "The weighted mean excess or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif m > 0 and t >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "The weighted mean excess is positive with t >= 2 and the slope on the forecast is positive (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The weighted mean excess has t >= 2 but the slope on the forecast is at or below 0 (inconclusive rule)."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "The weighted mean excess is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t of the weighted mean excess lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed if agreement is not None else True},
        "main_measure": {
            "name": "forecast-weighted mean Saturday excess return over the coin's mean daily return",
            "value": m,
            "statistic": None if t is None else {"name": "t of the weighted mean, cases of one day summed", "value": t},
            "threshold": threshold,
        },
        "supporting_check": {"name": "least-squares slope of Saturday excess on post_pipeline_value > 0",
                             "value": slope, "passed": slope_pass},
        "counts": {"cases": n_cases, "days": n_days},
        "decided_by": decided,
        "reading": reading,
    }
