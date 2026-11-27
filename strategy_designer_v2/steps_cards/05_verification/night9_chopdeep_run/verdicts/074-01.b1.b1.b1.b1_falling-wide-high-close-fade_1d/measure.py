import numpy as np
import pandas as pd
from scipy import stats


def _to_day(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        unit = "ms" if np.nanmedian(np.abs(v.values)) > 1e11 else "s"
        d = pd.to_datetime(v, unit=unit, utc=True)
    else:
        d = pd.to_datetime(s, utc=True)
    return d.dt.floor("D").dt.strftime("%Y-%m-%d").values


def measure(bars):
    W_COL = "debug_info.components.width.last_history_value"
    L_COL = "debug_info.components.loc.last_history_value"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    frames = []
    for coin, wins in bars.items():
        for wname, df0 in wins.items():
            df = df0.copy().reset_index(drop=True)
            if len(df) == 0:
                continue
            o = df["close"].astype(float)
            h = df["high"].astype(float)
            l = df["low"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            rng = h - l

            up = o / o.shift(1) - 1.0
            width_calc = rng / rng.rolling(20, min_periods=20).mean()
            loc_calc = (o - l) / rng.replace(0, np.nan)
            width = width_calc.copy()
            loc = loc_calc.copy()
            if W_COL in df.columns:
                wr = pd.to_numeric(df[W_COL], errors="coerce")
                width = wr.where(wr.notna(), width_calc)
            if L_COL in df.columns:
                lr = pd.to_numeric(df[L_COL], errors="coerce")
                loc = lr.where(lr.notna(), loc_calc)
            trend = (o / o.shift(60) - 1.0) * 100.0

            computable = up.notna() & width.notna() & loc.notna() & trend.notna()
            situ = (up > 0) & (width > 1.0) & (loc >= 0.75) & (trend < -10.0)
            active = fc != 0
            act_c = active & computable
            n_active += int(act_c.sum())
            n_active_uncomputable += int((active & ~computable).sum())
            n_agree += int((act_c & situ & (fc < 0)).sum())

            # forward 1-bar return inside window
            r1 = o.shift(-1) / o - 1.0
            frames.append(pd.DataFrame({
                "coin": coin,
                "window": wname,
                "day": _to_day(df["timestamp"]),
                "forecast": fc.values,
                "r1": r1.values,
            }))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation computed per window from prices and the recorded raw width/loc values: up = close above prior close, "
               "width > 1, close location >= 0.75, falling = 60-bar price change below -10 % (the veto's threshold read in percent), "
               "active bars whose conditions cannot be computed inside the window (first bar, first 60 bars) are left out of the share; "
               "the horizon grid is every bar (h = 1), drift is the coin's mean 1-bar return over all its windows, t clusters cases by UTC day "
               "(deviations summed per day, D/(D-1) correction), the slope is OLS of next-day excess return on forecast, and the plan's "
               "'fewer than 30 case days' is treated as the minimum count (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active,
                       "active bars not computable": n_active_uncomputable},
            "decided_by": ("Fewer than 90 % of the active bars are short bars of the plan's situation (up day, range above its "
                           "20-day mean, close in the top quarter, 60-bar fall beyond -10 %): the config's forecast does not "
                           "follow the Fidelity's situation and side."),
            "reading": reading,
        }

    allb = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(
        columns=["coin", "window", "day", "forecast", "r1"])
    drift = allb.dropna(subset=["r1"]).groupby("coin")["r1"].mean()
    allb["drift"] = allb["coin"].map(drift)
    cases = allb[(allb["forecast"] < 0) & allb["r1"].notna() & allb["drift"].notna()].copy()
    cases["excess"] = cases["r1"] - cases["drift"]
    cases["short_ex"] = -cases["excess"]

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_v = float(cases["short_ex"].mean()) if n_cases else None
    t_v = None
    if n_cases > 0 and n_days > 1:
        dev = cases["short_ex"] - mean_v
        s_d = dev.groupby(cases["day"]).sum()
        var_mean = (s_d ** 2).sum() / (n_cases ** 2) * (n_days / (n_days - 1))
        if var_mean > 0:
            t_v = float(mean_v / np.sqrt(var_mean))

    slope = None
    if n_cases >= 3 and cases["forecast"].nunique() > 1:
        slope = float(stats.linregress(cases["forecast"].values, cases["excess"].values).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"case days": n_days, "cases": n_cases}
    main = {
        "name": "mean next-day short-direction return beyond drift on case bars",
        "value": mean_v,
        "statistic": None if t_v is None else {"name": "t of the mean, cases grouped by day", "value": t_v},
        "threshold": "confirm: mean > 0 with t >= 2 and positive slope; reject: mean < 0 with t <= -2",
    }
    supp = {"name": "slope of next-day excess return on forecast", "value": slope, "passed": slope_pass}
    sc = {"agreement": agreement, "passed": True}

    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 case days across all coins and windows ({n_days})."
    elif t_v is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_v > 0 and t_v >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "The mean short-direction excess return is above 0 with t >= 2 and the supporting slope is positive."
        else:
            status = "inconclusive"
            decided = "A confirming mean (t >= 2) with a non-positive supporting slope is inconclusive by the plan."
    elif mean_v < 0 and t_v <= -2:
        status = "rejected"
        decided = "The mean short-direction excess return is below 0 with t <= -2: these days are followed by rises beyond drift."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
