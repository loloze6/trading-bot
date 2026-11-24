import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    RISE_COL = "debug_info.components.rise5.last_history_value"

    def prep(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        for c in ["open", "high", "low", "close", "forecast"]:
            d[c] = pd.to_numeric(d[c], errors="coerce")
        return d

    # ---------- 1. situation check ----------
    n_active = 0
    n_active_verifiable = 0
    n_agree = 0
    n_unverifiable = 0

    # ---------- 2. cases ----------
    case_rows = []          # (coin, date, ret10, forecast)
    drift_samples = {}      # coin -> list of grid 10-bar returns

    for coin, wins in bars.items():
        drift_samples.setdefault(coin, [])
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = prep(df)
            n = len(d)
            close = d["close"].values
            opn = d["open"].values
            high = d["high"].values
            low = d["low"].values
            fc = d["forecast"].fillna(0.0).values

            # --- situation from raw values / prices ---
            rise_price = d["close"] / d["close"].shift(5) - 1.0
            if RISE_COL in d.columns:
                rise_rec = pd.to_numeric(d[RISE_COL], errors="coerce")
                rise = rise_rec.where(rise_rec.notna(), rise_price)
            else:
                rise = rise_price
            rng = pd.Series(high - low)
            body_ratio = pd.Series(np.abs(close - opn)) / rng.replace(0, np.nan)
            mean_rng = rng.rolling(20, min_periods=20).mean()
            rmult = rng / mean_rng.replace(0, np.nan)

            c1 = rise.values
            c2 = body_ratio.values
            c3 = rmult.values
            for i in range(n):
                if fc[i] == 0:
                    continue
                n_active += 1
                conds = []
                unknown = False
                for val, test in ((c1[i], lambda v: v > 0.0),
                                  (c2[i], lambda v: v <= 0.1),
                                  (c3[i], lambda v: v >= 1.0)):
                    if val is None or not np.isfinite(val):
                        unknown = True
                    else:
                        conds.append(bool(test(val)))
                if any(c is False for c in conds):
                    in_sit = False
                elif unknown:
                    n_unverifiable += 1
                    continue
                else:
                    in_sit = True
                n_active_verifiable += 1
                if in_sit and fc[i] > 0:
                    n_agree += 1

            # --- drift grid ---
            for p in range(0, n, H):
                if p + H < n and np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] != 0:
                    drift_samples[coin].append(close[p + H] / close[p] - 1.0)

            # --- bets (long side) ---
            ref = 0.0
            bet_idx = []
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    bet_idx.append(i)
                    ref = f
                else:
                    ref = min(ref, f)
            seen_cells = set()
            for i in bet_idx:
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + H < n and np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] != 0:
                    r = close[i + H] / close[i] - 1.0
                    case_rows.append((coin, d["timestamp"].iloc[i].date(), r, float(fc[i])))

    agreement = (n_agree / n_active_verifiable) if n_active_verifiable > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)
    reading = ("Situation agreement is measured on active bars (forecast != 0) where the three rules can be computed "
               "(rise5 from its recorded raw value or else close/close[-5]-1, body |close-open|/(high-low) <= 0.1, "
               "range over the 20-row mean range including the day >= 1), leaving out active bars whose 20-day range "
               "history is not in the window; a case is the first long bet (forecast rise of >= 2 points from its low "
               "since the last bet, from 0 after flat) in each 10-row grid cell of a window, its unusual move is the "
               "10-bar return from its close minus the coin's mean 10-bar return on the non-overlapping grid of all its "
               "windows, the t sums deviations per UTC day (clustered SE with D/(D-1) correction), and the plan's "
               "'fewer than 30 cases' is applied as the minimum count.")

    sit = {"agreement": agreement, "passed": passed}
    thr = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; at least 30 cases"
    mm_name = "mean unusual 10-bar move after a long case (day-pooled)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars verifiable": n_active_verifiable,
                       "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of the active bars are bars where the 5-day return > 0, body <= 10% of range "
                           "and range >= its 20-day mean with a long forecast, so the config does not do what the "
                           "Fidelity's situation says."),
            "reading": reading,
        }

    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in drift_samples.items()}
    cases = pd.DataFrame(case_rows, columns=["coin", "date", "ret", "fc"])
    if len(cases):
        cases["unusual"] = cases["ret"] - cases["coin"].map(drift)
        cases = cases[np.isfinite(cases["unusual"]) & np.isfinite(cases["fc"])]
    n_cases = int(len(cases))
    n_days = int(cases["date"].nunique()) if n_cases else 0

    mean_u = float(cases["unusual"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["unusual"] - mean_u
        day_sums = dev.groupby(cases["date"]).sum().values
        var_mean = (n_days / (n_days - 1)) * np.sum(day_sums ** 2) / (n_cases ** 2)
        if var_mean > 0:
            t_val = float(mean_u / np.sqrt(var_mean))

    slope = None
    if n_cases >= 2:
        x = cases["fc"].values
        y = cases["unusual"].values
        vx = np.sum((x - x.mean()) ** 2)
        if vx > 0:
            slope = float(np.sum((x - x.mean()) * (y - y.mean())) / vx)
    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's 30, so the data cannot show the idea."
    elif t_val is not None and mean_u > 0 and t_val >= 2 and slope_pass:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the slope on the forecast is above 0."
    elif t_val is not None and mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    elif t_val is not None and t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope of the unusual move on the forecast is at or below 0 (or undefined)."
    else:
        status = "inconclusive"
        decided = "|t| < 2 (or t undefined): neither the confirm nor the reject rule is met."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": {"name": mm_name, "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases of one day pooled", "value": t_val}
                                       if t_val is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "OLS slope of unusual move on signal forecast > 0",
                             "value": slope, "passed": slope_pass},
        "counts": {"cases": n_cases, "days": n_days},
        "decided_by": decided,
        "reading": reading,
    }
