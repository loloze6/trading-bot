import json
import numpy as np
import pandas as pd
from scipy import stats


def _component_raw(df, comp_id):
    """Raw value (last_history_value) of a strategy component, NaN where not recorded."""
    flat = "debug_info.components.%s.last_history_value" % comp_id
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        out = []
        for v in df["debug_info.components"].values:
            val = np.nan
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get(comp_id)
                if isinstance(c, dict):
                    x = c.get("last_history_value")
                    try:
                        val = float(x) if x is not None else np.nan
                    except Exception:
                        val = np.nan
            out.append(val)
        return pd.Series(out, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def measure(bars):
    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    rows = []
    for coin in sorted(bars.keys()):
        wins = bars[coin]
        # coin mean daily return over all its windows together
        all_rets = []
        prepared = {}
        for w in sorted(wins.keys()):
            df = wins[w].copy().reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            df["_next_ret"] = nxt
            all_rets.append(nxt.dropna().values)
            prepared[w] = df
        all_rets = np.concatenate(all_rets) if len(all_rets) else np.array([])
        coin_mean = float(np.mean(all_rets)) if all_rets.size else np.nan

        for w, df in prepared.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            regime = df["regime"].astype(str)
            rng = _component_raw(df, "range_usual")
            hdrop = _component_raw(df, "high_drop_usual")
            # (close - low)/close / std = range/std + (-(high-close)/close)/std
            dist = rng + hdrop
            in_profile = regime == "unknown"
            situation = in_profile & dist.notna() & (dist > 1e-12)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            pos = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            day = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D")
            excess = df["_next_ret"] - coin_mean
            for i in range(len(df)):
                p = pos.iloc[i]
                e = excess.iloc[i]
                if pd.isna(p) or pd.isna(e) or p == 0:
                    continue
                rows.append((day.iloc[i], float(p) * float(e), float(fc.iloc[i]), float(e)))

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    main_name = "mean drift-adjusted per-bar position gain before costs (1 bar)"
    main_thr = "mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects; over >= 100 days in a position"
    sup_name = "correlation of forecast with next-day excess return, t by day"
    reading = ("Situation = regime 'unknown' (falling calm, no veto) with raw range_usual + high_drop_usual > 0 "
               "and a short forecast; bars in a position are those with nonzero postRebalance_current_allocation and a "
               "next close in the same window; main t uses a day-clustered standard error (deviations summed per day), "
               "the supporting correlation is computed on per-day mean forecast and per-day mean excess return with "
               "t = r*sqrt(D-2)/sqrt(1-r^2) over D days.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"days in a position": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are falling-calm bars whose close sits "
                           "above the low with a short forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    if len(rows) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"days in a position": 0},
            "decided_by": "Fewer than 100 days in a position (0).",
            "reading": reading,
        }

    d = pd.DataFrame(rows, columns=["day", "gain", "fc", "ex"])
    n_cases = len(d)
    n_days = int(d["day"].nunique())
    mean_gain = float(d["gain"].mean())

    # day-clustered t of the mean
    t_main = None
    if n_days >= 2:
        dev = d["gain"] - mean_gain
        s_day = dev.groupby(d["day"]).sum().values
        var = (n_days / (n_days - 1.0)) * np.sum(s_day ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        if se > 0:
            t_main = float(mean_gain / se)

    # supporting check: correlation counted by day
    by_day = d.groupby("day")[["fc", "ex"]].mean()
    r = None
    t_corr = None
    if len(by_day) >= 3 and by_day["fc"].std() > 0 and by_day["ex"].std() > 0:
        r = float(stats.pearsonr(by_day["fc"].values, by_day["ex"].values)[0])
        D = len(by_day)
        if abs(r) < 1:
            t_corr = float(r * np.sqrt(D - 2) / np.sqrt(1 - r * r))
        else:
            t_corr = float(np.sign(r) * np.inf)
    sup_pass = bool(t_corr is not None and r is not None and r > 0 and t_corr >= 2)

    counts = {"days in a position": n_days, "bars in a position": int(n_cases)}
    stat = {"name": "t of the mean, cases of one day summed", "value": t_main} if t_main is not None else None
    sup = {"name": sup_name, "value": t_corr, "passed": sup_pass if t_corr is not None else False}

    if n_days < 100:
        status = "not observable"
        decided = "Fewer than 100 days in a position (%d), the plan's minimum." % n_days
    elif t_main is None:
        status = "inconclusive"
        decided = "The t of the mean gain could not be computed, so neither confirm nor reject is met."
    elif mean_gain > 0 and t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean drift-adjusted gain above 0 with t >= 2, supporting check passed, over at least 100 days in a position."
    elif mean_gain < 0 and t_main <= -2:
        status = "rejected"
        decided = "Mean drift-adjusted gain below 0 with t <= -2, over at least 100 days in a position."
    elif mean_gain > 0 and t_main >= 2:
        status = "inconclusive"
        decided = "Main measure meets the confirm rule but the supporting correlation check fails."
    else:
        status = "inconclusive"
        decided = "The t of the mean gain lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_gain, "statistic": stat, "threshold": main_thr},
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
