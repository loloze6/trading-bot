import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    AGE = "debug_info.components.age.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    # ---------- collect rows per coin ----------
    frames = []
    for coin, wins in bars.items():
        for win, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True).copy()
            close = pd.to_numeric(d["close"], errors="coerce")
            d["fwd"] = close.shift(-H) / close - 1.0          # inside this window only
            d["pos_in_win"] = np.arange(len(d))
            d["coin"] = coin
            d["win"] = win
            d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce")
            d["age"] = pd.to_numeric(d[AGE], errors="coerce") if AGE in d.columns else np.nan
            d["alloc"] = pd.to_numeric(d[ALLOC], errors="coerce") if ALLOC in d.columns else np.nan
            frames.append(d[["coin", "win", "pos_in_win", "forecast", "age", "alloc", "fwd"]])
    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"non-overlapping 20-bar blocks with forecast > 0": 0},
            "decided_by": "No bars in the record.", "reading": "none",
        }
    allr = pd.concat(frames, ignore_index=True)

    # ---------- situation check ----------
    # Adapted situation: close above SMA(200) for n consecutive bars (graded) -> age > 0; side long.
    act = allr[allr["forecast"].notna() & (allr["forecast"] != 0)]
    act = act[act["age"].notna()]
    n_active = int(len(act))
    if n_active > 0:
        agree = float(((act["age"] > 0) & (act["forecast"] > 0)).mean())
    else:
        agree = 1.0
    passed = bool(agree >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agree, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": (f"Only {agree:.1%} of active bars are long bars with the close above its SMA(200) "
                           f"(age > 0), below the 90% the plan's adapted situation requires."),
            "reading": "Situation taken as the adapted graded one: recorded age > 0 (above SMA) with a long forecast.",
        }

    # ---------- excess return vs coin's pooled mean 20-bar return ----------
    coin_mean = allr.dropna(subset=["fwd"]).groupby("coin")["fwd"].mean()
    allr["excess"] = allr["fwd"] - allr["coin"].map(coin_mean)

    # non-overlapping grid: positions 0, 20, 40, ... of each window
    grid = allr[(allr["pos_in_win"] % H == 0)].dropna(subset=["excess", "forecast"])

    n_blocks_pos = int((grid["forecast"] > 0).sum())
    n_blocks = int(len(grid))

    # OLS of excess on forecast, pooled
    slope, tstat = None, None
    if n_blocks >= 3 and grid["forecast"].nunique() > 1:
        res = stats.linregress(grid["forecast"].values, grid["excess"].values)
        slope = float(res.slope)
        tstat = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    # position-weighted mean excess return (weights = position held after the bar's trade)
    pw = grid.dropna(subset=["alloc"])
    pw = pw[pw["alloc"] > 0]
    pw_mean = float((pw["excess"] * pw["alloc"]).sum() / pw["alloc"].sum()) if len(pw) and pw["alloc"].sum() > 0 else None

    # supporting check: age 5..20 on the grid
    early = grid[(grid["age"] >= 5) & (grid["age"] <= 20)]
    n_early = int(len(early))
    early_mean = float(early["excess"].mean()) if n_early > 0 else None
    early_pass = (early_mean < 0) if early_mean is not None else None

    counts = {
        "non-overlapping 20-bar blocks with forecast > 0": n_blocks_pos,
        "non-overlapping 20-bar blocks (all)": n_blocks,
        "blocks with age 5 to 20": n_early,
    }

    main = {
        "name": "pooled OLS slope of forward 20-bar excess return on forecast",
        "value": slope,
        "statistic": {"name": "OLS t of slope (non-overlapping 20-bar blocks)", "value": tstat} if tstat is not None else None,
        "threshold": "confirm: slope > 0 with t >= 2 and position-weighted mean excess > 0; reject: slope < 0 with t <= -2",
    }
    supporting = {"name": "mean forward 20-bar excess return at age 5-20 (< 0)",
                  "value": early_mean, "passed": early_pass}

    reading = ("Used non-overlapping 20-bar blocks at window positions 0,20,40,... with plain OLS t over all grid bars "
               "(forecast 0 included), the coin benchmark as the mean of all its in-window forward 20-bar returns, "
               "position weights as postRebalance_current_allocation on the grid, and the supporting check on the same grid.")

    if n_blocks_pos < 30:
        status = "not observable"
        decided = f"Only {n_blocks_pos} non-overlapping 20-bar blocks with forecast > 0, fewer than the 30 the plan requires."
    elif tstat is None or slope is None:
        status = "inconclusive"
        decided = "The slope t-statistic could not be computed, so neither confirm nor reject is met."
    elif slope > 0 and tstat >= 2 and pw_mean is not None and pw_mean > 0:
        status = "confirmed"
        decided = f"Slope is positive with t = {tstat:.2f} >= 2 and the position-weighted mean excess return {pw_mean:.4f} > 0."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = f"Slope is negative with t = {tstat:.2f} <= -2."
    else:
        status = "inconclusive"
        if tstat >= 2:
            decided = (f"Slope t = {tstat:.2f} >= 2 but the position-weighted mean excess return "
                       f"({pw_mean}) is not above 0, so the confirm rule is not met.")
        else:
            decided = f"Slope t = {tstat:.2f} lies between -2 and 2, which the plan calls inconclusive."

    main["position_weighted_mean_excess"] = pw_mean

    return {
        "status": status,
        "situation_check": {"agreement": agree, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
