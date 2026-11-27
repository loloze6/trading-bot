import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    FC = "forecast"
    RAW = "debug_info.components.fall30.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0)
            ret60 = (close / close.shift(60) - 1.0) * 100.0
            chop_px = (ret60 >= -10.0) & (ret60 <= 10.0)
            reg_chop = df["regime"].astype(str) == "chop"
            chop = pd.Series(np.where(ret60.notna(), chop_px, reg_chop), index=df.index).astype(bool)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            fall = raw < 0
            situation = chop & fall
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("Chop is recomputed as the 60-day percent return from closes in [-10, +10] where 60 bars of the window "
               "exist, else taken from the recorded regime; the fall is fall30's raw value < 0; the drift is the coin's "
               "mean 10-bar return on the non-overlapping grid of all its windows; the t is the clustered t with "
               "deviations summed per UTC day; the halves are |forecast| below the median (moderate) and at or above it "
               "(deep).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bars in the chop regime "
                           "(60-day return within +/-10 %) after a 30-day fall, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            reg = df["regime"].astype(str).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_all.append(r)
                f = fc[i]
                if reg[i] == "chop" and np.isfinite(f) and f < 0:
                    rows.append({"coin": coin, "day": ts.iloc[i].floor("D"), "f": float(f), "r": float(r)})
        drift = float(np.mean(grid_all)) if grid_all else np.nan
        for row in rows:
            if row["coin"] == coin and "drift" not in row:
                row["drift"] = drift

    cases = pd.DataFrame(rows)
    n_cases = int(len(cases))
    if n_cases > 0:
        cases = cases[np.isfinite(cases["drift"])]
        n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases > 0 else 0

    mm_name = "mean of forecast/10 x (10-bar return - coin drift) over chop short cases"
    mm_thr = "confirm: mean > 0 with t >= 2 (and both halves positive); reject: mean < 0 with t <= -2"
    counts = {"independent case-days": n_days, "cases": n_cases}

    if n_days < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": mm_thr},
            "supporting_check": {"name": "short gain over drift > 0 in both |forecast| halves",
                                 "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_days} independent case-days, fewer than the 30 the plan requires.",
            "reading": reading,
        }

    cases = cases.copy()
    cases["x"] = cases["f"] / 10.0 * (cases["r"] - cases["drift"])
    mean = float(cases["x"].mean())
    dev = cases["x"] - mean
    D = dev.groupby(cases["day"]).sum().values
    K = len(D)
    var = float(np.sum(D ** 2)) * K / (K - 1) if K > 1 else np.nan
    se = np.sqrt(var) / n_cases if np.isfinite(var) else np.nan
    t = float(mean / se) if (np.isfinite(se) and se > 0) else 0.0

    absf = cases["f"].abs()
    med = float(absf.median())
    gain = -(cases["r"] - cases["drift"])
    mod = gain[absf < med]
    deep = gain[absf >= med]
    mod_m = float(mod.mean()) if len(mod) else np.nan
    deep_m = float(deep.mean()) if len(deep) else np.nan
    sup_pass = bool(np.isfinite(mod_m) and np.isfinite(deep_m) and mod_m > 0 and deep_m > 0)
    sup_val = float(min(mod_m, deep_m)) if (np.isfinite(mod_m) and np.isfinite(deep_m)) else None

    if mean > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main mean is above 0 with t >= 2 and the short gain over drift is positive in both halves."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The main mean is below 0 with t <= -2."
    elif mean > 0 and t >= 2:
        status = "inconclusive"
        decided = "The main mean is above 0 with t >= 2 but one |forecast| half is not positive."
    else:
        status = "inconclusive"
        decided = "The t of the main mean lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {"name": mm_name, "value": mean,
                         "statistic": {"name": "t of the mean, cases summed per day", "value": t},
                         "threshold": mm_thr},
        "supporting_check": {"name": "min of mean short gain over drift in moderate and deep |forecast| halves "
                                     f"(moderate {mod_m}, deep {deep_m})",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
