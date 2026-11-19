import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.fall72.last_history_value"
    H = 2

    def prep(df):
        df = df.sort_values("timestamp").reset_index(drop=True).copy()
        ts = pd.to_datetime(df["timestamp"], utc=True)
        # Hours from the bar's close (start + 1h) to the next settlement (00, 08, 16 UTC).
        close_hour = (ts.dt.hour + 1) % 24
        hts = (8 - (close_hour % 8)) % 8
        hts = hts.where(hts != 0, 8)
        df["_hts"] = hts.values
        close = df["close"].astype(float)
        # 72-bar price change: use the recorded raw value where present, else recompute within the window.
        recomputed = close / close.shift(72) - 1.0
        if RAW in df.columns:
            raw = pd.to_numeric(df[RAW], errors="coerce")
            raw = raw.where(raw.notna(), recomputed)
        else:
            raw = recomputed
        df["_fall72"] = raw
        df["_fc"] = pd.to_numeric(df["forecast"], errors="coerce")
        df["_r2"] = close.shift(-H) / close - 1.0
        return df

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepped = {}
    for coin, wins in bars.items():
        prepped[coin] = {}
        for w, df in wins.items():
            d = prep(df)
            prepped[coin][w] = d
            fc = d["_fc"]
            active = fc.notna() & (fc != 0)
            in_window = d["_hts"].between(1, 2)
            fell = d["_fall72"] < 0
            agree = active & in_window & fell & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "t of the slope of excess 2-bar return on forecast, pooled pre-settlement episodes"
    threshold = "confirm: slope t >= 2 and mean excess t >= 2; reject: slope t <= -2 or mean excess t <= -2"
    reading = ("Situation = bars whose close is 1 or 2 hours before a 00/08/16 UTC settlement (bars stamped "
               "05/06, 13/14, 21/22, holding through 06/07, 14/15, 22/23) with a negative 72-bar price change, "
               "long side; a case is such a bar with HoursToSettlement = 2 (stamped 05, 13, 21), regime trending "
               "and forecast > 0; the coin's mean 2-bar return uses positions 0,2,4,... of every window pooled; "
               "the per-coin minimum applies to every coin in the record; unmet minimums give 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are pre-settlement bars after a "
                           "3-day fall with a long forecast, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- criterion ----------
    xs, ys = [], []
    per_coin = {}
    for coin, wins in prepped.items():
        grid = []
        for w, d in wins.items():
            g = d["_r2"].iloc[::H].dropna()
            grid.append(g.values)
        grid = np.concatenate(grid) if grid else np.array([])
        coin_mean = float(np.mean(grid)) if grid.size else np.nan
        cnt = 0
        for w, d in wins.items():
            reg_ok = d["regime"].astype(str) == "trending"
            sel = reg_ok & (d["_hts"] == 2) & (d["_fc"] > 0) & d["_r2"].notna()
            if np.isnan(coin_mean):
                continue
            sub = d.loc[sel]
            xs.extend(sub["_fc"].astype(float).tolist())
            ys.extend((sub["_r2"].astype(float) - coin_mean).tolist())
            cnt += int(sel.sum())
        per_coin[coin] = cnt

    x = np.asarray(xs, float)
    y = np.asarray(ys, float)
    n = int(len(y))
    counts = {"cases pooled": n}
    for c, v in per_coin.items():
        counts[f"cases {c}"] = v

    slope_t = None
    slope = None
    if n >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        slope_t = float(res.slope / res.stderr) if res.stderr > 0 else None
    mean_ex = float(np.mean(y)) if n > 0 else None
    mean_t = None
    if n >= 2:
        sd = float(np.std(y, ddof=1))
        if sd > 0:
            mean_t = float(mean_ex / (sd / np.sqrt(n)))
    check_pass = (mean_ex is not None and mean_t is not None and mean_ex > 0 and mean_t >= 2)

    main = {"name": main_name, "value": slope_t,
            "statistic": {"name": "OLS t of slope", "value": slope_t} if slope_t is not None else None,
            "threshold": threshold}
    supp = {"name": "mean excess 2-bar return over cases (t >= 2 and > 0); value is its t",
            "value": mean_t, "passed": bool(check_pass) if mean_t is not None else None}

    low_coins = [c for c, v in per_coin.items() if v < 20]
    if n < 300 or low_coins:
        if n < 300:
            why = f"Only {n} pooled cases, below the plan's minimum of 300."
        else:
            why = f"Fewer than 20 cases for {', '.join(low_coins)}, below the plan's per-coin minimum of 20."
        return {"status": "not observable",
                "situation_check": {"agreement": agreement, "passed": True},
                "main_measure": main, "supporting_check": supp, "counts": counts,
                "decided_by": why, "reading": reading}

    if slope_t is not None and slope_t >= 2 and check_pass:
        status = "confirmed"
        why = "The slope t is >= 2 and the mean excess 2-bar return is above 0 with t >= 2."
    elif (slope_t is not None and slope_t <= -2) or (mean_t is not None and mean_t <= -2):
        status = "rejected"
        why = "The slope t is <= -2 or the mean excess 2-bar return has t <= -2."
    else:
        status = "inconclusive"
        why = "Neither the confirm rule (both t >= 2) nor the reject rule (either t <= -2) is met."

    return {"status": status,
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": main, "supporting_check": supp, "counts": counts,
            "decided_by": why, "reading": reading}
