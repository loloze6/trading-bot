import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.depth.last_history_value"
    POS = "postRebalance_current_allocation"

    # ---------- coin mean daily return over all windows (returns inside windows only) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            r = (c.shift(-1) / c - 1.0).iloc[:-1]
            rets.append(r.dropna())
        allr = pd.concat(rets) if rets else pd.Series(dtype=float)
        coin_mean[coin] = float(allr.mean()) if len(allr) else np.nan

    # ---------- situation check and sample building ----------
    n_active = 0
    n_agree = 0
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            pos = pd.to_numeric(d[POS], errors="coerce") if POS in d.columns else pd.Series(np.nan, index=d.index)
            prev = close.shift(1)
            up = close > prev
            # first bar of a window has no prior close inside the window: fall back on the recorded regime
            if len(d) > 0 and "regime" in d.columns:
                up.iloc[0] = str(d["regime"].iloc[0]) == "mean_reversion"
            below_high = raw < 0
            situation = up & below_high
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            nxt = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            sample = up & active
            for i in np.where(sample.values)[0]:
                if i >= len(d) - 1:
                    continue
                r1 = nxt.iloc[i]
                if not np.isfinite(r1) or not np.isfinite(coin_mean[coin]):
                    continue
                ex = r1 - coin_mean[coin]
                rows.append({
                    "coin": coin,
                    "day": ts.iloc[i].floor("D") if pd.notna(ts.iloc[i]) else pd.NaT,
                    "pos": pos.iloc[i],
                    "excess": ex,
                    "depth": raw.iloc[i],
                })

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed_sit = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of the mean daily timing gain (position x (next-day return - coin mean daily return)), summed per day across coins"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"
    sup_name = "Welch t of next-day excess return, deepest third minus shallowest third by depth (pass: difference < 0 and t <= -1)"

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"up-day cases": None, "distinct days": None},
            "decided_by": "Fewer than 90% of active bars are up days below the 20-day high with a short forecast, as the plan's Fidelity requires.",
            "reading": "Up day = close above the prior close in the same window (first bar of a window: recorded regime); below the high = raw depth < 0; expected side short.",
        }

    s = pd.DataFrame(rows)
    # ---------- main measure ----------
    g = s.dropna(subset=["pos", "excess", "day"]).copy()
    g["gain"] = g["pos"] * g["excess"]
    daily = g.groupby("day")["gain"].sum()
    n_cases = int(len(g))
    n_days = int(daily.shape[0])
    if n_days >= 2 and daily.std(ddof=1) > 0:
        mean_gain = float(daily.mean())
        t_main = float(mean_gain / (daily.std(ddof=1) / np.sqrt(n_days)))
    else:
        mean_gain = float(daily.mean()) if n_days else None
        t_main = None

    # ---------- supporting check ----------
    h = s.dropna(subset=["depth", "excess"]).sort_values("depth", kind="mergesort").reset_index(drop=True)
    sup_val, sup_t, sup_pass = None, None, None
    n3 = len(h) // 3
    if n3 >= 2:
        deep = h["excess"].iloc[:n3].values          # most negative depth = deepest
        shallow = h["excess"].iloc[len(h) - n3:].values
        sup_val = float(deep.mean() - shallow.mean())
        tt = stats.ttest_ind(deep, shallow, equal_var=False)
        sup_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
        sup_pass = bool(sup_t is not None and sup_val < 0 and sup_t <= -1)

    counts = {"up-day cases": n_cases, "distinct days": n_days}

    if n_cases < 300 or n_days < 100:
        status = "not observable"
        decided = f"Minimum counts not reached: {n_cases} up-day cases (need 300) on {n_days} distinct days (need 100)."
    elif t_main is None:
        status = "inconclusive"
        decided = "The t of the mean daily timing gain could not be computed."
    elif mean_gain > 0 and t_main >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean daily timing gain positive with t >= 2 and the deepest-minus-shallowest Welch t <= -1."
        else:
            status = "inconclusive"
            decided = "Main measure meets the confirm rule (t >= 2) but the supporting check fails."
    elif mean_gain < 0 and t_main <= -2:
        status = "rejected"
        decided = "Mean daily timing gain negative with t <= -2: deep up days rise more than the drift."
    else:
        status = "inconclusive"
        decided = "The t of the mean daily timing gain lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_gain,
            "statistic": {"name": "t of the mean (daily sums)", "value": t_main} if t_main is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_t, "passed": sup_pass,
                             "difference": sup_val},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Up day = close above the prior close in the same window (first bar: recorded regime); position = postRebalance_current_allocation; "
                    "days with no case are left out of the daily series; terciles are pooled over all coins on the raw depth (last_history_value, most negative = deepest); "
                    "the minimum is read as at least 300 cases and at least 100 distinct days, either failing gives not observable."),
    }
