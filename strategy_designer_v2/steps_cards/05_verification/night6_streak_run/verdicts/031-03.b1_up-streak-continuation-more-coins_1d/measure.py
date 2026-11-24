import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.up_streak.last_history_value"

    # ---------- 1. Situation check: today closed higher (up streak n > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(d), np.nan)
            prev = np.r_[np.nan, close[:-1]]
            price_up = close > prev
            sit = np.where(np.isfinite(raw), raw > 0, price_up)
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars that closed higher "
                           "(up-close streak > 0) with a long (positive) forecast, as the Fidelity's situation and side require."),
            "reading": "The situation is an up-close streak length above 0 read from the component's raw value "
                       "(price close above the previous close where the raw value is missing), on the long side.",
        }

    # ---------- 2. Grid returns, coin drift ----------
    grid_rows = []   # (coin, day, forecast, ret)
    coin_grid_rets = {}
    case_rows = []   # (coin, day, signed ret)
    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            days = ts.dt.floor("D").to_numpy()
            n = len(d)
            # grid
            for g in range(0, n - H, H):
                r = close[g + H] / close[g] - 1.0
                if np.isfinite(r):
                    rets_all.append(r)
                    grid_rows.append((coin, days[g], fc[g], r))
            # bets (forecast rises on its side of at least the band)
            low = 0.0
            side = 0
            bet = np.zeros(n, dtype=bool)
            bet_side = np.zeros(n, dtype=int)
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    low, side = 0.0, 0
                    continue
                s = 1 if f > 0 else -1
                if s != side:
                    low, side = 0.0, s
                m = abs(f)
                if m - low >= BAND:
                    bet[i] = True
                    bet_side[i] = s
                    low = m
                else:
                    low = min(low, m)
            # one case per grid cell: first bet in the cell
            for g in range(0, n, H):
                idx = np.where(bet[g:g + H])[0]
                if len(idx) == 0:
                    continue
                i = g + idx[0]
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    case_rows.append((coin, days[i], bet_side[i], r))
        coin_grid_rets[coin] = float(np.mean(rets_all)) if rets_all else np.nan

    G = pd.DataFrame(grid_rows, columns=["coin", "day", "f", "r"])
    G = G[np.isfinite(G["f"]) & np.isfinite(G["r"])].copy()
    G["drift"] = G["coin"].map(coin_grid_rets)
    G["y"] = G["r"] - G["drift"]
    G = G[np.isfinite(G["y"])]

    pos = G[G["f"] > 0]
    n_pos = int(len(pos))
    n_pos_days = int(pos["day"].nunique())

    # ---------- main measure: slope, t with cases of a day pooled (clustered by day) ----------
    slope, t = None, None
    if len(G) > 2:
        x = G["f"].to_numpy(float)
        y = G["y"].to_numpy(float)
        xm = x - x.mean()
        sxx = float((xm ** 2).sum())
        if sxx > 0:
            b = float((xm * (y - y.mean())).sum() / sxx)
            a = y.mean() - b * x.mean()
            e = y - a - b * x
            sc = pd.Series(xm * e).groupby(G["day"].to_numpy()).sum().to_numpy()
            ncl = len(sc)
            N = len(y)
            if ncl > 1:
                corr = (ncl / (ncl - 1.0)) * ((N - 1.0) / (N - 2.0))
                var = corr * float((sc ** 2).sum()) / sxx ** 2
                slope = b
                t = float(b / np.sqrt(var)) if var > 0 else None

    # ---------- supporting check: mean unusual move over cases ----------
    C = pd.DataFrame(case_rows, columns=["coin", "day", "s", "r"])
    if len(C):
        C["drift"] = C["coin"].map(coin_grid_rets)
        C["u"] = C["s"] * (C["r"] - C["drift"])
        C = C[np.isfinite(C["u"])]
    mean_u = float(C["u"].mean()) if len(C) else None
    check_pass = (mean_u is not None) and (mean_u > 0)

    counts = {
        "grid bars with forecast > 0": n_pos,
        "distinct days of grid bars with forecast > 0": n_pos_days,
        "grid bars in regression": int(len(G)),
        "cases (bets on the 5-bar grid)": int(len(C)),
        "days in regression (clusters)": int(G["day"].nunique()) if len(G) else 0,
    }

    if n_pos < 200 or n_pos_days < 100:
        status = "not observable"
        decided = (f"The plan's minimum of 200 grid bars with forecast > 0 on at least 100 distinct days is not reached "
                   f"({n_pos} bars on {n_pos_days} days).")
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and check_pass:
        status = "confirmed"
        decided = "Confirm: the slope has t ≥ +2 and the mean unusual move over the cases is above 0."
    elif t >= 2:
        status = "inconclusive"
        decided = "A slope t ≥ +2 with a mean unusual move at or below 0 is inconclusive."
    elif t <= -2:
        status = "rejected"
        decided = "Reject: the slope has t ≤ −2."
    else:
        status = "inconclusive"
        decided = "The slope's t is between −2 and +2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of demeaned 5-bar forward return on forecast (non-overlapping grid)",
            "value": slope,
            "statistic": {"name": "slope t, cases of one day pooled (day-clustered)", "value": t} if t is not None else None,
            "threshold": "confirm if t ≥ +2 (with the supporting check), reject if t ≤ −2, else inconclusive",
        },
        "supporting_check": {
            "name": "mean unusual 5-bar move over bets on the grid, long direction",
            "value": mean_u,
            "passed": bool(check_pass) if mean_u is not None else None,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The regression uses every grid bar with a 5-bar forward return (forecast 0 included), demeaned by the "
                    "coin's mean grid 5-bar return over all its windows, with the slope's t from standard errors clustered "
                    "by day (residual deviations summed per day); the supporting check's cases are the first forecast rise "
                    "of at least 2 points in each 5-bar grid cell, and the plan's 'else inconclusive' for too few cases is "
                    "reported as 'not observable' as the workflow requires."),
    }
