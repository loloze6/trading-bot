import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    DROP = "debug_info.components.drop.last_history_value"

    rows = []
    for coin, wins in bars.items():
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float)
            prev_ret = close / close.shift(1) - 1.0          # inside this window only
            next_ret = close.shift(-1) / close - 1.0         # inside this window only
            if DROP in d.columns:
                drop_raw = pd.to_numeric(d[DROP], errors="coerce").astype(float)
                drop_val = drop_raw.where(drop_raw.notna(), prev_ret)
            else:
                drop_val = prev_ret
            fc = pd.to_numeric(d[FC], errors="coerce").astype(float) if FC in d.columns \
                else pd.Series(np.nan, index=d.index)
            reg = d["regime"].astype(str) if "regime" in d.columns \
                else pd.Series("nan", index=d.index)
            rows.append(pd.DataFrame({
                "coin": coin, "window": wname,
                "forecast": fc.values, "drop": drop_val.values,
                "next_ret": next_ret.values, "regime": reg.values,
            }))

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "net share of higher next closes, high-vol minus quiet, top-decile forecast bars",
                             "value": None, "statistic": None, "threshold": "z >= 2 confirms, z <= -2 rejects"},
            "supporting_check": None,
            "counts": {"top-decile drop bars, high volatility": 0, "top-decile drop bars, quiet": 0},
            "decided_by": "No bars in the record, so the minimum of 30 top-decile drop bars per volatility group is not reached.",
            "reading": "none",
        }

    allb = pd.concat(rows, ignore_index=True)

    # ---------- 1. situation check ----------
    active = allb[allb["forecast"].notna() & (allb["forecast"] != 0)]
    n_active = len(active)
    if n_active > 0:
        ok = (active["drop"] < 0) & (active["forecast"] > 0)
        agreement = float(ok.sum()) / n_active
    else:
        agreement = 0.0
    passed_sit = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Situation taken as a negative one-day change (drop component's raw value, else the close-to-close return) "
               "with a long forecast; top decile = bars whose forecast is at or above the 90th percentile of all non-missing "
               "forecasts pooled over coins and windows and is positive, keeping those with a next close in the same window; "
               "high volatility = regime 'trending' (volp >= 0.5) and quiet = regime 'unknown'; each bar's up indicator is netted "
               "by its coin's share of higher next closes over all windows, the z numerator is the difference of the net shares "
               "with the pooled raw share giving the standard error; the supporting check passes at t >= 2 since the plan states "
               "no threshold for it; fewer than 30 bars in a group is reported as not observable.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "net share of higher next closes, high-vol minus quiet, top-decile forecast bars",
                             "value": None, "statistic": None, "threshold": "z >= 2 confirms, z <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of active bars are one-day drops with a long forecast, below 90%: "
                           "the config's forecast does not follow the plan's long-after-a-drop situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    valid_next = allb["next_ret"].notna()
    # coin baselines over all windows together
    base_up = {}
    base_mean = {}
    for coin, g in allb[valid_next].groupby("coin"):
        base_up[coin] = float((g["next_ret"] > 0).mean())
        base_mean[coin] = float(g["next_ret"].mean())

    fvals = allb["forecast"].dropna().values
    q90 = float(np.quantile(fvals, 0.9)) if len(fvals) else np.nan
    top = allb[allb["forecast"].notna() & (allb["forecast"] >= q90) & (allb["forecast"] > 0) & valid_next].copy()
    top["up"] = (top["next_ret"] > 0).astype(float)
    top["base_up"] = top["coin"].map(base_up)
    top["base_mean"] = top["coin"].map(base_mean)

    hi = top[top["regime"] == "trending"]
    lo = top[top["regime"] == "unknown"]
    n1, n2 = len(hi), len(lo)
    counts = {"top-decile drop bars, high volatility": int(n1),
              "top-decile drop bars, quiet": int(n2)}

    main_name = "net share of higher next closes, high-vol minus quiet, top-decile forecast bars"
    thr = "two-proportion z >= 2 confirms, z <= -2 rejects, between is inconclusive; at least 30 bars per group"

    # supporting check
    sup = None
    if n1 >= 2:
        ex = (hi["next_ret"] - hi["base_mean"]).values
        m = float(np.mean(ex))
        sd = float(np.std(ex, ddof=1))
        t = float(m / (sd / np.sqrt(n1))) if sd > 0 else None
        sup = {"name": "mean next-bar excess return, top-decile high-vol drop bars (t of mean)",
               "value": m, "t": t, "passed": (bool(t >= 2) if t is not None else None)}
        sup = {"name": sup["name"] + (f", t={t:.3f}" if t is not None else ""),
               "value": m, "passed": sup["passed"]}
    else:
        sup = {"name": "mean next-bar excess return, top-decile high-vol drop bars (t of mean)",
               "value": None, "passed": None}

    if n1 < 30 or n2 < 30:
        val = None
        stat = None
        if n1 > 0 and n2 > 0:
            val = float((hi["up"] - hi["base_up"]).mean() - (lo["up"] - lo["base_up"]).mean())
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": val, "statistic": stat, "threshold": thr},
            "supporting_check": sup,
            "counts": counts,
            "decided_by": (f"The minimum of 30 top-decile drop bars in each volatility group is not reached "
                           f"(high volatility {n1}, quiet {n2})."),
            "reading": reading,
        }

    net1 = float((hi["up"] - hi["base_up"]).mean())
    net2 = float((lo["up"] - lo["base_up"]).mean())
    diff = net1 - net2
    p_pool = float((hi["up"].sum() + lo["up"].sum()) / (n1 + n2))
    se = np.sqrt(p_pool * (1 - p_pool) * (1.0 / n1 + 1.0 / n2))
    z = float(diff / se) if se > 0 else 0.0

    if z >= 2 and diff > 0:
        status = "confirmed"
        dec = f"Confirm rule met: the high-volatility net share exceeds the quiet share with z = {z:.2f} >= 2."
    elif z <= -2 and diff < 0:
        status = "rejected"
        dec = f"Reject rule met: the high-volatility net share is below the quiet share with z = {z:.2f} <= -2."
    else:
        status = "inconclusive"
        dec = f"Inconclusive rule met: z = {z:.2f} lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": diff,
                         "statistic": {"name": "two-proportion z", "value": z}, "threshold": thr},
        "supporting_check": sup,
        "counts": counts,
        "decided_by": dec,
        "reading": reading,
    }
