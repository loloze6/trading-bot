import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    RAW = "debug_info.components.close_loc.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            hi = pd.to_numeric(d["high"], errors="coerce").values
            lo = pd.to_numeric(d["low"], errors="coerce").values
            cl = pd.to_numeric(d["close"], errors="coerce").values
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                pos_px = np.where(rng > 0, 2.0 * (cl - lo) / rng - 1.0, 0.0)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
                pos = np.where(np.isnan(raw), pos_px, raw)
            else:
                pos = pos_px
            regime = d["regime"].astype(str).str.lower().values
            agitated = regime != "chop"
            upper = pos > 0
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & upper & agitated & (f > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are long bars with the close in the upper half of the "
                           "day's range in the agitated (non-chop) regime, as the Fidelity's situation requires."),
            "reading": ("The situation is a close above mid-range (raw Donchian position > 0, or from prices where "
                        "not recorded) on a non-chop regime bar, long side."),
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_means = {}
    for coin, wins in bars.items():
        allret = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            cl = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in range(0, len(d), H):
                if i + H >= len(d):
                    break
                if not (np.isfinite(cl[i]) and np.isfinite(cl[i + H])) or cl[i] == 0:
                    continue
                r = cl[i + H] / cl[i] - 1.0
                allret.append(r)
                if np.isfinite(f[i]) and f[i] > 0:
                    coin_rows.append((coin, ts.iloc[i].floor("D"), float(f[i]), r))
        if allret:
            coin_means[coin] = float(np.mean(allret))
            for c, day, fv, r in coin_rows:
                rows.append((c, day, fv, r - coin_means[coin]))

    n_cases = len(rows)
    counts = {"independent grid cases with forecast > 0": int(n_cases)}
    threshold = "weighted mean > 0 with t >= 2 to confirm; < 0 with t <= -2 to reject"
    reading = ("Cases are grid bars (positions 0, 7, 14, ... of each window) with forecast > 0 and a full 7-bar forward "
               "return; the coin mean is over all its grid returns in all windows; t uses day-clustered deviations of "
               "the weighted mean; terciles are the n//3 highest and lowest forecasts, unweighted means; fewer than "
               "100 cases is reported as not observable.")

    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": "forecast-weighted mean excess 7-bar return", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "top third minus bottom third mean excess return", "value": None,
                                 "passed": None},
            "counts": counts,
            "decided_by": "Fewer than 100 independent grid cases with forecast > 0.",
            "reading": reading,
        }

    df = pd.DataFrame(rows, columns=["coin", "day", "f", "x"])
    fw = df["f"].values
    x = df["x"].values
    m = float(np.sum(fw * x) / np.sum(fw))
    dev = fw * (x - m) / np.sum(fw)
    g = pd.Series(dev).groupby(df["day"].values).sum().values
    G = len(g)
    t = None
    if G > 1:
        se = np.sqrt(G / (G - 1.0) * np.sum(g ** 2))
        t = float(m / se) if se > 0 else None
    counts["days the cases fall on"] = int(G)

    # supporting check
    k = n_cases // 3
    sup = None
    if k >= 1:
        s = df.sort_values("f", kind="mergesort").reset_index(drop=True)
        sup = float(s["x"].iloc[-k:].mean() - s["x"].iloc[:k].mean())
    sup_pass = None if sup is None else bool(sup > 0)

    main = {"name": "forecast-weighted mean excess 7-bar return", "value": m,
            "statistic": {"name": "t of weighted mean, same-day cases together", "value": t} if t is not None else None,
            "threshold": threshold}
    supc = {"name": "top third minus bottom third mean excess return", "value": sup, "passed": sup_pass}

    if n_cases < 100:
        status = "not observable"
        decided = "Fewer than 100 independent grid cases with forecast > 0."
    elif t is not None and m > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Weighted mean excess 7-bar return above 0 with t >= 2 and a positive supporting check."
    elif t is not None and m < 0 and t <= -2:
        status = "rejected"
        decided = "Weighted mean excess 7-bar return below 0 with t <= -2."
    elif t is not None and m > 0 and t >= 2:
        status = "inconclusive"
        decided = "Positive main measure with t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 (or undefined): inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supc,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
