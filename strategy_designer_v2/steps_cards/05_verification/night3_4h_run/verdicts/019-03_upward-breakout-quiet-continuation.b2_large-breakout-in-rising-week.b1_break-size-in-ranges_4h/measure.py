import numpy as np
import pandas as pd


def measure(bars):
    H = 18
    BAND = 2.0
    LHV = "debug_info.components.break.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncheckable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            high = df["high"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            lhv = df[LHV].astype(float).values if LHV in df.columns else np.full(n, np.nan)
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                # 42-bar return from prices, inside the window only
                if t < 42 or not (np.isfinite(close[t]) and np.isfinite(close[t - 42]) and close[t - 42] != 0):
                    n_active_uncheckable += 1
                    continue
                week_up = close[t] / close[t - 42] - 1.0 > 0.0
                # break: raw component value if recorded, else from prices
                if np.isfinite(lhv[t]):
                    brk = lhv[t] > 0.0
                elif t >= 12:
                    brk = close[t] > np.nanmax(high[t - 12:t])
                else:
                    n_active_uncheckable += 1
                    continue
                n_active += 1
                if week_up and brk and f > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90
    reading_sit = ("situation = close above the prior-12-bar high (raw break > 0, or from prices where not recorded) "
                   "and 42-bar close-to-close return > 0 inside the window, side long; active bars whose 42-bar "
                   "return cannot be computed inside the window are left out of the agreement")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement) if agreement is not None else None, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active), "active bars not checkable": int(n_active_uncheckable)},
            "decided_by": ("fewer than 90% of the active bars (forecast != 0) are long bars where the close breaks "
                           "above the prior 12-bar high while the 42-bar return is positive"),
            "reading": reading_sit,
        }

    # ---------- 2. Drift per coin (non-overlapping 18-bar grid) ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. Cases: bets, first per 18-bar grid cell ----------
    excess = []
    sizes = []
    for coin, wins in bars.items():
        if not np.isfinite(drift[coin]):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            lhv = df[LHV].astype(float).values if LHV in df.columns else np.full(n, np.nan)
            low = 0.0
            on_long = False
            bets = []
            for t in range(n):
                f = fc[t] if np.isfinite(fc[t]) else 0.0
                if f > 0:
                    if not on_long:
                        on_long = True
                        low = 0.0
                    if f - low >= BAND:
                        bets.append(t)
                        low = f
                    else:
                        low = min(low, f)
                else:
                    on_long = False
                    low = 0.0
            used_cells = set()
            for t in bets:
                cell = t // H
                if cell in used_cells:
                    continue
                used_cells.add(cell)
                if t + H >= n or not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] == 0:
                    continue
                r = c[t + H] / c[t] - 1.0
                excess.append(r - drift[coin])
                sizes.append(lhv[t])

    excess = np.array(excess, dtype=float)
    sizes = np.array(sizes, dtype=float)
    n_cases = int(len(excess))
    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    if n_cases > 1:
        sd = float(np.std(excess, ddof=1))
        t_stat = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None
    else:
        t_stat = None

    ok = np.isfinite(sizes)
    large = excess[ok & (sizes >= 1.0)]
    small = excess[ok & (sizes < 1.0)]
    if len(large) > 0 and len(small) > 0:
        supp_val = float(np.mean(large) - np.mean(small))
        supp_pass = bool(supp_val > 0)
    else:
        supp_val = None
        supp_pass = None

    counts = {"independent cases": n_cases,
              "large-break cases": int(len(large)),
              "small-break cases": int(len(small))}

    if n_cases < 30:
        status = "not observable"
        decided = f"only {n_cases} independent cases over all coins, below the plan's minimum of 30"
    elif t_stat is not None and mean_ex > 0 and t_stat >= 2:
        if supp_pass:
            status = "confirmed"
            decided = "mean excess return above 0 with t >= 2 and large-minus-small break difference above 0"
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check (large minus small breaks) is at or below 0 or not measurable"
    elif t_stat is not None and mean_ex < 0 and t_stat <= -2:
        status = "rejected"
        decided = "mean excess return below 0 with t <= -2"
    else:
        status = "inconclusive"
        decided = "t of the mean excess return lies between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean 18-bar excess return over coin drift per case, before costs",
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t_stat} if t_stat is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "mean excess of breaks >= 1 range minus breaks < 1 range",
            "value": supp_val,
            "passed": supp_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": (reading_sit + "; a case is the first bet (forecast rise >= 2 from its lowest long level since the "
                    "last bet, reset after flat) in each 18-bar grid cell from the window's first row, with its "
                    "18-bar return inside the window minus the coin's mean non-overlapping 18-bar return over all "
                    "windows, and the break size is the raw last_history_value on the signal bar"),
    }
