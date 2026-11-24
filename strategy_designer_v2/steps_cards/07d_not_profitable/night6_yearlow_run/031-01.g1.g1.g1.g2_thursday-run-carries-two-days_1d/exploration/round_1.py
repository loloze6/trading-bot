def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    days = data["days"]; bars = data["bars"]
    coins = list(bars.keys())
    windows = sorted({w for c in coins for w in bars[c].keys()}, key=lambda s: int(s[1:]))
    # ---- per coin-day contributions split by side
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            d = days[c][w].sort_values("day").reset_index(drop=True)
            prev_alloc = b["postRebalance_current_allocation"].shift(1)
            br = b["postRebalance_total_value"].pct_change()
            df = pd.DataFrame({"day": b["timestamp"].dt.floor("D"), "ret": br, "palloc": prev_alloc,
                               "coin": c, "w": w, "close": b["close"]})
            rows.append(df)
    cd = pd.concat(rows)
    cd["side"] = np.where(cd["palloc"] > 1e-9, "long", np.where(cd["palloc"] < -1e-9, "short", "flat"))
    def book(series_df):
        # mean over coins per day per window, chain in window order
        out = []
        for w in windows:
            x = series_df[series_df.w == w]
            if len(x) == 0: continue
            out.append(x.groupby("day")["r"].mean().dropna().sort_index())
        return pd.concat(out).reset_index(drop=True)
    def stats_of(r):
        v = (1 + r).cumprod(); dd = (v / v.cummax() - 1)
        yr = v.iloc[-1] ** (365 / len(r)) - 1
        return {"sharpe": r.mean() / r.std() * np.sqrt(365), "yearly": yr, "maxdd": dd.min(),
                "calmar": yr / -dd.min()}
    res = {}
    tab = {}
    for name, mask in [("all", None), ("long_only", "long"), ("short_only", "short")]:
        x = cd.copy()
        x["r"] = x["ret"] if mask is None else np.where(x["side"] == mask, x["ret"], 0.0)
        x.loc[x["ret"].isna(), "r"] = np.nan
        tab[name] = stats_of(book(x))
    res["book_by_side"] = pd.DataFrame(tab).T
    # ---- deepest fall: which side lost
    x = cd.copy(); x["r"] = x["ret"]
    out = []
    for w in windows:
        xx = x[x.w == w]
        g = xx.groupby("day")["r"].mean().dropna().sort_index()
        gl = xx.assign(rl=np.where(xx.side == "long", xx.r, 0), rs=np.where(xx.side == "short", xx.r, 0)).groupby("day")[["rl", "rs"]].sum() / 6
        out.append(pd.DataFrame({"r": g, "rl": gl["rl"].reindex(g.index), "rs": gl["rs"].reindex(g.index), "w": w}))
    B = pd.concat(out).reset_index()
    B["year"] = pd.to_datetime(B["day"]).dt.year
    v = (1 + B.r).cumprod(); dd = v / v.cummax() - 1
    trough = dd.idxmin(); peak = v.iloc[:trough + 1].idxmax()
    seg = B.iloc[peak:trough + 1]
    res["deepest_fall"] = pd.Series({"depth": dd.min(), "days": trough - peak, "sum_long": seg.rl.sum(),
                                    "sum_short": seg.rs.sum(), "windows": seg.w.nunique(), "year_of_trough": B.year.iloc[trough]})
    res["by_year"] = B.groupby("year").agg(sum_r=("r", "sum"), sum_long=("rl", "sum"), sum_short=("rs", "sum"), n=("r", "size"))
    # ---- cases: Thursday signals
    cs = []
    for c in coins:
        drift_parts = []
        for w, b in bars[c].items():
            cl = b.sort_values("timestamp")["close"].values
            g = cl[::2]; drift_parts.append(g[1:] / g[:-1] - 1)
        drift = np.concatenate(drift_parts).mean()
        for w, b in bars[c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            cl = b["close"]
            r2 = cl.shift(-2) / cl - 1
            r1 = b["close"].pct_change()
            vol20 = r1.rolling(20).std()
            r60 = cl / cl.shift(60) - 1
            r14 = cl / cl.shift(14) - 1
            hi365 = cl.rolling(365, min_periods=120).max(); lo365 = cl.rolling(365, min_periods=120).min()
            pos = (cl - lo365) / (hi365 - lo365)
            ma100 = cl.rolling(100, min_periods=60).mean()
            df = pd.DataFrame({"f": b["forecast"], "r2": r2 - drift, "r2raw": r2, "vol20": vol20, "r60": r60, "r14": r14,
                               "pos": pos, "above100": cl > ma100, "alloc": b["postRebalance_current_allocation"],
                               "day": b["timestamp"].dt.floor("D"), "coin": c, "w": w,
                               "year": b["timestamp"].dt.year, "wd": b["timestamp"].dt.weekday})
            cs.append(df)
    A = pd.concat(cs)
    C = A[(A.f != 0) & A.r2.notna()].copy()
    C["sgn"] = np.sign(C.f)
    C["sr2"] = C.sgn * C.r2
    C["sr2raw"] = C.sgn * C.r2raw
    def tday(s, dayser):
        g = s.groupby(dayser).sum(); 
        return g.mean() / g.std() * np.sqrt(len(g)) if len(g) > 2 else np.nan
    def summ(df):
        return pd.Series({"n": len(df), "mean_signed_r2": df.sr2.mean(), "mean_raw_signed": df.sr2raw.mean(),
                          "t_day": tday(df.sr2, df.day), "mean_abs_f": df.f.abs().mean()})
    res["cases_by_side"] = C.groupby("sgn").apply(summ)
    C["absf_q"] = pd.qcut(C.f.abs(), 3, labels=["lo", "mid", "hi"])
    res["cases_by_side_absf"] = C.groupby(["sgn", "absf_q"]).apply(summ)
    C["vol_q"] = C.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    res["cases_by_side_vol"] = C.groupby(["sgn", "vol_q"]).apply(summ)
    res["cases_by_side_trend100"] = C.groupby(["sgn", "above100"]).apply(summ)
    res["cases_by_year"] = C.groupby("year").apply(summ)
    return res
