import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.fade1d.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    # ---------- coin means: mean daily return over all windows together (never across windows) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- collect per-bar rows ----------
    act_total = 0
    act_agree = 0
    gains = []
    sig_fc = []
    abs_fc = []
    adj_next = []
    n_nonzero_pos = 0

    for coin, wins in bars.items():
        mu = coin_mean[coin]
        for w, df in wins.items():
            df = df.sort_values("timestamp") if "timestamp" in df.columns else df
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            if n == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            alloc = (pd.to_numeric(df[ALLOC], errors="coerce").to_numpy(dtype=float)
                     if ALLOC in df.columns else np.full(n, np.nan))
            lhv = (pd.to_numeric(df[LHV], errors="coerce").to_numpy(dtype=float)
                   if LHV in df.columns else np.full(n, np.nan))

            # last day's move (1-bar return), inside the window; first bar falls back to the component's raw value
            prev_ret = np.full(n, np.nan)
            if n > 1:
                prev_ret[1:] = c[1:] / c[:-1] - 1.0
            move = np.where(np.isfinite(prev_ret), prev_ret, lhv)

            # next-bar return inside the window
            nxt = np.full(n, np.nan)
            if n > 1:
                nxt[:-1] = c[1:] / c[:-1] - 1.0

            # ---------- situation check ----------
            active = np.isfinite(fc) & (fc != 0)
            act_total += int(active.sum())
            ok = active & np.isfinite(move) & (move != 0) & (np.sign(fc) == -np.sign(move))
            act_agree += int(ok.sum())

            # ---------- main measure: every bar with a valid next return and position ----------
            valid = np.isfinite(nxt) & np.isfinite(alloc) & np.isfinite(mu)
            g = alloc[valid] * (nxt[valid] - mu)
            gains.append(g)
            n_nonzero_pos += int((alloc[valid] != 0).sum())

            # ---------- supporting check rows ----------
            v2 = np.isfinite(nxt) & np.isfinite(fc) & np.isfinite(mu)
            sig_fc.append(np.sign(fc[v2]))
            abs_fc.append(np.abs(fc[v2]))
            adj_next.append(nxt[v2] - mu)

    agreement = float(act_agree / act_total) if act_total > 0 else 0.0
    passed_sit = bool(act_total > 0 and agreement >= 0.9)

    main_name = "mean market-adjusted position gain per bar, 1 bar, pooled"
    threshold = "confirm t >= 2 with supporting check > 0; reject t <= -2; otherwise inconclusive; >= 1000 non-zero-position bars"
    reading = ("The plan's situation (a large move faded) is read as any non-zero 1-bar move with the forecast on the opposite side, "
               "taken from the in-window price return (the component's raw value on a window's first bar); the main measure is pooled over every bar "
               "with a next-bar return (zero positions included, as 'on every bar' says), the thirds are split by rank of |forecast| over all such bars "
               "(bottom n//3 and top n//3), and the 1000-bar minimum counts bars with a non-zero position that have a next-bar return.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"bars with a non-zero position": int(n_nonzero_pos), "active forecast bars": int(act_total)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars after a move with the forecast on the opposite side "
                           "(a fade of the last day's move), so the config does not do what the plan's Fidelity says."),
            "reading": reading,
        }

    g = np.concatenate(gains) if gains else np.array([])
    n = g.size
    mean_g = float(np.mean(g)) if n else None
    if n > 1:
        sd = float(np.std(g, ddof=1))
        t = float(mean_g / (sd / np.sqrt(n))) if sd > 0 else 0.0
    else:
        t = None

    # supporting check
    s = np.concatenate(sig_fc) if sig_fc else np.array([])
    a = np.concatenate(abs_fc) if abs_fc else np.array([])
    y = np.concatenate(adj_next) if adj_next else np.array([])
    m = s.size
    diff = None
    k = m // 3
    if k > 0:
        order = np.argsort(a, kind="mergesort")
        bot = order[:k]
        top = order[m - k:]
        top_mean = float(np.mean(s[top] * y[top]))
        bot_mean = float(np.mean(s[bot] * y[bot]))
        diff = top_mean - bot_mean
    check_pass = (diff is not None) and (diff > 0)

    counts = {"bars with a non-zero position": int(n_nonzero_pos), "bars in main measure": int(n)}

    if n_nonzero_pos < 1000 or t is None:
        status = "not observable"
        decided = f"Only {n_nonzero_pos} bars with a non-zero position, below the plan's minimum of 1000."
    elif t >= 2 and check_pass:
        status = "confirmed"
        decided = "The mean market-adjusted gain has t >= 2 and the top-minus-bottom third difference is greater than 0."
    elif t <= -2:
        status = "rejected"
        decided = "The mean market-adjusted gain has t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "The mean market-adjusted gain has t >= 2 but the supporting check fails (top minus bottom third not greater than 0)."
    else:
        status = "inconclusive"
        decided = "The t of the mean market-adjusted gain lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_g,
            "statistic": ({"name": "ordinary t of the mean", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "top third minus bottom third of |forecast|, sign(forecast) x (next-day return - coin mean)",
            "value": diff,
            "passed": (bool(check_pass) if diff is not None else None),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
