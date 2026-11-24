def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H = 14
    grid = []; daily = []; pos = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            s = b["close"].astype(float); v = b["volume"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r1 = s.pct_change()
            vol20 = r1.rolling(20, min_periods=10).std()
            ret60 = s / s.shift(60) - 1
            ret28 = s / s.shift(28) - 1
            ret14 = s / s.shift(14) - 1
            vr = v.rolling(14).mean() / v.rolling(30).mean() - 1
            vr3 = v.rolling(3).mean() / v.rolling(30).mean() - 1
            hi60 = b["high"].rolling(60, min_periods=30).max()
            dhi = s / hi60 - 1
            n = len(b)
            for i in range(0, n - H, H):
                grid.append(dict(coin=coin, w=w, day=ts[i].normalize(), year=ts[i].year,
                                 fwd=s[i+H]/s[i]-1, fc=b["forecast"][i], ret60=ret60[i], ret28=ret28[i],
                                 ret14=ret14[i], vr=vr[i], vr3=vr3[i], dhi=dhi[i],
                                 vol=vol20[i]))
            nxt = s.shift(-1) / s - 1
            alloc = b["postRebalance_current_allocation"].astype(float)
            daily.append(pd.DataFrame(dict(coin=coin, z=r1/vol20, r1=r1, nxt=nxt, wd=ts.dt.weekday,
                                           year=ts.dt.year, gain=alloc*nxt, alloc=alloc, fc=b["forecast"],
                                           vr=vr, ret14=ret14, vol=vol20)))
    g = pd.DataFrame(grid)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    def ct(x, d):
        dd = pd.DataFrame({"x": x - x.mean(), "d": d}).groupby("d")["x"].sum()
        D = len(dd); se = np.sqrt((dd**2).sum() * D/(D-1)) / len(x) if D > 1 else np.nan
        return x.mean()/se if se else np.nan
    def tab(col, q=5, df=None):
        df = g if df is None else df
        d = df.dropna(subset=[col, "ex"]).copy()
        d["q"] = pd.qcut(d[col].rank(method="first"), q, labels=False)
        out = d.groupby("q").apply(lambda x: pd.Series(dict(lo=x[col].min(), hi=x[col].max(),
              mean_ex=x["ex"].mean(), t=ct(x["ex"], x["day"]), n=len(x))))
        return out.round(4)
    res = {}
    res["fc_quint_ex14"] = tab("fc")
    res["ret60_quint_ex14"] = tab("ret60")
    res["ret28_quint_ex14"] = tab("ret28")
    res["ret14_quint_ex14"] = tab("ret14")
    res["vr3_quint_ex14"] = tab("vr3")
    res["dhi60_quint_ex14"] = tab("dhi")
    res["vol_quint_ex14"] = tab("vol")
    d = g.dropna(subset=["vr", "ret14"]).copy()
    d["vrhi"] = d["vr"] > d["vr"].median(); d["up"] = d["ret14"] > 0
    res["vr_x_ret14sign"] = d.groupby(["vrhi", "up"]).apply(lambda x: pd.Series(dict(
        mean_ex=x["ex"].mean(), t=ct(x["ex"], x["day"]), n=len(x)))).round(4)
    g["sig"] = np.sign(g["fc"]) * g["ex"]
    res["signal_by_year"] = g.groupby("year").apply(lambda x: pd.Series(dict(
        dir_ex=x["sig"].mean(), t=ct(x["sig"], x["day"]), n=len(x)))).round(4)
    res["signal_long_vs_short"] = g.assign(side=np.sign(g["fc"])).groupby("side").apply(lambda x: pd.Series(dict(
        dir_ex=x["sig"].mean(), raw_fwd=x["fwd"].mean(), t=ct(x["sig"], x["day"]), n=len(x)))).round(4)
    dl = pd.concat(daily).dropna(subset=["z", "nxt"])
    dl["q"] = pd.qcut(dl["z"].rank(method="first"), 10, labels=False)
    res["next_day_after_zmove_decile"] = dl.groupby("q").apply(lambda x: pd.Series(dict(
        zlo=x["z"].min(), mean_nxt=x["nxt"].mean(), t=x["nxt"].mean()/(x["nxt"].std()/np.sqrt(len(x))), n=len(x)))).round(4)
    res["weekday_next"] = dl.groupby("wd")["r1"].agg(["mean", "count", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))]).round(5)
    gl = dl.dropna(subset=["gain"])
    gl["side"] = np.sign(gl["alloc"])
    res["book_gain_by_side"] = gl.groupby("side")["gain"].agg(["mean", "count", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))]).round(5)
    res["book_gain_by_year"] = gl.groupby("year")["gain"].agg(["mean", "count", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))]).round(5)
    big = gl["gain"].abs().quantile(0.98)
    res["extreme_gain_days_fc_side"] = gl[gl["gain"].abs() > big].assign(pos=lambda x: x["gain"] > 0).groupby(["pos", "side"]).size()
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    tr = pd.concat(tr)
    res["trades_by_side"] = tr.groupby("side")["net_profit_loss_percent"].agg(["mean", "median", "count"]).round(3)
    return res
