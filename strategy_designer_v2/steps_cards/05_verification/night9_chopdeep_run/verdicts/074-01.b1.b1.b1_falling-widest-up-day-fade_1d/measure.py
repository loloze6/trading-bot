import numpy as np
import pandas as pd


def measure(bars):
    RM = "debug_info.components.range_multiple.last_history_value"
    BAND = 2.0
    EPS = 1e-9

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    case_rows = []
    drift = {}

    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            all_rets.append((close.shift(-1) / close - 1.0).dropna().values)
        allr = np.concatenate(all_rets) if all_rets else np.array([])
        drift[coin] = float(np.mean(allr)) if allr.size else np.nan

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            high = df["high"].astype(float)
            low = df["low"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)
            rng = high - low
            width_calc = rng / rng.rolling(20, min_periods=20).mean()
            if RM in df.columns:
                width = pd.to_numeric(df[RM], errors="coerce").combine_first(width_calc)
            else:
                width = width_calc
            ret1 = close / close.shift(1) - 1.0

            known = ret1.notna() & width.notna()
            situ = (ret1 > 0) & (width >= 1.0 - EPS)
            active = (fc != 0) & known
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())

            # ---------- cases: short bets on mean_reversion bars ----------
            nxt = close.shift(-1) / close - 1.0
            lowest = 0.0
            side = 0
            for i in range(len(df)):
                f = fc.iloc[i]
                s = np.sign(f)
                if s == 0:
                    lowest, side = 0.0, 0
                    continue
                if s != side:
                    lowest, side = 0.0, s
                mag = abs(f)
                is_bet = mag - lowest >= BAND
                if is_bet:
                    lowest = mag
                else:
                    lowest = min(lowest, mag)
                if (is_bet and s < 0 and df["regime"].iloc[i] == "mean_reversion"
                        and pd.notna(nxt.iloc[i])):
                    rmv = pd.to_numeric(df[RM].iloc[i], errors="coerce") if RM in df.columns else np.nan
                    case_rows.append({
                        "day": pd.Timestamp(df["timestamp"].iloc[i]).tz_localize(None).normalize()
                        if pd.Timestamp(df["timestamp"].iloc[i]).tzinfo else
                        pd.Timestamp(df["timestamp"].iloc[i]).normalize(),
                        "u": -(float(nxt.iloc[i]) - drift[coin]),
                        "rm": float(rmv) if pd.notna(rmv) else np.nan,
                    })

    agreement = n_agree / n_active if n_active else 0.0
    passed = agreement >= 0.9
    reading = ("Situation computed as close above prior close with range multiple >= 1 (recorded value where "
               "present, else recomputed), bars where it cannot be computed left out of the agreement; cases are "
               "short bets (forecast rising >= 2 points on the short side) on mean_reversion bars with a next bar "
               "in the window; the wider half is cases above the median range multiple, the narrower half at or "
               "below it; fewer than the plan's minimum counts is reported as not observable.")
    threshold = "mean > 0 with t >= 2 confirms (with wider half beating narrower half); t <= -2 rejects"
    mm_name = "mean short-direction next-bar unusual move (return minus drift)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars are short bars on up days with range at or above "
                           "the 20-bar mean range, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["day", "u", "rm"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_u = float(cases["u"].mean()) if n_cases else None
    t = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["u"] - mean_u
        D = dev.groupby(cases["day"]).sum()
        K = len(D)
        var = float((D ** 2).sum()) * K / (K - 1)
        se = np.sqrt(var) / n_cases
        t = float(mean_u / se) if se > 0 else None

    sup_val, sup_pass = None, None
    c2 = cases.dropna(subset=["rm"])
    if len(c2) >= 2:
        med = c2["rm"].median()
        wide = c2.loc[c2["rm"] > med, "u"]
        narrow = c2.loc[c2["rm"] <= med, "u"]
        if len(wide) and len(narrow):
            sup_val = float(wide.mean() - narrow.mean())
            sup_pass = bool(sup_val > 0)

    main = {"name": mm_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases summed per day", "value": t} if t is not None else None,
            "threshold": threshold}
    sup = {"name": "wider-half minus narrower-half mean unusual move (median split of range_multiple)",
           "value": sup_val, "passed": sup_pass}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = f"The plan's minimum of 30 cases on 30 distinct days is not reached ({n_cases} cases, {n_days} days)."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean short-direction unusual move is above 0 with t >= 2 and the wider half beats the narrower half."
        else:
            status = "inconclusive"
            decided = "The mean meets the confirm rule (above 0, t >= 2) but the width check fails, which the plan calls inconclusive."
    elif t <= -2:
        status = "rejected"
        decided = "The mean short-direction unusual move has t <= -2: wide up days are followed by a rise beyond drift."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or the mean is not above 0), meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
