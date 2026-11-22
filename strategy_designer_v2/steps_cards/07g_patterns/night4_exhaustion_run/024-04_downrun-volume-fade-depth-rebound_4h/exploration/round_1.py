def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    hb = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            v = df["volume"].astype(float).values
            n = len(c)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            # streaks
            sgn = np.sign(np.nan_to_num(r1))
            slen = np.zeros(n); ssum = np.zeros(n); sv0 = np.full(n, np.nan)
            for i in range(1, n):
                if sgn[i] != 0 and sgn[i] == sgn[i-1] and slen[i-1] != 0:
                    slen[i] = slen[i-1] + 1; ssum[i] = ssum[i-1] + np.log(c[i]/c[i-1]); sv0[i] = sv0[i-1]
                elif sgn[i] != 0:
                    slen[i] = 1; ssum[i] = np.log(c[i]/c[i-1]); sv0[i] = v[i]
            mabs = pd.Series(np.abs(r1)).rolling(180, min_periods=60).mean().values
            loss_u = ssum / mabs
            fade = np.log(np.where(v > 0, sv0, np.nan) / np.where(v > 0, v, np.nan))
            ret6 = pd.Series(c).pct_change(6).values
            ret18 = pd.Series(c).pct_change(18).values
            ret42 = pd.Series(c).pct_change(42).values
            vol30 = pd.Series(r1).rolling(180, min_periods=60).std().values
            vol5 = pd.Series(r1).rolling(30, min_periods=20).std().values
            vrel = pd.Series(v).rolling(6).sum().values / pd.Series(v).rolling(180, min_periods=60).sum().values * 30
            ts = pd.to_datetime(df["timestamp"])
            alloc = df["postRebalance_current_allocation"].astype(float).values
            fwd1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            for i in range(n):
                hb.append((coin, ts.iloc[i].hour, ts.iloc[i].dayofweek, fwd1[i], alloc[i], df["forecast"].iloc[i]))
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fwd=c[i+H]/c[i]-1, slen=slen[i]*np.sign(ssum[i]), loss_u=loss_u[i],
                                 fade=fade[i], ret6=ret6[i]/ (vol30[i]*np.sqrt(6)) if vol30[i] else np.nan,
                                 ret18=ret18[i]/(vol30[i]*np.sqrt(18)) if vol30[i] else np.nan,
                                 ret42=ret42[i]/(vol30[i]*np.sqrt(42)) if vol30[i] else np.nan,
                                 volratio=vol5[i]/vol30[i] if vol30[i] else np.nan, vol30=vol30[i], vrel=vrel[i],
                                 hour=ts.iloc[i].hour, fc=df["forecast"].iloc[i]))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    def tab(col, q=5):
        d = g.dropna(subset=[col, "ex"]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        a = d.groupby("b")["ex"].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        a["x_mean"] = d.groupby("b")[col].mean()
        sp = stats.spearmanr(d[col], d["ex"])
        a["spearman_all"] = sp.correlation
        return a.drop(columns="std")
    out = {}
    for col in ["loss_u", "ret6", "ret18", "ret42", "volratio", "vol30", "vrel", "slen"]:
        out["q_" + col] = tab(col)
    d = g.dropna(subset=["loss_u", "fade"])
    dn = d[d["loss_u"] < -3]
    out["down_streak_lossu<-3_by_fade_q"] = dn.assign(b=pd.qcut(dn["fade"].rank(method="first"), 3, labels=False)).groupby("b")["ex"].agg(["mean", "count"])
    up = d[d["loss_u"] > 3]
    out["up_streak_lossu>3_by_fade_q"] = up.assign(b=pd.qcut(up["fade"].rank(method="first"), 3, labels=False)).groupby("b")["ex"].agg(["mean", "count"])
    out["by_coin_ret42_spearman"] = g.dropna(subset=["ret42"]).groupby("coin").apply(lambda x: stats.spearmanr(x["ret42"], x["ex"]).correlation)
    h = pd.DataFrame(hb, columns=["coin", "hour", "wd", "f1", "alloc", "fc"]).dropna(subset=["f1"])
    a = h.groupby("hour")["f1"].agg(["mean", "count", "std"]); a["t"] = a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["hour_next_bar"] = a.drop(columns="std")
    a = h.groupby("wd")["f1"].agg(["mean", "count", "std"]); a["t"] = a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["weekday_next_bar"] = a.drop(columns="std")
    h["in"] = h["alloc"] > 0.01
    out["next_bar_in_vs_out"] = h.groupby("in")["f1"].agg(["mean", "count"])
    out["alloc_desc"] = h["alloc"].describe()
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df[["day", "book_return", "coin_return"]].copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    dd = pd.concat(dd)
    bk = dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    bk["year"] = pd.to_datetime(bk.index.get_level_values("day")).year
    out["book_by_year"] = bk.groupby("year")[["book_return", "coin_return"]].agg(["mean", "count"])
    out["book_by_window"] = bk.groupby(level="w")[["book_return", "coin_return"]].mean().T
    thr_hi = bk["book_return"].quantile(0.98); thr_lo = bk["book_return"].quantile(0.02)
    out["book_extreme_days"] = pd.DataFrame({"top2%": bk[bk.book_return >= thr_hi].mean(), "bottom2%": bk[bk.book_return <= thr_lo].mean(), "all": bk.mean()})
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    tr["dur_d"] = tr["duration_minutes"]/1440
    out["trades"] = tr.groupby(pd.qcut(tr["entry_forecast"].rank(method="first"), 4, labels=False))[["net_profit_loss_percent", "dur_d", "entry_forecast"]].agg(["mean", "count"])
    return out
