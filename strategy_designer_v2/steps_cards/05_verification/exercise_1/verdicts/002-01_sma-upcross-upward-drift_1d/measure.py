import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    recs = []  # (window, fwd_return, forecast)
    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys()):
            df = bars[coin][win].reset_index(drop=True)
            if "close" not in df.columns or "forecast" not in df.columns:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1, f = close[t], close[t + H], fc[t]
                if np.isnan(c0) or np.isnan(c1) or np.isnan(f) or c0 == 0:
                    continue
                recs.append((f"{coin}:{win}", c1 / c0 - 1.0, f))

    reading = ("Blocks start every 10 rows from each window's first row, using only blocks whose 10-bar end is inside "
               "the window; the random-point baseline is the pooled mean (and hit rate) over all such blocks; the "
               "per-window excess is that window's long-block mean minus the pooled baseline; the slope is fitted "
               "over all blocks; 'carried by a single window' means the pooled excess turns <= 0 once the window "
               "with the largest summed excess is removed; a failed hit-rate test with t >= 2 counts as inconclusive.")

    main_name = "mean excess 10-bar forward return in long blocks over all-block mean (pooled, before costs)"
    thr = "> 0 with t >= 2 to confirm; <= 0 rejects"

    if not recs:
        return {"status": "inconclusive",
                "main_measure": {"name": main_name, "value": None, "threshold": thr},
                "supporting_check": None, "cases": 0,
                "decided_by": "Inconclusive: fewer than 20 non-overlapping 10-bar long blocks.",
                "reading": reading}

    d = pd.DataFrame(recs, columns=["win", "ret", "fc"])
    base_mean = float(d["ret"].mean())
    base_hit = float((d["ret"] > 0).mean())
    long_ = d[d["fc"] > 0].copy()
    n_long = int(len(long_))
    long_["exc"] = long_["ret"] - base_mean
    wins_with_long = sorted(long_["win"].unique().tolist())
    n_wins = len(wins_with_long)

    mean_exc = float(long_["exc"].mean()) if n_long > 0 else None
    if n_long > 1:
        sd = float(long_["exc"].std(ddof=1))
        t_stat = float(mean_exc / (sd / np.sqrt(n_long))) if sd > 0 else (
            float("inf") if mean_exc > 0 else (float("-inf") if mean_exc < 0 else 0.0))
    else:
        t_stat = None
    hit_long = float((long_["ret"] > 0).mean()) if n_long > 0 else None
    hit_pass = None if hit_long is None else bool(hit_long > base_hit)

    slope = None
    if len(d) >= 3 and d["fc"].nunique() > 1:
        slope = float(stats.linregress(d["fc"].values, d["ret"].values).slope)

    per_win = long_.groupby("win")["exc"].mean() if n_long > 0 else pd.Series(dtype=float)
    n_pos_wins = int((per_win > 0).sum())

    carried = False
    if n_long > 0 and n_wins >= 1:
        sums = long_.groupby("win")["exc"].sum()
        top = sums.idxmax()
        rest = long_[long_["win"] != top]
        carried = bool(len(rest) == 0 or rest["exc"].mean() <= 0)

    sup = {"name": "hit rate in long blocks minus all-block hit rate (second view: slope of return on forecast)",
           "value": None if hit_long is None else float(hit_long - base_hit),
           "passed": hit_pass,
           "hit_rate_long": hit_long, "hit_rate_all": base_hit,
           "slope_return_on_forecast": slope,
           "slope_positive": None if slope is None else bool(slope > 0),
           "t_stat": t_stat, "windows_with_long_blocks": n_wins,
           "windows_with_positive_excess": n_pos_wins}

    if n_long < 20 or n_wins < 2:
        status = "inconclusive"
        decided = (f"Inconclusive: {n_long} non-overlapping long blocks (need >= 20) across {n_wins} windows "
                   f"with long blocks (need >= 2).")
    elif mean_exc <= 0:
        status = "rejected"
        if t_stat is not None and t_stat <= -2:
            decided = "Rejected: mean excess <= 0 with t <= -2, a reversal (the cross marks exhaustion)."
        else:
            decided = "Rejected: mean excess 10-bar return in long blocks is <= 0."
    elif t_stat is not None and t_stat >= 2 and hit_pass and n_pos_wins >= 4 and not carried:
        status = "confirmed"
        decided = ("Confirmed: mean excess > 0 with t >= 2, long-block hit rate above the unconditional one, "
                   "and excess positive in at least 4 windows with long blocks.")
    else:
        status = "inconclusive"
        why = []
        if t_stat is None or t_stat < 2:
            why.append("excess > 0 but t < 2")
        if not hit_pass:
            why.append("hit rate not above unconditional")
        if n_pos_wins < 4:
            why.append("excess positive in fewer than 4 windows")
        if carried:
            why.append("result carried by a single window")
        decided = "Inconclusive: " + "; ".join(why) + "."

    return {"status": status,
            "main_measure": {"name": main_name, "value": mean_exc, "threshold": thr},
            "supporting_check": sup,
            "cases": n_long,
            "decided_by": decided,
            "reading": reading}
