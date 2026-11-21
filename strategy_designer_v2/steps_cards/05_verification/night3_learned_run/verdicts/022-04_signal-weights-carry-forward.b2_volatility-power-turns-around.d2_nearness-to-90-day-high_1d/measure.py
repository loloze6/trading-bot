import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    NH_RAW = "debug_info.components.near_high.last_history_value"
    NH_POST = "debug_info.components.near_high.post_pipeline_value"
    OF_RAW = "debug_info.components.offset.last_history_value"
    OF_POST = "debug_info.components.offset.post_pipeline_value"
    STD_WIN, STD_MINP = 90, 22

    def standardise(raw, post_fallback):
        # value(t) * 10 / mean(|last `window` raw values, t left out|), capped +-20.
        # Built from the window's recorded raw values. Where the record holds fewer
        # than min_periods past values (warm-up not recorded), use the recorded
        # post-pipeline value.
        raw = pd.Series(raw, dtype=float).reset_index(drop=True)
        absmean = raw.abs().shift(1).rolling(STD_WIN, min_periods=STD_MINP).mean()
        out = raw * 10.0 / absmean
        out = out.where(absmean != 0, 0.0)
        out = out.clip(-20, 20)
        fb = pd.Series(post_fallback, dtype=float).reset_index(drop=True)
        return out.where(absmean.notna(), fb)

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if NH_RAW in df.columns:
                nh_raw = pd.to_numeric(df[NH_RAW], errors="coerce")
            else:
                nh_raw = pd.Series(np.nan, index=df.index)
            nh_post = (pd.to_numeric(df[NH_POST], errors="coerce")
                       if NH_POST in df.columns else pd.Series(np.nan, index=df.index))
            nh_std = standardise(nh_raw, nh_post)
            if OF_RAW in df.columns:
                of_raw = pd.to_numeric(df[OF_RAW], errors="coerce")
                of_post = (pd.to_numeric(df[OF_POST], errors="coerce")
                           if OF_POST in df.columns else pd.Series(10.0, index=df.index))
                of_std = standardise(of_raw, of_post)
            else:
                of_std = pd.Series(10.0, index=df.index)
            combined = (nh_std + of_std) / 2.0
            # the situation: a distance below the 90-bar closing high (<= 0), graded,
            # side = nearer than usual -> long, farther -> short
            is_distance = nh_raw <= 1e-9
            active = fc.notna() & (fc != 0)
            agree = (active & is_distance & combined.notna() & (combined != 0)
                     & (np.sign(combined) == np.sign(fc)))
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"independent grid cases": None},
            "decided_by": ("Fewer than 90% of active bars have a forecast whose sign matches the "
                           "rebuilt (standardised 90-bar distance below high + standardised +10 "
                           "offset)/2, i.e. nearer than usual long and farther short."),
            "reading": "none",
        }

    # ---------------- 2. main measure ----------------
    grid = []  # (coin, fwd_return, forecast)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            for i in range(0, len(df) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid.append((coin, c1 / c0 - 1.0, fc[i]))
    g = pd.DataFrame(grid, columns=["coin", "ret", "fc"])
    # normal drift: coin's mean 5-bar return over all its windows' grids
    if len(g):
        drift = g.groupby("coin")["ret"].mean()
        g["ex"] = g["ret"] - g["coin"].map(drift)
    else:
        g["ex"] = []
    g = g.dropna(subset=["ex", "fc"])
    n_cases = int(len(g))

    slope = None
    tstat = None
    if n_cases >= 3:
        x = g["fc"].values.astype(float)
        y = g["ex"].values.astype(float)
        xm = x - x.mean()
        sxx = float(np.sum(xm ** 2))
        if sxx > 0:
            b = float(np.sum(xm * (y - y.mean())) / sxx)
            a = y.mean() - b * x.mean()
            resid = y - a - b * x
            s2 = float(np.sum(resid ** 2) / (n_cases - 2))
            se = np.sqrt(s2 / sxx)
            slope = b
            tstat = float(b / se) if se > 0 else None

    # ---------------- 3. supporting check: timing gain before costs ----------------
    # coin mean daily return over all windows
    coin_mu = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            rs.append((c / c.shift(1) - 1.0).iloc[1:])
        if rs:
            coin_mu[coin] = float(pd.concat(rs).dropna().mean())
    rows = []
    for coin, wins in bars.items():
        if coin not in coin_mu:
            continue
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce")
            pos = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").shift(1)
            r = c / c.shift(1) - 1.0
            day = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D")
            d = pd.DataFrame({"day": day, "book": pos * r, "mkt": pos * coin_mu[coin]}).iloc[1:]
            d = d.dropna()
            rows.append(d)
    timing = None
    if rows:
        allr = pd.concat(rows)
        daily = allr.groupby("day")[["book", "mkt"]].mean()
        if len(daily):
            timing = float(daily["book"].mean() - daily["mkt"].mean())
    sup_passed = None if timing is None else bool(timing > 0)

    # ---------------- 4. decision ----------------
    if n_cases < 1000:
        status = "not observable"
        decided = f"Fewer than 1000 independent grid cases ({n_cases}): the minimum count is not reached."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed."
    elif tstat >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The slope's t is 2 or more over at least 1000 grid cases and the timing gain is positive."
        else:
            status = "inconclusive"
            decided = "A confirming slope (t >= 2) whose timing gain before costs is not positive."
        pass
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less over at least 1000 grid cases."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 over at least 1000 grid cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "OLS slope of 5-bar forward return minus coin drift on forecast, non-overlapping grid, pooled",
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS t of slope", "value": tstat},
            "threshold": "t >= 2 confirms, t <= -2 rejects, over at least 1000 grid cases",
        },
        "supporting_check": {
            "name": "timing gain before costs (mean daily position gain minus gain from coin mean drift)",
            "value": timing,
            "passed": sup_passed,
        },
        "counts": {"independent grid cases": n_cases},
        "decided_by": decided,
        "reading": ("All grid bars (positions 0,5,10,... of each window with a full 5-bar return, "
                    "flat forecasts included) enter an ordinary least-squares slope with intercept, the drift "
                    "is the coin's mean grid 5-bar return over all windows, and the book before costs is the "
                    "previous bar's allocation times the coin's daily return, averaged over coins per day."),
    }
