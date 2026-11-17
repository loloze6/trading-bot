import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 30
    RAW = "debug_info.components.hpm.last_history_value"
    THRESH_TXT = "main slope t >= +2 confirms (with near-minus-far slope difference > 0); t <= -2 rejects; at least 300 independent grid cases"

    def _f(x):
        try:
            x = float(x)
        except Exception:
            return None
        return x if np.isfinite(x) else None

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(float)
            raw = (pd.to_numeric(d[RAW], errors="coerce").to_numpy(float)
                   if RAW in d.columns else np.full(len(d), np.nan))
            n = len(d)
            for i in range(n):
                if not np.isfinite(fc[i]) or fc[i] == 0:
                    continue
                n_active += 1
                # expected side: sign of the past 30-bar return (prices when inside the window, else raw component value)
                exp = 0.0
                if i >= H and np.isfinite(close[i]) and np.isfinite(close[i - H]) and close[i - H] > 0:
                    exp = np.sign(close[i] / close[i - H] - 1.0)
                    if np.isfinite(raw[i]) and raw[i] != 0 and np.sign(raw[i]) != exp:
                        exp = 0.0  # raw component disagrees with the price move: not the plan's situation
                elif np.isfinite(raw[i]):
                    exp = np.sign(raw[i])
                if exp != 0 and np.sign(fc[i]) == exp:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "slope of excess forward 30-bar return on forecast/10", "value": None,
                             "statistic": None, "threshold": THRESH_TXT},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars have a forecast whose sign equals the sign of the past "
                           "30-bar return (momentum side weighted by nearness to the 365-bar high) that the Fidelity requires."),
            "reading": "Expected side taken as the sign of the past 30-bar close return (from recorded closes when inside the window, else from the raw hpm value).",
        }

    # ---------- 2. grid cases ----------
    rows = []  # coin, fwd, forecast, pos, past, raw
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(float)
            raw = (pd.to_numeric(d[RAW], errors="coerce").to_numpy(float)
                   if RAW in d.columns else np.full(len(d), np.nan))
            n = len(d)
            for p in (0, 30, 60, 90):
                if p + H >= n:
                    continue
                if not (np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0):
                    continue
                fwd = close[p + H] / close[p] - 1.0
                past = np.nan
                if p >= H and np.isfinite(close[p - H]) and close[p - H] > 0:
                    past = close[p] / close[p - H] - 1.0
                rows.append((coin, fwd, fc[p], p, past, raw[p]))
    g = pd.DataFrame(rows, columns=["coin", "fwd", "fc", "pos", "past", "raw"])
    if len(g):
        g["coin_mean"] = g.groupby("coin")["fwd"].transform("mean")
        g["excess"] = g["fwd"] - g["coin_mean"]

    main = g.dropna(subset=["excess", "fc"]) if len(g) else g
    n_main = int(len(main))
    slope = None
    tval = None
    if n_main >= 3 and np.std(main["fc"].to_numpy()) > 0:
        lr = stats.linregress(main["fc"].to_numpy() / 10.0, main["excess"].to_numpy())
        slope = _f(lr.slope)
        if lr.stderr and lr.stderr > 0:
            tval = _f(lr.slope / lr.stderr)

    # ---------- supporting check ----------
    diff = None
    n_near = n_far = 0
    if len(g):
        s = g[g["pos"].isin([30, 60, 90])].dropna(subset=["past", "raw", "excess"])
        s = s[s["past"] != 0].copy()
        s["W"] = s["raw"] / s["past"]
        s = s[np.isfinite(s["W"])]
        if len(s) >= 6:
            med = s["W"].median()
            near = s[s["W"] > med]
            far = s[s["W"] < med]
            n_near, n_far = int(len(near)), int(len(far))
            if (n_near >= 3 and n_far >= 3 and np.std(near["past"]) > 0 and np.std(far["past"]) > 0):
                sn = stats.linregress(near["past"].to_numpy(), near["excess"].to_numpy()).slope
                sf = stats.linregress(far["past"].to_numpy(), far["excess"].to_numpy()).slope
                diff = _f(sn - sf)
    sup_pass = None if diff is None else bool(diff > 0)

    # ---------- decision ----------
    if n_main < 300:
        status = "not observable"
        decided = f"Only {n_main} independent grid cases, fewer than the 300 the plan requires, so nothing is decided."
    elif tval is None:
        status = "inconclusive"
        decided = "The main slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The main slope's t is at least +2 and the near-minus-far slope difference is greater than 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The main slope's t is at most -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The main slope's t is at least +2 but the near-minus-far slope difference is 0 or less (or not computable)."
    else:
        status = "inconclusive"
        decided = "The main slope's t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "pooled OLS slope of excess forward 30-bar return on forecast/10",
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": THRESH_TXT,
        },
        "supporting_check": {
            "name": "slope of excess forward return on past return, above-median W minus below-median W",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": {
            "independent grid cases": n_main,
            "above-median W cases": n_near,
            "below-median W cases": n_far,
        },
        "decided_by": decided,
        "reading": ("Grid positions 0/30/60/90 are used only where the bar 30 rows later exists in the same window; "
                    "the coin mean is the mean of that coin's grid forward returns over all windows; the regression "
                    "has an intercept; the median split is pooled over all coins, with cases exactly at the median left out."),
    }
