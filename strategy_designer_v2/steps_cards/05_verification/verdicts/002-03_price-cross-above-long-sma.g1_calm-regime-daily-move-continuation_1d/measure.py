import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    LHV = "debug_info.components.scaled_move.last_history_value"

    def scaled_move(close):
        r = close.pct_change()
        vol = r.rolling(20, min_periods=20).std()
        return r, r / vol

    def standardise(x):
        m = x.rolling(60, min_periods=20).mean()
        s = x.rolling(60, min_periods=20).std()
        return (x - m) / s

    # ---------- per-window preparation ----------
    prepared = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            close = d["close"].astype(float)
            ret1, sm = scaled_move(close)
            d["_ret1"] = ret1
            d["_z"] = standardise(sm)
            d["_fwd"] = close.shift(-H) / close - 1.0
            d["_grid"] = (np.arange(len(d)) % H) == 0
            d["_fc"] = pd.to_numeric(d["forecast"], errors="coerce")
            d["_low"] = d["regime"].astype(str) == "trending"
            prepared.setdefault(coin, {})[w] = d

    # ---------- situation check ----------
    n_active, n_ok = 0, 0
    for coin, wins in prepared.items():
        for w, d in wins.items():
            act = d["_fc"].notna() & (d["_fc"] != 0)
            if not act.any():
                continue
            move = d["_ret1"].copy()
            if LHV in d.columns:
                lhv = pd.to_numeric(d[LHV], errors="coerce")
                move = move.where(move.notna(), lhv)
            side_ok = np.sign(d["_fc"]) == np.sign(move)
            ok = act & d["_low"] & side_ok & move.notna() & (move != 0)
            n_active += int(act.sum())
            n_ok += int(ok.sum())
    agreement = float(n_ok / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The plan's low-volatility situation is read from the recorded regime "
               "('trending' is the config rule volpct <= 0.5, since the 100-bar percentile "
               "cannot be recomputed inside ~120-bar windows), the side is the sign of the "
               "day's return, the coin mean 5-bar return is the mean over all its grid bars "
               "of all windows, and on high-volatility bars the forecast is recomputed as "
               "k*sign(z)*z^2 (clipped to +-20) from the price-recomputed standardised scaled "
               "move, with k fitted on the active bars against the recorded forecast.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of non-zero-forecast bars are low-volatility "
                           "(trending) bars with the forecast in the direction of the day's "
                           "move, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- coin mean 5-bar return over all windows ----------
    coin_mu = {}
    for coin, wins in prepared.items():
        vals = []
        for w, d in wins.items():
            g = d[d["_grid"] & d["_fwd"].notna()]
            vals.append(g["_fwd"].values)
        allv = np.concatenate(vals) if vals else np.array([])
        coin_mu[coin] = float(np.mean(allv)) if len(allv) else np.nan

    # ---------- calibrate k for recomputed forecast ----------
    num, den = 0.0, 0.0
    for coin, wins in prepared.items():
        for w, d in wins.items():
            m = d["_fc"].notna() & (d["_fc"] != 0) & d["_z"].notna() & (d["_fc"].abs() < 20)
            if m.any():
                gz = np.sign(d.loc[m, "_z"]) * d.loc[m, "_z"] ** 2
                num += float((d.loc[m, "_fc"] * gz).sum())
                den += float((gz * gz).sum())
    k = num / den if den > 0 else 1.0

    # ---------- main measure and supporting check ----------
    lo_prod, hi_prod = [], []
    for coin, wins in prepared.items():
        mu = coin_mu[coin]
        if not np.isfinite(mu):
            continue
        for w, d in wins.items():
            g = d[d["_grid"] & d["_fwd"].notna()]
            a = g[g["_fc"].notna() & (g["_fc"] != 0)]
            lo_prod.extend((a["_fc"] * (a["_fwd"] - mu)).tolist())
            hv = g[(~g["_low"]) & g["_z"].notna()]
            if len(hv):
                fh = np.clip(k * np.sign(hv["_z"]) * hv["_z"] ** 2, -20, 20)
                hi_prod.extend((fh * (hv["_fwd"] - mu)).tolist())

    lo = np.array(lo_prod, dtype=float)
    hi = np.array(hi_prod, dtype=float)
    n = int(len(lo))
    mean_lo = float(lo.mean()) if n > 0 else None
    t = None
    if n > 1:
        sd = lo.std(ddof=1)
        t = float(mean_lo / (sd / np.sqrt(n))) if sd > 0 else None
    mean_hi = float(hi.mean()) if len(hi) > 0 else None
    diff = (mean_lo - mean_hi) if (mean_lo is not None and mean_hi is not None) else None
    sup_pass = (bool(diff > 0) if diff is not None else None)

    if n < 30:
        status = "not observable"
        decided = f"Only {n} non-zero-forecast grid cases pooled across coins, fewer than the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean product could not be computed, so neither confirm nor reject is met."
    elif mean_lo > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean product positive with t >= 2 on at least 30 cases, and low-vol minus high-vol mean product is above 0."
        else:
            status = "inconclusive"
            decided = "Confirm-level main measure (positive, t >= 2) but the supporting check fails (low-vol minus high-vol mean not above 0)."
    elif mean_lo < 0 and t <= -2:
        status = "rejected"
        decided = "Mean product negative with t <= -2 on at least 30 cases: calm-market strong days reverse."
    else:
        status = "inconclusive"
        decided = "The t of the mean product lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean of forecast x (5-bar forward return minus coin mean 5-bar return), non-overlapping grid, pooled",
            "value": mean_lo,
            "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
            "threshold": "confirm: mean > 0 with t >= 2 on >= 30 cases and supporting check passes; reject: mean < 0 with t <= -2 on >= 30 cases",
        },
        "supporting_check": {
            "name": "low-vol mean product minus high-vol mean product (recomputed) > 0",
            "value": (float(diff) if diff is not None else None),
            "passed": sup_pass,
        },
        "counts": {
            "non-zero-forecast grid cases pooled across coins": n,
            "high-volatility grid cases": int(len(hi)),
        },
        "decided_by": decided,
        "reading": reading,
    }
