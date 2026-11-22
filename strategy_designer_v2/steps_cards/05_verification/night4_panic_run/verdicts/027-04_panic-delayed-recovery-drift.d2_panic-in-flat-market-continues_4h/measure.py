import numpy as np
import pandas as pd


def measure(bars):
    H = 78
    FC = "forecast"
    RAW = "debug_info.components.panic.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            for t in range(n):
                if f[t] == 0:
                    continue
                n_active += 1
                in_regime = reg[t] == "mean_reversion"
                raw_fall = np.isfinite(raw[t]) and raw[t] > 0
                # the 24h stretch ending 6 bars ago fell (price check where it can be computed in-window)
                if t - 12 >= 0 and np.isfinite(close[t - 12]) and np.isfinite(close[t - 6]):
                    price_fall = close[t - 6] < close[t - 12]
                else:
                    price_fall = True
                if in_regime and raw_fall and price_fall and f[t] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed_sit = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Situation = regime 'mean_reversion' (the detector's recorded decision for the flat-prior rule) with the "
               "panic raw value > 0 and close[t-6] < close[t-12] where computable, expected side short; a case is the "
               "first bar of each 78-bar grid cell (positions 0, 78, ... of each window) with forecast <= -10 whose "
               "78-bar forward return lies inside the window, its forecast at that bar sets the supporting-check group, "
               "the normal drift is the coin's mean 78-bar return on the same grid over all its windows, and the "
               "plan's 'fewer than 30 cases' minimum is reported as not observable.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short bars in the flat-prior regime after a falling "
                           "24h stretch: the config's forecast does not follow the plan's situation and side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # normal drift per coin
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for s in range(0, len(c) - H, H):
                if np.isfinite(c[s]) and np.isfinite(c[s + H]) and c[s] > 0:
                    rets.append(c[s + H] / c[s] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (unusual short move, forecast)
    for coin, wins in bars.items():
        d = drift[coin]
        if not np.isfinite(d):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df[FC], errors="coerce").values
            c = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            for s in range(0, n, H):
                e = min(s + H, n)
                for t in range(s, e):
                    if np.isfinite(f[t]) and f[t] <= -10:
                        if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0:
                            r = c[t + H] / c[t] - 1.0
                            cases.append((-(r - d), float(f[t])))
                        break

    ncase = len(cases)
    vals = np.array([x[0] for x in cases], dtype=float)
    fcs = np.array([x[1] for x in cases], dtype=float)

    mean = float(np.mean(vals)) if ncase > 0 else None
    tstat = None
    if ncase > 1:
        sd = float(np.std(vals, ddof=1))
        tstat = float(mean / (sd / np.sqrt(ncase))) if sd > 0 else None

    strong = vals[fcs <= -15] if ncase else np.array([])
    mid = vals[(fcs > -15) & (fcs <= -10)] if ncase else np.array([])
    if len(strong) > 0 and len(mid) > 0:
        diff = float(np.mean(strong) - np.mean(mid))
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = None

    counts = {
        "cases": int(ncase),
        "cases forecast <= -15": int(len(strong)),
        "cases forecast between -15 and -10": int(len(mid)),
    }

    if ncase < 30:
        status = "not observable"
        decided = f"Only {ncase} cases over all coins and windows, fewer than the plan's minimum of 30."
    elif tstat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed (no dispersion), so neither rule is met."
    elif mean > 0 and tstat >= 2:
        if sup_pass is True:
            status = "confirmed"
            decided = ("Mean unusual short move above 0 with t >= 2 over at least 30 cases, and the cases at or below "
                       "-15 move more than those between -15 and -10.")
        else:
            status = "inconclusive"
            decided = "A confirming t (>= 2, mean above 0) whose supporting check fails is inconclusive."
    elif mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "Mean unusual short move below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean 78-bar unusual move in the short direction, cases forecast <= -10",
            "value": mean,
            "statistic": ({"name": "t of the mean", "value": tstat} if tstat is not None else None),
            "threshold": "confirm: mean > 0 with t >= 2 over >= 30 cases; reject: mean < 0 with t <= -2 over >= 30 cases",
        },
        "supporting_check": {
            "name": "mean unusual move (forecast <= -15) minus (forecast in (-15, -10])",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
