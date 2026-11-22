import json
import numpy as np
import pandas as pd
from scipy import stats


def _component_value(df, comp_id, field):
    flat = "debug_info.components.%s.%s" % (comp_id, field)
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        out = []
        for v in df["debug_info.components"].values:
            val = np.nan
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get(comp_id)
                if isinstance(c, dict):
                    x = c.get(field)
                    try:
                        val = float(x) if x is not None else np.nan
                    except Exception:
                        val = np.nan
            out.append(val)
        return pd.Series(out, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def measure(bars):
    H = 84
    BAND = 2.0
    MIN_CASES = 20

    n_active = 0
    n_agree = 0

    cases = []  # (coin, unusual, weight)
    coin_grid_returns = {}
    coin_bets = {}

    for coin in sorted(bars.keys()):
        grid_rets = []
        bets_list = []
        for w in sorted(bars[coin].keys(), key=lambda s: (len(str(s)), str(s))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True) if "timestamp" in df.columns else df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            high = pd.to_numeric(df["high"], errors="coerce").astype(float)
            low = pd.to_numeric(df["low"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).astype(float).values
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            n = len(df)

            # --- situation, recomputed from prices inside the window ---
            prior_ret = close.shift(6) / close.shift(186) - 1.0
            rng = (high - low) / close
            ratio = rng.rolling(180, min_periods=180).mean() / rng.rolling(6, min_periods=6).mean()
            fall_raw = _component_value(df, "fall", "last_history_value")
            ret6 = close / close.shift(6) - 1.0
            fall_sign = fall_raw.where(fall_raw.notna(), ret6)

            prior_ok = prior_ret < 0
            range_ok = ratio <= 0.3333
            prior_known = prior_ret.notna()
            range_known = ratio.notna()
            in_regime = regime == "mean_reversion"
            prior_cond = np.where(prior_known.values, prior_ok.values, in_regime)
            range_cond = np.where(range_known.values, range_ok.values, in_regime)
            fall_cond = (fall_sign < 0).values
            situation = prior_cond & range_cond & fall_cond

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            # --- coin's normal drift: grid returns over all windows ---
            cv = close.values
            for p in range(0, n, H):
                if p + H < n and np.isfinite(cv[p]) and np.isfinite(cv[p + H]) and cv[p] > 0:
                    grid_rets.append(cv[p + H] / cv[p] - 1.0)

            # --- bets: rise of the long forecast of at least the band ---
            lowlvl = 0.0
            seen_cells = set()
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    lowlvl = 0.0
                    continue
                if f - lowlvl >= BAND:
                    lowlvl = f
                    cell = i // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if i + H < n and np.isfinite(cv[i]) and np.isfinite(cv[i + H]) and cv[i] > 0:
                        bets_list.append((cv[i + H] / cv[i] - 1.0, f))
                else:
                    lowlvl = min(lowlvl, f)
        coin_grid_returns[coin] = grid_rets
        coin_bets[coin] = bets_list

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 84-bar move per case (return minus coin's normal 84-bar drift)"
    threshold = "confirm: mean > 0 with t >= 2 on >= 20 independent cases and supporting check passes; reject: mean < 0 with t <= -2 on >= 20 cases"
    support_name = "forecast-weighted case mean minus unweighted mean (>= 0 passes)"
    reading = ("Situation recomputed per window from prices (prior return close[t-6]/close[t-186]-1 < 0, "
               "bar range (high-low)/close with 180-bar mean / 6-bar mean <= 0.3333, and a fall: the recorded raw "
               "'fall' value, else the 6-bar return, < 0), using the recorded regime for the prior/range rules on "
               "bars too early in a window to recompute them; cases are the first long bet (forecast rise >= 2 from "
               "its low since the last bet) in each 84-bar grid cell of a window, with a full 84-bar forward return, "
               "and the normal drift is the coin's mean 84-bar grid return over all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "independent cases": None},
            "decided_by": ("No active bars in the record." if agreement is None else
                           "Only %.1f%% of the bars with a non-zero forecast are long bars of the plan's situation "
                           "(negative lagged 30-day return, 6-bar range >= 3x its 180-bar mean, a 24h fall), below 90%%."
                           % (100 * agreement)),
            "reading": reading,
        }

    unusual, weights = [], []
    for coin in coin_bets:
        g = coin_grid_returns.get(coin, [])
        if len(g) == 0:
            continue
        drift = float(np.mean(g))
        for r, f in coin_bets[coin]:
            unusual.append(r - drift)
            weights.append(f)
    unusual = np.array(unusual, dtype=float)
    weights = np.array(weights, dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        t_val = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None
    wmean = float(np.sum(unusual * weights) / np.sum(weights)) if n_cases > 0 and np.sum(weights) > 0 else None
    sup_val = (wmean - mean_u) if (wmean is not None and mean_u is not None) else None
    sup_pass = (bool(sup_val >= 0) if sup_val is not None else None)

    counts = {"independent cases": n_cases, "active bars": n_active}
    main = {"name": main_name, "value": mean_u,
            "statistic": ({"name": "t of the mean", "value": t_val} if t_val is not None else None),
            "threshold": threshold}
    support = {"name": support_name, "value": sup_val, "passed": sup_pass}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = "Fewer than the plan's minimum of 20 independent cases (%d)." % n_cases
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither rule is met."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2 on at least 20 cases, and the weighted mean is at least the unweighted mean."
        else:
            status = "inconclusive"
            decided = "A confirming t whose supporting check fails (weighted mean below the unweighted mean)."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 on at least 20 independent cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 on at least 20 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
