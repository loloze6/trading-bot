import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.fall_vol_volat.last_history_value"
    MIN_CASES = 300

    # ---------- collect per-coin data, returns inside each window only ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        all_r = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            opn = pd.to_numeric(d["open"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            nxt = close.shift(-1) / close - 1.0
            prev_fall = (close < close.shift(1)) | (close < opn)
            all_r.append(nxt.dropna().values)
            rows.append(pd.DataFrame({
                "coin": coin, "window": w, "forecast": fc.values,
                "raw": raw.values, "price_fall": prev_fall.values, "ret": nxt.values,
            }))
        coin_rets[coin] = np.concatenate(all_r) if all_r else np.array([])

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "forecast-weighted mean next-day excess return", "value": None,
                             "statistic": None, "threshold": "above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"cases with forecast > 0": 0},
            "decided_by": "No bars in the record; the minimum of 300 cases with forecast > 0 is not reached.",
            "reading": "none",
        }

    data = pd.concat(rows, ignore_index=True)

    # ---------- situation check: a down day (raw fall-weighted value > 0), long side ----------
    active = data[data["forecast"].notna() & (data["forecast"] != 0)]
    n_active = len(active)
    situ = np.where(active["raw"].notna(), active["raw"] > 0, active["price_fall"].astype(bool))
    agree_mask = situ & (active["forecast"] > 0).values
    agreement = float(agree_mask.mean()) if n_active > 0 else 1.0
    passed = bool(agreement >= 0.90)

    reading = ("The situation holds on bars where the component's raw value (fall x volume ratio x volatility ratio) "
               "is above 0, falling back to a price fall when it is missing, on the long side; the t of the weighted "
               "mean is the ordinary t of the per-case values forecast x excess / mean forecast; the top and bottom "
               "thirds are the n//3 cases with the highest and lowest forecast; the 300-case minimum gives "
               "'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "forecast-weighted mean next-day excess return", "value": None,
                             "statistic": None, "threshold": "above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are down days with a long forecast, "
                           "so the config does not trade the plan's situation (a day's fall, long)."),
            "reading": reading,
        }

    # ---------- main measure ----------
    coin_mean = {c: (float(np.mean(r)) if len(r) else np.nan) for c, r in coin_rets.items()}
    cases = data[(data["forecast"] > 0) & data["ret"].notna()].copy()
    cases["excess"] = cases["ret"] - cases["coin"].map(coin_mean)
    cases = cases[cases["excess"].notna()]
    n = int(len(cases))
    counts = {"cases with forecast > 0": n}
    threshold = "confirm: above 0 with t >= 2 and supporting check passes; reject: below 0 with t <= -2"

    if n < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": "forecast-weighted mean next-day excess return", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {n} cases with forecast > 0, below the plan's minimum of 300.",
            "reading": reading,
        }

    w = cases["forecast"].values.astype(float)
    x = cases["excess"].values.astype(float)
    wmean = float(np.sum(w * x) / np.sum(w))
    y = w * x / np.mean(w)
    sd = float(np.std(y, ddof=1))
    t = float(np.mean(y) / (sd / np.sqrt(n))) if sd > 0 else 0.0

    # ---------- supporting check ----------
    order = np.argsort(w, kind="mergesort")
    k = n // 3
    bottom = x[order[:k]]
    top = x[order[n - k:]]
    diff = float(np.mean(top) - np.mean(bottom)) if k > 0 else None
    sup_pass = bool(diff is not None and diff > 0)

    if wmean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The weighted mean excess return is above 0 with t >= 2 and the top-third minus bottom-third difference is above 0."
        else:
            status = "inconclusive"
            decided = "The weighted mean excess return is above 0 with t >= 2 but the top-third minus bottom-third check fails."
    elif wmean < 0 and t <= -2:
        status = "rejected"
        decided = "The weighted mean excess return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the weighted mean excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "forecast-weighted mean next-day excess return", "value": wmean,
                         "statistic": {"name": "t of the weighted mean over cases", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": "top-third minus bottom-third mean excess return", "value": diff,
                             "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
