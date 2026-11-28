import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    BAND = 2.0
    RAW_RISE = "debug_info.components.scaled_rise.last_history_value"
    RAW_DEPTH = "debug_info.components.depth_below_high.last_history_value"

    def prep(df):
        df = df.sort_values("timestamp").reset_index(drop=True).copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df["forecast"] = pd.to_numeric(df["forecast"], errors="coerce")
        return df

    data = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            data[(coin, w)] = prep(df)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for (coin, w), df in data.items():
        c = df["close"]
        rise_p = c / c.shift(H) - 1.0
        high30 = c.rolling(30, min_periods=1).max()
        dist_p = c / high30 - 1.0
        rise_r = pd.to_numeric(df[RAW_RISE], errors="coerce") if RAW_RISE in df else pd.Series(np.nan, index=df.index)
        dist_r = pd.to_numeric(df[RAW_DEPTH], errors="coerce") if RAW_DEPTH in df else pd.Series(np.nan, index=df.index)
        rise = rise_r.where(rise_r.notna(), rise_p)
        dist = dist_r.where(dist_r.notna(), dist_p)
        f = df["forecast"]
        active = f.notna() & (f != 0)
        situ = (rise > 0) & (dist < 0)
        n_active += int(active.sum())
        n_agree += int((active & situ & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean unusual 7-bar move after long bets", "value": None,
                             "statistic": None, "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are bars with a positive 7-day return and a close below its 30-day high on the long side, so the config does not do what the plan's Fidelity says.",
            "reading": "The situation is read from the recorded raw values of scaled_rise (sign of the 7-day return) and depth_below_high, falling back to prices where not recorded; the profile is not part of the situation check.",
        }

    # ---------- 2. coin's mean 7-bar return over all windows ----------
    coin_rets = {}
    for (coin, w), df in data.items():
        c = df["close"].values
        rets = []
        for t in range(0, len(c), H):
            if t + H < len(c) and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0:
                rets.append(c[t + H] / c[t] - 1.0)
        coin_rets.setdefault(coin, []).extend(rets)
    coin_mean = {k: (float(np.mean(v)) if len(v) else np.nan) for k, v in coin_rets.items()}

    # ---------- 3. bets and cases ----------
    cases = []  # (day, unusual move)
    grid_pos = []  # (forecast, unusual move)
    for (coin, w), df in data.items():
        c = df["close"].values
        f = df["forecast"].fillna(0.0).values
        n = len(df)
        drift = coin_mean.get(coin, np.nan)
        if not np.isfinite(drift):
            continue
        # bets: rise of the long forecast of >= BAND from its lowest level since last bet
        bet = np.zeros(n, dtype=bool)
        ref = 0.0
        for i in range(n):
            if f[i] <= 0:
                ref = 0.0
                continue
            if f[i] - ref >= BAND:
                bet[i] = True
                ref = f[i]
            else:
                ref = min(ref, f[i])
        for start in range(0, n, H):
            idx = [i for i in range(start, min(start + H, n)) if bet[i]]
            if idx:
                t = idx[0]
                if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0:
                    u = c[t + H] / c[t] - 1.0 - drift
                    cases.append((df["timestamp"].iloc[t].normalize(), u))
            # grid bar for the supporting check
            if f[start] > 0 and start + H < n and np.isfinite(c[start]) and np.isfinite(c[start + H]) and c[start] > 0:
                grid_pos.append((f[start], c[start + H] / c[start] - 1.0 - drift))

    n_cases = len(cases)
    mean_u = None
    t_stat = None
    n_days = 0
    if n_cases > 0:
        cdf = pd.DataFrame(cases, columns=["day", "u"])
        mean_u = float(cdf["u"].mean())
        cdf["e"] = cdf["u"] - mean_u
        e_day = cdf.groupby("day")["e"].sum().values
        n_days = len(e_day)
        if n_days > 1:
            var = (e_day ** 2).sum() / (n_cases ** 2) * n_days / (n_days - 1)
            se = np.sqrt(var)
            t_stat = float(mean_u / se) if se > 0 else None

    # ---------- 4. supporting check ----------
    sup_val = None
    sup_pass = None
    if len(grid_pos) > 0:
        g = pd.DataFrame(grid_pos, columns=["f", "u"])
        med = g["f"].median()
        hi = g.loc[g["f"] > med, "u"]
        lo = g.loc[g["f"] < med, "u"]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False
    else:
        sup_pass = False

    # ---------- 5. decision ----------
    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases (independent days): {n_days} days, so the data could not show the idea."
    elif mean_u is not None and t_stat is not None and mean_u > 0 and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the supporting check passes (confirm rule)."
    elif mean_u is not None and t_stat is not None and mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2 (reject rule)."
    elif mean_u is not None and t_stat is not None and mean_u > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean unusual 7-bar move after long bets",
            "value": mean_u,
            "statistic": {"name": "t of the mean, cases grouped by day", "value": t_stat} if t_stat is not None else None,
            "threshold": "mean > 0 with t >= 2 (and the supporting check) to confirm; mean < 0 with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "mean unusual move above-median forecast minus below-median, grid bars with forecast > 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "independent days": n_days, "grid bars with forecast above 0": len(grid_pos)},
        "decided_by": decided,
        "reading": "One case per 7-bar grid cell (the cell's first long bet, a forecast rise of at least 2 from its lowest level since the last bet), its return taken from that bet's close over 7 bars inside the window minus the coin's mean grid 7-bar return over all windows; the day-grouped t is the clustered t of the mean; the supporting check uses the grid bars themselves with ties at the median left out; the 30-case minimum is counted in independent days and, per the workflow, gives 'not observable'.",
    }
