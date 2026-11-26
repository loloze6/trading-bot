import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FC = "forecast"
    RAW = "debug_info.components.vol_growth.last_history_value"
    PROFILE_PERIOD = 60
    PROFILE_LEVEL = -10.0  # veto: price evolution >= -10 -> chop; falling is < -10

    def price_evolution(close):
        # PriceEvolutionComponent(period 60, scaling 1): % change over 60 bars, inside the window
        return (close / close.shift(PROFILE_PERIOD) - 1.0) * 100.0

    def log_vol_ratio(vol):
        recent = vol.rolling(30, min_periods=30).mean()
        prior = vol.shift(30).rolling(30, min_periods=30).mean()
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.log(recent / prior)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df[FC], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            pe = price_evolution(close)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series(["?"] * len(df))
            # falling profile: price evolution < -10 where computable in the window,
            # else the detector's own decision (regime 'unknown' = not vetoed)
            falling = np.where(pe.notna(), pe < PROFILE_LEVEL, regime == "unknown")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw = raw.where(raw.notna(), log_vol_ratio(vol))
            active = fc.notna() & (fc != 0)
            for i in np.where(active.values)[0]:
                n_active += 1
                r = raw.iloc[i]
                if bool(falling[i]) and pd.notna(r) and r != 0 and np.sign(r) == np.sign(fc.iloc[i]):
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "OLS slope of 5-bar excess return on forecast (grid cases, nonzero forecast)"
    threshold = "confirm t >= 2 (with positive-minus-negative difference > 0); reject t <= -2; at least 100 cases"
    reading = ("Falling profile recomputed as 60-bar % price change < -10 inside each window (detector regime "
               "'unknown' where 60 prior bars are not in the window), expected side = sign of the raw log volume "
               "ratio; the slope is one pooled least-squares fit with intercept over all coins' grid cases, each "
               "coin's drift being its mean grid 5-bar return over all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on expected side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are falling-profile bars whose "
                           "forecast sign matches the sign of the log volume ratio (growth long, shrinkage short)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rets = []
        cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] != 0:
                    cases.append((fc[i], r))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for f, r in cases:
            xs.append(float(f))
            ys.append(r - drift)

    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    n_cases = int(len(xs))
    n_pos = int((xs > 0).sum())
    n_neg = int((xs < 0).sum())

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    diff = None
    if n_pos > 0 and n_neg > 0:
        diff = float(ys[xs > 0].mean() - ys[xs < 0].mean())
    sup_pass = None if diff is None else bool(diff > 0)

    counts = {"grid cases with a nonzero forecast": n_cases,
              "cases with a positive forecast": n_pos,
              "cases with a negative forecast": n_neg}

    if n_cases < 100:
        status = "not observable"
        decided = f"Fewer than 100 grid cases with a nonzero forecast ({n_cases})."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope has t >= 2 and the positive-minus-negative excess return difference is above 0, with at least 100 cases."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope has t <= -2, with at least 100 cases."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope has t >= 2 but the supporting difference is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
                         "threshold": threshold},
        "supporting_check": {"name": "mean excess 5-bar return, positive minus negative forecast cases",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
