import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    VR_COL = "debug_info.components.absorb.last_history_value"
    EPS = 1e-9

    # Expected side from the Fidelity outcome: "the coin rises over the next day" -> long (+1)
    expected_sign = 1.0

    sit_total = 0
    sit_agree = 0

    case_rows = []      # (day, coin, excess)
    control_vals = []   # excess next-day returns of control days

    for coin, wins in bars.items():
        # Coin's mean daily (1-bar) return over all windows together, never across windows
        all_rets = []
        prepared = {}
        for w, df in wins.items():
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            nxt = d["close"].shift(-1)
            d["ret1"] = nxt / d["close"] - 1.0
            all_rets.append(d["ret1"].dropna().values)
            prepared[w] = d
        if len(all_rets) == 0:
            continue
        pooled = np.concatenate(all_rets) if len(all_rets) else np.array([])
        if pooled.size == 0:
            continue
        coin_mean = float(np.mean(pooled))

        for w, d in prepared.items():
            rng = d["high"] - d["low"]
            rng = rng.where(rng > 0)
            # share of the range between the high and the close (1 = close at the low)
            dist_high = (d["high"] - d["close"]) / rng
            # volume over the prior 20-bar mean, current bar excluded, inside this window
            vr_price = d["volume"] / d["volume"].rolling(20, min_periods=20).mean().shift(1)
            # fallback from the recorded raw component value (surge x closeness to low)
            if VR_COL in d.columns:
                lhv = pd.to_numeric(d[VR_COL], errors="coerce")
                vr_impl = lhv / dist_high.where(dist_high > 0)
            else:
                vr_impl = pd.Series(np.nan, index=d.index)
            vr = vr_price.where(vr_price.notna(), vr_impl)

            fc = pd.to_numeric(d["forecast"], errors="coerce")

            # ---- situation check ----
            active = fc.notna() & (fc != 0)
            determinable = vr.notna() & dist_high.notna()
            situation = (vr >= 2.0 - EPS) & (dist_high >= 0.8 - EPS)
            mask = active & determinable
            sit_total += int(mask.sum())
            sit_agree += int((mask & situation & (np.sign(fc) == expected_sign)).sum())

            # ---- cases: forecast rises >= 2 from flat on the long side ----
            prev = fc.shift(1)
            is_case = prev.notna() & (prev == 0) & (fc >= 2.0) & d["ret1"].notna()
            for i in np.where(is_case.values)[0]:
                case_rows.append((d["timestamp"].iloc[i].normalize(), coin,
                                  float(d["ret1"].iloc[i] - coin_mean)))

            # ---- controls: vr < 1.5 and close in bottom 20% of range (from prices) ----
            is_ctrl = vr_price.notna() & dist_high.notna() & (vr_price < 1.5) & \
                (dist_high >= 0.8 - EPS) & d["ret1"].notna()
            control_vals.extend((d.loc[is_ctrl, "ret1"] - coin_mean).astype(float).tolist())

    agreement = (sit_agree / sit_total) if sit_total > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean excess next-day return of long cases (vs coin mean daily return)"
    threshold = "confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2; at least 30 distinct case days"
    reading = ("A case is a bar whose forecast is >= 2 while the previous bar in the same window is exactly 0 "
               "(a window's first bar has no known previous forecast and is not a case); the t clusters case "
               "deviations by UTC day; the volume ratio uses the prior 20 bars inside the window, falling back to "
               "the recorded absorb value divided by the close's distance from the high on the first 20 bars; "
               "the supporting check uses Welch t on case-level excess returns of these same cases against "
               "control days recomputed from prices; the plan's 'fewer than 30 distinct case days' minimum is "
               "applied as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(sit_total)},
            "decided_by": ("Fewer than 90 % of active forecast bars are long bars with volume >= 2x the prior 20-day "
                           "mean and a close in the bottom 20 % of the range, as the Fidelity's situation requires."),
            "reading": reading,
        }

    # ---- main measure ----
    n_cases = len(case_rows)
    days = sorted(set(r[0] for r in case_rows))
    n_days = len(days)
    mean_ex = None
    t_main = None
    if n_cases > 0:
        x = np.array([r[2] for r in case_rows])
        mean_ex = float(x.mean())
        dev = pd.Series(x - mean_ex, index=[r[0] for r in case_rows])
        day_sums = dev.groupby(level=0).sum().values
        J = len(day_sums)
        if J > 1:
            var = (J / (J - 1)) * np.sum(day_sums ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            t_main = float(mean_ex / se) if se > 0 else None

    # ---- supporting check ----
    diff = None
    t_welch = None
    check_passed = None
    n_ctrl = len(control_vals)
    if n_cases >= 2 and n_ctrl >= 2:
        cx = np.array([r[2] for r in case_rows])
        cc = np.array(control_vals)
        diff = float(cx.mean() - cc.mean())
        tw = stats.ttest_ind(cx, cc, equal_var=False).statistic
        t_welch = float(tw) if np.isfinite(tw) else None
        check_passed = bool(t_welch is not None and diff > 0 and t_welch >= 1.0)
    elif n_cases > 0:
        check_passed = False

    counts = {"distinct case days": int(n_days), "cases": int(n_cases), "control days": int(n_ctrl)}

    if n_days < 30:
        status = "not observable"
        decided_by = f"Only {n_days} distinct case days, below the plan's minimum of 30."
    elif t_main is None:
        status = "inconclusive"
        decided_by = "The t of the cases' mean excess return could not be computed; anything else is inconclusive."
    elif mean_ex > 0 and t_main >= 2:
        if check_passed:
            status = "confirmed"
            decided_by = "Mean excess next-day return above 0 with t >= 2 and the supporting check passes (confirm rule)."
        else:
            status = "inconclusive"
            decided_by = "Main measure meets the confirm rule but the supporting check fails (inconclusive rule)."
    elif mean_ex < 0 and t_main <= -2:
        status = "rejected"
        decided_by = "Mean excess next-day return below 0 with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided_by = "The t of the mean excess next-day return lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean, cases summed per day", "value": t_main}
                          if t_main is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "cases minus low-volume low-close controls, mean excess next-day return (Welch t >= 1)",
            "value": diff,
            "passed": check_passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
