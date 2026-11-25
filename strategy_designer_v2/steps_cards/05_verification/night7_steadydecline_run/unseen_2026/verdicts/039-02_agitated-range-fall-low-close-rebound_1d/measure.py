import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.fall_low_close.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            regime = df["regime"].astype(str).values
            agitated = regime != "chop"
            situation = agitated & np.isfinite(raw) & (raw > 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    sit = {"agreement": agreement, "passed": passed}
    main_name = "forecast-weighted mean next-day excess return on forecast > 0 bars"
    thr = "above 0 with t >= 2 (confirm, with supporting check); below 0 with t <= -2 (reject)"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are agitated-profile down days "
                           "with a positive fall-times-low-close value and a long forecast."),
            "reading": "Situation taken as regime not 'chop' (agitated) and raw component value > 0, long side as forecast > 0.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        # coin mean daily return over all windows
        all_r = []
        per_win = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            r = np.full(len(df), np.nan)
            r[:-1] = close[1:] / close[:-1] - 1.0
            all_r.append(r[np.isfinite(r)])
            per_win.append((df, r))
        if not all_r:
            continue
        cat = np.concatenate(all_r)
        if len(cat) == 0:
            continue
        mu = float(np.mean(cat))
        for df, r in per_win:
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").values
            m = np.isfinite(fc) & (fc > 0) & np.isfinite(r)
            for i in np.where(m)[0]:
                rows.append((coin, ts[i], float(fc[i]), float(r[i] - mu)))

    cases = pd.DataFrame(rows, columns=["coin", "day", "f", "ex"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"distinct days with forecast > 0": n_days, "cases (coin-bars with forecast > 0)": n_cases}

    value = None
    tval = None
    if n_cases > 0:
        f = cases["f"].values
        ex = cases["ex"].values
        sf = f.sum()
        value = float(np.sum(f * ex) / sf)
        contrib = f * (ex - value) / sf
        D = pd.Series(contrib).groupby(cases["day"].values).sum().values
        G = len(D)
        if G > 1:
            var = np.sum(D ** 2) * G / (G - 1)
            se = float(np.sqrt(var))
            tval = float(value / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        srt = cases.sort_values("f", kind="mergesort").reset_index(drop=True)
        h = n_cases // 2
        bottom = srt["ex"].values[:h]
        top = srt["ex"].values[n_cases - h:]
        sup_val = float(np.mean(top) - np.mean(bottom))
        sup_pass = bool(sup_val > 0)

    stat = {"name": "t of weighted mean, same-day cases summed (day-clustered)",
            "value": tval} if tval is not None else None
    main = {"name": main_name, "value": value, "statistic": stat, "threshold": thr}
    sup = {"name": "top-half minus bottom-half mean excess return by forecast",
           "value": sup_val, "passed": sup_pass}

    reading = ("Every bar is on the 1-bar grid; the coin's mean daily return is over all its windows; the t "
               "sums each day's weighted deviations into one piece (day-clustered standard error); halves are "
               "the n//2 lowest and n//2 highest forecasts (middle case dropped if odd), unweighted means; "
               "the 100-day minimum counts distinct UTC days with a forecast > 0 case that has a next-day return.")

    if n_days < 100 or value is None or tval is None:
        status = "not observable"
        decided = f"Only {n_days} distinct days with forecast > 0, below the plan's minimum of 100."
    elif value > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Weighted mean excess return above 0 with t >= 2 and the top-minus-bottom-half check above 0."
    elif value < 0 and tval <= -2:
        status = "rejected"
        decided = "Weighted mean excess return below 0 with t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check (top half minus bottom half above 0) fails."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
