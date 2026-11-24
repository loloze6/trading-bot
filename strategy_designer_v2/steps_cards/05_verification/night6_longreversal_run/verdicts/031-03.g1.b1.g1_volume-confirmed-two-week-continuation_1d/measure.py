import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    FOLLOW = "debug_info.components.follow.last_history_value"
    FADE = "debug_info.components.fade.last_history_value"

    def regime_name(r):
        r = str(r)
        if r.startswith("trend"):
            return "trending"
        if r.startswith("mean"):
            return "mean_reversion"
        return r

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            v14 = vol.rolling(14, min_periods=14).mean()
            v30 = vol.rolling(30, min_periods=30).mean()
            volr = v14 / v30.replace(0, np.nan)
            ret14 = close / close.shift(14) - 1.0
            rec_reg = df["regime"].map(regime_name) if "regime" in df.columns else pd.Series([None] * len(df))
            fol = pd.to_numeric(df[FOLLOW], errors="coerce") if FOLLOW in df.columns else pd.Series(np.nan, index=df.index)
            fad = pd.to_numeric(df[FADE], errors="coerce") if FADE in df.columns else pd.Series(np.nan, index=df.index)
            for i in range(len(df)):
                f = fc.iloc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                vr = volr.iloc[i]
                if np.isfinite(vr):
                    reg = "trending" if vr >= 1.0 else "mean_reversion"
                else:
                    reg = rec_reg.iloc[i]
                if reg not in ("trending", "mean_reversion"):
                    continue
                raw = fol.iloc[i] if reg == "trending" else fad.iloc[i]
                if np.isfinite(raw) and raw != 0:
                    rs = np.sign(raw)
                else:
                    r = ret14.iloc[i]
                    if not np.isfinite(r) or r == 0:
                        continue
                    rs = np.sign(r)
                expected = rs if reg == "trending" else -rs
                if np.sign(f) == expected:
                    n_agree += 1

    threshold_words = "mean > 0 with t >= 2 confirms (with both regime means > 0); mean < 0 with t <= -2 rejects; min 100 cases, 30 per regime"
    mm_name = "mean signed 14-bar forward return minus coin's mean 14-bar return, on 14-bar grid"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold_words},
            "supporting_check": None,
            "counts": {"cases": 0, "trending cases": 0, "mean_reversion cases": 0},
            "decided_by": "No bar has a non-zero forecast, so the minimum of 100 cases is not reached.",
            "reading": "none",
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold_words},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars follow the 14-day return when 14/30 volume ratio >= 1 and fade it when < 1, as the Fidelity states.",
            "reading": "Regime recomputed from volume (14-bar over 30-bar mean, current bar included), falling back to the recorded regime in a window's first 29 bars; return sign from the active component's raw value, else from the 14-bar price return.",
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, fwd, sign, regime)
    coin_mu = {}
    for coin, wins in bars.items():
        all_fwd = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            reg = df["regime"].map(regime_name).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_fwd.append(r)
                f = fc[i]
                if np.isfinite(f) and f != 0:
                    cases.append((coin, ts.iloc[i].floor("D"), r, float(np.sign(f)), reg[i]))
        coin_mu[coin] = float(np.mean(all_fwd)) if all_fwd else np.nan

    rows = [(c, d, (r - coin_mu[c]) * s, g) for (c, d, r, s, g) in cases if np.isfinite(coin_mu.get(c, np.nan))]
    cdf = pd.DataFrame(rows, columns=["coin", "day", "x", "regime"])

    def clustered(sub):
        n = len(sub)
        if n == 0:
            return np.nan, np.nan, 0
        m = sub["x"].mean()
        dev = (sub["x"] - m).groupby(sub["day"]).sum()
        D = len(dev)
        if D < 2:
            return float(m), np.nan, D
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / n
        t = m / se if se > 0 else np.nan
        return float(m), float(t), D

    m, t, D = clustered(cdf)
    tr = cdf[cdf["regime"] == "trending"]
    mr = cdf[cdf["regime"] == "mean_reversion"]
    m_tr = float(tr["x"].mean()) if len(tr) else np.nan
    m_mr = float(mr["x"].mean()) if len(mr) else np.nan
    sc_pass = bool(np.isfinite(m_tr) and np.isfinite(m_mr) and m_tr > 0 and m_mr > 0)

    counts = {"cases": int(len(cdf)), "trending cases": int(len(tr)),
              "mean_reversion cases": int(len(mr)), "days": int(D)}

    def nz(v):
        return float(v) if v is not None and np.isfinite(v) else None

    if len(cdf) < 100:
        status, dec = "not observable", "Fewer than 100 cases in total."
    elif len(tr) < 30:
        status, dec = "not observable", "Fewer than 30 trending cases."
    elif len(mr) < 30:
        status, dec = "not observable", "Fewer than 30 mean_reversion cases."
    elif np.isfinite(t) and m > 0 and t >= 2:
        if sc_pass:
            status, dec = "confirmed", "Main mean above 0 with t >= 2 and both regime means above 0."
        else:
            status, dec = "inconclusive", "Main mean above 0 with t >= 2 but one regime's mean is not above 0."
    elif np.isfinite(t) and m < 0 and t <= -2:
        status, dec = "rejected", "Main mean below 0 with t <= -2."
    else:
        status, dec = "inconclusive", "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": mm_name, "value": nz(m),
                         "statistic": {"name": "t of the mean, same-day cases summed", "value": nz(t)},
                         "threshold": threshold_words},
        "supporting_check": {"name": "mean > 0 in both trending and mean_reversion cases",
                             "value": nz(min(m_tr, m_mr)) if np.isfinite(m_tr) and np.isfinite(m_mr) else None,
                             "passed": sc_pass},
        "counts": counts,
        "decided_by": dec,
        "reading": "Cases are assigned to a regime by the recorded regime on the grid bar, the coin's mean is over its 14-bar grid returns in all windows, the t sums same-day deviations into one per day, and the plan's 'too few cases' rule is reported as not observable; supporting-check value is the smaller regime mean.",
    }
