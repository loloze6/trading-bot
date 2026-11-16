import numpy as np
import pandas as pd


def measure(bars):
    H = 24
    LAGS = 24
    FC = "forecast"
    VAL = "debug_info.components.rsi_low_cont.last_history_value"
    SCALE = 0.4

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[[FC, VAL]].dropna()
            f = d[FC].to_numpy(float)
            rsi = 50.0 - d[VAL].to_numpy(float) / SCALE
            act = f != 0
            n_active += int(act.sum())
            n_agree += int((act & (rsi < 50.0) & (f < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean fwd 24-bar return, most-short forecast decile minus zero-forecast bars"
    main_thr = "confirm if difference < 0 with Newey-West t <= -2 (24 lags); reject if > 0 with t >= +2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "The plan's situation is RSI below 50 with a short position, but fewer than 90% of the "
                          "bars with a non-zero forecast are short bars with RSI below 50.",
            "reading": "Situation taken as RSI < 50 (last_history_value > 0) and expected side short (forecast < 0).",
        }

    # ---------- 2. Build per-window data ----------
    blocks = []  # list of dicts per (coin, window)
    all_fc = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            close = df["close"].to_numpy(float)
            f = df[FC].to_numpy(float)
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:n - H] = close[H:] / close[:n - H] - 1.0
            blocks.append({"coin": coin, "w": w, "f": f, "fwd": fwd, "pos": np.arange(n)})
            all_fc.append(f[~np.isnan(f)])
    all_fc = np.concatenate(all_fc) if all_fc else np.array([])
    q10 = float(np.quantile(all_fc, 0.10)) if all_fc.size else np.nan

    for b in blocks:
        f, fwd = b["f"], b["fwd"]
        ok = ~np.isnan(f) & ~np.isnan(fwd)
        b["ok"] = ok
        b["ext"] = ok & (f <= q10) & (f < 0)
        b["zero"] = ok & (f == 0)

    def hac_ols(ys, Xs, masks):
        k = Xs[0].shape[1]
        XtX = np.zeros((k, k))
        Xty = np.zeros(k)
        for y, X, m in zip(ys, Xs, masks):
            Xm, ym = X[m], y[m]
            XtX += Xm.T @ Xm
            Xty += Xm.T @ ym
        if np.linalg.matrix_rank(XtX) < k:
            return None, None
        B = np.linalg.inv(XtX)
        beta = B @ Xty
        meat = np.zeros((k, k))
        for y, X, m in zip(ys, Xs, masks):
            u = np.where(m, y - np.nan_to_num(X) @ beta, 0.0)
            S = np.nan_to_num(X) * u[:, None]
            S[~m] = 0.0
            meat += S.T @ S
            for l in range(1, LAGS + 1):
                if l >= len(S):
                    break
                G = S[l:].T @ S[:-l]
                meat += (1.0 - l / (LAGS + 1.0)) * (G + G.T)
        V = B @ meat @ B
        se = np.sqrt(np.maximum(np.diag(V), 0.0))
        return beta, se

    # ---------- 3. Main measure: extreme minus zero, NW t ----------
    ys, Xs, ms = [], [], []
    for b in blocks:
        m = b["ext"] | b["zero"]
        X = np.column_stack([np.ones(len(m)), b["ext"].astype(float)])
        ys.append(np.nan_to_num(b["fwd"]))
        Xs.append(X)
        ms.append(m)
    beta, se = hac_ols(ys, Xs, ms)
    if beta is not None and se[1] > 0:
        diff = float(beta[1])
        t_main = float(beta[1] / se[1])
    else:
        diff, t_main = None, None

    # per-coin differences
    coins = sorted(bars.keys())
    coin_diff = {}
    for c in coins:
        e = np.concatenate([b["fwd"][b["ext"]] for b in blocks if b["coin"] == c] or [np.array([])])
        z = np.concatenate([b["fwd"][b["zero"]] for b in blocks if b["coin"] == c] or [np.array([])])
        coin_diff[c] = float(e.mean() - z.mean()) if e.size and z.size else None
    n_neg = sum(1 for v in coin_diff.values() if v is not None and v < 0)
    n_pos = sum(1 for v in coin_diff.values() if v is not None and v > 0)

    # ---------- 4. Supporting check: slope of demeaned fwd return on forecast ----------
    coin_mean = {}
    for c in coins:
        r = np.concatenate([b["fwd"][b["ok"]] for b in blocks if b["coin"] == c] or [np.array([])])
        coin_mean[c] = float(r.mean()) if r.size else 0.0
    ys2, Xs2, ms2 = [], [], []
    for b in blocks:
        y = np.where(b["ok"], b["fwd"] - coin_mean[b["coin"]], 0.0)
        X = np.column_stack([np.ones(len(y)), np.nan_to_num(b["f"])])
        ys2.append(y)
        Xs2.append(X)
        ms2.append(b["ok"])
    beta2, se2 = hac_ols(ys2, Xs2, ms2)
    slope = float(beta2[1]) if beta2 is not None else None
    sup_passed = (slope > 0) if slope is not None else None

    # ---------- 5. Episode counts (non-overlapping grid) ----------
    ep_coin = {}
    for c in coins:
        cnt = 0
        for b in blocks:
            if b["coin"] != c:
                continue
            grid = (b["pos"] % H) == 0
            cnt += int((grid & b["ext"]).sum())
        ep_coin[c] = cnt
    ep_pooled = int(sum(ep_coin.values()))
    enough = all(v >= 30 for v in ep_coin.values()) and ep_pooled >= 100 and len(ep_coin) > 0

    counts = {f"non-overlapping extreme episodes {c}": int(v) for c, v in ep_coin.items()}
    counts["non-overlapping extreme episodes pooled"] = ep_pooled
    counts["extreme bars pooled"] = int(sum(b["ext"].sum() for b in blocks))
    counts["zero-forecast bars pooled"] = int(sum(b["zero"].sum() for b in blocks))
    counts["coins with negative difference"] = int(n_neg)
    counts["coins with positive difference"] = int(n_pos)
    counts["coins in record"] = int(len(coins))

    # ---------- 6. Decision ----------
    if not enough:
        status = "inconclusive"
        decided = ("Fewer than 30 non-overlapping 24-bar extreme episodes in some coin or fewer than 100 pooled, "
                   "so the test neither confirms nor rejects.")
    elif diff is None or t_main is None:
        status = "inconclusive"
        decided = "The extreme-minus-neutral difference or its t-stat could not be computed, so the test is inconclusive."
    elif diff < 0 and t_main <= -2 and n_neg >= 2:
        status = "confirmed"
        decided = "The extreme-minus-neutral difference is negative with t <= -2 and negative in at least 2 coins."
    elif diff > 0 and t_main >= 2 and n_pos >= 2:
        status = "rejected"
        decided = "The extreme-minus-neutral difference is positive with t >= +2 (reversal or no extra fall)."
    else:
        status = "inconclusive"
        decided = "|t| < 2 or the coins split in sign, which the plan calls inconclusive."

    reading = ("Most-short decile = bars whose forecast is at or below the 10th percentile of all pooled forecasts "
               "(and negative), neutral = forecast exactly 0, Newey-West uses 24 Bartlett lags within each "
               "coin-window, per-coin sign uses the plain per-coin mean difference, with only "
               f"{len(coins)} coins present 'at least 2 coins' is applied to those (rejection likewise needs 2 "
               "positive coins), and the supporting slope check is reported but not used as a gate since the "
               "confirm/reject rules do not name it.")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": ({"name": "Newey-West t (24 lags)", "value": t_main} if t_main is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "slope of demeaned fwd 24-bar return on forecast must be positive",
            "value": slope,
            "passed": (bool(sup_passed) if sup_passed is not None else None),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
