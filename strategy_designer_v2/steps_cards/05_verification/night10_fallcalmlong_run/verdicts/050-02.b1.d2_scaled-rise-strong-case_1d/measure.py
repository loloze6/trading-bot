import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    RAW = "debug_info.components.scaled_week_rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            # where raw is not recorded, recompute the sign of the 7-day return from prices
            ret7 = np.full(len(df), np.nan)
            if len(df) > 7:
                ret7[7:] = close[7:] / close[:-7] - 1.0
            rise = np.where(np.isnan(raw), ret7 > 0, raw > 0)
            # falling calm profile: the regime detector's non-vetoed regime ("unknown")
            profile = df["regime"].astype(str).str.lower().values == "unknown"
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & rise & profile & (fc > 0)).sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean unusual 3-day move after scaled weekly rises",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"distinct case days": 0, "cases": 0},
            "decided_by": "No active bars: fewer than 30 distinct case days.",
            "reading": "none",
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are long bars with a positive 7-day scaled rise "
                           "inside the falling calm profile (regime 'unknown')."),
            "reading": "The falling calm profile is read from the recorded regime 'unknown' (no veto fired).",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        # normal drift: mean non-overlapping 3-bar return over all the coin's windows
        grid_rets = []
        per_win = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            per_win.append(df)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for df in per_win:
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            # bets: long rises of the forecast of at least the band from its lowest level since last bet
            bet = np.zeros(n, dtype=bool)
            low = 0.0
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bet[i] = True
                    low = f
                else:
                    low = min(low, f)
            # one case per grid cell: the first bet in the cell
            for c0 in range(0, n, H):
                idx = np.where(bet[c0:c0 + H])[0]
                if len(idx) == 0:
                    continue
                t = c0 + int(idx[0])
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                rows.append({"day": ts.iloc[t].strftime("%Y-%m-%d"),
                             "forecast": float(fc[t]),
                             "unusual": float(r - drift)})

    cases = pd.DataFrame(rows, columns=["day", "forecast", "unusual"])
    n_cases = len(cases)
    n_days = int(cases["day"].nunique()) if n_cases else 0
    threshold = "mean > 0 with t >= 2 (and Spearman > 0) to confirm; mean < 0 with t <= -2 to reject"
    reading = ("A case is the first long bet (forecast rise >= 2 points from its lowest level since the last bet, "
               "from 0 after flat) in each non-overlapping 3-bar cell counted from each window's first row, the "
               "falling calm profile is the recorded regime 'unknown', the day-pooled t uses cluster-robust "
               "standard errors with per-day summed deviations (G/(G-1) correction), and fewer than 30 case days "
               "is reported as not observable.")

    mean = float(cases["unusual"].mean()) if n_cases else None
    tval = None
    if n_cases >= 2:
        dev = cases["unusual"] - mean
        s_d = dev.groupby(cases["day"]).sum().values
        G = len(s_d)
        if G >= 2:
            se = np.sqrt(G / (G - 1) * np.sum(s_d ** 2)) / n_cases
            tval = float(mean / se) if se > 0 else None
    rho = None
    if n_cases >= 3 and cases["forecast"].nunique() > 1 and cases["unusual"].nunique() > 1:
        rho = float(stats.spearmanr(cases["forecast"], cases["unusual"]).correlation)

    sup_pass = None if rho is None else bool(rho > 0)

    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 distinct case days across coins and windows ({n_days})."
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed."
    elif mean > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and a positive Spearman correlation."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2: a reversal after scaled weekly rises."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the Spearman correlation is not above 0."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "mean unusual 3-day move after scaled weekly rises",
                         "value": mean,
                         "statistic": None if tval is None else {"name": "t of the mean, cases pooled by day",
                                                                 "value": tval},
                         "threshold": threshold},
        "supporting_check": {"name": "Spearman(forecast at signal, unusual move) > 0",
                             "value": rho, "passed": sup_pass},
        "counts": {"distinct case days": n_days, "cases": int(n_cases)},
        "decided_by": decided,
        "reading": reading,
    }
