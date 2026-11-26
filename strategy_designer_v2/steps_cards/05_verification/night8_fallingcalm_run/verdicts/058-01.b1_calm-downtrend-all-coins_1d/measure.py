import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    COMP = "fall30"

    def to_time(s):
        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce")
            mx = np.nanmax(v.values) if len(v) else 0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")

    def comp_raw(df):
        flat = "debug_info.components.%s.last_history_value" % COMP
        if flat in df.columns:
            return pd.to_numeric(df[flat], errors="coerce").values
        out = np.full(len(df), np.nan)
        if "debug_info.components" in df.columns:
            import json
            for i, d in enumerate(df["debug_info.components"].values):
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except Exception:
                        d = None
                if isinstance(d, dict):
                    c = d.get(COMP)
                    if isinstance(c, dict):
                        v = c.get("last_history_value")
                        try:
                            out[i] = float(v)
                        except (TypeError, ValueError):
                            pass
        return out

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            close = pd.to_numeric(df["close"], errors="coerce").values
            raw = comp_raw(df)
            # fall back on prices where the raw value is not recorded
            back = np.full(len(df), np.nan)
            if len(df) > 30:
                back[30:] = close[30:] / close[:-30] - 1.0
            f30 = np.where(np.isnan(raw), back, raw)
            regime = df["regime"].astype(str).values
            active = (~np.isnan(fc)) & (fc != 0)
            situ = (regime == "unknown") & (~np.isnan(f30)) & (f30 < 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)
    situation_check = {"agreement": agreement, "passed": passed}

    main_name = "slope of 5-bar excess return on short size (-forecast), day-clustered t"
    threshold = "confirm: slope < 0 with t <= -2 and mean excess < 0; reject: slope > 0 with t >= +2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"grid cases with forecast < 0": None, "distinct days": None},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars inside the falling-calm "
                          "profile (regime 'unknown') with the coin below its close of 30 bars ago.",
            "reading": "The profile is read from the recorded regime ('unknown' = falling calm, the vetoes give 'chop'), "
                       "and the 30-day fall from fall30's last_history_value, recomputed from closes where not recorded.",
        }

    # ---------- criterion ----------
    xs, ys, days = [], [], []
    for coin, wins in bars.items():
        grid_rets = []
        cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = to_time(df["timestamp"])
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0:
                    d = ts.iloc[t]
                    cases.append((r, -fc[t], None if pd.isna(d) else d.strftime("%Y-%m-%d")))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for r, size, d in cases:
            if d is None:
                continue
            xs.append(size)
            ys.append(r - drift)
            days.append(d)

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    days = np.array(days)
    n_cases = int(len(x))
    n_days = int(len(np.unique(days))) if n_cases else 0
    counts = {"grid cases with forecast < 0": n_cases, "distinct days": n_days}

    slope, tstat, mean_ex = None, None, None
    if n_cases >= 3 and n_days >= 2:
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        mean_ex = float(y.mean())
        if sxx > 0:
            slope = float(np.sum(xc * (y - y.mean())) / sxx)
            intercept = y.mean() - slope * x.mean()
            e = y - intercept - slope * x
            dfc = pd.DataFrame({"d": days, "s": xc * e})
            sd = dfc.groupby("d")["s"].sum().values
            G = len(sd)
            var = (G / (G - 1.0)) * float(np.sum(sd ** 2)) / sxx ** 2
            tstat = float(slope / np.sqrt(var)) if var > 0 else None
    elif n_cases > 0:
        mean_ex = float(y.mean())

    sup_pass = None if mean_ex is None else bool(mean_ex < 0)
    supporting = {"name": "mean excess return of the short cases below 0", "value": mean_ex, "passed": sup_pass}
    main = {"name": main_name, "value": slope,
            "statistic": None if tstat is None else {"name": "slope t, cases of one day summed (day-clustered)", "value": tstat},
            "threshold": threshold}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = "Minimum not reached: the plan needs at least 100 grid cases with forecast < 0 on at least 50 distinct days (have %d cases on %d days)." % (n_cases, n_days)
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope t could not be computed (no spread in the short size), so neither the confirm nor the reject rule is met."
    elif slope < 0 and tstat <= -2:
        if sup_pass:
            status = "confirmed"
            decided = "Confirm rule: slope negative with t <= -2 and mean excess return below 0."
        else:
            status = "inconclusive"
            decided = "Inconclusive rule: a confirming slope (t <= -2) whose supporting check (mean excess < 0) fails."
    elif slope > 0 and tstat >= 2:
        status = "rejected"
        decided = "Reject rule: slope positive with t >= +2 (deeper falls followed by relative rises)."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the slope t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": "Grid bars at positions 0,5,10,... per window with a full 5-bar return; the coin's drift is the mean of "
                   "all its grid 5-bar returns over all windows; the slope t uses day-clustered OLS standard errors "
                   "(score sums per UTC day, G/(G-1) correction); the profile is the recorded regime 'unknown'; and short "
                   "counts follow the instructions' 'not observable' for the plan's minimums.",
    }
