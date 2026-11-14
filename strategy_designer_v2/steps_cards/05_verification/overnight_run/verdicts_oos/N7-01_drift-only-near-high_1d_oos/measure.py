import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    P = 20
    REC_COL = "debug_info.components.recency.last_history_value"

    def window_frame(df):
        df = df.reset_index(drop=True)
        close = pd.to_numeric(df["close"], errors="coerce")
        fc = pd.to_numeric(df["forecast"], errors="coerce")
        n = len(df)

        # Plan's regime condition: the close above its 20-day SMA.
        sma = close.rolling(P, min_periods=P).mean()
        above = pd.Series(np.where(sma.notna(), (close > sma).astype(float), np.nan))

        # New 20-day closing high, and the bars since it (recomputed from prices).
        rmax = close.rolling(P, min_periods=P).max()
        is_high = pd.Series(np.where(rmax.notna(), (close >= rmax).astype(float), np.nan))
        bsh_ok = np.full(n, np.nan)
        hv = is_high.values
        for t in range(n):
            lo = t - (P - 1)
            seg = hv[max(lo, 0): t + 1]
            if np.any(seg == 1.0):
                bsh_ok[t] = 1.0
            elif lo >= 0 and not np.any(np.isnan(seg)):
                bsh_ok[t] = 0.0
        bsh_ok = pd.Series(bsh_ok)

        # Prefer the recorded raw BarsSinceHigh value where it exists.
        if REC_COL in df.columns:
            rec = pd.to_numeric(df[REC_COL], errors="coerce")
            bsh_ok = pd.Series(np.where(rec.notna(), (rec > 0).astype(float), bsh_ok))

        # Where the prices cannot decide (start of the window), use the regime label.
        reg = (df["regime"].astype(str) == "trending").astype(float) if "regime" in df.columns \
            else pd.Series(np.nan, index=df.index)
        sit = pd.Series(np.where(above.notna() & bsh_ok.notna(),
                                 ((above == 1) & (bsh_ok == 1)).astype(float), reg.values))

        fwd = close.shift(-H) / close - 1.0
        pos = np.arange(n)
        grid = (pos % H) == 0

        return pd.DataFrame({
            "fc": fc,
            "sit": sit,
            "above": above,
            "bsh_ok": bsh_ok,
            "fwd": fwd,
            "grid": grid,
        })

    frames = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = window_frame(df)
            f["coin"] = coin
            frames[(coin, w)] = f

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "forecast-weighted mean 5-bar excess return", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
            "supporting_check": None,
            "counts": {"non-overlapping active 5-bar blocks": 0},
            "decided_by": "No data in the record.",
            "reading": "none",
        }

    allf = pd.concat(frames.values(), ignore_index=True)

    # ---- Situation check ----
    act = allf[allf["fc"].notna() & (allf["fc"] != 0)]
    act_known = act[act["sit"].notna()]
    if len(act_known) > 0:
        agree = float(((act_known["sit"] == 1) & (act_known["fc"] > 0)).mean())
    else:
        agree = None
    passed = agree is not None and agree >= 0.9

    reading = ("Situation = close > SMA20 of closes and a 20-bar closing high within the last 20 bars "
               "(the recorded raw BarsSinceHigh > 0 where present, else recomputed from closes, else the "
               "regime label where the window start lacks history), long side; the coin's mean 5-bar return "
               "is taken over all its non-overlapping grid bars in all windows; the t of the forecast-weighted "
               "mean uses the weighted standard error sqrt(n/(n-1)*sum(w^2(x-m)^2))/sum(w); the supporting "
               "check's 'excess over holding' is the same excess over the coin's mean 5-bar return, on "
               "flat grid bars, and it is reported but does not change the confirm/reject rule.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agree, "passed": False},
            "main_measure": {"name": "forecast-weighted mean 5-bar excess return", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
            "supporting_check": None,
            "counts": {"active bars": int(len(act))},
            "decided_by": ("Fewer than 90% of active bars are long bars with the close above SMA20 and a new "
                           "20-day high within 20 bars, as the Fidelity's situation requires."),
            "reading": reading,
        }

    # ---- Main measure ----
    g = allf[allf["grid"] & allf["fwd"].notna()].copy()
    coin_mean = g.groupby("coin")["fwd"].mean()
    g["exc"] = g["fwd"] - g["coin"].map(coin_mean)

    a = g[g["fc"].notna() & (g["fc"] > 0)]
    n_blocks = int(len(a))
    mean_w = None
    t_w = None
    if n_blocks > 0:
        w = a["fc"].values.astype(float)
        x = a["exc"].values.astype(float)
        sw = w.sum()
        mean_w = float((w * x).sum() / sw)
        if n_blocks > 1:
            var_term = (n_blocks / (n_blocks - 1.0)) * np.sum(w ** 2 * (x - mean_w) ** 2)
            se = np.sqrt(var_term) / sw
            t_w = float(mean_w / se) if se > 0 else None

    # ---- Supporting check ----
    s = g[g["fc"].notna() & (g["fc"] == 0) & (g["bsh_ok"] == 1) & (g["above"] == 0)]
    sup_val = float(s["exc"].mean()) if len(s) > 0 else None
    sup_pass = (sup_val <= 0) if sup_val is not None else None
    supporting = {"name": "mean 5-bar excess return, flat bars with recent high but close below SMA20",
                  "value": sup_val, "passed": sup_pass}

    counts = {"non-overlapping active 5-bar blocks": n_blocks,
              "flat below-SMA20 recent-high blocks": int(len(s))}

    if n_blocks < 100:
        status = "not observable"
        decided = "Fewer than 100 non-overlapping active 5-bar blocks across all coins and windows."
    elif t_w is None or mean_w is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_w > 0 and t_w >= 2:
        status = "confirmed"
        decided = "The forecast-weighted mean excess return is positive with t >= 2."
    elif mean_w < 0 and t_w <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic is strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agree, "passed": True},
        "main_measure": {"name": "forecast-weighted mean 5-bar excess return over coin mean",
                         "value": mean_w,
                         "statistic": {"name": "t of weighted mean", "value": t_w} if t_w is not None else None,
                         "threshold": "positive with t >= 2 confirms; negative with t <= -2 rejects"},
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
