def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; v = b["volume"].values.astype(float)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            for t in range(0, n, 24):
                if t < 72 or t+72 >= n: continue
                past24 = c[t]/c[t-24]-1; past72 = c[t]/c[t-72]-1
                hr = r1[t-23:t+1]
                sh = np.nanmax(np.abs(hr))/np.nansum(np.abs(hr)) if np.nansum(np.abs(hr))>0 else np.nan
                vv = v[t-23:t+1]; vs = vv.max()/vv.sum() if vv.sum()>0 else np.nan
                eff = abs(past24)/np.nansum(np.abs(hr)) if np.nansum(np.abs(hr))>0 else np.nan
                vol24 = np.nanstd(hr)
                rows.append(dict(coin=coin, w=w, past24=past24, past72=past72, maxshare=sh, volshare=vs, eff=eff,
                                 vol24=vol24, f24=c[t+24]/c[t]-1, f72=c[t+72]/c[t]-1, f24_72=c[t+72]/c[t+24]-1,
                                 fc=b["forecast"].iloc[t], hour=ts.iloc[t].hour, wd=ts.iloc[t].weekday(),
                                 year=ts.iloc[t].year, pos=b["postRebalance_current_allocation"].iloc[t]))
    d = pd.DataFrame(rows)
    for col in ["f24","f72","f24_72"]:
        d[col+"x"] = d[col] - d.groupby("coin")[col].transform("mean")
    d["z24"] = d.groupby("coin")["past24"].transform(lambda s: s/s.std())
    def tt(s): s=s.dropna(); return s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan
    # past24 quintile -> fwd (24-grid, note f72 overlaps across grid)
    d["q24"] = d.groupby("coin")["past24"].transform(lambda s: pd.qcut(s,5,labels=False))
    g = d.groupby("q24").agg(n=("f24x","size"), f24x=("f24x","mean"), f24_72x=("f24_72x","mean"))
    g["t_f24"] = d.groupby("q24")["f24x"].apply(tt)
    out["past24 quintile -> fwd excess (24h grid)"] = g
    # signed past move x efficiency: grind vs jump, conditional on size
    d["dirf24"] = np.sign(d["past24"])*d["f24x"]
    d["dirf24_72"] = np.sign(d["past24"])*d["f24_72x"]
    big = d[d.groupby("coin")["past24"].transform(lambda s: s.abs()>s.abs().quantile(0.5))].copy()
    big["qeff"] = pd.qcut(big["eff"],3,labels=False)
    big["qmax"] = pd.qcut(big["maxshare"],3,labels=False)
    big["qvol"] = pd.qcut(big["volshare"],3,labels=False)
    for k in ["qeff","qmax","qvol"]:
        gg = big.groupby(k).agg(n=("dirf24","size"), dirf24=("dirf24","mean"), dirf24_72=("dirf24_72","mean"))
        gg["t24"] = big.groupby(k)["dirf24"].apply(tt)
        out["large moves: continuation by "+k] = gg
    # volatility level
    d["qv"] = d.groupby("coin")["vol24"].transform(lambda s: pd.qcut(s,5,labels=False))
    gv = d.groupby("qv").agg(f24x=("f24x","mean"), dirf24=("dirf24","mean"))
    gv["t_dir"] = d.groupby("qv")["dirf24"].apply(tt)
    out["vol quintile"] = gv
    # regime 72 down vs up: reversal of past24
    d["down72"] = d["past72"]<0
    out["corr past24 z vs f24x by 72h sign"] = d.groupby("down72").apply(lambda x: pd.Series({"n":len(x),"r":stats.pearsonr(x["z24"],x["f24x"])[0]}))
    # weekday / hour of hourly returns
    hrs=[]
    for coin, wins in data["bars"].items():
        for w,b in wins.items():
            ts=pd.to_datetime(b["timestamp"]); r=b["close"].pct_change()
            hrs.append(pd.DataFrame({"h":ts.dt.hour,"wd":ts.dt.weekday,"r":r,"coin":coin}))
    H=pd.concat(hrs).dropna()
    H["rx"]=H["r"]-H.groupby("coin")["r"].transform("mean")
    gh=H.groupby("h")["rx"].agg(["mean","count"]); gh["t"]=H.groupby("h")["rx"].apply(tt)
    out["hour excess return"]=gh
    gw=H.groupby("wd")["rx"].agg(["mean","count"]); gw["t"]=H.groupby("wd")["rx"].apply(tt)
    out["weekday excess return"]=gw
    # book: daily returns, by year, and timing vs market
    D=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            D.append(x.assign(coin=coin,w=w))
    D=pd.concat(D)
    D["year"]=pd.to_datetime(D["day"]).dt.year
    out["book by year"]=D.groupby("year").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","count"))
    # trades
    T=pd.concat([x.assign(coin=c) for c,ws in data["trades"].items() for x in ws.values()])
    out["trades"]=pd.Series({"n":len(T),"mean_pl":T["profit_loss_percent"].mean(),"mean_net":T["net_profit_loss_percent"].mean(),
        "med_dur_h":T["duration_minutes"].median()/60,"fee_mean":T["total_commission"].mean()})
    return out
