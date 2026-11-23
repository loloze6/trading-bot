import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 12
    P, B = 48, 120
    COMP = "debug_info.components.wkmove.last_history_value"

    # ---------- coin mean 12-bar return over all windows (non-overlapping grid) ----------
    coin_drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].to_numpy(dtype=float)
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                rets.append(r[np.isfinite(r)])
        rets = np.concatenate(rets) if rets else np.array([])
        coin_drift[coin] = float(np.mean(rets)) if len(rets) else np.nan

    # ---------- situation check and cases ----------
    n_active = 0
    n_agree = 0
    case_signed = []
    case_absf = []

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            close = df["close"].to_numpy(dtype=float)
            vol = df["volume"].astype(float)
            fc = df["forecast"].astype(float).to_numpy()
            n = len(df)

            # situation: bar stamped Sunday 23:00 UTC (its close is Sunday's last close)
            is_sun23 = ((ts.dt.weekday == 6) & (ts.dt.hour == 23)).to_numpy()

            # weekend (last 48 bars) over the 120 bars before them, from the prices' volume
            recent = vol.rolling(P, min_periods=P).mean()
            prior = vol.shift(P).rolling(B, min_periods=B).mean()
            vr = (recent / prior).to_numpy()
            regime_tr = (df["regime"].astype(str) == "trending").to_numpy() if "regime" in df else np.zeros(n, bool)
            heavy = np.where(np.isfinite(vr), vr >= 1.0, regime_tr)

            # expected side: sign of the 48-bar return to that close (continuation)
            r48 = np.full(n, np.nan)
            if n > P:
                r48[P:] = close[P:] / close[:-P] - 1.0
            raw = df[COMP].astype(float).to_numpy() if COMP in df else np.full(n, np.nan)
            side = np.where(np.isfinite(r48), np.sign(r48), np.sign(raw))
            side = np.nan_to_num(side, nan=0.0)

            active = np.isfinite(fc) & (fc != 0)
            sit = is_sun23 & heavy
            agree = active & sit & (np.sign(fc) == side) & (side != 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            # cases: non-zero forecast on a Sunday 23:00 bar
            drift = coin_drift.get(coin, np.nan)
            for i in np.where(active & is_sun23)[0]:
                if i + H < n and np.isfinite(close[i]) and np.isfinite(close[i + H]) and np.isfinite(drift):
                    r = close[i + H] / close[i] - 1.0
                    case_signed.append(np.sign(fc[i]) * (r - drift))
                    case_absf.append(abs(fc[i]))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation bars are those stamped Sunday 23:00 UTC with the mean volume of the last 48 rows at least "
               "the mean of the 120 rows before them (regime used where history is short), side = sign of the 48-row "
               "return; the coin's mean 12-bar return is pooled over non-overlapping 12-bar grids of all its windows; "
               "upper/lower halves of |forecast| are the top and bottom floor(n/2) cases sorted by |forecast| "
               "(the middle case dropped if n is odd); the plan's 'fewer than 200 cases' rule is reported as not observable.")

    main_name = "mean signed excess 12-bar return after Sunday 23:00 forecasts"
    threshold = "above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject"

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": int(len(case_signed)), "active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of active bars are Sunday 23:00 bars of a heavy-volume weekend "
                           "with the forecast on the side of the weekend move, below the 90 % required."),
            "reading": reading,
        }

    x = np.array(case_signed, dtype=float)
    a = np.array(case_absf, dtype=float)
    n_cases = int(len(x))

    mean = float(np.mean(x)) if n_cases else None
    t = None
    if n_cases >= 2:
        sd = float(np.std(x, ddof=1))
        t = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val, sup_pass = None, None
    if n_cases >= 2:
        order = np.argsort(a, kind="mergesort")
        half = n_cases // 2
        lower = x[order[:half]]
        upper = x[order[n_cases - half:]]
        if half > 0:
            sup_val = float(np.mean(upper) - np.mean(lower))
            sup_pass = bool(sup_val > 0)

    counts = {"cases": n_cases}

    if n_cases < 200:
        status = "not observable"
        decided = f"Only {n_cases} cases over all coins and windows, fewer than the plan's minimum of 200."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither rule is met."
    elif mean > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean signed excess 12-bar return above 0 with t >= 2, and the upper |forecast| half beats the lower half."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean signed excess 12-bar return below 0 with t <= -2."
    elif mean > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": passed},
        "main_measure": {"name": main_name,
                         "value": mean,
                         "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "upper minus lower half of |forecast|, mean signed excess return",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
