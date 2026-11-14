import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.drop.last_history_value"
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            close = pd.to_numeric(d["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            prev_ret = close / close.shift(1) - 1.0
            if LHV in d.columns:
                drop_raw = pd.to_numeric(d[LHV], errors="coerce")
                drop_raw = drop_raw.where(drop_raw.notna(), prev_ret)
            else:
                drop_raw = prev_ret
            rows.append(pd.DataFrame({
                "coin": coin,
                "window": w,
                "forecast": pd.to_numeric(d["forecast"], errors="coerce"),
                "regime": d["regime"].astype(str),
                "drop_raw": drop_raw,
                "next_ret": nxt,
            }))
    if not rows:
        return {"status": "not observable", "situation_check": {"agreement": None, "passed": False},
                "main_measure": None, "supporting_check": None, "counts": {},
                "decided_by": "no bars in the record", "reading": "none"}
    all_df = pd.concat(rows, ignore_index=True)

    # ---- situation check: active bars should be one-day falls, long side
    active = all_df[all_df["forecast"].notna() & (all_df["forecast"] != 0)]
    n_active = len(active)
    if n_active > 0:
        ok = (active["drop_raw"] < 0) & (active["forecast"] > 0)
        agreement = float(ok.mean())
    else:
        agreement = 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active_bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars are one-day-fall bars held long, as the plan's graded drop situation requires.",
            "reading": "The situation is a negative one-bar change of the drop component (prices where missing) with a positive forecast.",
        }

    # ---- coin base rates over all windows together (within-window next returns)
    valid = all_df[all_df["next_ret"].notna()]
    base_up = valid.groupby("coin")["next_ret"].apply(lambda s: float((s > 0).mean()))
    base_mean = valid.groupby("coin")["next_ret"].mean()

    # ---- top decile of forecast, pooled over all coins and windows
    fc = all_df["forecast"].dropna()
    q90 = float(fc.quantile(0.9))
    top = all_df[all_df["forecast"].notna() & (all_df["forecast"] >= q90) & (all_df["forecast"] > 0)
                 & all_df["next_ret"].notna()].copy()
    top["up"] = (top["next_ret"] > 0).astype(float)
    top["up_net"] = top["up"] - top["coin"].map(base_up)
    top["ret_net"] = top["next_ret"] - top["coin"].map(base_mean)

    hi = top[top["regime"] == "trending"]
    lo = top[top["regime"] != "trending"]
    n_hi, n_lo = len(hi), len(lo)
    counts = {"high_volatility_top_decile_drop_bars": int(n_hi),
              "quiet_top_decile_drop_bars": int(n_lo)}

    reading = ("Top 10 percent means forecast at or above the 90th percentile of all bars' forecasts pooled (and positive); "
               "high-volatility bars are those the detector labelled 'trending' (volp >= 0.5), quiet bars the rest; "
               "the z-test uses the difference of coin-netted shares over the pooled raw-share standard error; "
               "the supporting check passes when its one-sample t is >= 2; fewer than 30 bars in a group gives 'not observable'.")

    # supporting check
    sup = None
    if n_hi >= 2:
        m = float(hi["ret_net"].mean())
        sd = float(hi["ret_net"].std(ddof=1))
        t_sup = m / (sd / np.sqrt(n_hi)) if sd > 0 else None
        sup = {"name": "mean next-bar return net of coin mean, high-vol top-decile drops (t)",
               "value": m, "t": t_sup,
               "passed": (bool(t_sup >= 2) if t_sup is not None else None)}
    else:
        sup = {"name": "mean next-bar return net of coin mean, high-vol top-decile drops (t)",
               "value": None, "passed": None}

    threshold = "confirm if z >= 2 (high-vol share above quiet), reject if z <= -2, otherwise inconclusive"
    if n_hi < 30 or n_lo < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": "net up-share high-vol minus quiet, top-decile drops",
                             "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": sup,
            "counts": counts,
            "decided_by": "Fewer than 30 top-decile drop bars in at least one volatility group.",
            "reading": reading,
        }

    net_hi = float(hi["up_net"].mean())
    net_lo = float(lo["up_net"].mean())
    diff = net_hi - net_lo
    p_pool = float((hi["up"].sum() + lo["up"].sum()) / (n_hi + n_lo))
    se = np.sqrt(p_pool * (1 - p_pool) * (1.0 / n_hi + 1.0 / n_lo))
    z = float(diff / se) if se > 0 else 0.0

    if z >= 2 and diff > 0:
        status = "confirmed"
        decided = "The high-volatility net share of higher next closes exceeds the quiet share with z >= 2."
    elif z <= -2 and diff < 0:
        status = "rejected"
        decided = "The high-volatility net share is below the quiet share with z <= -2."
    else:
        status = "inconclusive"
        decided = "z lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "net up-share high-vol minus quiet, top-decile drops",
                         "value": diff,
                         "statistic": {"name": "two-proportion z", "value": z},
                         "threshold": threshold},
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
