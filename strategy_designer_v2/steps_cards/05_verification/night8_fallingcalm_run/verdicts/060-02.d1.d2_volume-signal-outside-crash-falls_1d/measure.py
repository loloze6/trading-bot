import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.vol_growth.last_history_value"
    ALLOC = "postRebalance_current_allocation"
    H = 5

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    n_agree_fallback = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = df[FC].astype(float).fillna(0.0)
            r20 = (close / close.shift(20) - 1.0) * 100.0
            r60 = (close / close.shift(60) - 1.0) * 100.0
            m_recent = vol.rolling(30).mean()
            m_before = vol.shift(30).rolling(30).mean()
            with np.errstate(divide="ignore", invalid="ignore"):
                raw_re = np.log(m_recent / m_before)
            raw = df[RAW].astype(float) if RAW in df.columns else pd.Series(np.nan, index=df.index)
            raw = raw.where(raw.notna(), raw_re)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            for i in np.where(fc.values != 0)[0]:
                s_raw = np.sign(raw.iloc[i]) if pd.notna(raw.iloc[i]) else np.nan
                side_ok = pd.notna(s_raw) and s_raw == np.sign(fc.iloc[i])
                if pd.notna(r20.iloc[i]) and pd.notna(r60.iloc[i]):
                    n_active += 1
                    situ = (r60.iloc[i] < -10.0) and (r20.iloc[i] >= -20.0) and (r20.iloc[i] < 0.0)
                    if situ and side_ok:
                        n_agree += 1
                else:
                    n_active_uncomputable += 1
                    if regime.iloc[i] == "mean_reversion" and side_ok:
                        n_agree_fallback += 1
    if n_active > 0:
        agreement = n_agree / n_active
    elif n_active_uncomputable > 0:
        agreement = n_agree_fallback / n_active_uncomputable
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Situation = falling profile (60-bar return below -10 %, the config's veto) and 20-bar return in [-20 %, 0 %), "
               "recomputed from closes inside each window and checked on active bars where it is computable (the detector's "
               "regime is used only if none is), the expected side being the sign of the raw log volume ratio; the main "
               "measure is one pooled OLS of (5-bar return minus the coin's mean grid 5-bar return over all windows) on "
               "the forecast across all coins; the supporting check uses the before-cost book built from the held "
               "position times the next bar's return, each day averaged over coins.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90 % of the active bars are bars of the plan's moderate-fall situation inside the "
                           "falling profile with the forecast on the sign of the volume log ratio."),
            "reading": reading,
        }

    # ---------------- 2. main measure ----------------
    grid_rows = []
    coin_mean5 = {}
    coin_mean1 = {}
    for coin, wins in bars.items():
        all5 = []
        all1 = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    all5.append(r)
                    grid_rows.append((coin, float(df[FC].iloc[p]) if pd.notna(df[FC].iloc[p]) else np.nan, r))
            r1 = close[1:] / close[:-1] - 1.0
            all1.extend(list(r1[np.isfinite(r1)]))
        coin_mean5[coin] = float(np.mean(all5)) if all5 else np.nan
        coin_mean1[coin] = float(np.mean(all1)) if all1 else np.nan

    xs, ys = [], []
    for coin, f, r in grid_rows:
        if pd.notna(f) and f != 0 and np.isfinite(coin_mean5[coin]):
            xs.append(f)
            ys.append(r - coin_mean5[coin])
    xs = np.array(xs)
    ys = np.array(ys)
    n_cases = int(len(xs))

    slope = None
    tval = None
    if n_cases >= 3 and np.var(xs) > 0:
        res = stats.linregress(xs, ys)
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr > 0 else None

    # ---------------- supporting check ----------------
    book_parts = []
    mkt_parts = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            alloc = df[ALLOC].astype(float) if ALLOC in df.columns else pd.Series(np.nan, index=df.index)
            ret = close.shift(-1) / close - 1.0
            gain = alloc * ret
            mkt = alloc * coin_mean1[coin]
            day = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").shift(-1)
            tmp = pd.DataFrame({"day": day, "coin": coin, "gain": gain, "mkt": mkt}).dropna()
            book_parts.append(tmp)
    if book_parts:
        allg = pd.concat(book_parts, ignore_index=True)
        daily = allg.groupby("day")[["gain", "mkt"]].mean()
        timing = float(daily["gain"].mean() - daily["mkt"].mean()) if len(daily) else None
    else:
        timing = None
    sup_pass = None if timing is None else bool(timing > 0)

    main = {
        "name": "slope of next-5-bar excess return on forecast",
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
        "threshold": "confirm: slope positive with t >= 2 and supporting check passes; reject: slope negative with t <= -2",
    }
    sup = {"name": "book mean daily return minus market-rise gain (timing), before costs",
           "value": timing, "passed": sup_pass}
    counts = {"grid cases where the forecast is not 0": n_cases}

    if n_cases < 30:
        status = "not observable"
        decided = "Fewer than 30 grid cases where the forecast is not 0."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the timing part is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check fails."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
