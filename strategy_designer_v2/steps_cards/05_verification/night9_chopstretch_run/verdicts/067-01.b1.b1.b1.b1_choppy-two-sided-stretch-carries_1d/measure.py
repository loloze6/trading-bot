import numpy as np
import pandas as pd

H = 10
FC = "forecast"
RAW = "debug_info.components.stretch.last_history_value"


def _num(s):
    return pd.to_numeric(s, errors="coerce")


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = _num(df["close"])
            fc = _num(df[FC]).fillna(0.0)
            raw = _num(df[RAW]) if RAW in df.columns else pd.Series(np.nan, index=df.index)
            # 60-bar price evolution in percent, recomputed inside the window only
            evo = (close / close.shift(60) - 1.0) * 100.0
            if "regime" in df.columns:
                reg = df["regime"].astype(str)
            else:
                reg = pd.Series("", index=df.index)
            chop_calc = (evo >= -10.0) & (evo <= 10.0)
            # where the 60-bar return cannot be computed inside the window, use the recorded profile decision
            choppy = np.where(evo.notna(), chop_calc, reg != "chop")
            active = fc != 0
            side_ok = np.sign(fc) == np.sign(raw)
            side_ok = side_ok & raw.notna() & (raw != 0)
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(choppy, index=df.index) & side_ok).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of the 10-bar forward return minus the coin's normal 10-bar drift on the recorded forecast"
    thr = "slope t >= 2 confirms (with both sides' mean unusual move > 0); t <= -2 rejects; otherwise inconclusive"
    reading_base = ("The choppy situation is |60-bar close return| <= 10 % recomputed inside each window, falling back "
                    "on the recorded regime (not 'chop') for bars without 60 prior bars in the window, and the side is the "
                    "sign of the raw stretch; the drift is the coin's mean 10-bar return on the non-overlapping grid of all "
                    "its windows; the slope's t uses day-clustered (CR1) standard errors on cases grouped by UTC date; "
                    "the plan's 'fewer cases than the minimum' is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast lie in the choppy profile "
                           "(|60-day return| <= 10 %) with the forecast's sign equal to the stretch's sign."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = _num(df["close"]).values
            fc = _num(df[FC]).fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if fc[i] != 0:
                    coin_rows.append((coin, ts.iloc[i].strftime("%Y-%m-%d"), float(fc[i]), r))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for c, d, f, r in coin_rows:
            rows.append({"coin": c, "day": d, "f": f, "y": r - drift})

    cases = pd.DataFrame(rows, columns=["coin", "day", "f", "y"])
    n_total = int(len(cases))
    n_long = int((cases["f"] > 0).sum()) if n_total else 0
    n_short = int((cases["f"] < 0).sum()) if n_total else 0
    n_days = int(cases["day"].nunique()) if n_total else 0
    counts = {"cases in total": n_total, "cases with forecast > 0": n_long,
              "cases with forecast < 0": n_short, "days": n_days}

    slope = None
    tval = None
    if n_total >= 3 and cases["f"].nunique() > 1:
        X = np.column_stack([np.ones(n_total), cases["f"].values])
        y = cases["y"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        meat = np.zeros((2, 2))
        G = 0
        for _, idx in cases.groupby("day").indices.items():
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
            G += 1
        k = 2
        adj = (G / (G - 1.0)) * ((n_total - 1.0) / (n_total - k)) if G > 1 and n_total > k else 1.0
        V = adj * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tval = float(slope / se) if np.isfinite(se) and se > 0 else None

    if n_long > 0:
        m_long = float(cases.loc[cases["f"] > 0, "y"].mean())
    else:
        m_long = None
    if n_short > 0:
        m_short = float((-cases.loc[cases["f"] < 0, "y"]).mean())
    else:
        m_short = None
    sup_pass = None
    if m_long is not None and m_short is not None:
        sup_pass = bool(m_long > 0 and m_short > 0)
    sup = {"name": "mean unusual move in the forecast's direction > 0 on each side",
           "value": {"long": m_long, "short": m_short}, "passed": sup_pass}
    # value must be a number: report the smaller side, keep both in name
    sup_value = None if (m_long is None or m_short is None) else float(min(m_long, m_short))
    sup = {"name": "smaller of the two sides' mean unusual move in the forecast's direction (long %s, short %s), must be > 0"
                   % (m_long, m_short),
           "value": sup_value, "passed": sup_pass}

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "slope t, cases of one day clustered", "value": tval} if tval is not None else None),
            "threshold": thr}

    if n_total < 100 or n_long < 30 or n_short < 30:
        status = "not observable"
        decided = ("A minimum count is not reached: the plan needs at least 100 cases in total and 30 on each side "
                   "(got %d total, %d long, %d short)." % (n_total, n_long, n_short))
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and both sides' mean unusual move in the forecast's direction is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger stretches are followed by moves back toward the average."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but one side's mean unusual move is 0 or below."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
