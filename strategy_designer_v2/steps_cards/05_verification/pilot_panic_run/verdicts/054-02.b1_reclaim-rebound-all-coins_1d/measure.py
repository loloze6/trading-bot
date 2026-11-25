import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    LHV = "debug_info.components.reclaim.last_history_value"
    PPV = "debug_info.components.reclaim.post_pipeline_value"

    n_active = 0
    n_agree = 0
    cases = []    # dicts: coin, day, ret, ppv
    others = []   # forward returns of the other falling-agitated grid bars
    drift = {}    # coin -> normal 5-bar drift

    for coin, wins in bars.items():
        coin_grid_rets = []
        for wname, df0 in wins.items():
            if df0 is None or len(df0) == 0:
                continue
            df = df0.sort_values("timestamp").reset_index(drop=True)
            n = len(df)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            low = pd.to_numeric(df["low"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).astype(float).values
            reg = df["regime"].astype(str).str.strip().str.lower().values
            lhv = (pd.to_numeric(df[LHV], errors="coerce").values
                   if LHV in df.columns else np.full(n, np.nan))
            ppv = (pd.to_numeric(df[PPV], errors="coerce").values
                   if PPV in df.columns else np.full(n, np.nan))
            ts = pd.to_datetime(df["timestamp"], utc=True)
            days = ts.dt.floor("D").values

            # --- situation: pierce and reclaim of the prior 30-day low, inside the falling-agitated profile
            L = low.shift(1).rolling(30, min_periods=30).min().values
            reclaim = np.where(np.isfinite(L),
                               (low.values < L) & (close.values > L),
                               np.nan_to_num(lhv, nan=0.0) > 0)
            r60 = (close / close.shift(60) - 1.0).values
            falling = np.where(np.isfinite(r60), r60 < -0.10, True)
            in_profile = np.isin(reg, ["mean_reversion", "unknown"]) & falling
            situation = reclaim & in_profile

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            # --- bets: rise of the long forecast of >= BAND from its lowest level since the last bet
            bet = np.zeros(n, dtype=bool)
            base = 0.0
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    base = 0.0
                    continue
                if f - base >= BAND:
                    bet[i] = True
                    base = f
                else:
                    base = min(base, f)

            fwd = (close.shift(-H) / close - 1.0).values
            pos = np.arange(n)
            cell = pos // H

            # coin's normal drift: non-overlapping 5-bar returns on each window's grid
            g = (pos % H == 0) & np.isfinite(fwd)
            coin_grid_rets.extend(fwd[g].tolist())

            # cases: first bet of each grid cell
            case_cells = set()
            seen = set()
            for i in range(n):
                if bet[i] and cell[i] not in seen:
                    seen.add(cell[i])
                    case_cells.add(cell[i])
                    if np.isfinite(fwd[i]):
                        cases.append({"coin": coin, "day": days[i], "ret": float(fwd[i]),
                                      "ppv": float(ppv[i]) if np.isfinite(ppv[i]) else np.nan})

            # other falling-agitated bars on the grid, cells without a case
            for i in range(0, n, H):
                if in_profile[i] and (cell[i] not in case_cells) and np.isfinite(fwd[i]):
                    others.append(float(fwd[i]))
        drift[coin] = float(np.mean(coin_grid_rets)) if coin_grid_rets else np.nan

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "5-day forward return after case bars minus that of the other falling-agitated bars"
    threshold = "confirm: difference > 0 with Welch t >= 2 (and Spearman > 0); reject: difference < 0 with t <= -2"
    reading = ("The falling-agitated profile is taken from the detector's recorded regime (mean_reversion or unknown, "
               "i.e. no veto fired) intersected with a 60-day close return below -10 % where the window allows, because "
               "the 365-day volatility median cannot be rebuilt inside a ~122-bar window; cases are the first long bet "
               "(forecast rise >= 2 from its low since the last bet) in each 5-bar grid cell, others are in-profile grid "
               "bars of cells without a case, and the Welch t uses a day-clustered standard error on the case side.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long reclaim days "
                           "(low under, close above the prior 30-day low) inside the falling-agitated profile."),
            "reading": reading,
        }

    n_cases = len(cases)
    n_days = len(set(c["day"] for c in cases))
    counts = {"cases": n_cases, "distinct days": n_days, "other falling-agitated bars": len(others)}

    # main measure
    value, t = None, None
    if n_cases >= 2 and len(others) >= 2:
        cr = np.array([c["ret"] for c in cases])
        mc = cr.mean()
        dev = pd.Series(cr - mc).groupby(pd.Series([c["day"] for c in cases])).sum().values
        D = len(dev)
        if D >= 2:
            var_c = (dev ** 2).sum() / (n_cases ** 2) * (D / (D - 1.0))
        else:
            var_c = np.nan
        o = np.array(others)
        var_o = o.var(ddof=1) / len(o)
        value = float(mc - o.mean())
        se = np.sqrt(var_c + var_o) if np.isfinite(var_c) else np.nan
        t = float(value / se) if (np.isfinite(se) and se > 0) else None

    # supporting check
    rho, sc_pass = None, None
    xs, ys = [], []
    for c in cases:
        d = drift.get(c["coin"], np.nan)
        if np.isfinite(c["ppv"]) and np.isfinite(d):
            xs.append(c["ppv"])
            ys.append(c["ret"] - d)
    if len(xs) >= 3 and np.std(xs) > 0 and np.std(ys) > 0:
        r = stats.spearmanr(xs, ys).correlation
        if np.isfinite(r):
            rho = float(r)
            sc_pass = bool(rho > 0)
        else:
            sc_pass = False
    else:
        sc_pass = False if n_cases > 0 else None

    main = {"name": main_name, "value": value,
            "statistic": ({"name": "Welch t (cases of a day taken together)", "value": t} if t is not None else None),
            "threshold": threshold}
    support = {"name": "Spearman of reclaim post_pipeline_value vs drift-adjusted 5-day return",
               "value": rho, "passed": sc_pass}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"Minimum count not reached: {n_cases} cases (needs 30) on {n_days} distinct days (needs 20).")
    elif value is None or t is None:
        status = "inconclusive"
        decided = "The difference or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif value > 0 and t >= 2:
        if sc_pass:
            status = "confirmed"
            decided = "The difference is positive with t >= 2 and the supporting Spearman correlation is above 0."
        else:
            status = "inconclusive"
            decided = "The difference is positive with t >= 2 but the supporting correlation is not above 0."
    elif value < 0 and t <= -2:
        status = "rejected"
        decided = "The difference is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or its sign disagrees with the difference), meeting neither rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
