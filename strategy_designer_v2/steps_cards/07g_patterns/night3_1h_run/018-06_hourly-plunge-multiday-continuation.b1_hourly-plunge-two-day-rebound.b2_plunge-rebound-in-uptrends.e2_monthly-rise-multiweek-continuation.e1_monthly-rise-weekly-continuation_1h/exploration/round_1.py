import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    out = {}
    # ---- 1. horizon profile by 30d return quintile (recomputed), non-overlapping grids
    rows = []
    for H in [24, 72, 168, 336]:
        recs = []
        for c, ws in bars.items():
            allr = []
            tmp = []
            for w, df in ws.items():
                cl = df["close"].values
                r30 = pd.Series(cl).pct_change(720).values
                r7 = pd.Series(cl).pct_change(168).values
                lr = np.log(pd.Series(cl)).diff()
                vol30 = lr.rolling(720).std().values
                idx = np.arange(0, len(cl) - H, H)
                fwd = cl[idx + H] / cl[idx] - 1
                allr.append(fwd)
                tmp.append(pd.DataFrame({"r30": r30[idx], "r7": r7[idx], "vol": vol30[idx], "fwd": fwd,
                                         "fc": df["forecast"].values[idx]}))
            allr = np.concatenate(allr)
            mu, sd = np.nanmean(allr), np.nanstd(allr)
            t = pd.concat(tmp); t["s"] = (t["fwd"] - mu) / sd; t["coin"] = c
            # vol rank within coin
            t["volq"] = pd.qcut(t["vol"].rank(method="first"), 3, labels=["lowvol", "midvol", "highvol"]) if t["vol"].notna().sum() > 10 else np.nan
            recs.append(t)
        T = pd.concat(recs).dropna(subset=["r30", "s"])
        T["q"] = T.groupby("coin")["r30"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        g = T.groupby("q")["s"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        for q, r in g.iterrows():
            rows.append({"H": H, "r30_quintile": q, "strength": r["mean"], "n": r["count"], "t": r["t"]})
        if H == 168:
            T168 = T
    out["horizon_by_r30q"] = pd.DataFrame(rows)
    T = T168
    # 2. vol interaction
    g = T.groupby(["volq", T["r30"] > 0])["s"].agg(["mean", "count", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["s168_by_vol_and_r30pos"] = g
    # 3. 7d return quintile (shorter lookback)
    T["q7"] = T.groupby("coin")["r7"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    g = T.groupby("q7")["s"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["s168_by_r7q"] = g
    # slope of s on r30 standardized for negative side
    neg = T[T["r30"] < 0]
    sl = stats.linregress(neg["r30"], neg["s"])
    out["neg_side_slope_t"] = f"slope {sl.slope:.3f} t {sl.slope/sl.stderr:.2f} n {len(neg)}"
    # by coin
    g = T.groupby(["coin", T["r30"] > 0])["s"].agg(["mean", "count"])
    out["s168_by_coin_r30pos"] = g
    # 4. book by year and coin
    D = []
    for c, ws in days.items():
        for w, df in ws.items():
            d = df.copy(); d["coin"] = c; d["w"] = w; D.append(d)
    D = pd.concat(D)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    g = D.groupby("year")[["book_return", "coin_return"]].agg(["mean", "std", "count"])
    out["book_by_year"] = g
    gc = D.groupby("coin")[["book_return", "coin_return"]].mean()
    out["book_by_coin_mean"] = gc
    # 5. trades by entry forecast and duration
    TR = []
    for c, ws in trades.items():
        for w, df in ws.items():
            if len(df): d = df.copy(); d["coin"] = c; TR.append(d)
    TR = pd.concat(TR)
    TR["fq"] = pd.qcut(TR["entry_forecast"].rank(method="first"), 5, labels=False)
    out["trades_by_entry_fc_q"] = TR.groupby("fq")[["entry_forecast", "net_profit_loss_percent", "duration_minutes"]].agg(["mean", "count"]).iloc[:, [0, 2, 3, 4]]
    TR["dq"] = pd.qcut(TR["duration_minutes"].rank(method="first"), 4, labels=False)
    out["trades_by_duration_q"] = TR.groupby("dq")[["duration_minutes", "net_profit_loss_percent"]].agg(["mean", "median", "count"])
    # 6. hourly / weekday returns
    H = []
    for c, ws in bars.items():
        for w, df in ws.items():
            ts = pd.to_datetime(df["timestamp"])
            r = df["close"].pct_change()
            H.append(pd.DataFrame({"hour": ts.dt.hour, "wd": ts.dt.weekday, "r": r, "coin": c}))
    H = pd.concat(H).dropna()
    gh = H.groupby("hour")["r"].agg(["mean", "std", "count"]); gh["t"] = gh["mean"] / (gh["std"] / np.sqrt(gh["count"]))
    out["hourly_ret_by_hour_bps"] = (gh[["mean", "t"]] * [1e4, 1])
    gw = H.groupby("wd")["r"].agg(["mean", "std", "count"]); gw["t"] = gw["mean"] / (gw["std"] / np.sqrt(gw["count"]))
    out["hourly_ret_by_weekday_bps"] = (gw[["mean", "t"]] * [1e4, 1])
    return out
