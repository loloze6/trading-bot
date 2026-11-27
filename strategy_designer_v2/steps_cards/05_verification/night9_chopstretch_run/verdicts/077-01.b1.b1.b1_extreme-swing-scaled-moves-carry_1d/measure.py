import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    RAW = "debug_info.components.swing_move.last_history_value"
    reading = ("The choppy calm profile is read from the recorded `regime` column (regime 'unknown' = no veto fired = "
               "the profile, since the detector's 365-day components cannot be rebuilt inside the windows), the "
               "situation's side is the sign of the raw swing-scaled 14-day move, the coin's mean 7-day return is taken "
               "over every window's non-overlapping 7-bar grid, the day-clustered t sums |forecast|-weighted deviations "
               "per UTC day with a D/(D-1) correction, and the thirds are the floor(n/3) cases with the largest and "
               "smallest |forecast|.")

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            active = f != 0
            if not active.any():
                continue
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            in_profile = reg == "unknown"
            raw_ok = np.isfinite(raw) & (raw != 0)
            side_ok = np.sign(np.where(np.isfinite(raw), raw, 0.0)) == np.sign(f)
            good = active & in_profile & raw_ok & side_ok
            n_active += int(active.sum())
            n_agree += int(good.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "|forecast|-weighted mean signed unusual 7-day move"
    main_thr = "above 0 with day-clustered t >= 2 to confirm; below 0 with t <= -2 to reject"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars of the choppy calm profile "
                           "with the forecast signed like the swing-scaled 14-day move (agreement %.3f)." % agreement),
            "reading": reading,
        }

    # ---------- grid returns ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            for i in range(0, len(df) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                rets.append(r)
                if np.isfinite(f[i]) and f[i] != 0 and not pd.isna(ts.iloc[i]):
                    rows.append((coin, ts.iloc[i].strftime("%Y-%m-%d"), float(f[i]), r))
        if rets:
            coin_rets[coin] = float(np.mean(rets))

    if rows:
        cases = pd.DataFrame(rows, columns=["coin", "day", "f", "r"])
        cases["mu"] = cases["coin"].map(coin_rets)
        cases = cases.dropna()
        cases["u"] = np.sign(cases["f"]) * (cases["r"] - cases["mu"])
        cases["w"] = cases["f"].abs()
    else:
        cases = pd.DataFrame(columns=["coin", "day", "f", "r", "mu", "u", "w"])

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "distinct days": n_days}

    if n_cases < 100 or n_days < 60:
        which = []
        if n_cases < 100:
            which.append("fewer than 100 grid cases (%d)" % n_cases)
        if n_days < 60:
            which.append("cases on fewer than 60 distinct days (%d)" % n_days)
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The plan's minimum count is not reached: " + " and ".join(which) + ".",
            "reading": reading,
        }

    u = cases["u"].values.astype(float)
    wt = cases["w"].values.astype(float)
    W = wt.sum()
    m = float((u * wt).sum() / W)
    cases["dev"] = wt * (u - m)
    s = cases.groupby("day")["dev"].sum().values
    D = len(s)
    var = (s ** 2).sum() * (D / (D - 1.0)) / (W ** 2) if D > 1 else np.nan
    se = float(np.sqrt(var)) if np.isfinite(var) else np.nan
    t_main = float(m / se) if (np.isfinite(se) and se > 0) else 0.0

    # ---------- growth check ----------
    srt = cases.sort_values("w", kind="mergesort").reset_index(drop=True)
    k = n_cases // 3
    bottom = srt["u"].values[:k]
    top = srt["u"].values[n_cases - k:]
    if k >= 2:
        t_g = stats.ttest_ind(top, bottom, equal_var=False).statistic
        t_g = float(t_g) if np.isfinite(t_g) else 0.0
        diff = float(np.mean(top) - np.mean(bottom))
        g_pass = bool(diff > 0 and t_g >= 1.0)
    else:
        t_g, diff, g_pass = None, None, None
    counts["top third cases"] = int(k)
    counts["bottom third cases"] = int(k)

    if m > 0 and t_main >= 2:
        if g_pass:
            status = "confirmed"
            decided = "The weighted mean signed unusual move is above 0 with t >= 2 and the growth check passes (Welch t >= 1)."
        else:
            status = "inconclusive"
            decided = "The weighted mean signed unusual move is above 0 with t >= 2 but the growth check fails, which the plan calls inconclusive."
    elif m < 0 and t_main <= -2:
        status = "rejected"
        decided = "The weighted mean signed unusual move is below 0 with t <= -2: the moves reverse."
    else:
        status = "inconclusive"
        decided = "The day-clustered t of the weighted mean signed unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": m,
                         "statistic": {"name": "t, cases of one day together", "value": t_main},
                         "threshold": main_thr},
        "supporting_check": {"name": "top third minus bottom third of |forecast|: mean signed unusual move (Welch t >= 1)",
                             "value": t_g, "passed": g_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
