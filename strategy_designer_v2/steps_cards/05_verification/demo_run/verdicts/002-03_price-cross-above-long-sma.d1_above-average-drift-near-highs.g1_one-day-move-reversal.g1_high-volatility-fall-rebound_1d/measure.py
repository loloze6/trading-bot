import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.fall.last_history_value"
    VOL_PERIOD, LOOKBACK, SMOOTH = 20, 100, 5
    MIN_PCT_VALUES = 20

    def pct_rank_last(a):
        a = a[~np.isnan(a)]
        if len(a) == 0:
            return np.nan
        return float(np.mean(a <= a[-1]))

    def ols(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        m = ~(np.isnan(x) | np.isnan(y))
        x, y = x[m], y[m]
        if len(x) < 3 or np.var(x) == 0:
            return None, None, int(len(x))
        r = stats.linregress(x, y)
        t = r.slope / r.stderr if r.stderr and r.stderr > 0 else None
        return float(r.slope), (float(t) if t is not None and np.isfinite(t) else None), int(len(x))

    frames = []
    active_total = 0
    active_ok = 0

    for coin, wins in bars.items():
        coin_frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True).copy()
            close = d["close"].astype(float)
            d["ret1"] = close.pct_change()
            d["next_ret"] = close.shift(-1) / close - 1.0
            fc = pd.to_numeric(d[FC], errors="coerce") if FC in d.columns else pd.Series(np.nan, index=d.index)
            d["fc"] = fc
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            d["raw"] = raw
            in_regime = d["regime"].astype(str) == "mean_reversion"

            # situation check: active bars must be regime bars, on a vol-scaled fall, and long
            fall = raw < 0
            active = fc.notna() & (fc != 0)
            ok = active & in_regime & fall & (fc > 0)
            active_total += int(active.sum())
            active_ok += int(ok.sum())

            # recomputed 20-day volatility percentile, inside this window only
            vol = d["ret1"].rolling(VOL_PERIOD, min_periods=VOL_PERIOD).std()
            pct = vol.rolling(LOOKBACK, min_periods=MIN_PCT_VALUES).apply(pct_rank_last, raw=True)
            d["vol_pct"] = pct.rolling(SMOOTH, min_periods=SMOOTH).mean()

            d["in_regime"] = in_regime
            d["coin"] = coin
            coin_frames.append(d[["coin", "ret1", "next_ret", "fc", "in_regime", "vol_pct"]])
        if coin_frames:
            cdf = pd.concat(coin_frames, ignore_index=True)
            coin_mean = cdf["ret1"].mean()  # mean daily return over all windows, within-window returns only
            cdf["excess_next"] = cdf["next_ret"] - coin_mean
            frames.append(cdf)

    agreement = (active_ok / active_total) if active_total > 0 else None
    passed_sit = True if agreement is None else bool(agreement >= 0.9)

    reading = ("The fall is read as the recorded raw VolatilityScaledReturn (last_history_value) below 0 and the regime "
               "as the recorded 'mean_reversion' label; the main regression uses every mean_reversion bar (forecast 0 "
               "included) with an OLS slope t; the supporting check's percentile is recomputed inside each window as "
               "the rank of the 20-bar return std among its last up-to-100 values (at least 20), smoothed over 5 bars "
               "as in the config, and compares OLS slopes of next-bar return on forecast among forecast>0 bars "
               "(>=0.9 minus 0.8-0.9); the 100-bar minimum is applied as a minimum count giving 'not observable'.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "slope of next-bar excess return on forecast in mean_reversion regime",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirms (with check), t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"bars with forecast > 0 in the regime": None},
            "decided_by": ("Fewer than 90% of active bars are long bars in the mean_reversion regime on a negative "
                           "vol-scaled one-day return, so the forecast does not trade the plan's situation."),
            "reading": reading,
        }

    allb = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(
        columns=["coin", "ret1", "next_ret", "fc", "in_regime", "vol_pct", "excess_next"])
    reg = allb[allb["in_regime"].astype(bool)]
    reg = reg.dropna(subset=["fc", "excess_next"])
    slope, t, n_reg = ols(reg["fc"], reg["excess_next"])
    n_pos = int((reg["fc"] > 0).sum())

    pos = allb[(allb["in_regime"].astype(bool)) & (allb["fc"] > 0)].dropna(subset=["fc", "next_ret", "vol_pct"])
    hi = pos[pos["vol_pct"] >= 0.9]
    mid = pos[(pos["vol_pct"] >= 0.8) & (pos["vol_pct"] < 0.9)]
    s_hi, _, n_hi = ols(hi["fc"], hi["next_ret"])
    s_mid, _, n_mid = ols(mid["fc"], mid["next_ret"])
    if s_hi is not None and s_mid is not None:
        diff = float(s_hi - s_mid)
        check_passed = bool(diff > 0)
    else:
        diff = None
        check_passed = None

    if n_pos < 100:
        status = "not observable"
        decided = f"Only {n_pos} bars with forecast > 0 in the regime, below the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and check_passed is True:
        status = "confirmed"
        decided = "The slope's t is >= 2 and the high-vs-mid volatility slope difference is > 0."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is <= -2: larger vol-scaled falls are followed by smaller-than-average next-day returns."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None),
                            "passed": passed_sit},
        "main_measure": {"name": "slope of next-bar return minus coin mean on forecast, mean_reversion bars, pooled",
                         "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": t} if t is not None else None),
                         "threshold": "t >= 2 confirms (with supporting check), t <= -2 rejects, otherwise inconclusive"},
        "supporting_check": {"name": "slope(pct>=0.9) minus slope(0.8<=pct<0.9) among forecast>0 bars",
                             "value": diff, "passed": check_passed},
        "counts": {"bars with forecast > 0 in the regime": n_pos,
                   "regime bars in regression": n_reg,
                   "forecast>0 bars with percentile >= 0.9": int(n_hi),
                   "forecast>0 bars with percentile 0.8-0.9": int(n_mid),
                   "active bars": int(active_total)},
        "decided_by": decided,
        "reading": reading,
    }
