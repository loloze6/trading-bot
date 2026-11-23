import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.heavy_fall.last_history_value"

    # ---------- collect per-bar data, inside each window only ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fwd = close.shift(-1) / close - 1.0  # next-day return, same window
            prev_ret = close / close.shift(1) - 1.0
            rets_all.append(fwd.dropna().values)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            for i in range(len(d)):
                rows.append({
                    "coin": coin, "window": w,
                    "forecast": fc.iloc[i], "raw": raw.iloc[i],
                    "prev_ret": prev_ret.iloc[i], "fwd": fwd.iloc[i],
                })
        coin_rets[coin] = np.concatenate(rets_all) if rets_all else np.array([])
    data = pd.DataFrame(rows)
    coin_mean = {c: (float(np.mean(r)) if len(r) else np.nan) for c, r in coin_rets.items()}

    # ---------- situation check ----------
    active = data[data["forecast"].notna() & (data["forecast"] != 0)].copy()
    if len(active) == 0:
        agreement = 0.0
    else:
        # situation: a down day, read on the raw component (negative = fall x volume ratio);
        # where the raw value is missing, the day's price return from the close before
        down = np.where(active["raw"].notna(), active["raw"] < 0,
                        active["prev_ret"].notna() & (active["prev_ret"] < 0))
        ok = down & (active["forecast"] > 0).values
        agreement = float(np.mean(ok))
    passed = bool(agreement >= 0.9)
    situation = {"agreement": agreement, "passed": passed}

    main_name = "forecast-weighted mean next-day excess return on forecast > 0 bars"
    main_thr = "confirm: > 0 with t >= 2 (and upper half beats lower half); reject: < 0 with t <= -2"
    reading = ("Down day read as a negative raw component value (price return where missing); t is the "
               "weighted mean over its weighted standard error (sqrt(n/(n-1)) * sqrt(sum w^2 (x-m)^2) / sum w); "
               "the upper half is forecast > median, the lower half forecast <= median; with a 1-bar horizon every bar is a grid cell.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"bars with forecast > 0": int((data["forecast"] > 0).sum()) if len(data) else 0},
            "decided_by": ("Fewer than 90% of active bars are down days with a long forecast: the config's "
                           "forecast does not follow the plan's situation (down day, long side)."),
            "reading": reading,
        }

    # ---------- main measure ----------
    pos = data[(data["forecast"] > 0) & data["fwd"].notna()].copy()
    pos["excess"] = pos["fwd"] - pos["coin"].map(coin_mean)
    pos = pos[pos["excess"].notna()]
    n = int(len(pos))
    counts = {"bars with forecast > 0": n}

    if n < 200:
        return {
            "status": "not observable",
            "situation_check": situation,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Fewer than 200 bars with forecast > 0 ({n}): the minimum count is not reached.",
            "reading": reading,
        }

    w = pos["forecast"].values.astype(float)
    x = pos["excess"].values.astype(float)
    m = float(np.sum(w * x) / np.sum(w))
    se = float(np.sqrt(n / (n - 1.0)) * np.sqrt(np.sum((w ** 2) * (x - m) ** 2)) / np.sum(w))
    t = float(m / se) if se > 0 else 0.0

    # ---------- supporting check ----------
    med = float(np.median(w))
    up = x[w > med]
    lo = x[w <= med]
    if len(up) > 0 and len(lo) > 0:
        diff = float(np.mean(up) - np.mean(lo))
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = False
    counts["upper half bars"] = int(len(up))
    counts["lower half bars"] = int(len(lo))

    if m > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The forecast-weighted mean excess return is above 0 with t >= 2 and the upper half beats the lower half."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return is below 0 with t <= -2."
    elif t >= 2 and m > 0 and not sup_pass:
        status = "inconclusive"
        decided = "t >= 2 but the upper half does not beat the lower half."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2: neither the confirm nor the reject rule is met."

    return {
        "status": status,
        "situation_check": situation,
        "main_measure": {"name": main_name, "value": m,
                         "statistic": {"name": "t of the weighted mean", "value": t},
                         "threshold": main_thr},
        "supporting_check": {"name": "upper-half minus lower-half mean next-day excess return",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
