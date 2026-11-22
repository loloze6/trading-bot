import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.bounce.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            if "timestamp" in df.columns:
                df = df.sort_values("timestamp")
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            r90 = close / close.shift(90) - 1.0
            r30 = close / close.shift(30) - 1.0
            regime_on = (df["regime"].astype(str) == "mean_reversion") if "regime" in df.columns \
                else pd.Series(False, index=df.index)
            both_neg = pd.Series(np.where(r90.notna() & r30.notna(),
                                          (r90 < 0) & (r30 < 0),
                                          regime_on), index=df.index).astype(bool)
            ret1 = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            rise = pd.Series(np.where(raw.notna(), raw > 0, ret1 > 0), index=df.index).astype(bool)
            situ = both_neg & rise
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The 90- and 30-bar price changes are recomputed from closes inside each window where 90/30 prior bars exist, "
               "falling back to the recorded regime elsewhere, and the rise is the bounce raw value > 0; a case is a short bet "
               "(forecast's short size rising >= 2 points above its lowest short level since the last bet, from 0 after flat), "
               "taking the first bet bar of each non-overlapping 2-bar grid cell with its full 2-bar return inside the window; "
               "drift is the mean of each coin's non-overlapping 2-bar returns over all its windows; the supporting split puts "
               "|forecast| >= median in the larger half and < median in the smaller half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the active forecast bars are short bars where the 90- and 30-bar returns are both "
                           "negative and the day rose, so the config does not do what the plan's Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. drift per coin ----------
    drift = {}
    for coin in sorted(bars):
        rets = []
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            if "timestamp" in df.columns:
                df = df.sort_values("timestamp")
            c = df["close"].astype(float).to_numpy()
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    excess = []
    absf = []
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            if "timestamp" in df.columns:
                df = df.sort_values("timestamp")
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                fi = f[i]
                if not np.isfinite(fi) or fi >= 0:
                    ref = 0.0
                    continue
                m = -fi
                if m - ref >= BAND:
                    bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            for start in range(0, n, H):
                idx = [j for j in range(start, min(start + H, n)) if bet[j]]
                if not idx:
                    continue
                j = idx[0]
                if j + H >= n:
                    continue
                if not (np.isfinite(c[j]) and np.isfinite(c[j + H]) and c[j] != 0):
                    continue
                d = drift.get(coin, np.nan)
                if not np.isfinite(d):
                    continue
                r = c[j + H] / c[j] - 1.0
                excess.append(-(r - d))
                absf.append(abs(f[j]))

    excess = np.asarray(excess, dtype=float)
    absf = np.asarray(absf, dtype=float)
    n_cases = int(len(excess))

    mean = float(np.mean(excess)) if n_cases > 0 else None
    tval = None
    if n_cases > 1:
        sd = float(np.std(excess, ddof=1))
        tval = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_large = n_small = 0
    if n_cases > 0:
        med = float(np.median(absf))
        large = excess[absf >= med]
        small = excess[absf < med]
        n_large, n_small = int(len(large)), int(len(small))
        if n_large > 0 and n_small > 0:
            sup_val = float(np.mean(large) - np.mean(small))
            sup_pass = bool(sup_val > 0)

    main = {
        "name": "mean short-direction 2-bar return in excess of the coin's drift per short bet",
        "value": mean,
        "statistic": {"name": "t of the mean", "value": tval} if tval is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2",
    }
    sup = {"name": "excess return of larger-|forecast| half minus smaller half",
           "value": sup_val, "passed": sup_pass}
    counts = {"cases": n_cases, "larger half cases": n_large, "smaller half cases": n_small}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than {MIN_CASES} cases in total across coins and windows ({n_cases})."
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and tval >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The main mean is positive with t >= 2 and the larger-|forecast| half beats the smaller half."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The main mean is negative with t <= -2: the bounces are followed by rises beyond the coin's drift."
    elif mean > 0 and tval >= 2:
        status = "inconclusive"
        decided = "The main t is >= 2 but the supporting check fails (difference not above 0)."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
