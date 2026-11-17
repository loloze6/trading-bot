import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    FC = "forecast"
    REG = "regime"
    SHARE = "debug_info.components.rsi_share.last_history_value"
    ALLOC = "postRebalance_current_allocation"
    PVAL = "postRebalance_total_value"

    # ---------- 1. situation check ----------
    # Situation (Fidelity): low-volatility regime (vol rank <= 0.5 -> detector's "trending")
    # and the side follows the RSI share against one half (above 0.5 -> long, below -> short).
    share_vals = []
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            if SHARE in df.columns:
                share_vals.append(pd.to_numeric(df[SHARE], errors="coerce").dropna().values)
    share_all = np.concatenate(share_vals) if share_vals else np.array([])
    # raw share lies in [0, 1]; if the recorded raw value is already centred (has negatives), centre is 0
    centre = 0.0 if (share_all.size and np.nanmin(share_all) < 0) else 0.5

    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            reg = df[REG].astype(str).values
            if SHARE in df.columns:
                sh = pd.to_numeric(df[SHARE], errors="coerce").values
            else:
                sh = np.full(len(df), np.nan)
            active = fc != 0
            n_active += int(active.sum())
            side = np.sign(sh - centre)
            ok = active & (reg == "trending") & np.isfinite(sh) & (side != 0) & (np.sign(fc) == side)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of pooled slope of demeaned 14-bar forward return on forecast (non-overlapping grid, trending, non-zero forecast)"
    thr = "confirm if t >= 2 with timing part > 0; reject if t <= -2; at least 100 independent grid cases"
    sup_name = "timing part of book mean daily return over trending-regime bars"
    reading_base = ("Low-volatility regime taken from the recorded `regime` == 'trending' (the detector's volrank <= 0.5 "
                    "rule, not recomputable inside windows without warm-up), side from the raw RSI share against 0.5; "
                    "coin mean 14-bar return taken over all grid bars of all its windows; a book daily return "
                    "postRebalance_total_value[t+1]/postRebalance_total_value[t]-1 is attributed to bar t and kept "
                    "when bar t is trending; fewer than 100 grid cases gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"independent grid cases": None, "active bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars are low-volatility (trending) bars with the forecast "
                           "on the side of the RSI share against 0.5, so the config does not do what the Fidelity says."),
            "reading": reading_base,
        }

    # ---------- 2. main measure ----------
    xs, ys = [], []
    for coin in bars:
        grid_rets = []
        sel = []
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            reg = df[REG].astype(str).values
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if reg[p] == "trending" and np.isfinite(fc[p]) and fc[p] != 0:
                    sel.append((fc[p], r))
        if not grid_rets:
            continue
        mu = float(np.mean(grid_rets))
        for f, r in sel:
            xs.append(f)
            ys.append(r - mu)
    xs = np.asarray(xs, float)
    ys = np.asarray(ys, float)
    n_cases = int(len(xs))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.var(xs) > 0:
        xm, ym = xs.mean(), ys.mean()
        sxx = np.sum((xs - xm) ** 2)
        b = np.sum((xs - xm) * (ys - ym)) / sxx
        a = ym - b * xm
        resid = ys - a - b * xs
        s2 = np.sum(resid ** 2) / (n_cases - 2)
        se = np.sqrt(s2 / sxx) if s2 > 0 else np.nan
        slope = float(b)
        t_slope = float(b / se) if np.isfinite(se) and se > 0 else None

    # ---------- 3. supporting check: timing part ----------
    rows = []
    for coin in bars:
        dr = []
        for w in bars[coin]:
            df = bars[coin][w]
            close = pd.to_numeric(df["close"], errors="coerce").values
            r = close[1:] / close[:-1] - 1.0
            dr.append(r[np.isfinite(r)])
        cat = np.concatenate(dr) if dr else np.array([])
        mu_d = float(np.mean(cat)) if cat.size else np.nan
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            pv = pd.to_numeric(df[PVAL], errors="coerce").values
            al = pd.to_numeric(df[ALLOC], errors="coerce").values
            reg = df[REG].astype(str).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for t in range(len(df) - 1):
                if reg[t] != "trending":
                    continue
                if not (np.isfinite(pv[t]) and np.isfinite(pv[t + 1]) and pv[t] != 0 and np.isfinite(al[t])):
                    continue
                book = pv[t + 1] / pv[t] - 1.0
                mkt = al[t] * mu_d
                rows.append((ts[t + 1].normalize(), book, mkt))
    timing = None
    if rows:
        d = pd.DataFrame(rows, columns=["day", "book", "mkt"]).groupby("day")[["book", "mkt"]].mean()
        timing = float(d["book"].mean() - d["mkt"].mean())
    sup_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. decision ----------
    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} independent grid cases, below the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast)."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the timing part is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the timing part is 0 or less."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": timing, "passed": sup_pass},
        "counts": {"independent grid cases": n_cases, "active bars": n_active},
        "decided_by": decided,
        "reading": reading_base,
    }
