import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.scaled_move.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    n_active_nan = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            ret = close / close.shift(1) - 1.0
            vol20 = ret.rolling(20, min_periods=20).std()
            volratio = vol20 / vol20.rolling(60, min_periods=60).mean()
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # day's move: the component's raw value if recorded, else the price return
            move = raw.where(raw.notna(), ret)
            active = fc != 0
            for i in df.index[active]:
                vr = volratio.iloc[i]
                mv = move.iloc[i]
                if pd.isna(vr) or pd.isna(mv):
                    # fall back on the detector's decision when the ratio cannot be rebuilt in-window
                    if pd.isna(mv):
                        n_active_nan += 1
                        n_active += 1
                        continue
                    in_sit = str(df["regime"].iloc[i]) == "trending"
                else:
                    in_sit = vr >= 1.0 - 1e-12
                n_active += 1
                side_ok = np.sign(fc.iloc[i]) == -np.sign(mv) and mv != 0
                if in_sit and side_ok:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "pooled OLS slope of next-bar excess return on forecast/10 (high-vol bars)"
    threshold = "confirm: slope > 0 with t >= 2 and >= 2 of 3 coins positive; reject: slope < 0 with t <= -2 and >= 2 of 3 coins negative"
    reading = ("The situation is rebuilt in each window as the 20-day std of daily returns at or above its 60-bar mean "
               "(falling back on regime == 'trending' where the window is too short to rebuild it), the expected side is "
               "opposite to the day's scaled move; the OLS includes an intercept; the per-coin minimum of 60 and the "
               "'2 of the 3 coins' rule are applied to the coins present in the record.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are high-volatility bars (20-day vol at or above its 60-day mean) with a forecast against the day's move.",
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    def ols(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        n = len(x)
        if n < 3 or np.var(x) == 0:
            return None, None
        X = np.column_stack([np.ones(n), x])
        beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X @ beta
        s2 = resid @ resid / (n - 2)
        cov = s2 * np.linalg.inv(X.T @ X)
        se = np.sqrt(cov[1, 1])
        t = beta[1] / se if se > 0 else None
        return float(beta[1]), (float(t) if t is not None else None)

    xs_all, ys_all = [], []
    per_coin = {}
    for coin, wins in bars.items():
        # coin's mean daily return over all its windows
        all_rets = []
        frames = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            nxt = close.shift(-1) / close - 1.0
            all_rets.append(nxt.dropna().values)
            frames.append((df, nxt))
        allr = np.concatenate(all_rets) if all_rets else np.array([])
        mu = float(np.mean(allr)) if len(allr) else 0.0
        xs, ys = [], []
        for df, nxt in frames:
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            m = (df["regime"].astype(str) == "trending") & fc.notna() & (fc != 0) & nxt.notna()
            xs.extend((fc[m] / 10.0).tolist())
            ys.extend((nxt[m] - mu).tolist())
        per_coin[coin] = (xs, ys)
        xs_all.extend(xs)
        ys_all.extend(ys)

    n_pooled = len(xs_all)
    counts = {"pooled high-volatility bars": int(n_pooled)}
    for coin, (xs, ys) in per_coin.items():
        counts[f"high-volatility bars {coin}"] = int(len(xs))

    slope, t = ols(xs_all, ys_all)
    coin_slopes = {c: ols(xs, ys)[0] for c, (xs, ys) in per_coin.items()}

    stat = {"name": "OLS t of pooled slope", "value": t} if t is not None else None
    main = {"name": main_name, "value": slope, "statistic": stat, "threshold": threshold}

    short = [c for c, (xs, _) in per_coin.items() if len(xs) < 60]
    if n_pooled < 300 or short or slope is None or t is None:
        why = []
        if n_pooled < 300:
            why.append(f"{n_pooled} pooled high-volatility bars < 300")
        if short:
            why.append("fewer than 60 high-volatility bars for " + ", ".join(short))
        if not why:
            why.append("slope could not be estimated")
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": main,
            "supporting_check": {"name": "coins with per-coin slope of pooled sign", "value": None, "passed": None},
            "counts": counts,
            "decided_by": "Minimum count not reached: " + "; ".join(why) + ".",
            "reading": reading,
        }

    psign = np.sign(slope)
    same = sum(1 for s in coin_slopes.values() if s is not None and np.sign(s) == psign and psign != 0)
    n_pos = sum(1 for s in coin_slopes.values() if s is not None and s > 0)
    n_neg = sum(1 for s in coin_slopes.values() if s is not None and s < 0)
    check_pass = same >= 2
    support = {"name": "coins with per-coin slope of pooled sign (need >= 2)", "value": int(same), "passed": bool(check_pass)}

    if slope > 0 and t >= 2 and n_pos >= 2 and check_pass:
        status = "confirmed"
        dec = "Pooled slope positive with t >= 2 and at least 2 coins with positive slopes."
    elif slope < 0 and t <= -2 and n_neg >= 2:
        status = "rejected"
        dec = "Pooled slope negative with t <= -2 and at least 2 coins with negative slopes: the next day continues the scaled move."
    elif -2 < t < 2:
        status = "inconclusive"
        dec = "Pooled t lies between -2 and 2."
    else:
        status = "inconclusive"
        dec = "|t| >= 2 but the coins do not agree as required."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": dec,
        "reading": reading,
    }
