import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    C_MOM30 = "debug_info.components.mom30.last_history_value"
    C_NEAR = "debug_info.components.near_high.last_history_value"
    C_MOM7 = "debug_info.components.mom7.last_history_value"
    P_COLS = ["debug_info.components.near_high.post_pipeline_value",
              "debug_info.components.mom30.post_pipeline_value",
              "debug_info.components.mom7.post_pipeline_value"]
    H = 7
    MIN_CASES = 100

    reading = ("Situation = 30-bar return > 0, read from the recorded mom30 raw value "
               "(recomputed from closes inside the window where it is missing). The expected side "
               "of this graded long idea is a forecast whose sign follows the equal-weight mean of "
               "the three standardised terms, so higher readings give a higher forecast. "
               "Each coin's mean 7-bar return is taken over its non-overlapping grid bars in all "
               "windows and all regimes. The slope t is the ordinary OLS t. "
               "The plan's 'fewer than 100 trending grid cases' is treated as a minimum count, "
               "so it gives 'not observable'.")

    def get(df, col):
        return pd.to_numeric(df[col], errors="coerce") if col in df.columns else pd.Series(np.nan, index=df.index)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            m30 = get(df, C_MOM30)
            m30_px = close / close.shift(30) - 1.0
            m30 = m30.where(m30.notna(), m30_px)
            situ = (m30 > 0).fillna(False)
            post = pd.concat([get(df, c) for c in P_COLS], axis=1)
            score = post.mean(axis=1, skipna=False)
            side_ok = (np.sign(fc) == np.sign(score)) & score.notna()
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & side_ok).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are bars where the 30-day return is positive "
                           "and the forecast follows the graded near-high, 30-day and 7-day terms."),
            "reading": reading,
        }

    # ---------- main measure ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            n = len(df)
            for t in range(0, n, H):
                if t + H < n:
                    r = close[t + H] / close[t] - 1.0
                    rows.append((coin, r, fc[t], reg[t]))
    g = pd.DataFrame(rows, columns=["coin", "ret", "fc", "regime"])
    g = g[np.isfinite(g["ret"])]
    coin_mean = g.groupby("coin")["ret"].mean()
    tr = g[g["regime"] == "trending"].copy()
    tr["ex"] = tr["ret"] - tr["coin"].map(coin_mean)
    tr = tr.dropna(subset=["ex", "fc"])
    n_cases = int(len(tr))

    slope = None
    t_slope = None
    if n_cases >= 3 and tr["fc"].std() > 0:
        res = stats.linregress(tr["fc"].values, tr["ex"].values)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr > 0 else None

    # ---------- supporting check: timing part ----------
    book_parts = []
    for coin, wins in bars.items():
        drets = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce")
            drets.append(c / c.shift(1) - 1.0)
        mu = pd.concat(drets).dropna().mean() if drets else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            day = ts.dt.floor("D")
            v = pd.to_numeric(df["postRebalance_total_value"], errors="coerce")
            a = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            d = pd.DataFrame({"day": day, "v": v, "a": a})
            d = d.groupby("day").last()
            d["book"] = d["v"] / d["v"].shift(1) - 1.0
            d["mkt"] = d["a"].shift(1) * mu
            d = d.dropna(subset=["book", "mkt"])
            d["coin"] = coin
            book_parts.append(d[["book", "mkt", "coin"]].reset_index())
    timing = None
    if book_parts:
        bp = pd.concat(book_parts, ignore_index=True)
        if len(bp):
            daily = bp.groupby("day")[["book", "mkt"]].mean()
            timing = float(daily["book"].mean() - daily["mkt"].mean())
    sup_pass = None if timing is None else bool(timing > 0)

    # ---------- decision ----------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} trending grid cases, fewer than the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast)."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the timing part is positive."
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
            "name": "slope of trending-grid 7-bar forward return minus coin mean on forecast",
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": "t >= 2 confirms (with positive timing), t <= -2 rejects",
        },
        "supporting_check": {
            "name": "book mean daily return minus market-rise gain (timing part) > 0",
            "value": timing,
            "passed": sup_pass,
        },
        "counts": {"trending grid cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
