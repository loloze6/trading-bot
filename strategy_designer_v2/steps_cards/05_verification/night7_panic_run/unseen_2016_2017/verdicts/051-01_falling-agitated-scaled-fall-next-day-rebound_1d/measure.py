import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.scaled_fall.last_history_value"
    MIN_DAYS = 30

    rows = []          # case rows: day, coin, unusual move, forecast
    n_active = 0
    n_agree = 0

    for coin, windows in bars.items():
        # coin's normal drift: mean 1-bar return over all its windows (never across windows)
        all_rets = []
        for w, df in windows.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                all_rets.append(r[np.isfinite(r)])
        if all_rets:
            allr = np.concatenate(all_rets)
            drift = float(np.mean(allr)) if allr.size else np.nan
        else:
            drift = np.nan

        for w, df in windows.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df[FC], errors="coerce").astype(float)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            raw = (pd.to_numeric(df[RAW], errors="coerce").astype(float)
                   if RAW in df.columns else pd.Series(np.nan, index=df.index))
            prev_ret = close / close.shift(1) - 1.0

            # down day: raw scaled return < 0; where raw is not recorded, the price change
            down = pd.Series(np.where(raw.notna(), raw < 0, prev_ret < 0), index=df.index).astype(bool)
            # falling agitated profile: the detector's vetoes not triggered (regime is not "chop")
            in_profile = (regime != "chop") & (regime != "nan")
            situation = down & in_profile

            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            nxt = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            day = ts.dt.floor("D")
            case = (fc > 0) & nxt.notna() & np.isfinite(nxt) & day.notna()
            if np.isfinite(drift):
                for i in np.where(case.to_numpy())[0]:
                    rows.append((day.iloc[i], coin, float(nxt.iloc[i] - drift), float(fc.iloc[i])))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean next-day unusual move (close[t+1]/close[t]-1 minus coin mean daily return) over bars with forecast > 0"
    thr = "confirm: mean > 0 with t >= 2 and slope > 0 with t >= 2; reject: mean < 0 with t <= -2 or slope < 0 with t <= -2"
    sup_name = "slope of next-day unusual move on forecast (day-pooled t)"

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long on a down day inside the falling agitated profile (regime not chop, negative scaled return), so the config does not do what the Fidelity says.",
            "reading": "The profile is read from the recorded regime (the detector's vetoes give chop outside it) and a down day from a negative raw scaled return (price change where unrecorded).",
        }

    cdf = pd.DataFrame(rows, columns=["day", "coin", "y", "f"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean_val = None
    t_mean = None
    slope = None
    t_slope = None
    if n_cases > 0:
        y = cdf["y"].to_numpy()
        f = cdf["f"].to_numpy()
        m = float(np.mean(y))
        mean_val = m
        D = n_days
        if D > 1:
            S = (cdf.assign(d=y - m).groupby("day")["d"].sum()).to_numpy()
            var_m = np.sum(S ** 2) / (n_cases ** 2) * D / (D - 1)
            se = np.sqrt(var_m)
            t_mean = float(m / se) if se > 0 else None
            fbar = f.mean()
            Sxx = np.sum((f - fbar) ** 2)
            if Sxx > 0:
                b = float(np.sum((f - fbar) * (y - m)) / Sxx)
                a = m - b * fbar
                e = y - a - b * f
                sc = (cdf.assign(s=(f - fbar) * e).groupby("day")["s"].sum()).to_numpy()
                var_b = np.sum(sc ** 2) / (Sxx ** 2) * D / (D - 1)
                seb = np.sqrt(var_b)
                slope = b
                t_slope = float(b / seb) if seb > 0 else None

    sup_pass = None
    if slope is not None and t_slope is not None:
        sup_pass = bool(slope > 0 and t_slope >= 2)

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30."
    else:
        rej_main = mean_val is not None and t_mean is not None and mean_val < 0 and t_mean <= -2
        rej_slope = slope is not None and t_slope is not None and slope < 0 and t_slope <= -2
        conf_main = mean_val is not None and t_mean is not None and mean_val > 0 and t_mean >= 2
        if rej_main or rej_slope:
            status = "rejected"
            decided = ("Reject: the mean unusual move is below 0 with t <= -2." if rej_main
                       else "Reject: the slope on the forecast is negative with t <= -2.")
        elif conf_main and sup_pass:
            status = "confirmed"
            decided = "Confirm: the mean unusual move is above 0 with t >= 2 and the slope is positive with t >= 2."
        else:
            status = "inconclusive"
            decided = ("Inconclusive: the mean unusual move is positive with t >= 2 but the slope is not positive with t >= 2."
                       if conf_main else
                       "Inconclusive: neither the confirm nor the reject rule is met.")

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": (float(mean_val) if mean_val is not None else None),
            "statistic": ({"name": "t of the mean, cases of one day pooled", "value": float(t_mean)}
                          if t_mean is not None else None),
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name,
                             "value": (float(slope) if slope is not None else None),
                             "passed": sup_pass,
                             "t": (float(t_slope) if t_slope is not None else None)},
        "counts": {"cases": n_cases, "distinct case days": n_days},
        "decided_by": decided,
        "reading": ("Cases are every bar with forecast > 0 and a next close in the same window, the drift is the coin's mean 1-bar return over all its windows, "
                    "day pooling uses per-day sums of deviations (mean) or of scores (OLS slope) with a D/(D-1) correction, and the plan's 'fewer than 30 distinct case days' is applied as a minimum count giving 'not observable'."),
    }
