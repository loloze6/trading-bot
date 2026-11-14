import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    P = 20
    MAXB = 20
    rec_col = "debug_info.components.recency.last_history_value"

    def bars_since_high_score(close):
        # BarsSinceHigh(lookback 20, max_bars 20): 20 on the day of a new 20-day closing high, minus 1 each bar after, 0 after 20 bars
        c = close.values.astype(float)
        rmax = close.rolling(P, min_periods=P).max().values
        out = np.full(len(c), np.nan)
        last = None
        for i in range(len(c)):
            if np.isnan(rmax[i]) or np.isnan(c[i]):
                continue
            if c[i] >= rmax[i]:
                last = i
            if last is None:
                out[i] = 0.0
            else:
                k = i - last
                out[i] = float(max(MAXB - k, 0))
        return pd.Series(out, index=close.index)

    # coin mean 5-bar return over all its windows together
    coin_mean = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            r = (c.shift(-H) / c - 1.0).dropna()
            rs.append(r.values)
        allr = np.concatenate(rs) if rs else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if allr.size else np.nan

    n_active = 0
    n_agree = 0
    act_x, act_w = [], []
    sup_x = []

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            f = df["forecast"].astype(float)
            sma = c.rolling(P, min_periods=P).mean()
            dist = c / sma - 1.0
            bsh_p = bars_since_high_score(c)
            if rec_col in df.columns:
                bsh = df[rec_col].astype(float).where(df[rec_col].notna(), bsh_p)
            else:
                bsh = bsh_p
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            above = dist > 0
            # where the SMA cannot be computed inside the window, the detector's decision stands in
            above = above.where(dist.notna(), reg == "trending")
            bsh_ok = (bsh > 0).where(bsh.notna(), reg == "trending")
            situ = above & bsh_ok

            # situation check on all active bars
            act = f.notna() & (f != 0)
            n_active += int(act.sum())
            n_agree += int((act & situ & (f > 0)).sum())

            # non-overlapping grid
            fwd = c.shift(-H) / c - 1.0
            cm = coin_mean[coin]
            for i in range(0, len(df), H):
                r = fwd.iloc[i]
                if pd.isna(r) or pd.isna(f.iloc[i]) or np.isnan(cm):
                    continue
                x = r - cm
                if f.iloc[i] != 0:
                    act_x.append(x)
                    act_w.append(abs(f.iloc[i]))
                else:
                    if pd.notna(dist.iloc[i]) and pd.notna(bsh.iloc[i]) and bsh.iloc[i] > 0 and dist.iloc[i] < 0:
                        sup_x.append(x)

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading = ("Situation taken as the gate (close above SMA20 and a new 20-day closing high within the last 20 bars, long), "
               "nearness to the high being graded not gated; the coin's mean 5-bar return uses every bar's 5-bar return in all its windows; "
               "the t of the forecast-weighted mean uses the weighted standard error sqrt(sum w^2 (x-m)^2)/sum w; "
               "the supporting check uses excess over the coin's mean on grid flat bars and does not enter the decision rule.")
    threshold = "confirm if mean > 0 and t >= 2; reject if mean < 0 and t <= -2; else inconclusive; at least 100 active blocks"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "forecast-weighted mean 5-bar excess return", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"non-overlapping active 5-bar blocks": int(len(act_x)), "active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars are long bars with close above SMA20 and a new 20-day high within 20 bars.",
            "reading": reading,
        }

    x = np.array(act_x, dtype=float)
    wt = np.array(act_w, dtype=float)
    n_blocks = int(len(x))
    m = None
    t = None
    if n_blocks > 0 and wt.sum() > 0:
        m = float(np.sum(x * wt) / np.sum(wt))
        se = float(np.sqrt(np.sum(wt ** 2 * (x - m) ** 2)) / np.sum(wt))
        if n_blocks > 1 and se > 0:
            t = float(m / se)

    sup_val = float(np.mean(sup_x)) if len(sup_x) > 0 else None
    sup_pass = (bool(sup_val <= 0) if sup_val is not None else None)

    if n_blocks < 100:
        status = "not observable"
        decided = f"Only {n_blocks} non-overlapping active 5-bar blocks, below the plan's minimum of 100."
    elif m is not None and t is not None and m > 0 and t >= 2:
        status = "confirmed"
        decided = "The forecast-weighted mean excess return is positive with t >= 2."
    elif m is not None and t is not None and m < 0 and t <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies strictly between -2 and 2 (or could not be computed)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "forecast-weighted mean 5-bar excess return", "value": m,
                         "statistic": ({"name": "weighted t of the mean", "value": t} if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean 5-bar excess return on flat bars, recent high, close below SMA20 (<= 0)",
                             "value": sup_val, "passed": sup_pass},
        "counts": {"non-overlapping active 5-bar blocks": n_blocks,
                   "supporting flat blocks": int(len(sup_x)),
                   "active bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
