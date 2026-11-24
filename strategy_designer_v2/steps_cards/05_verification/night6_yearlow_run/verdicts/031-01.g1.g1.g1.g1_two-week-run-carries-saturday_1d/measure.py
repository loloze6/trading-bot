import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.run14.last_history_value"
    PPV = "debug_info.components.run14.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True)
            fc = pd.to_numeric(df[FC], errors="coerce")
            active = fc.notna() & (fc != 0)
            if active.sum() == 0:
                continue
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            friday = ts.dt.dayofweek == 4  # Friday-stamped bar: its close is Friday's close, the coming bar is Saturday
            same_side = np.sign(fc) == np.sign(raw)
            ok = active & friday & raw.notna() & (raw != 0) & same_side
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "slope of Saturday's excess return on the Friday run14 forecast"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 300 Friday cases and 100 distinct Saturdays"
    reading = ("Friday-close bars are bars stamped Friday (dayofweek 4) whose regime is 'trending'; the regression has an "
               "intercept and the slope's t uses standard errors clustered by Saturday (score contributions summed per day "
               "across coins, with a G/(G-1) correction); the coin's mean daily return is over all its windows' within-window daily returns.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on expected side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Friday-close bars whose forecast sign "
                           "matches the sign of the 14-day volatility-scaled return (the plan's situation and long-after-rise side)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys, days = [], [], []
    for coin, wins in bars.items():
        # coin's mean daily return over all windows
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            r = c[1:] / c[:-1] - 1.0
            rets.append(r[np.isfinite(r)])
        if not rets:
            continue
        allr = np.concatenate(rets)
        if len(allr) == 0:
            continue
        mu = float(np.mean(allr))
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True).reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            reg = df["regime"].reset_index(drop=True).astype(str)
            if PPV in df.columns:
                x = pd.to_numeric(df[PPV], errors="coerce").reset_index(drop=True)
            else:
                x = pd.Series(np.nan, index=range(len(df)))
            fwd = c.shift(-1) / c - 1.0
            nxt_ts = ts.shift(-1)
            sel = (ts.dt.dayofweek == 4) & (reg == "trending") & fwd.notna() & x.notna() & np.isfinite(fwd)
            for i in np.where(sel.values)[0]:
                xs.append(float(x.iloc[i]))
                ys.append(float(fwd.iloc[i]) - mu)
                d = nxt_ts.iloc[i]
                days.append(str(pd.Timestamp(d).normalize().date()) if pd.notna(d) else str((ts.iloc[i] + pd.Timedelta(days=1)).date()))

    n = len(xs)
    n_days = len(set(days))
    counts = {"Friday cases": n, "distinct Saturdays": n_days}

    slope = None
    tval = None
    if n >= 3 and n_days >= 2:
        X = np.column_stack([np.ones(n), np.array(xs)])
        y = np.array(ys)
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ X.T @ y
            e = y - X @ beta
            dser = pd.Series(days)
            meat = np.zeros((2, 2))
            sc = X * e[:, None]
            g = pd.DataFrame(sc).groupby(dser.values).sum().values
            for row in g:
                meat += np.outer(row, row)
            G = g.shape[0]
            V = XtX_inv @ meat @ XtX_inv * (G / (G - 1.0))
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            slope = float(beta[1])
            tval = float(slope / se) if se and np.isfinite(se) and se > 0 else None

    if n < 300 or n_days < 100:
        status = "not observable"
        decided = (f"Minimum count not reached: {n} Friday cases (300 needed) on {n_days} distinct Saturdays (100 needed).")
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed on the Friday cases."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "Confirm rule met: the slope is positive with t >= 2 over at least 300 Friday cases."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "Reject rule met: the slope is negative with t <= -2 over at least 300 Friday cases."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule met: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "slope t (clustered by Saturday)", "value": tval} if tval is not None else None),
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
