import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LOC_COL = "debug_info.components.loc_from_high.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    coin_mean = {}
    case_rows = []  # (forecast, next-day return, coin)

    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = df["forecast"].astype(float)

            # Volume ratio: today's volume over the mean of the prior 20 days (current bar excluded).
            prior_mean = vol.rolling(20, min_periods=20).mean().shift(1)
            vr = vol / prior_mean
            vr = vr.where(prior_mean > 0)
            # Where the prior 20 bars are not in the window, fall back on the detector's recorded regime.
            regime_heavy = df["regime"].astype(str) == "mean_reversion"
            heavy = np.where(vr.notna(), vr >= 2.0, regime_heavy)
            heavy = pd.Series(heavy, index=df.index).astype(bool)

            # Graded close location from the high: 0 at the high, 1 at the low.
            if LOC_COL in df.columns:
                loc = pd.to_numeric(df[LOC_COL], errors="coerce")
            else:
                loc = pd.Series(np.nan, index=df.index)
            rng = (df["high"] - df["low"]).astype(float)
            loc_px = ((df["high"] - df["close"]) / rng).where(rng > 0)
            loc = loc.fillna(loc_px)
            loc_ok = loc.fillna(0.0) > 0  # a close away from the high gives a long size

            situation = heavy & loc_ok
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            # next-day returns inside the window
            ret = close.shift(-1) / close - 1.0
            all_rets.append(ret.dropna().values)
            mask = (fc > 0) & ret.notna()
            for f, r in zip(fc[mask].values, ret[mask].values):
                case_rows.append((float(f), float(r), coin))

        allr = np.concatenate(all_rets) if all_rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if allr.size else np.nan

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    threshold_txt = ("confirm: slope t >= 2 with forecast-weighted mean excess > 0 and >= 100 cases; "
                     "reject: slope t <= -2 with >= 100 cases")
    reading = ("Situation bars are bars whose volume is at least 2x the mean of the prior 20 bars (recomputed "
               "from prices, the recorded regime used where the window lacks 20 prior bars) with a close "
               "location from the high above 0, on the long side; cases are all forecast>0 bars with a next "
               "bar in the same window (a 1-bar grid is every bar), pooled over coins and windows, the excess "
               "removing each coin's mean 1-bar return over all its windows, and the slope t is the OLS t "
               "of excess return on forecast.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are heavy-volume (>=2x prior "
                           "20-day mean) days with a close below the high and a long forecast."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    f = np.array([c[0] for c in case_rows], dtype=float)
    ex = np.array([c[1] - coin_mean[c[2]] for c in case_rows], dtype=float)
    ok = np.isfinite(f) & np.isfinite(ex)
    f, ex = f[ok], ex[ok]
    n_cases = int(len(f))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(f) > 0:
        lr = stats.linregress(f, ex)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    wmean = float(np.sum(ex * f) / np.sum(f)) if n_cases > 0 and np.sum(f) > 0 else None
    support_pass = (wmean is not None and wmean > 0)

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} cases with forecast > 0, below the plan's minimum of 100 cases."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither rule is met."
    elif t_slope >= 2 and support_pass:
        status = "confirmed"
        decided = "Slope t >= 2 and forecast-weighted mean excess return > 0 with at least 100 cases (confirm rule)."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Slope t <= -2 with at least 100 cases (reject rule)."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Slope t >= 2 but the forecast-weighted mean excess return is at or below 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "Slope t between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of next-day excess return on forecast, over cases with forecast > 0",
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "forecast-weighted mean next-day excess return > 0",
            "value": wmean,
            "passed": (bool(support_pass) if wmean is not None else None),
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
