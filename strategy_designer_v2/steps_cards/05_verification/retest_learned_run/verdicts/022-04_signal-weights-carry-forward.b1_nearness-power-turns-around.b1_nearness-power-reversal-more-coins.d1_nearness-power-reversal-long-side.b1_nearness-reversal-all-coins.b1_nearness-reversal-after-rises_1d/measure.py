import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.power_turn.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            r30 = close / close.shift(30) - 1.0
            regime_tr = df["regime"].astype(str) == "trending" if "regime" in df.columns else pd.Series(False, index=df.index)
            # 30-day return from prices where computable, else the detector's own decision
            trending = np.where(r30.notna(), r30 > 0, regime_tr)
            reversal_up = (raw < 0).fillna(False).values  # negated raw > 0
            active = (fc != 0).values
            ok = active & trending & reversal_up & (fc > 0).values
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars where the negated power component is positive and the 30-day return is above 0, as the Fidelity's situation requires.",
            "reading": "The 30-day return is computed from closes inside the window, falling back to the recorded regime on the first 30 bars of a window.",
        }

    # ---------- 2. Main measure: slope of excess 5-bar return on forecast ----------
    xs, ys_raw, coins_of = [], [], []
    drift = {}
    mu_daily = {}
    for coin, wins in bars.items():
        grid_rets = []
        day_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n - H, H):
                if np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                    r = close[i + H] / close[i] - 1.0
                    grid_rets.append(r)
                    if np.isfinite(fc[i]):
                        xs.append(fc[i]); ys_raw.append(r); coins_of.append(coin)
            if n > 1:
                dr = close[1:] / close[:-1] - 1.0
                day_rets.extend(list(dr[np.isfinite(dr)]))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan
        mu_daily[coin] = float(np.mean(day_rets)) if day_rets else np.nan

    x = np.array(xs, dtype=float)
    y = np.array([ys_raw[k] - drift[coins_of[k]] for k in range(len(ys_raw))], dtype=float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    n_grid = int(len(x))
    n_pos = int((x > 0).sum())
    slope, tstat = None, None
    if n_grid >= 3:
        xm, ym = x.mean(), y.mean()
        sxx = float(((x - xm) ** 2).sum())
        if sxx > 0:
            b = float(((x - xm) * (y - ym)).sum() / sxx)
            a = ym - b * xm
            resid = y - a - b * x
            s2 = float((resid ** 2).sum() / (n_grid - 2))
            se = np.sqrt(s2 / sxx) if s2 > 0 else 0.0
            slope = b
            tstat = float(b / se) if se > 0 else (float(np.sign(b) * np.inf) if b != 0 else 0.0)

    # ---------- 3. Supporting check: timing gain before costs ----------
    recs = []
    for coin, wins in bars.items():
        mu = mu_daily[coin]
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            alloc = pd.to_numeric(df[ALLOC], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").values
            for t in range(1, len(df)):
                if np.isfinite(close[t]) and np.isfinite(close[t - 1]) and close[t - 1] > 0 and np.isfinite(alloc[t - 1]) and np.isfinite(mu):
                    r = close[t] / close[t - 1] - 1.0
                    recs.append((ts[t], coin, alloc[t - 1] * r, alloc[t - 1] * mu))
    timing = None
    if recs:
        d = pd.DataFrame(recs, columns=["day", "coin", "gain", "mkt"])
        daily = d.groupby("day")[["gain", "mkt"]].mean()
        timing = float(daily["gain"].mean() - daily["mkt"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. Decision ----------
    if n_pos < 100 or slope is None:
        status = "not observable"
        decided = f"Only {n_pos} grid cases with a forecast above 0, fewer than the plan's minimum of 100."
    elif slope > 0 and tstat >= 2:
        if timing_pass:
            status = "confirmed"
            decided = "Slope above 0 with t >= 2 over at least 100 grid cases with a forecast above 0, and the timing gain is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming slope (above 0, t >= 2) but the timing gain is at or below 0."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "Slope below 0 with t <= -2 over at least 100 grid cases with a forecast above 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (no confirm or reject rule met)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "OLS slope of 5-bar return minus coin's normal 5-bar drift on forecast",
            "value": None if slope is None else float(slope),
            "statistic": None if tstat is None else {"name": "OLS slope t", "value": float(tstat)},
            "threshold": "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; over at least 100 grid cases with forecast > 0",
        },
        "supporting_check": {
            "name": "book's timing gain before costs (mean daily gain minus coin-rise part)",
            "value": timing,
            "passed": timing_pass,
        },
        "counts": {"grid cases with a forecast above 0": n_pos, "grid cases": n_grid},
        "decided_by": decided,
        "reading": "All grid cases (forecast 0 included) enter the pooled regression, the drift is each coin's mean non-overlapping 5-bar return over all its windows, and the timing gain uses the position before costs (allocation x next-bar return) minus allocation x the coin's mean daily return, averaged over coins per day then over days.",
    }
