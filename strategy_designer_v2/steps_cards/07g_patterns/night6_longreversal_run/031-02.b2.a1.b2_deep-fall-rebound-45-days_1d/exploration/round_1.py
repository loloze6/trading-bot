def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # --- build per-coin grid samples for several horizons, with signed raw signal
    def grid(h):
        rows = []
        # coin mean h-return over all windows
        for c in bars:
            rets = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rets.append(cl[i+h]/cl[i]-1)
            mu = np.mean(rets) if rets else np.nan
            sd = np.std(rets, ddof=1) if len(rets) > 2 else np.nan
            for w, df in bars[c].items():
                cl = df["close"].values
                raw = df.get("debug_info.components.fall90.last_history_value")
                raw = raw.values if raw is not None else np.full(len(cl), np.nan)
                fc = df["forecast"].values
                r90 = pd.Series(cl).pct_change(90).values
                lr = np.log(pd.Series(cl)).diff()
                vol30 = lr.rolling(30).std().values
                vol365 = lr.rolling(120, min_periods=60).std().values
                r20 = pd.Series(cl).pct_change(20).values
                ts = pd.to_datetime(df["timestamp"]).values
                for i in range(0, len(cl) - h, h):
                    r = cl[i+h]/cl[i]-1
                    rows.append(dict(coin=c, win=w, day=str(ts[i])[:10], ret=r, ex=r-mu, z=(r-mu)/sd,
                                     raw=raw[i], fc=fc[i], r20=r20[i], vr=vol30[i]/vol365[i] if vol365[i] else np.nan,
                                     year=str(ts[i])[:4]))
        return pd.DataFrame(rows)
    def clt(g, col):
        d = g.groupby("day")[col].sum()
        n = len(g)
        m = g[col].mean()
        se = np.sqrt((d - d.mean()*0).pow(2).sum())/n if n else np.nan
        # cluster: sum of deviations per day
        dev = (g[col]-m).groupby(g["day"]).sum()
        se = np.sqrt((dev**2).sum())/n
        return m/se if se>0 else np.nan
    for h in (10, 20, 45):
        g = grid(h)
        g = g.dropna(subset=["raw"])
        g["rawq"] = pd.qcut(g["raw"], 5, labels=False, duplicates="drop")
        t = g.groupby("rawq").apply(lambda x: pd.Series(dict(n=len(x), days=x["day"].nunique(),
              raw_mean=x["raw"].mean(), mean_ex=x["ex"].mean(), mean_z=x["z"].mean(), t_clust=clt(x,"ex"))))
        out[f"raw signed quintile -> excess {h}d"] = t.round(4)
        if h == 20:
            g2 = g.dropna(subset=["r20"]).copy()
            g2["q"] = pd.qcut(g2["r20"], 5, labels=False, duplicates="drop")
            out["prior 20d return quintile -> excess 20d"] = g2.groupby("q").apply(lambda x: pd.Series(dict(n=len(x), r20=x["r20"].mean(), mean_ex=x["ex"].mean(), mean_z=x["z"].mean(), t=clt(x,"ex")))).round(4)
            g3 = g.dropna(subset=["vr"]).copy()
            g3["q"] = pd.qcut(g3["vr"], 5, labels=False, duplicates="drop")
            out["vol ratio 30d/120d quintile -> excess 20d"] = g3.groupby("q").apply(lambda x: pd.Series(dict(n=len(x), vr=x["vr"].mean(), mean_ex=x["ex"].mean(), t=clt(x,"ex")))).round(4)
        if h == 45:
            out["45d by year, raw<0 vs raw>0 mean excess"] = g.groupby(["year", g["raw"]<0])["ex"].agg(["count","mean"]).unstack().round(4)
    # --- daily bars: next-day return after large daily moves, by weekday
    rows = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy()
            r = d["coin_return"]
            sd = r.rolling(60, min_periods=30).std().shift(1)
            d["zr"] = r/sd
            d["next1"] = r.shift(-1)
            d["next5"] = (1+r).shift(-1).rolling(5).apply(np.prod, raw=True).shift(-4)-1
            d["wd"] = pd.to_datetime(d["day"]).dt.dayofweek
            d["coin"] = c
            rows.append(d[["coin","day","zr","next1","next5","coin_return","book_return","wd"]])
    D = pd.concat(rows)
    Dz = D.dropna(subset=["zr","next1"]).copy()
    Dz["zb"] = pd.cut(Dz["zr"], [-99,-3,-2,-1,1,2,3,99])
    out["daily z-move bucket -> next 1d / next 5d"] = Dz.groupby("zb").agg(n=("next1","size"), next1=("next1","mean"), next5=("next5","mean")).round(5)
    out["weekday coin return"] = D.groupby("wd")["coin_return"].agg(["count","mean", lambda x: x.mean()/x.std()*np.sqrt(x.count())]).round(5)
    # book: by year
    bk = D.groupby("day")[["book_return","coin_return"]].mean()
    bk["year"] = bk.index.str[:4]
    out["book by year"] = bk.groupby("year").agg(n=("book_return","size"), book=("book_return","mean"), coin=("coin_return","mean"), book_sd=("book_return","std")).round(5)
    # trades
    tr = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            if len(t): tr.append(t.assign(coin=c))
    T = pd.concat(tr)
    T["fq"] = pd.qcut(T["entry_forecast"], 4, labels=False, duplicates="drop")
    out["trades by entry forecast quartile"] = T.groupby("fq").agg(n=("net_profit_loss_percent","size"), ef=("entry_forecast","mean"), pnl=("net_profit_loss_percent","mean"), med=("net_profit_loss_percent","median"), days=("duration_minutes", lambda x: x.mean()/1440)).round(3)
    return out
