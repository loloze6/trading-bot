import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FC = "forecast"
    LHV = "debug_info.components.scaled_day.last_history_value"
    CALM = "trending"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df[FC], errors="coerce")
            active = fc.notna() & (fc != 0)
            if not active.any():
                continue
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            if LHV in df.columns:
                z = pd.to_numeric(df[LHV], errors="coerce")
            else:
                z = pd.Series(np.nan, index=df.index)
            ok = (reg == CALM) & z.notna() & (np.sign(fc) == np.sign(z)) & (z != 0)
            n_active += int(active.sum())
            n_agree += int((ok & active).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are calm-regime bars whose "
                           "forecast sign follows the sign of the standardised scaled day return"
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": "The situation is checked as regime == 'trending' (detector's vol percentile <= 0.5) "
                       "and sign(forecast) == sign(recorded standardised scaled_day value).",
        }

    # ---------- 2. grid samples ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
            reg = df["regime"].astype(str).to_numpy()
            if LHV in df.columns:
                z = pd.to_numeric(df[LHV], errors="coerce").to_numpy(dtype=float)
            else:
                z = np.full(len(df), np.nan)
            for i in range(0, len(df) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append({"coin": coin, "r": c1 / c0 - 1.0, "fc": fc[i],
                             "z": z[i], "calm": reg[i] == CALM})
    g = pd.DataFrame(rows, columns=["coin", "r", "fc", "z", "calm"])
    if len(g):
        coin_mean = g.groupby("coin")["r"].mean()
        g["ex"] = g["r"] - g["coin"].map(coin_mean)
    else:
        g["ex"] = []

    calm = g[g["calm"] & g["fc"].notna()]
    prod_calm = (calm["fc"] / 10.0) * calm["ex"]
    n_calm = int(len(prod_calm))

    hv = g[(~g["calm"]) & g["z"].notna()]
    prod_hv = (hv["z"] / 10.0) * hv["ex"]
    n_hv = int(len(prod_hv))

    mean_calm = float(prod_calm.mean()) if n_calm > 0 else None
    t_calm = None
    if n_calm > 1:
        sd = float(prod_calm.std(ddof=1))
        if sd > 0:
            t_calm = mean_calm / (sd / np.sqrt(n_calm))
    mean_hv = float(prod_hv.mean()) if n_hv > 0 else None
    diff = (mean_calm - mean_hv) if (mean_calm is not None and mean_hv is not None) else None
    sup_pass = (diff > 0) if diff is not None else None

    reading = ("Calm bars are grid bars with regime 'trending' and high-vol bars the other grid bars; the coin's "
               "mean 5-bar return is the mean of its non-overlapping grid returns over all windows; calm bars with "
               "zero forecast are kept as zero products; the high-vol product uses the recorded standardised "
               "scaled_day value in place of the forecast, i.e. (value / 10) x excess return; the 100-case minimum "
               "is counted on calm grid bars with a valid 5-bar return.")

    main = {"name": "mean of (forecast/10) x excess 5-bar return on calm grid bars",
            "value": mean_calm,
            "statistic": ({"name": "t of the mean", "value": float(t_calm)} if t_calm is not None else None),
            "threshold": "confirm: mean > 0 with t >= 2 and supporting difference > 0; reject: mean < 0 with t <= -2"}
    support = {"name": "calm mean minus high-vol mean of the product",
               "value": diff, "passed": sup_pass}
    counts = {"calm grid cases": n_calm, "high-vol grid cases": n_hv}

    if n_calm < 100:
        status = "not observable"
        decided = f"Only {n_calm} calm grid cases, below the plan's minimum of 100."
    elif t_calm is None:
        status = "inconclusive"
        decided = "The t-statistic cannot be computed (zero dispersion), so neither rule is met."
    elif mean_calm > 0 and t_calm >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The calm mean is positive with t >= 2 and the calm minus high-vol difference is above 0."
    elif mean_calm < 0 and t_calm <= -2:
        status = "rejected"
        decided = "The calm mean is negative with t <= -2."
    elif t_calm >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails (difference not above 0), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
