import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    LOOK = 20
    WITHIN = 9  # high day plus the next 9 bars
    COL_RAW = "debug_info.components.range.last_history_value"

    def bars_since_high(close):
        """Bars since the last close above each of its prior 20 closes, computed inside one window.
        NaN where the window's history is too short to know."""
        c = close.to_numpy(dtype=float)
        n = len(c)
        newh = np.full(n, np.nan)
        for t in range(LOOK, n):
            prior = c[t - LOOK:t]
            if np.all(np.isfinite(prior)) and np.isfinite(c[t]):
                newh[t] = 1.0 if c[t] > prior.max() else 0.0
        bsh = np.full(n, np.nan)
        for t in range(n):
            for k in range(0, WITHIN + 1):
                j = t - k
                if j < 0:
                    break
                if np.isnan(newh[j]):
                    break  # cannot know further back
                if newh[j] == 1.0:
                    bsh[t] = k
                    break
            else:
                bsh[t] = WITHIN + 1  # no new high in the last 10 bars, all known
                continue
            if np.isnan(bsh[t]):
                # either unknown, or we stopped on a known 0 chain? (only break on unknown)
                pass
        # bars where every one of the last 10 bars was known and none was a new high
        for t in range(n):
            if np.isnan(bsh[t]):
                ks = [t - k for k in range(WITHIN + 1)]
                if all(j >= 0 and not np.isnan(newh[j]) for j in ks):
                    bsh[t] = WITHIN + 1
        return bsh

    # ---------- situation check and per-window data ----------
    act_total = 0
    act_agree = 0
    per = {}  # coin -> list of DataFrames (grid rows)
    for coin, wins in bars.items():
        per[coin] = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float)
            regime = df["regime"].astype(str)
            bsh = bars_since_high(close)
            known = ~np.isnan(bsh)
            in_sit = np.where(known, bsh <= WITHIN, (regime == "trending").to_numpy())
            below_high = np.where(
                known,
                bsh >= 1,
                (df[COL_RAW].astype(float) < 1.0).to_numpy() if COL_RAW in df.columns else False,
            )
            active = (fc != 0) & fc.notna()
            a = active.to_numpy()
            act_total += int(a.sum())
            act_agree += int((a & in_sit & (fc > 0).to_numpy()).sum())

            pos = np.arange(0, len(df), H)
            rows = []
            for p in pos:
                if p + H < len(df):
                    r = close.iloc[p + H] / close.iloc[p] - 1.0
                else:
                    r = np.nan
                rows.append({
                    "ret": r,
                    "fc": fc.iloc[p],
                    "regime_on": bool(in_sit[p]),
                    "below_high": bool(below_high[p]),
                })
            per[coin].append(pd.DataFrame(rows))

    agreement = act_agree / act_total if act_total > 0 else 0.0
    passed = act_total > 0 and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(act_total)},
            "decided_by": "Fewer than 90% of the active bars are long bars within 10 bars of a 20-bar closing high, "
                          "so the config does not trade the plan's situation on its long side.",
            "reading": "Situation recomputed from closes inside each window (new close above the prior 20 closes, "
                       "bars since <= 9); where the window's history is too short the recorded regime is used.",
        }

    # ---------- main measure ----------
    main_ex = []
    supp_ex = []
    for coin, lst in per.items():
        g = pd.concat(lst, ignore_index=True) if lst else pd.DataFrame()
        if g.empty:
            continue
        g = g[g["ret"].notna()]
        if g.empty:
            continue
        mu = g["ret"].mean()
        sel = g[(g["fc"] > 0)]
        main_ex.extend((sel["ret"] - mu).tolist())
        sel2 = g[g["regime_on"] & g["below_high"]]
        supp_ex.extend((sel2["ret"] - mu).tolist())

    main_ex = np.array(main_ex, dtype=float)
    supp_ex = np.array(supp_ex, dtype=float)
    n = len(main_ex)
    n_s = len(supp_ex)
    mean = float(main_ex.mean()) if n > 0 else None
    if n > 1 and main_ex.std(ddof=1) > 0:
        t = float(mean / (main_ex.std(ddof=1) / np.sqrt(n)))
    else:
        t = None
    s_mean = float(supp_ex.mean()) if n_s > 0 else None
    s_pass = (s_mean > 0) if s_mean is not None else None

    reading = ("Situation recomputed from closes inside each window (close above its prior 20 closes, bars since <= 9), "
               "falling back on the recorded regime where history is too short; the coin's mean 10-bar return is the "
               "mean over all its non-overlapping grid returns in all windows; the supporting check takes all grid "
               "bars in the regime with bars since the high >= 1, whatever their forecast; the plan's 'fewer than 20 "
               "pooled independent cases' is applied as a minimum count (not observable).")

    out = {
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean 10-bar excess return of grid bars with forecast > 0, pooled",
            "value": mean,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "mean 10-bar excess of regime grid bars below the 20-bar high",
            "value": s_mean,
            "passed": s_pass,
        },
        "counts": {"pooled independent cases": int(n), "supporting cases": int(n_s)},
        "reading": reading,
    }

    if n < 20 or t is None:
        out["status"] = "not observable"
        out["decided_by"] = f"Only {n} pooled independent cases, fewer than the plan's minimum of 20."
        return out

    if mean > 0 and t >= 2:
        if s_pass:
            out["status"] = "confirmed"
            out["decided_by"] = "Mean excess is above 0 with t >= 2 and the supporting check passes."
        else:
            out["status"] = "inconclusive"
            out["decided_by"] = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif mean < 0 and t <= -2:
        out["status"] = "rejected"
        out["decided_by"] = "Mean excess is below 0 with t <= -2."
    else:
        out["status"] = "inconclusive"
        out["decided_by"] = "t lies strictly between -2 and 2, which the plan calls inconclusive."
    return out
