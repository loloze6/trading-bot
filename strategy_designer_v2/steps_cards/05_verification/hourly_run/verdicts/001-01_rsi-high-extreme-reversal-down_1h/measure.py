import numpy as np
import pandas as pd


def measure(bars):
    H = 12
    COL_RAW = "debug_info.components.rsi_high.last_history_value"
    SCALE = 0.4

    # ---------- 1. Situation check: RSI above 50, short side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            if COL_RAW not in df.columns:
                continue  # missing column is not a value: those active bars cannot agree
            raw = pd.to_numeric(df[COL_RAW], errors="coerce")
            rsi = 50.0 - raw / SCALE
            situ = rsi > 50.0
            agree = active & situ & (f < 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean forward 12-bar log return after top-decile |forecast| bars minus coin's unconditional mean"
    thr_text = "confirm: negative with t <= -2 and negative in >= 2 coins; reject: positive with t >= +2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_text},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast are bars with RSI above 50 and a short (negative) forecast, so the config does not do what the plan's Fidelity says.",
            "reading": "Situation taken as RSI(14) > 50 from last_history_value (RSI = 50 - value/0.4), expected side short.",
        }

    # ---------- 2. Build samples ----------
    # all |forecast| for pooled thresholds
    all_abs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").abs()
            all_abs.append(f.dropna().values)
    all_abs = np.concatenate(all_abs) if all_abs else np.array([])
    dec_thr = float(np.quantile(all_abs, 0.9)) if all_abs.size else np.nan
    nz = all_abs[all_abs > 0]
    q_edges = np.quantile(nz, [0.2, 0.4, 0.6, 0.8]) if nz.size else None

    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1, fi = close[i], close[i + H], f[i]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(fi)) or c0 <= 0 or c1 <= 0:
                    continue
                rows.append((coin, w, float(np.log(c1 / c0)), abs(float(fi))))
    samp = pd.DataFrame(rows, columns=["coin", "window", "r", "af"])

    coins = list(bars.keys())
    if len(samp):
        drift = samp.groupby("coin")["r"].mean()
        samp["ex"] = samp["r"] - samp["coin"].map(drift)
        samp["extreme"] = (samp["af"] >= dec_thr) & (samp["af"] > 0)

        def grp(a):
            if a == 0:
                return 0
            return int(1 + np.searchsorted(q_edges, a, side="right")) if q_edges is not None else -1

        samp["grp"] = samp["af"].apply(grp)
    ext = samp[samp["extreme"]] if len(samp) else samp

    counts = {"pooled extreme episodes": int(len(ext))}
    per_coin_mean = {}
    for c in coins:
        e = ext[ext["coin"] == c] if len(ext) else ext
        counts[f"extreme episodes {c}"] = int(len(e))
        per_coin_mean[c] = float(e["ex"].mean()) if len(e) else np.nan

    m = float(ext["ex"].mean()) if len(ext) else np.nan
    if len(ext) > 1 and ext["ex"].std(ddof=1) > 0:
        t = float(m / (ext["ex"].std(ddof=1) / np.sqrt(len(ext))))
    else:
        t = np.nan
    n_neg_coins = int(sum(1 for c in coins if np.isfinite(per_coin_mean[c]) and per_coin_mean[c] < 0))
    counts["coins with negative excess"] = n_neg_coins

    # ---------- supporting check ----------
    sup_val = None
    sup_pass = None
    if len(samp):
        g_means = [float(samp.loc[samp["grp"] == g, "ex"].mean()) if (samp["grp"] == g).any() else np.nan
                   for g in range(6)]
        diffs = np.diff(g_means)
        steady = bool(np.all(np.isfinite(g_means)) and np.all(diffs <= 0))
        coin_neg = 0
        for c in coins:
            sc = samp[samp["coin"] == c]
            a = sc.loc[sc["grp"] == 5, "ex"]
            b = sc.loc[sc["grp"] == 0, "ex"]
            if len(a) and len(b) and (a.mean() - b.mean()) < 0:
                coin_neg += 1
        sup_val = float(g_means[5] - g_means[0]) if np.isfinite(g_means[5]) and np.isfinite(g_means[0]) else None
        sup_pass = bool(steady and coin_neg >= 2)
    supporting = {
        "name": "excess return falls steadily from neutral (zero) group through |forecast| quintiles 1-5, and top-minus-neutral negative in >= 2 coins (value: Q5 minus neutral)",
        "value": sup_val,
        "passed": sup_pass,
    }

    # ---------- decision ----------
    min_ok = counts["pooled extreme episodes"] >= 100 and all(counts[f"extreme episodes {c}"] >= 30 for c in coins)
    if not min_ok:
        status = "not observable"
        decided = "The plan's minimum of 30 non-overlapping extreme episodes per coin and 100 pooled is not reached."
    elif np.isfinite(t) and m < 0 and t <= -2 and n_neg_coins >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Pooled excess return after extreme bars is negative with t <= -2, negative in at least 2 coins, and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "The main measure meets the confirm rule (t <= -2, >= 2 coins negative) but the supporting check fails."
    elif np.isfinite(t) and m > 0 and t >= 2:
        status = "rejected"
        decided = "Pooled excess return after extreme bars is positive with t >= +2 (continuation rather than give-back)."
    elif np.isfinite(t) and t <= -2:
        status = "inconclusive"
        decided = "Pooled t <= -2 but fewer than 2 coins agree on a negative excess return."
    else:
        status = "inconclusive"
        decided = "Pooled t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": m if np.isfinite(m) else None,
            "statistic": {"name": "t of the mean on non-overlapping 12-bar blocks", "value": t} if np.isfinite(t) else None,
            "threshold": thr_text,
        },
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": "Top decile is the 90th percentile of |forecast| over all bars pooled across coins and windows (nonzero only), returns are 12-bar log returns on each window's 0,12,24,... grid with each coin's drift being its mean over all its windows, quintiles are pooled quintiles of nonzero |forecast| with zero-forecast bars as neutral, 'steadily' means each group mean is no higher than the previous one, and with only BTC and ETH present the '2 of 3 coins' rules need both coins and the per-coin minimums apply to the coins present.",
    }
