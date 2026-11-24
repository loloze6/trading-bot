import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]; out = {}
    def tday(v, ts):
        x = pd.Series(np.asarray(v)).groupby(pd.Series(np.asarray(ts))).sum()
        return pd.Series({"mean": np.mean(v), "t_day": x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x)>2 else np.nan, "n": len(v), "days": len(x)})
    def slope(d, xcol, ycol="un"):
        d = d[[xcol, ycol, "ts"]].dropna()
        x = d[xcol]-d[xcol].mean(); y = d[ycol]
        b = (x*y).sum()/(x*x).sum()
        res = y - y.mean() - b*x
        sc = (x*res).groupby(d["ts"]).sum()
        se = np.sqrt((sc**2).sum())/(x*x).sum()
        return pd.Series({"slope": b, "t": b/se, "n": len(d), "days": d["ts"].nunique()})
    rows = []
    for c, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True); cl = df["close"].values; n = len(cl)
            mr = (df["regime"]=="mean_reversion").values
            # days since last close that was the lowest close so far in this window (running low, max 365)
            run = np.full(n, np.nan); last_low = None
            for i in range(n):
                lo = cl[max(0,i-364):i+1].min()
                if cl[i] <= lo: last_low = i
                run[i] = i-last_low if last_low is not None else np.nan
            # consecutive mr bars
            cons = np.zeros(n)
            for i in range(n):
                cons[i] = (cons[i-1]+1 if i>0 and mr[i] else (1 if mr[i] else 0))
            for h in (20,):
                for i in range(0, n-h, h):
                    rows.append({"coin": c, "ts": df["timestamp"].iloc[i], "fwd": cl[i+h]/cl[i]-1,
                                 "mr": mr[i], "cons": cons[i], "since_low": run[i],
                                 "bir": df["debug_info.bars_in_regime"].iloc[i],
                                 "p60": cl[i]/cl[i-60]-1 if i>=60 else np.nan})
    g = pd.DataFrame(rows)
    g["un"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    m = g[g.mr].copy()
    out["mr: slope un on consecutive mr days"] = slope(m, "cons")
    out["mr: slope un on bir"] = slope(m, "bir")
    out["mr: slope un on days since window low"] = slope(m, "since_low")
    m["cq"] = pd.qcut(m["cons"].rank(method="first"), 4, labels=False)
    out["mr by consecutive-days quartile"] = m.groupby("cq").apply(lambda d: pd.concat([pd.Series({"cons_med": d["cons"].median()}), tday(d["un"].values, d["ts"].values)]))
    m["half"] = np.where(m["coin"].isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"]), "old6", "rest")
    out["cons slope by coin group"] = m.groupby("half").apply(lambda d: slope(d, "cons"))
    m["yr"] = pd.to_datetime(m["ts"]).dt.year
    m["late"] = (m["cons"] >= 41).astype(int)
    out["mr late-minus-early by year"] = m.groupby(["yr","late"])["un"].mean().unstack()
    # weekday, day clustered: per day cross-coin mean deviation
    dl = []
    for c, wins in data["days"].items():
        for w, df in wins.items():
            dl.append(df.assign(coin=c))
    D = pd.concat(dl)
    D["dev"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    pd_ = D.groupby("day")["dev"].mean().dropna().reset_index()
    pd_["wd"] = pd.to_datetime(pd_["day"]).dt.weekday
    pd_["yr"] = pd.to_datetime(pd_["day"]).dt.year
    wk = pd_.groupby("wd")["dev"].agg(["mean","std","count"]); wk["t"] = wk["mean"]/(wk["std"]/np.sqrt(wk["count"]))
    out["weekday, one value per day"] = wk
    out["weekday by year (mean dev)"] = pd_.groupby(["yr","wd"])["dev"].mean().unstack()
    # trades: t by forecast quartile
    tr = []
    for c, wins in data["trades"].items():
        for w, df in wins.items():
            if len(df): tr.append(df.assign(coin=c))
    T = pd.concat(tr)
    out["trade pl describe"] = T["net_profit_loss_percent"].describe()
    T["fq"] = pd.qcut(T["entry_forecast"].abs().rank(method="first"), 4, labels=False)
    out["trades by forecast quartile, median"] = T.groupby("fq")["net_profit_loss_percent"].agg(["median","mean","count"])
    return out
