import numpy as np
import pandas as pd


def measure(bars):
    H = 24
    LAGS = 24
    VCOL = "debug_info.components.rsi_low_cont.last_history_value"

    def hac_t(segs):
        # segs: list of (y, x, valid) arrays per coin-window, in bar order
        Xs, Ys = [], []
        for y, x, v in segs:
            if v.sum() == 0:
                continue
            Xs.append(np.column_stack([np.ones(v.sum()), x[v]]))
            Ys.append(y[v])
        if not Xs:
            return None, None
        X = np.vstack(Xs)
        Y = np.concatenate(Ys)
        if X.shape[0] < 3:
            return None, None
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) < 2:
            return None, None
        beta = np.linalg.solve(XtX, X.T @ Y)
        meat = np.zeros((2, 2))
        for y, x, v in segs:
            if v.sum() == 0:
                continue
            n = len(y)
            G = np.zeros((n, 2))
            xv = np.where(v, x, 0.0)
            yv = np.where(v, y, 0.0)
            u = yv - beta[0] - beta[1] * xv
            G[:, 0] = np.where(v, u, 0.0)
            G[:, 1] = np.where(v, u * xv, 0.0)
            meat += G.T @ G
            for l in range(1, min(LAGS, n - 1) + 1):
                w = 1.0 - l / (LAGS + 1.0)
                Gamma = G[l:].T @ G[:-l]
                meat += w * (Gamma + Gamma.T)
        Binv = np.linalg.inv(XtX)
        V = Binv @ meat @ Binv
        se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
        t = beta[1] / se if se and np.isfinite(se) and se > 0 else None
        return float(beta[1]), (float(t) if t is not None and np.isfinite(t) else None)

    # ---------- prepare frames ----------
    frames = []
    for coin in sorted(bars):
        for win in sorted(bars[coin]):
            df = bars[coin][win].reset_index(drop=True).copy()
            df["fwd"] = df["close"].shift(-H) / df["close"] - 1.0
            df["pos"] = np.arange(len(df))
            df["_coin"] = coin
            df["_win"] = win
            frames.append(df)
    coins = sorted(bars)

    # ---------- situation check ----------
    tot_active, agree = 0, 0
    for df in frames:
        f = df["forecast"]
        v = df[VCOL]
        ok = f.notna() & v.notna()
        act = ok & (f != 0)
        tot_active += int(act.sum())
        agree += int((act & (v > 0) & (f < 0)).sum())
    agreement = agree / tot_active if tot_active > 0 else 0.0
    passed = bool(tot_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(tot_active)},
            "decided_by": ("The plan's situation is RSI below 50 with a short position, but fewer than 90% of the "
                           "bars with a non-zero forecast are short bars with RSI below 50 (the standardised, negated "
                           "RSI shortfall is non-zero, and can be positive, outside that situation)."),
            "reading": "Situation taken as raw component value > 0 (RSI < 50) with forecast < 0.",
        }

    # ---------- main measure ----------
    allneg = pd.concat([df.loc[df["forecast"] < 0, "forecast"] for df in frames]) if frames else pd.Series(dtype=float)
    if len(allneg) == 0:
        q = None
    else:
        q = float(np.quantile(allneg.values, 0.10))

    segs = []
    ext_all, neu_all = [], []
    per_coin = {c: {"ext": [], "neu": [], "ep": 0} for c in coins}
    for df in frames:
        f = df["forecast"].values.astype(float)
        y = df["fwd"].values.astype(float)
        fin = np.isfinite(f) & np.isfinite(y)
        ext = fin & (f < 0) & (f <= q) if q is not None else np.zeros(len(f), bool)
        neu = fin & (f == 0)
        valid = ext | neu
        segs.append((y, ext.astype(float), valid))
        c = df["_coin"].iloc[0] if len(df) else None
        if c is None:
            continue
        per_coin[c]["ext"].append(y[ext])
        per_coin[c]["neu"].append(y[neu])
        grid = (df["pos"].values % H) == 0
        per_coin[c]["ep"] += int((ext & grid).sum())
        ext_all.append(y[ext]); neu_all.append(y[neu])

    ext_all = np.concatenate(ext_all) if ext_all else np.array([])
    neu_all = np.concatenate(neu_all) if neu_all else np.array([])
    diff = float(ext_all.mean() - neu_all.mean()) if len(ext_all) and len(neu_all) else None
    _, t_main = hac_t(segs) if diff is not None else (None, None)

    coin_diffs = {}
    for c in coins:
        e = np.concatenate(per_coin[c]["ext"]) if per_coin[c]["ext"] else np.array([])
        n = np.concatenate(per_coin[c]["neu"]) if per_coin[c]["neu"] else np.array([])
        coin_diffs[c] = float(e.mean() - n.mean()) if len(e) and len(n) else None
    n_neg = sum(1 for d in coin_diffs.values() if d is not None and d < 0)
    n_pos = sum(1 for d in coin_diffs.values() if d is not None and d > 0)

    # ---------- supporting check ----------
    coin_mean = {}
    for c in coins:
        ys = np.concatenate([df["fwd"].values.astype(float) for df in frames if df["_coin"].iloc[0] == c])
        ys = ys[np.isfinite(ys)]
        coin_mean[c] = float(ys.mean()) if len(ys) else np.nan
    segs2 = []
    for df in frames:
        f = df["forecast"].values.astype(float)
        y = df["fwd"].values.astype(float) - coin_mean[df["_coin"].iloc[0]]
        v = np.isfinite(f) & np.isfinite(y)
        segs2.append((y, f, v))
    slope, t_slope = hac_t(segs2)
    sup_passed = None if slope is None else bool(slope > 0)

    # ---------- counts & decision ----------
    counts = {f"non-overlapping extreme episodes {c}": int(per_coin[c]["ep"]) for c in coins}
    pooled_ep = int(sum(per_coin[c]["ep"] for c in coins))
    counts["non-overlapping extreme episodes pooled"] = pooled_ep
    counts["coins"] = len(coins)
    counts["coins with negative difference"] = n_neg
    counts["coins with positive difference"] = n_pos

    enough = all(per_coin[c]["ep"] >= 30 for c in coins) and pooled_ep >= 100 and len(coins) > 0
    if not enough:
        status = "inconclusive"
        decided = "Fewer than 30 non-overlapping 24-bar extreme episodes in some coin or fewer than 100 pooled, so the test neither confirms nor rejects."
    elif diff is None or t_main is None:
        status = "inconclusive"
        decided = "The extreme-minus-neutral difference or its Newey-West t could not be computed, so the test is inconclusive."
    elif diff < 0 and t_main <= -2 and n_neg >= 2:
        status = "confirmed"
        decided = "The extreme-minus-neutral difference is negative with Newey-West t <= -2 and negative in at least 2 coins."
    elif diff > 0 and t_main >= 2 and n_pos >= 2:
        status = "rejected"
        decided = "The extreme-minus-neutral difference is positive with Newey-West t >= +2 and positive in at least 2 coins (reversal at matching strength)."
    else:
        status = "inconclusive"
        decided = "|t| < 2 or the coins split in sign, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean fwd 24-bar return, most-short decile minus zero-forecast bars",
            "value": diff,
            "statistic": {"name": "Newey-West t (24 lags)", "value": t_main} if t_main is not None else None,
            "threshold": "confirm if negative with t <= -2 and negative in at least 2 of 3 coins; reject if positive with t >= +2",
        },
        "supporting_check": {
            "name": "HAC slope of demeaned fwd 24-bar return on forecast (must be positive)",
            "value": slope,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The most-short decile is the 10% most negative forecasts among all negative-forecast bars pooled over coins and windows, "
                    "neutral bars are forecast == 0, the Newey-West t is the HAC t of the extreme-dummy slope with lags kept within each coin-window, "
                    "'at least 2 of the 3 coins' and 'matching strength' are both applied as at least 2 coins of those present having the difference's sign, "
                    "and the episode minimums apply to each coin present."),
    }
