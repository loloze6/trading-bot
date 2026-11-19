def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    hourly = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            v = b["volume"].values.astype(float)
            n = len(c)
            r = np.r_[np.nan, c[1:]/c[:-1]-1]
            ts = pd.to_datetime(b["timestamp"])
            hourly.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour.values,"wd":ts.dt.weekday.values,"r":r,
                                        "alloc":b["postRebalance_current_allocation"].values}))
            for t in range(0, n, 72):
                if t-72 < 0 or t+72 >= n: continue
                past = c[t]/c[t-72]-1
                fwd = c[t+72]/c[t]-1
                fwd24 = c[t+24]/c[t]-1
                rr = r[t-71:t+1]
                rr = rr[~np.isnan(rr)]
                top3 = np.sort(rr)[-3:].sum()
                bot3 = np.sort(rr)[:3].sum()
                vol = np.std(rr)
                vv = v[t-71:t+1]
                vshare = np.sort(vv)[-3:].sum()/vv.sum() if vv.sum()>0 else np.nan
                pv = v[t-143:t-71].sum() if t>=144 else np.nan
                vratio = vv.sum()/pv if pv and pv>0 else np.nan
                eff = abs(np.log(c[t]/c[t-72]))/np.abs(np.log1p(rr)).sum()
                past24 = c[t]/c[t-24]-1
                rows.append(dict(coin=coin,w=w,past=past,fwd=fwd,fwd24=fwd24,top3=top3,bot3=bot3,vol=vol,
                                 vshare=vshare,vratio=vratio,eff=eff,past24=past24))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["grind_up"] = np.where(g.past>0, 1-np.clip(g.top3/g.past.where(g.past>0),0,1), np.nan)
    g["grind_dn"] = np.where(g.past<0, 1-np.clip(g.bot3/g.past.where(g.past<0),0,1), np.nan)
    def corr_t(x,y):
        m = x.notna()&y.notna()
        if m.sum()<30: return (np.nan,np.nan,int(m.sum()))
        rho = np.corrcoef(x[m],y[m])[0,1]; k=m.sum()
        return (rho, rho*np.sqrt((k-2)/(1-rho**2)), int(k))
    res = {}
    for name in ["past","past24","top3","bot3","vol","vshare","vratio","eff","grind_up","grind_dn"]:
        res[name] = corr_t(g[name], g["ex"])
    out["corr_feature_vs_fwd72_excess (rho,t,n)"] = pd.DataFrame(res, index=["rho","t","n"]).T
    # quintiles of past return
    g["pq"] = g.groupby("coin")["past"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["fwd72 excess by past72 quintile"] = g.groupby("pq")["ex"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    g["vq"] = g.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["fwd72 excess by vol quintile"] = g.groupby("vq")["ex"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    g["eq"] = g.groupby("coin")["eff"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    g["sx"] = np.sign(g.past)*g.ex
    out["signed fwd72 excess (continuation) by efficiency quintile"] = g.groupby("eq")["sx"].agg(["mean","count",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["per coin corr past vs ex"] = g.groupby("coin").apply(lambda d: pd.Series(corr_t(d.past,d.ex),index=["rho","t","n"]))
    h = pd.concat(hourly)
    out["hour mean ret (bp) & t"] = h.groupby("hour")["r"].agg(lambda s: s.mean()*1e4).to_frame("bp").join(h.groupby("hour")["r"].agg(lambda s: s.mean()/s.std()*np.sqrt(s.count())).rename("t"))
    # book
    ds = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"]=coin; d["w"]=w; ds.append(d)
    D = pd.concat(ds)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["coin daily ret by weekday (bp,t)"] = D.groupby("wd")["coin_return"].agg([lambda s: s.mean()*1e4, lambda s: s.mean()/s.std()*np.sqrt(s.count())])
    out["book daily ret by weekday (bp,t)"] = D.groupby("wd")["book_return"].agg([lambda s: s.mean()*1e4, lambda s: s.mean()/s.std()*np.sqrt(s.count())])
    out["mean alloc"] = float(h["alloc"].mean())
    out["share bars in position"] = float((h["alloc"].abs()>1e-6).mean())
    return out
