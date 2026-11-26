import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.vol_dryup.last_history_value"

    # ---------- 1. situation check ----------
    active_total = 0
    active_ok = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            reg = df["regime"].astype(str).values
            raw = pd.to_numeric(df[RAW], errors="coerce").values if RAW in df.columns else np.full(len(df), np.nan)
            n = len(df)
            for t in range(n):
                if f[t] == 0:
                    continue
                active_total += 1
                ok = reg[t] == "mean_reversion"
                if t >= 10 and np.isfinite(close[t]) and np.isfinite(close[t - 10]):
                    ok = ok and (close[t] / close[t - 10] - 1.0 < 0.0)
                if t >= 60 and np.isfinite(close[t]) and np.isfinite(close[t - 60]):
                    ok = ok and ((close[t] / close[t - 60] - 1.0) * 100.0 < -10.0)
                if np.isfinite(raw[t]):
                    ok = ok and (raw[t] < 0.0)
                ok = ok and (f[t] < 0)
                if ok:
                    active_ok += 1
    agreement = (active_ok / active_total) if active_total > 0 else 0.0
    passed = bool(active_total > 0 and agreement >= 0.9)

    mm_name = "mean unusual 5-bar short move per case (drift - return)"
    mm_thr = "confirm: mean > 0 with day-clustered t >= 2 over >= 30 cases and supporting difference > 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("Situation = regime 'mean_reversion' (falling-profile veto passed and 10-day return < 0), re-checked from prices "
               "(10-day return < 0, 60-day return < -10 %) where the window holds enough bars and raw volume log ratio < 0 where recorded; "
               "a case is the first short bet (rise of short forecast >= 2 points from its lowest level since the last bet) in each "
               "5-bar grid cell with a full 5-bar return in the window; the day-clustered t uses a G/(G-1) correction; "
               "the split puts |forecast| > median in the larger half and <= median in the smaller.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": mm_thr},
            "supporting_check": None,
            "counts": {"cases": None, "active bars": int(active_total)},
            "decided_by": ("Fewer than 90 % of the active bars are short bars of the plan's situation (falling profile with "
                           "10-day return below 0 and shrunk volume): the config's forecast does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. normal drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for t in range(0, len(c) - H, H):
                if np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0:
                    rets.append(c[t + H] / c[t] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    vals, absf, days = [], [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for t in range(n):
                s = -f[t] if f[t] < 0 else 0.0
                if s <= 0:
                    ref = 0.0
                    continue
                ref = min(ref, s)
                if s - ref >= BAND:
                    bet[t] = True
                    ref = s
            for start in range(0, n, H):
                idx = [t for t in range(start, min(start + H, n)) if bet[t]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n or not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] <= 0:
                    continue
                if not np.isfinite(drift[coin]):
                    continue
                r = c[t + H] / c[t] - 1.0
                vals.append(-r + drift[coin])
                absf.append(abs(f[t]))
                days.append(ts.iloc[t].strftime("%Y-%m-%d"))

    vals = np.array(vals, dtype=float)
    absf = np.array(absf, dtype=float)
    ncase = int(len(vals))
    ndays = int(len(set(days)))

    mean = float(np.mean(vals)) if ncase > 0 else None
    tstat = None
    if ncase > 1:
        dev = vals - mean
        s = pd.Series(dev).groupby(pd.Series(days)).sum().values
        G = len(s)
        if G > 1:
            var = (G / (G - 1)) * np.sum(s ** 2) / ncase ** 2
            if var > 0:
                tstat = float(mean / np.sqrt(var))

    diff, welch_t, sc_pass = None, None, None
    if ncase >= 2:
        med = np.median(absf)
        hi = vals[absf > med]
        lo = vals[absf <= med]
        if len(hi) >= 1 and len(lo) >= 1:
            diff = float(np.mean(hi) - np.mean(lo))
            sc_pass = bool(diff > 0)
            if len(hi) >= 2 and len(lo) >= 2:
                wt = stats.ttest_ind(hi, lo, equal_var=False).statistic
                welch_t = float(wt) if np.isfinite(wt) else None

    counts = {"cases": ncase, "days": ndays}

    if ncase < 30:
        status = "not observable"
        decided = f"Only {ncase} cases, fewer than the plan's minimum of 30."
    elif tstat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual short move cannot be computed, so neither confirm nor reject is met."
    elif mean > 0 and tstat >= 2:
        if sc_pass:
            status = "confirmed"
            decided = "Mean unusual short move above 0 with t >= 2 over at least 30 cases, and larger-minus-smaller shrinkage difference above 0."
        else:
            status = "inconclusive"
            decided = "The main measure confirms (mean > 0, t >= 2, >= 30 cases) but the supporting check's difference is not above 0."
    elif mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "Mean unusual short move below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual short move lies between -2 and 2 (neither rule met) over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": mm_name,
            "value": mean,
            "statistic": ({"name": "t of the mean, cases of one day summed", "value": tstat} if tstat is not None else None),
            "threshold": mm_thr,
        },
        "supporting_check": {
            "name": "mean unusual short move, larger |forecast| half minus smaller half (Welch difference)",
            "value": diff,
            "passed": sc_pass,
            "welch_t": welch_t,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
