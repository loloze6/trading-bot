import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    PP = "debug_info.components.loc_low.post_pipeline_value"
    HEAVY = "mean_reversion"

    # ---------- 1. Situation check: heavy volume (vr >= 2, prior 20-bar mean), long side ----------
    n_active = 0
    n_agree = 0
    n_active_unverifiable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            vol = pd.to_numeric(d["volume"], errors="coerce")
            base = vol.rolling(20, min_periods=20).mean().shift(1)
            vr = vol / base
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            active = fc != 0
            verifiable = vr.notna() & np.isfinite(vr)
            n_active_unverifiable += int((active & ~verifiable).sum())
            act_v = active & verifiable
            n_active += int(act_v.sum())
            situ = vr >= 2.0 - 1e-9
            n_agree += int((act_v & situ & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = (
        "The volume ratio is recomputed inside each window as volume over the mean of the 20 prior bars, so active bars "
        "with fewer than 20 prior bars in their window are left out of the agreement; heavy-volume days are the bars "
        "with regime mean_reversion and a next-day return in the same window; the coin's mean daily return is over all "
        "its 1-day returns in all windows; the slope's t is the OLS slope over its standard error; the 'other heavy-volume "
        "days' are heavy days with loc_low post_pipeline_value below 8.4; the minimum counts make the result "
        "'not observable' when not reached."
    )

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active,
                       "active bars without 20 prior bars": n_active_unverifiable},
            "decided_by": ("Fewer than 90% of the active bars are heavy-volume days (volume >= 2x its prior 20-day "
                           "mean) with a long forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_rows = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            r1 = close.shift(-1) / close - 1.0
            coin_rets.append(r1.dropna().values)
            pp = pd.to_numeric(d[PP], errors="coerce") if PP in d.columns else pd.Series(np.nan, index=d.index)
            sub = pd.DataFrame({
                "coin": coin,
                "fc": pd.to_numeric(d[FC], errors="coerce"),
                "pp": pp,
                "r1": r1,
                "heavy": d["regime"].astype(str) == HEAVY,
            })
            coin_rows.append(sub)
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        mu = float(np.mean(allr)) if allr.size else np.nan
        for sub in coin_rows:
            sub = sub[sub["heavy"]].copy()
            sub["ex"] = sub["r1"] - mu
            rows.append(sub)

    data = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=["fc", "pp", "ex"])
    main = data.dropna(subset=["fc", "ex"])
    n_heavy = int(len(main))

    slope = None
    t_slope = None
    if n_heavy >= 3 and main["fc"].nunique() > 1:
        lr = stats.linregress(main["fc"].values.astype(float), main["ex"].values.astype(float))
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup = data.dropna(subset=["pp", "ex"])
    low = sup[sup["pp"] >= 8.4]["ex"].values.astype(float)
    oth = sup[sup["pp"] < 8.4]["ex"].values.astype(float)
    n_low = int(len(low))
    n_oth = int(len(oth))
    diff = None
    t_w = None
    if n_low >= 2 and n_oth >= 2:
        diff = float(np.mean(low) - np.mean(oth))
        tw = stats.ttest_ind(low, oth, equal_var=False)
        t_w = float(tw.statistic) if np.isfinite(tw.statistic) else None
    sup_pass = None if t_w is None else bool(diff > 0 and t_w >= 2)

    counts = {"heavy-volume days": n_heavy,
              "lowest-quarter days": n_low,
              "other heavy-volume days": n_oth}

    main_measure = {
        "name": "OLS slope of next-day excess return on forecast, heavy-volume days",
        "value": slope,
        "statistic": None if t_slope is None else {"name": "OLS t of slope", "value": t_slope},
        "threshold": "confirm: slope positive with t >= 2; reject: slope negative with t <= -2",
    }
    supporting = {
        "name": "mean next-day excess return, lowest-quarter minus other heavy days (Welch t >= 2)",
        "value": diff,
        "passed": sup_pass,
    }

    if n_heavy < 300 or n_low < 60:
        status = "not observable"
        decided_by = (f"Minimum counts not reached: {n_heavy} heavy-volume days (need 300) and "
                      f"{n_low} lowest-quarter days (need 60).")
    else:
        slope_conf = slope is not None and t_slope is not None and slope > 0 and t_slope >= 2
        slope_rej = slope is not None and t_slope is not None and slope < 0 and t_slope <= -2
        sup_rej = diff is not None and t_w is not None and diff < 0 and t_w <= -2
        if slope_conf and sup_pass:
            status = "confirmed"
            decided_by = "Confirm: the slope is positive with t >= 2 and lowest-quarter days beat the other heavy days with Welch t >= 2."
        elif slope_rej or sup_rej:
            status = "rejected"
            decided_by = ("Reject: " + ("the slope is negative with t <= -2" if slope_rej else "") +
                          (" and " if slope_rej and sup_rej else "") +
                          ("lowest-quarter days have a lower mean next-day excess return with Welch t <= -2" if sup_rej else "") + ".")
        else:
            status = "inconclusive"
            decided_by = ("Inconclusive: the results meet neither the confirm rule (slope t >= 2 with the supporting check passed) "
                          "nor a reject rule (slope t <= -2 or Welch t <= -2).")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main_measure,
        "supporting_check": supporting if t_w is None else dict(supporting, value=diff),
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading + (f" Welch t = {t_w:.3f}." if t_w is not None else ""),
    }
