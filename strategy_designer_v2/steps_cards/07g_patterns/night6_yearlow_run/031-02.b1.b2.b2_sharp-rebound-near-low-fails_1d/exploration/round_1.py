import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    out = {}
    # build grid cases for horizons
    def grid(h, look_list=(5,10,20,40)):
        rows = []
        for c, wins in bars.items():
            for w, df in wins.items():
                df = df.reset_index(drop=True)
                cl = df["close"].values
                n = len(cl)
                lr = np.log(cl)
                dr = np.r_[np.nan, np.diff(lr)]
                for i in range(0, n - h, h):
                    r = cl[i+h]/cl[i]-1
                    d = {"coin": c, "win": w, "ts": df["timestamp"].iloc[i], "fwd": r,
                         "regime": df["regime"].iloc[i],
                         "bir": df["debug_info.bars_in_regime"].iloc[i] if "debug_info.bars_in_regime" in df else np.nan,
                         "wd": pd.Timestamp(df["timestamp"].iloc[i]).weekday()}
                    for L in look_list:
                        d[f"p{L}"] = cl[i]/cl[i-L]-1 if i >= L else np.nan
                    d["vol20"] = np.nanstd(dr[max(1,i-19):i+1]) if i >= 20 else np.nan
                    d["d1"] = cl[i]/cl[i-1]-1 if i >= 1 else np.nan
                    rows.append(d)
        g = pd.DataFrame(rows)
        g["drift"] = g.groupby("coin")["fwd"].transform("mean")
        g["un"] = g["fwd"] - g["drift"]
        return g
    def tday(s, ts):
        x = pd.Series(s.values).groupby(pd.Series(ts.values)).sum()
        return x.mean()/ (x.std(ddof=1)/np.sqrt(len(x))) if len(x)>2 else np.nan
    def slope(g, xcol, ycol="un"):
        d = g[[xcol, ycol, "ts"]].dropna()
        x = d[xcol]-d[xcol].mean(); y = d[ycol]
        b = (x*y).sum()/(x*x).sum()
        res = y - y.mean() - b*x
        sc = (x*res).groupby(d["ts"]).sum()
        se = np.sqrt((sc**2).sum())/(x*x).sum()
        return pd.Series({"slope": b, "t": b/se, "n": len(d), "days": d["ts"].nunique()})
    for h in (20, 5):
        g = grid(h)
        g["mr"] = (g["regime"] == "mean_reversion")
        rg = g.groupby("mr")["un"].agg(["mean","count"])
        rg["t_day"] = [tday(g.loc[g.mr==k,"un"], g.loc[g.mr==k,"ts"]) for k in rg.index]
        out[f"h{h} unusual by regime"] = rg
        rows = {}
        for sub, gg in (("mr", g[g.mr]), ("other", g[~g.mr]), ("all", g)):
            for L in (5,10,20,40):
                rows[f"{sub} p{L}"] = slope(gg, f"p{L}")
            rows[f"{sub} vol20"] = slope(gg, "vol20")
            rows[f"{sub} d1"] = slope(gg, "d1")
        out[f"h{h} slopes"] = pd.DataFrame(rows).T
        if h == 20:
            m = g[g.mr].copy()
            m["birq"] = pd.qcut(m["bir"].rank(method="first"), 4, labels=False)
            out["h20 mr by bars_in_regime quartile"] = m.groupby("birq").agg(bir=("bir","median"), un=("un","mean"), n=("un","count"))
            g["volq"] = pd.qcut(g["vol20"].rank(method="first"), 5, labels=False)
            out["h20 by vol quintile"] = g.groupby(["mr","volq"])["un"].agg(["mean","count"])
            g["yr"] = pd.to_datetime(g["ts"]).dt.year
            out["h20 mr by year"] = g[g.mr].groupby("yr")["un"].agg(["mean","count"])
    # daily: weekday and book
    dl = []
    for c, wins in data["days"].items():
        for w, df in wins.items():
            d = df.copy(); d["coin"]=c; d["win"]=w; dl.append(d)
    D = pd.concat(dl)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["cr_dev"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    wk = D.groupby("wd")["cr_dev"].agg(["mean","std","count"])
    wk["t"] = wk["mean"]/(wk["std"]/np.sqrt(wk["count"]))
    out["weekday coin daily dev"] = wk
    bk = D.groupby("day")["book_return"].mean().dropna()
    out["book daily: n, mean, share of gain from top 10 days"] = pd.Series({"n": len(bk), "mean": bk.mean(),
        "sum": bk.sum(), "top10": bk.nlargest(10).sum(), "bot10": bk.nsmallest(10).sum()})
    tr = []
    for c, wins in data["trades"].items():
        for w, df in wins.items():
            if len(df): tr.append(df.assign(coin=c))
    T = pd.concat(tr)
    T["absf"] = T["entry_forecast"].abs()
    T["fq"] = pd.qcut(T["absf"].rank(method="first"), 4, labels=False)
    out["trades by entry forecast quartile"] = T.groupby("fq").agg(f=("absf","median"), pl=("net_profit_loss_percent","mean"), n=("pl" if False else "net_profit_loss_percent","count"))
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["mean","count"])
    return out
