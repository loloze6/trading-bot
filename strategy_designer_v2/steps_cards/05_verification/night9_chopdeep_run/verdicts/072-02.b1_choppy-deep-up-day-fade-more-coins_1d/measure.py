import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.depth.last_history_value"

    sit_total = 0
    sit_ok = 0
    rows = []  # (forecast, excess next-day return)

    for coin, wins in bars.items():
        # coin's mean daily return over all its windows (1-bar returns inside each window)
        all_r = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            if len(c) > 1:
                all_r.append(c[1:] / c[:-1] - 1.0)
        if not all_r:
            continue
        all_r = np.concatenate(all_r)
        all_r = all_r[np.isfinite(all_r)]
        coin_mean = float(np.mean(all_r)) if len(all_r) else np.nan

        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            prev_ret = close / close.shift(1) - 1.0
            ret60 = (close / close.shift(60) - 1.0) * 100.0
            next_ret = close.shift(-1) / close - 1.0
            raw = (pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns
                   else pd.Series(np.nan, index=df.index))
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)

            active = fc != 0
            for i in np.where(active.values)[0]:
                # situation check (bars without a prior close in the window are left out)
                if np.isfinite(prev_ret.iloc[i]):
                    sit_total += 1
                    up = prev_ret.iloc[i] > 0
                    deep = np.isfinite(raw.iloc[i]) and raw.iloc[i] < 0
                    if np.isfinite(ret60.iloc[i]):
                        choppy = (-10.0 <= ret60.iloc[i] <= 10.0)
                    else:
                        choppy = regime.iloc[i] != "chop"
                    short = fc.iloc[i] < 0
                    if up and deep and choppy and short:
                        sit_ok += 1
                # main-measure row
                nr = next_ret.iloc[i]
                if np.isfinite(nr) and np.isfinite(coin_mean):
                    rows.append((float(fc.iloc[i]), float(nr - coin_mean)))

    agreement = float(sit_ok / sit_total) if sit_total > 0 else 0.0
    passed = sit_total > 0 and agreement >= 0.90
    reading = ("Thirds are cut on the pooled active bars sorted by forecast (stable sort, np.array_split, lowest third = deepest); "
               "the choppy profile is checked as a 60-bar close-to-close change within +/-10 % where the window holds 60 prior bars, "
               "else as a regime other than 'chop', the up day as close above the prior close in the window (first bar of a window left out), "
               "and the depth as a negative raw distance from the high.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "next-day excess return, deepest third minus shallowest third of forecast",
                             "value": None, "statistic": None,
                             "threshold": "Welch t <= -2 to confirm, >= +2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": int(sit_total)},
            "decided_by": ("Fewer than 90 % of the active bars are choppy up-day closes below the 20-day high with a short forecast, "
                           "so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    n = len(rows)
    if n > 0:
        arr = np.array(rows)
        order = np.argsort(arr[:, 0], kind="mergesort")
        parts = np.array_split(order, 3)
        deep = arr[parts[0], 1]
        shallow = arr[parts[2], 1]
    else:
        deep = np.array([])
        shallow = np.array([])

    counts = {"active bars": int(n), "deepest third": int(len(deep)),
              "middle third": int(len(parts[1])) if n > 0 else 0,
              "shallowest third": int(len(shallow))}

    main = {"name": "next-day excess return, deepest third minus shallowest third of forecast",
            "value": None, "statistic": None,
            "threshold": "Welch t <= -2 (with deepest third mean < 0) to confirm, >= +2 to reject"}
    supp = {"name": "deepest third mean next-day excess return below 0", "value": None, "passed": None}

    if n < 300 or min(len(deep), len(shallow), counts["middle third"]) < 100:
        if len(deep) > 1 and len(shallow) > 1:
            main["value"] = float(np.mean(deep) - np.mean(shallow))
            t = stats.ttest_ind(deep, shallow, equal_var=False).statistic
            main["statistic"] = {"name": "Welch t", "value": float(t)}
            supp["value"] = float(np.mean(deep))
            supp["passed"] = bool(np.mean(deep) < 0)
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": main, "supporting_check": supp, "counts": counts,
            "decided_by": "The plan's minimum of 100 bars in each third (300 active bars) is not reached.",
            "reading": reading,
        }

    diff = float(np.mean(deep) - np.mean(shallow))
    t = float(stats.ttest_ind(deep, shallow, equal_var=False).statistic)
    deep_mean = float(np.mean(deep))
    main["value"] = diff
    main["statistic"] = {"name": "Welch t", "value": t}
    supp["value"] = deep_mean
    supp["passed"] = bool(deep_mean < 0)

    if t <= -2 and deep_mean < 0:
        status = "confirmed"
        decided = "Welch t <= -2 and the deepest third's mean excess return is below 0 (confirm rule)."
    elif t >= 2:
        status = "rejected"
        decided = "Welch t >= +2: deep up-day closes are followed by better next days than shallow ones (reject rule)."
    elif t <= -2:
        status = "inconclusive"
        decided = "Welch t <= -2 but the deepest third's mean excess return is at or above 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "Welch t lies between -2 and +2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
