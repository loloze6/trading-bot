def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    out = {}
    def clt(g, col):
        n = len(g)
        if n < 3: return np.nan
        m = g[col].mean()
        dev = (g[col]-m).groupby(g["day"]).sum()
        se = np.sqrt((dev**2).sum())/n
        return m/se if se > 0 else np.nan
    def grid(h):
        rows = []
        for c in bars:
            rets = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rets.append(cl[i+h]/cl[i]-1)
            if len(rets) < 3: continue
            mu = np.mean(rets); sd = np.std(rets, ddof=1)
            for w, df in bars[c].items():
                cl = df["close"].astype(float).values
                col = "debug_info.components.fall90.last_history_value"
                raw = pd.to_numeric(df[col], errors="coerce").values if col in df else np.full(len(cl), np.nan)
                s = pd.Series(cl)
                lr = np.log(s).diff()
                vol30 = lr.rolling(30).std().values
                vol120 = lr.rolling(120, min_periods=60).std().values
                r20 = s.pct_change(20).values
                r90 = s.pct_change(90).values
                dd = (s / s.cummax() - 1).values
                ts = pd.to_datetime(df["timestamp"])
                for i in range(0, len(cl) - h, h):
                    r = cl[i+h]/cl[i]-1
                    rows.append(dict(coin=c, win=w, day=str(ts.iloc[i].date()), year=ts.iloc[i].year,
                                     ret=r, ex=r-mu, z=(r-mu)/sd, raw=raw[i], r20=r20[i], r90=r90[i],
                                     vr=(vol30[i]/vol120[i]) if vol120[i] and not np.isnan(vol120[i]) else np.nan,
                                     dd=dd[i]))
        return pd.DataFrame(rows)
    def qtab(g, col, q=5):
        g = g.dropna(subset=[col]).copy()
        g["q"] = pd.qcut(g[col], q, labels=False, duplicates="drop")
        return g.groupby("q").apply(lambda x: pd.Series(dict(n=len(x), days=x["day"].nunique(), v=x[col].mean(),
                    mean_ex=x["ex"].mean(), mean_z=x["z"].mean(), t=clt(x, "ex")))).round(4)
    for h in (10, 20, 45):
        try:
            g = grid(h)
            out[f"raw signed quintile -> excess {h}d"] = qtab(g, "raw")
            if h in (10, 20):
                out[f"prior 20d ret quintile -> excess {h}d"] = qtab(g, "r20")
                out[f"vol ratio 30/120 quintile -> excess {h}d"] = qtab(g, "vr")
            if h == 45:
                out["vol ratio 30/120 quintile -> excess 45d"] = qtab(g, "vr")
                out["raw<0 by year, 45d excess"] = g.dropna(subset=["raw"]).assign(neg=lambda x: x["raw"] < 0).groupby(["year", "neg"])["ex"].agg(["count", "mean"]).unstack().round(4)
        except Exception as e:
            out[f"err grid {h}"] = str(e)[:200]
    try:
        rows = []
        for c in days:
            for w, d in days[c].items():
                d = d.copy()
                r = d["coin_return"]
                sd = r.rolling(60, min_periods=30).std().shift(1)
                d["zr"] = r/sd
                d["next1"] = r.shift(-1)
                d["next5"] = (1+r).shift(-1).rolling(5).apply(np.prod, raw=True).shift(-4) - 1
                dt = pd.to_datetime(d["day"])
                d["wd"] = dt.dt.dayofweek.values
                d["year"] = dt.dt.year.values
                d["dstr"] = dt.dt.strftime("%Y-%m-%d").values
                d["coin"] = c
                rows.append(d[["coin", "dstr", "year", "zr", "next1", "next5", "coin_return", "book_return", "wd"]])
        D = pd.concat(rows, ignore_index=True)
        Dz = D.dropna(subset=["zr", "next1"]).copy()
        Dz["zb"] = pd.cut(Dz["zr"], [-99, -3, -2, -1, 1, 2, 3, 99])
        def tt(x): return x.mean()/x.std()*np.sqrt(x.count()) if x.count() > 2 else np.nan
        out["daily z bucket -> next1/next5"] = Dz.groupby("zb").agg(n=("next1", "size"), next1=("next1", "mean"), t1=("next1", tt), next5=("next5", "mean"), t5=("next5", tt)).round(5)
        out["weekday coin return"] = D.groupby("wd")["coin_return"].agg(["count", "mean", tt]).round(5)
        bk = D.groupby("dstr").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), year=("year", "first")).dropna()
        out["book by year"] = bk.groupby("year").agg(n=("book", "size"), book=("book", "mean"), coin=("coin", "mean"), book_sd=("book", "std"), sharpe=("book", lambda x: x.mean()/x.std()*np.sqrt(365))).round(5)
        bk = bk.reset_index()
        big = bk.nlargest(20, "book"); small = bk.nsmallest(20, "book")
        out["20 best/worst book days: mean book, mean coin"] = pd.DataFrame({"best": [big["book"].mean(), big["coin"].mean()], "worst": [small["book"].mean(), small["coin"].mean()]}, index=["book", "coin"]).round(4)
        out["corr book vs coin daily"] = float(np.corrcoef(bk["book"], bk["coin"])[0, 1])
    except Exception as e:
        out["err days"] = str(e)[:200]
    try:
        tr = []
        for c in data["trades"]:
            for w, t in data["trades"][c].items():
                if len(t): tr.append(t.assign(coin=c))
        T = pd.concat(tr, ignore_index=True)
        T["fq"] = pd.qcut(T["entry_forecast"], 4, labels=False, duplicates="drop")
        out["trades by entry forecast quartile"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"), ef=("entry_forecast", "mean"), pnl=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median"), dur_d=("duration_minutes", lambda x: x.mean()/1440)).round(3)
        T["dq"] = pd.qcut(T["duration_minutes"], 4, labels=False, duplicates="drop")
        out["trades by duration quartile"] = T.groupby("dq").agg(n=("net_profit_loss_percent", "size"), dur_d=("duration_minutes", lambda x: x.mean()/1440), pnl=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda x: (x > 0).mean())).round(3)
    except Exception as e:
        out["err trades"] = str(e)[:200]
    return out
