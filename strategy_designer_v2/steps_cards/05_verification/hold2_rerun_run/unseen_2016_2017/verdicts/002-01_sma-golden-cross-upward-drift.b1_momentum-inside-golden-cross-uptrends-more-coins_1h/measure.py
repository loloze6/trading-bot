import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 240
    FAST, SLOW = 1200, 4800

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_sma_recomputed = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            regime = d["regime"].astype(str)
            # situation: 1200-bar SMA above 4800-bar SMA; recomputed from prices where the
            # window holds enough bars, else taken from the detector's recorded regime
            sit = (regime == "trending").to_numpy()
            if len(d) >= SLOW:
                f = close.rolling(FAST, min_periods=FAST).mean()
                s = close.rolling(SLOW, min_periods=SLOW).mean()
                ok = (f.notna() & s.notna()).to_numpy()
                sit = np.where(ok, (f > s).to_numpy(), sit)
                n_sma_recomputed += int(ok.sum())
            active = (fc.notna() & (fc != 0)).to_numpy()
            n_active += int(active.sum())
            # expected side: long (a rise)
            n_agree += int((active & sit & (fc > 0).to_numpy()).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)
    situation_check = {"agreement": agreement, "passed": passed}

    reading_sit = ("the 4800-bar SMA cannot be rebuilt inside windows shorter than 4800 bars, so on "
                   "those bars the situation is read from the recorded regime 'trending' "
                   f"(SMAs recomputed from prices on {n_sma_recomputed} bars), with long (forecast > 0) "
                   "as the expected side")

    main_name = "pooled OLS slope of next 240-bar excess return on forecast, trending grid bars"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are long bars of the plan's "
                           "situation (1200-bar SMA above the 4800-bar SMA)"),
            "reading": reading_sit,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy()
            regime = d["regime"].astype(str).to_numpy()
            n = len(d)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, w, regime[t], fc[t], c1 / c0 - 1.0))
    g = pd.DataFrame(rows, columns=["coin", "window", "regime", "forecast", "fwd"])

    if len(g):
        g["coin_mean"] = g.groupby("coin")["fwd"].transform("mean")
        g["excess"] = g["fwd"] - g["coin_mean"]
        tr = g[(g["regime"] == "trending") & g["forecast"].notna() & g["excess"].notna()]
    else:
        tr = g

    n_tr = int(len(tr))
    n_zero = int((tr["forecast"] == 0).sum()) if n_tr else 0
    n_pos = int((tr["forecast"] > 0).sum()) if n_tr else 0
    counts = {"grid cases in trending": n_tr,
              "cases at forecast 0": n_zero,
              "cases with forecast > 0": n_pos}

    slope, tval = None, None
    if n_tr >= 3 and tr["forecast"].nunique() > 1:
        lr = stats.linregress(tr["forecast"].to_numpy(float), tr["excess"].to_numpy(float))
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
            "threshold": threshold}

    reading = (reading_sit + "; the coin's mean 240-bar return is the mean over all its windows' "
               "non-overlapping grid bars (all regimes), the regression has an intercept, and the plan's "
               "minimum counts are applied as 'not observable'.")

    if n_tr < 200:
        status, decided = "not observable", f"fewer than 200 grid cases in trending ({n_tr})."
    elif n_zero < 50:
        status, decided = "not observable", f"fewer than 50 cases at forecast 0 ({n_zero})."
    elif n_pos < 50:
        status, decided = "not observable", f"fewer than 50 cases with forecast > 0 ({n_pos})."
    elif tval is None:
        status, decided = "inconclusive", "the slope's t could not be computed, so neither rule is met."
    elif slope > 0 and tval >= 2:
        status, decided = "confirmed", "the slope is positive with t >= 2."
    elif slope < 0 and tval <= -2:
        status, decided = "rejected", "the slope is negative with t <= -2."
    else:
        status, decided = "inconclusive", "the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
