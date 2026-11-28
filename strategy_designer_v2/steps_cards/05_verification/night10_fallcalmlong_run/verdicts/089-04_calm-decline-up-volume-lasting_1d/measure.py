import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    HALF = 5
    SHARE_COL = "debug_info.components.up_vol_share.last_history_value"
    PERIOD = 20

    def recompute_share(df):
        # 20-bar share of volume on up-close days, minus 0.5 ("centred"), inside the window only
        c = df["close"].astype(float)
        v = df["volume"].astype(float)
        up = (c.diff() > 0).astype(float)
        up[c.diff().isna()] = np.nan
        upv = (v * up).rolling(PERIOD, min_periods=PERIOD).sum()
        totv = v.where(~up.isna()).rolling(PERIOD, min_periods=PERIOD).sum()
        sh = upv / totv - 0.5
        sh[totv == 0] = np.nan
        return sh

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if SHARE_COL in df.columns:
                share = pd.to_numeric(df[SHARE_COL], errors="coerce")
            else:
                share = pd.Series(np.nan, index=df.index)
            share = share.fillna(recompute_share(df))
            in_profile = df["regime"].astype(str) == "unknown"
            situation = in_profile & (share > 0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of the 10-bar excess return on the forecast (cases forecast > 0, day-clustered)"
    threshold = "confirm: slope > 0 with t >= 2 and second-half check passes; reject: slope < 0 with t <= -2; at least 30 cases on at least 30 distinct days"
    reading_txt = ("The falling calm profile is read from the recorded regime (the detector's 'unknown' regime, the one left when "
                   "neither the trend veto nor the volatility veto fires) and the up side of the situation as the raw centred share > 0; "
                   "the slope is the OLS slope of excess return on forecast with a day-clustered standard error; the coin's mean 10-bar "
                   "return is the mean over the non-overlapping 10-bar grids of all its windows, and the second-half excess return is "
                   "close[t+10]/close[t+5]-1 minus the coin's mean 5-bar return over the non-overlapping 5-bar grids of all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None, "active bars": int(n_active)},
            "decided_by": ("Only %.1f%% of the bars with a non-zero forecast are bars of the falling calm profile with an up-day "
                           "volume lean (share > 0.5) and a long forecast, below the 90%% required." % (100 * agreement)),
            "reading": reading_txt,
        }

    # ---------- 2. criterion ----------
    # coin drifts on non-overlapping grids, all windows together
    drift10 = {}
    drift5 = {}
    for coin, wins in bars.items():
        r10, r5 = [], []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            n = len(c)
            for i in range(0, n - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    r10.append(c[i + H] / c[i] - 1)
            for i in range(0, n - HALF, HALF):
                if np.isfinite(c[i]) and np.isfinite(c[i + HALF]) and c[i] > 0:
                    r5.append(c[i + HALF] / c[i] - 1)
        drift10[coin] = float(np.mean(r10)) if r10 else np.nan
        drift5[coin] = float(np.mean(r5)) if r5 else np.nan

    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                f = fc[i]
                if not np.isfinite(f) or f <= 0:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and np.isfinite(c[i + HALF]) and c[i] > 0 and c[i + HALF] > 0):
                    continue
                ex = c[i + H] / c[i] - 1 - drift10[coin]
                ex2 = c[i + H] / c[i + HALF] - 1 - drift5[coin]
                if not (np.isfinite(ex) and np.isfinite(ex2)):
                    continue
                rows.append((ts.iloc[i].normalize(), float(f), float(ex), float(ex2)))

    n_cases = len(rows)
    days = [r[0] for r in rows]
    n_days = int(len(set(days)))
    counts = {"cases": int(n_cases), "distinct days": n_days}

    slope = None
    tstat = None
    if n_cases >= 3:
        d = pd.DataFrame(rows, columns=["day", "f", "ex", "ex2"])
        X = np.column_stack([np.ones(len(d)), d["f"].to_numpy()])
        y = d["ex"].to_numpy()
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ X.T @ y
            e = y - X @ beta
            meat = np.zeros((2, 2))
            codes = pd.factorize(d["day"])[0]
            G = int(codes.max() + 1)
            for g in range(G):
                m = codes == g
                s = X[m].T @ e[m]
                meat += np.outer(s, s)
            N = len(d)
            corr = (G / (G - 1)) * ((N - 1) / (N - 2)) if G > 1 and N > 2 else 1.0
            V = XtX_inv @ meat @ XtX_inv * corr
            slope = float(beta[1])
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            tstat = float(slope / se) if np.isfinite(se) and se > 0 else None
        wsum = d["f"].sum()
        sup_val = float((d["ex2"] * d["f"]).sum() / wsum) if wsum > 0 else None
    else:
        sup_val = None
        if n_cases > 0:
            d = pd.DataFrame(rows, columns=["day", "f", "ex", "ex2"])
            wsum = d["f"].sum()
            sup_val = float((d["ex2"] * d["f"]).sum() / wsum) if wsum > 0 else None
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = ("The plan's minimum of 30 cases on 30 distinct days is not reached (%d cases on %d days)." % (n_cases, n_days))
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the forecast-weighted second-half excess return is above 0 (confirm rule)."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    elif slope > 0 and tstat >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the second-half check fails (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope has |t| < 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tstat is None else {"name": "t of the OLS slope, day-clustered", "value": tstat},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "forecast-weighted mean excess return over t+5 to t+10 > 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading_txt,
    }
