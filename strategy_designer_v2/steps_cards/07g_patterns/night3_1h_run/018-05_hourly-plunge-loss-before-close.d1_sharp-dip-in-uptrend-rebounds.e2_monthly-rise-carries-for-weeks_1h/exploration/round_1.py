def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    col = "debug_info.components.scaled_30d_return.last_history_value"
    out = {}

    def tstat(x):
        x = np.asarray(x, float); x = x[~np.isnan(x)]
        if len(x) < 3: return np.nan
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

    # grid samples per horizon
    recs = []
    for h in (24, 168, 336):
        for coin, ws in bars.items():
            rows = []
            for w, b in ws.items():
                c = b["close"].values
                raw = pd.to_numeric(b[col], errors="coerce").values if col in b else np.full(len(c), np.nan)
                lr = np.log(b["close"]).diff().values
                vol = pd.Series(lr).rolling(168, min_periods=120).std().values
                ts = pd.to_datetime(b["timestamp"])
                idx = np.arange(0, len(c) - h, h)
                for i in idx:
                    rows.append((coin, w, h, c[i + h] / c[i] - 1, raw[i], vol[i], ts.iloc[i].year))
            df = pd.DataFrame(rows, columns=["coin", "w", "h", "ret", "raw", "vol", "year"])
            df["ex"] = df["ret"] - df["ret"].mean()
            recs.append(df)
    g = pd.concat(recs)

    # A: excess by raw scaled-return bucket, per horizon
    tabA = []
    for h, d in g.groupby("h"):
        d = d.dropna(subset=["raw"]).copy()
        d["bucket"] = pd.cut(d["raw"], [-np.inf, -1.0, -0.3, 0, 0.3, 1.0, np.inf])
        for bk, e in d.groupby("bucket", observed=True):
            tabA.append((h, str(bk), len(e), e["ex"].mean(), tstat(e["ex"])))
    out["A_excess_by_scaled30d"] = pd.DataFrame(tabA, columns=["h", "bucket", "n", "mean_ex", "t"])

    # A2: slope on negative side and positive side, per horizon
    tabA2 = []
    for h, d in g.groupby("h"):
        d = d.dropna(subset=["raw"])
        for side, e in (("neg", d[d.raw < 0]), ("pos", d[d.raw > 0])):
            r = stats.linregress(e["raw"], e["ex"])
            tabA2.append((h, side, len(e), r.slope, r.slope / r.stderr))
    out["A2_slope_by_side"] = pd.DataFrame(tabA2, columns=["h", "side", "n", "slope", "t"])

    # C: vol tercile (within coin) x sign of raw, 336h
    d = g[g.h == 336].dropna(subset=["raw", "vol"]).copy()
    d["volT"] = d.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    d["pos"] = d.raw > 0
    out["C_336_by_vol_and_sign"] = d.groupby(["volT", "pos"])["ex"].agg(["count", "mean", tstat])
    d168 = g[g.h == 168].dropna(subset=["raw", "vol"]).copy()
    d168["volT"] = d168.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["C_168_by_vol"] = d168.groupby("volT")["ex"].agg(["count", "mean", tstat])

    # 336 by year among pos
    out["Y_336_pos_by_year"] = d[d.pos].groupby("year")["ex"].agg(["count", "mean", tstat])

    # D: weekday and hour
    dd = []
    for coin, ws in days.items():
        for w, x in ws.items():
            x = x.copy(); x["coin"] = coin
            dd.append(x)
    D = pd.concat(dd)
    D["day"] = pd.to_datetime(D["day"])
    D["wd"] = D["day"].dt.weekday
    D["cex"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    out["D_weekday"] = D.groupby("wd")["cex"].agg(["count", "mean", tstat])
    hh = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            r = b["close"].pct_change()
            hr = pd.to_datetime(b["timestamp"]).dt.hour
            hh.append(pd.DataFrame({"hr": hr, "r": r - 0, "coin": coin}))
    H = pd.concat(hh).dropna()
    H["r"] = H["r"] - H.groupby("coin")["r"].transform("mean")
    Hs = H.groupby("hr")["r"].agg(["count", "mean", tstat])
    out["D_hour"] = Hs

    # G: daily returns after large daily moves (z vs past 30d std within window)
    gg = []
    for coin, ws in days.items():
        for w, x in ws.items():
            r = x["coin_return"].reset_index(drop=True)
            sd = r.rolling(30, min_periods=20).std().shift(1)
            z = r / sd
            nxt = r.shift(-1); nxt7 = (1 + r).rolling(7).apply(np.prod, raw=True).shift(-7) - 1
            gg.append(pd.DataFrame({"z": z, "n1": nxt, "n7": nxt7, "coin": coin}))
    G = pd.concat(gg).dropna()
    G["n1"] -= G.groupby("coin")["n1"].transform("mean")
    G["n7"] -= G.groupby("coin")["n7"].transform("mean")
    G["zb"] = pd.cut(G["z"], [-np.inf, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, np.inf])
    out["G_after_daily_z"] = G.groupby("zb", observed=True).agg(n=("n1", "size"), n1=("n1", "mean"),
                                                               t1=("n1", tstat), n7=("n7", "mean"))

    # E: book
    D["bex"] = D["book_return"]
    D = D.sort_values(["coin", "day"])
    D["bnext"] = D.groupby(["coin"])["book_return"].shift(-1)
    out["E_book_autocorr"] = float(D[["book_return", "bnext"]].dropna().corr().iloc[0, 1])
    q = D["book_return"].quantile([0.02, 0.98])
    out["E_after_worst2pct"] = D[D.book_return <= q.iloc[0]]["bnext"].agg(["count", "mean"]).to_frame().T
    out["E_after_best2pct"] = D[D.book_return >= q.iloc[1]]["bnext"].agg(["count", "mean"]).to_frame().T

    # F: trades
    tt = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = coin; tt.append(t)
    T = pd.concat(tt)
    T["fT"] = pd.qcut(T["entry_forecast"].rank(method="first"), 3, labels=False)
    out["F_trades_by_entry_fc"] = T.groupby("fT")["net_profit_loss_percent"].agg(["count", "mean", "median", tstat])
    out["F_trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", tstat])
    return out
