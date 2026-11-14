import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    LHV = "debug_info.components.drop.last_history_value"

    rows = []
    for coin in sorted(bars.keys()):
        wins = bars[coin]
        for w in sorted(wins.keys(), key=lambda s: int(str(s).lstrip("w")) if str(s).lstrip("w").isdigit() else str(s)):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            prev_ret = close / close.shift(1) - 1.0          # one-day change, inside the window
            next_ret = close.shift(-1) / close - 1.0         # next bar's return, inside the window
            fc = pd.to_numeric(d[FC], errors="coerce") if FC in d.columns else pd.Series(np.nan, index=d.index)
            lhv = pd.to_numeric(d[LHV], errors="coerce") if LHV in d.columns else pd.Series(np.nan, index=d.index)
            reg = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            rows.append(pd.DataFrame({
                "coin": coin, "window": w,
                "fc": fc.values, "prev_ret": prev_ret.values, "lhv": lhv.values,
                "next_ret": next_ret.values, "regime": reg.values,
            }))

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "net up-share difference, high-vol minus quiet, top-decile drop bars",
                             "value": None, "statistic": None, "threshold": "z >= 2 confirms, z <= -2 rejects"},
            "supporting_check": None,
            "counts": {"top-decile drop bars high-volatility": 0, "top-decile drop bars quiet": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }

    a = pd.concat(rows, ignore_index=True)

    # ---------- situation check: active bars must be drop days, held long ----------
    active = a[a["fc"].notna() & (a["fc"] != 0)]
    n_active = len(active)
    drop_flag = np.where(active["prev_ret"].notna(), active["prev_ret"] < 0,
                         np.where(active["lhv"].notna(), active["lhv"] < 0, False))
    ok = drop_flag & (active["fc"].values > 0)
    agreement = float(ok.mean()) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Drop day = close below the previous close in the same window (raw drop component value < 0 on a "
               "window's first bar), expected side long; top 10 percent = forecast at or above the 90th percentile of "
               "all non-missing forecasts pooled over coins and windows, and positive; high volatility = regime "
               "'trending' (the detector's volp >= 0.5 rule), quiet = 'unknown'; each bar's up indicator is netted by "
               "its coin's up-day share over all windows, the z uses the difference of net shares over the pooled "
               "raw-proportion standard error; the supporting check passes when its one-sample t >= 2; the plan's "
               "'fewer than 30 in either group' is treated as the minimum count (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "net up-share difference, high-vol minus quiet, top-decile drop bars",
                             "value": None, "statistic": None, "threshold": "z >= 2 confirms, z <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of active bars are drop days held long, below 90%: the forecast "
                           "does not follow the plan's graded long-after-a-one-day-fall situation."),
            "reading": reading,
        }

    # ---------- coin baselines over all windows together ----------
    valid = a[a["next_ret"].notna()].copy()
    valid["up"] = (valid["next_ret"] > 0).astype(float)
    p_coin = valid.groupby("coin")["up"].mean()
    mu_coin = valid.groupby("coin")["next_ret"].mean()

    # ---------- top decile of forecasts, pooled ----------
    fc_all = a["fc"].dropna()
    q90 = float(np.quantile(fc_all.values, 0.9)) if len(fc_all) else np.inf
    top = valid[valid["fc"].notna() & (valid["fc"] >= q90) & (valid["fc"] > 0)].copy()
    top["net_up"] = top["up"] - top["coin"].map(p_coin)
    top["excess"] = top["next_ret"] - top["coin"].map(mu_coin)

    hi = top[top["regime"] == "trending"]
    lo = top[top["regime"] == "unknown"]
    n_hi, n_lo = len(hi), len(lo)

    counts = {"top-decile drop bars high-volatility": int(n_hi),
              "top-decile drop bars quiet": int(n_lo)}

    main_name = "net share of higher next closes, high-vol minus quiet, top-decile drop bars"
    thr = "z >= 2 confirms, z <= -2 rejects, otherwise inconclusive"

    if n_hi < 30 or n_lo < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "Fewer than 30 top-decile drop bars in at least one volatility group.",
            "reading": reading,
        }

    s_hi = float(hi["net_up"].mean())
    s_lo = float(lo["net_up"].mean())
    diff = s_hi - s_lo
    p_pool = float((hi["up"].sum() + lo["up"].sum()) / (n_hi + n_lo))
    se = np.sqrt(p_pool * (1 - p_pool) * (1.0 / n_hi + 1.0 / n_lo))
    z = float(diff / se) if se > 0 else 0.0

    ex = hi["excess"].dropna().values
    if len(ex) > 1 and np.std(ex, ddof=1) > 0:
        sup_mean = float(np.mean(ex))
        sup_t = float(sup_mean / (np.std(ex, ddof=1) / np.sqrt(len(ex))))
        sup_pass = bool(sup_t >= 2)
    else:
        sup_mean = float(np.mean(ex)) if len(ex) else None
        sup_t = None
        sup_pass = False

    if z >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "High-volatility net share of higher next closes exceeds the quiet share with z >= 2, and the supporting excess return passes."
        else:
            status = "inconclusive"
            decided = "z >= 2 meets the confirm rule, but the supporting excess-return check fails, so inconclusive."
    elif z <= -2:
        status = "rejected"
        decided = "High-volatility net share is below the quiet share with z <= -2."
    else:
        status = "inconclusive"
        decided = "z lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": diff,
                         "statistic": {"name": "two-proportion z", "value": z},
                         "threshold": thr},
        "supporting_check": {"name": "mean next-bar return minus coin mean, top-decile high-vol drop bars (t)",
                             "value": sup_mean, "passed": sup_pass,
                             "t": sup_t, "n": int(len(ex))},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
