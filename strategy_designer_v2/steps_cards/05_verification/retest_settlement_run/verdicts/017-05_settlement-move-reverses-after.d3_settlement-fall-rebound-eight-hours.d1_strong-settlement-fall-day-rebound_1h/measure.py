import numpy as np
import pandas as pd


def measure(bars):
    H = 24
    FC_COL = "forecast"
    RAW_COL = "debug_info.components.settle_fall.last_history_value"

    def _prep(df):
        df = df.reset_index(drop=True).copy()
        ts = pd.to_datetime(df["timestamp"], utc=True)
        close_time = ts + pd.Timedelta(hours=1)
        df["_settle"] = close_time.dt.hour.isin([0, 16]) & (close_time.dt.minute == 0)
        c = df["close"].astype(float)
        ret2 = c / c.shift(2) - 1.0
        if RAW_COL in df.columns:
            raw = pd.to_numeric(df[RAW_COL], errors="coerce")
            sig = raw.where(raw.notna(), ret2)
        else:
            sig = ret2
        df["_fall"] = sig < 0
        df["_fc"] = pd.to_numeric(df[FC_COL], errors="coerce").fillna(0.0)
        df["_fwd"] = c.shift(-H) / c - 1.0
        return df

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = _prep(df)
            prepared[coin][w] = d
            act = d["_fc"] != 0
            n_active += int(act.sum())
            n_agree += int((act & d["_settle"] & d["_fall"] & (d["_fc"] > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    main_name = "forecast-weighted mean excess 24-bar return of settlement-fall cases (forecast >= 2)"
    main_thr = "confirm: weighted mean > 0 with t >= 2 (and supporting check passes); reject: weighted mean < 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars closing at 00:00 or 16:00 UTC "
                          "after a 2-hour fall, so the config does not trade the plan's situation.",
            "reading": "A settlement bar is one whose close (timestamp + 1h) is at 00:00 or 16:00 UTC; a fall is a negative raw "
                       "component value (or 2-bar return when not recorded).",
        }

    # ---------- criterion ----------
    ex_list, f_list = [], []
    for coin, wins in prepared.items():
        samples = []
        for w, d in wins.items():
            g = d["_fwd"].iloc[::H].dropna()
            samples.extend(g.tolist())
        drift = float(np.mean(samples)) if len(samples) > 0 else np.nan
        for w, d in wins.items():
            cand = d[d["_settle"] & (d["_fc"] >= 2)].copy()
            if len(cand) == 0:
                continue
            cand["_cell"] = cand.index // H
            for _, grp in cand.groupby("_cell"):
                row = grp.loc[grp["_fc"].idxmax()]
                r = row["_fwd"]
                if pd.isna(r) or not np.isfinite(drift):
                    continue
                ex_list.append(float(r) - drift)
                f_list.append(float(row["_fc"]))

    ex = np.array(ex_list, dtype=float)
    fc = np.array(f_list, dtype=float)
    n = len(ex)

    wmean = float(np.sum(ex * fc) / np.sum(fc)) if n > 0 and np.sum(fc) > 0 else None
    if n >= 2:
        sd = float(np.std(ex, ddof=1))
        tval = float(np.mean(ex) / (sd / np.sqrt(n))) if sd > 0 else None
    else:
        tval = None

    big = ex[fc >= 10]
    small = ex[(fc >= 2) & (fc < 10)]
    if len(big) > 0 and len(small) > 0:
        diff = float(np.mean(big) - np.mean(small))
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = None

    counts = {"cases": int(n), "cases forecast >= 10": int(len(big)), "cases forecast 2 to below 10": int(len(small))}
    reading = ("Settlement bars are those whose close (timestamp + 1h) is at 00:00 or 16:00 UTC; in each 24-bar grid cell "
               "counted from a window's first row the bar with the largest forecast is the case and is dropped if its 24-bar "
               "return leaves the window; the coin's mean 24-bar return is taken on the non-overlapping grid of all its windows; "
               "the supporting check is the difference of the two groups' unweighted mean excess returns (>=10 minus 2 to <10).")

    if n < 30:
        status = "not observable"
        decided = f"Only {n} cases across all coins and windows, fewer than the plan's minimum of 30."
    elif wmean is None or tval is None:
        status = "inconclusive"
        decided = "The weighted mean or its t could not be computed, meeting neither the confirm nor the reject rule."
    elif wmean > 0 and tval >= 2:
        if sup_pass is True:
            status = "confirmed"
            decided = "Weighted mean excess return above 0 with t >= 2 and the largest falls rebounding more: confirm rule met."
        else:
            status = "inconclusive"
            decided = "A confirming weighted mean and t, but the supporting check failed or could not be measured: inconclusive."
    elif wmean < 0 and tval <= -2:
        status = "rejected"
        decided = "Weighted mean excess return below 0 with t <= -2: reject rule met."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or its sign disagrees with the weighted mean): inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": wmean,
            "statistic": ({"name": "ordinary t of case excess returns", "value": tval} if tval is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "mean excess return of forecast >= 10 cases minus forecast 2 to <10 cases",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
