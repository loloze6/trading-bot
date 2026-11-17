import numpy as np
import pandas as pd


def measure(bars):
    POS = "postRebalance_current_allocation"
    RAW = "debug_info.components.fade_move.last_history_value"

    # ---------- gather per-coin, per-window series ----------
    frames = []  # (coin, window, df)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            if "timestamp" in d.columns:
                d = d.sort_values("timestamp")
            d = d.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            d["_move"] = close / close.shift(1) - 1.0          # this bar's one-day move (inside window)
            d["_next"] = close.shift(-1) / close - 1.0          # next bar's return (inside window)
            d["_fc"] = pd.to_numeric(d["forecast"], errors="coerce") if "forecast" in d.columns else np.nan
            d["_pos"] = pd.to_numeric(d[POS], errors="coerce") if POS in d.columns else np.nan
            d["_raw"] = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else np.nan
            frames.append((coin, w, d))

    # ---------- situation check ----------
    # Orientation of the raw column vs. the price move (the raw value may or may not already carry the negation);
    # used only on bars where the price move cannot be computed inside the window (first bar of each window).
    agree_sign, total_sign = 0, 0
    for _, _, d in frames:
        m = d["_move"].notna() & d["_raw"].notna() & (d["_move"] != 0) & (d["_raw"] != 0)
        total_sign += int(m.sum())
        agree_sign += int((np.sign(d.loc[m, "_move"]) == np.sign(d.loc[m, "_raw"])).sum())
    raw_orient = 1.0 if (total_sign == 0 or agree_sign >= total_sign / 2.0) else -1.0

    n_active, n_ok = 0, 0
    for _, _, d in frames:
        mv = d["_move"].copy()
        fill = mv.isna() & d["_raw"].notna()
        mv[fill] = raw_orient * d.loc[fill, "_raw"]
        active = d["_fc"].notna() & (d["_fc"] != 0)
        n_active += int(active.sum())
        expected_side = -np.sign(mv)  # fade the move: long after a fall, short after a rise
        ok = active & mv.notna() & (mv != 0) & (np.sign(d["_fc"]) == expected_side)
        n_ok += int(ok.sum())
    agreement = float(n_ok / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled mean next-day timing gain: position x (next return - coin's mean daily return), before costs"
    main_thr = "confirm: mean > 0 with ordinary t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2"
    sup_name = "per-unit-|position| timing gain, top third minus bottom third by |position|"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"non-zero-position bars": None},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are on the side opposite to the bar's one-day move, which the plan's fade-the-move situation requires.",
            "reading": "The situation is any non-zero one-day move, expected side opposite to the move; the move comes from closes inside the window, and from the oriented raw component value on each window's first bar.",
        }

    # ---------- coin mean daily return over all its windows ----------
    coin_rets = {}
    for coin, _, d in frames:
        coin_rets.setdefault(coin, []).append(d["_next"].dropna().values)
    coin_mu = {c: (float(np.mean(np.concatenate(v))) if sum(len(x) for x in v) > 0 else np.nan)
               for c, v in coin_rets.items()}

    # ---------- timing gain per bar ----------
    gains, poss = [], []
    for coin, _, d in frames:
        mu = coin_mu.get(coin, np.nan)
        m = d["_pos"].notna() & d["_next"].notna()
        if not np.isfinite(mu):
            continue
        g = d.loc[m, "_pos"].values * (d.loc[m, "_next"].values - mu)
        gains.append(g)
        poss.append(d.loc[m, "_pos"].values)
    gains = np.concatenate(gains) if gains else np.array([])
    poss = np.concatenate(poss) if poss else np.array([])

    n_all = int(len(gains))
    nz = poss != 0
    n_nonzero = int(nz.sum())

    mean_g = float(np.mean(gains)) if n_all > 0 else None
    t_g = None
    if n_all > 1:
        sd = float(np.std(gains, ddof=1))
        t_g = float(mean_g / (sd / np.sqrt(n_all))) if sd > 0 else None

    # ---------- supporting check ----------
    sup_val, sup_pass = None, None
    if n_nonzero >= 3:
        g_nz, a_nz = gains[nz], np.abs(poss[nz])
        order = np.argsort(a_nz, kind="mergesort")
        k = len(order) // 3
        bot, top = order[:k], order[-k:]
        if k > 0 and a_nz[top].sum() > 0 and a_nz[bot].sum() > 0:
            top_pu = float(g_nz[top].sum() / a_nz[top].sum())
            bot_pu = float(g_nz[bot].sum() / a_nz[bot].sum())
            sup_val = top_pu - bot_pu
            sup_pass = bool(sup_val > 0)

    counts = {"non-zero-position bars": n_nonzero, "bars in main measure": n_all}

    if n_nonzero < 1000:
        status = "not observable"
        decided = f"Only {n_nonzero} non-zero-position bars, below the plan's minimum of 1000."
    elif mean_g is not None and t_g is not None and mean_g > 0 and t_g >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The main mean is positive with t >= 2 and the top-minus-bottom per-unit gain is positive."
    elif mean_g is not None and t_g is not None and mean_g < 0 and t_g <= -2:
        status = "rejected"
        decided = "The main mean is negative with t <= -2."
    else:
        status = "inconclusive"
        if t_g is not None and t_g >= 2:
            decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
        else:
            decided = "The main t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_g,
            "statistic": ({"name": "ordinary t of the mean", "value": t_g} if t_g is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "The main mean pools every bar with a position and a next close in the same window, zero positions included. The supporting check ranks only the non-zero-position bars into thirds by |position| and measures each third's gain per unit as sum(gain)/sum(|position|). The plan's 'else inconclusive' minimum of 1000 non-zero-position bars is applied as 'not observable', as the workflow requires.",
    }
