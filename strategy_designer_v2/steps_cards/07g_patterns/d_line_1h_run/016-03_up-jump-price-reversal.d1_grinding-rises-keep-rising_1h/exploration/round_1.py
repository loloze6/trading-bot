def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    rows72 = []; rows24 = []; hr = []
    for coin in bars:
        for w, df in bars[coin].items():
            c = df["close"].values.astype(float); v = df["volume"].values.astype(float)
            ts = pd.to_datetime(df["timestamp"])
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            n = len(c)
            hh = pd.DataFrame({"coin":coin,"hour":ts.dt.hour.values,"wd":ts.dt.weekday.values,"r":r1,
                               "alloc":df["postRebalance_current_allocation"].values})
            hr.append(hh)
            for t in range(72, n-72, 72):
                seg = r1[t-71:t+1]; pr = c[t]/c[t-72]-1
                gains = np.sort(seg[seg>0])[::-1]; losses = np.sort(seg[seg<0])
                g3 = gains[:3].sum()/gains.sum() if gains.sum()>0 else np.nan
                l3 = losses[:3].sum()/losses.sum() if losses.sum()<0 else np.nan
                vs = v[t-71:t+1]; vtop = np.sort(vs)[::-1][:3].sum()/vs.sum() if vs.sum()>0 else np.nan
                vol = np.nanstd(seg)
                eff = abs(np.log(c[t]/c[t-72]))/np.nansum(np.abs(np.log1p(seg)))
                rows72.append(dict(coin=coin,w=w,past=pr,g3=g3,l3=l3,vtop=vtop,vol=vol,eff=eff,
                                   fwd=c[t+72]/c[t]-1,fc=df["forecast"].values[t]))
            for t in range(24, n-24, 24):
                seg = r1[t-23:t+1]; sd = np.nanstd(r1[max(1,t-167):t+1])
                rows24.append(dict(coin=coin,past=c[t]/c[t-24]-1,last1=r1[t],maxz=np.nanmax(np.abs(seg))/sd,
                                   z1=r1[t]/sd, fwd=c[t+24]/c[t]-1))
    g = pd.DataFrame(rows72); g["ex"] = g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    d = pd.DataFrame(rows24); d["ex"] = d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    def reg(df, x, y="ex"):
        s = df[[x,y,"coin"]].dropna()
        xs = s[x]-s.groupby("coin")[x].transform("mean")
        r = stats.linregress(xs, s[y]); return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":len(s)})
    res = {}
    res["past72_all"] = reg(g,"past"); res["g3_rises"] = reg(g[g.past>0],"g3"); res["l3_falls"] = reg(g[g.past<0],"l3")
    res["vtop_all"] = reg(g,"vtop"); res["vtop_rises"]=reg(g[g.past>0],"vtop"); res["vtop_falls"]=reg(g[g.past<0],"vtop")
    res["vol_all"] = reg(g,"vol"); res["eff_rises"]=reg(g[g.past>0],"eff"); res["eff_falls"]=reg(g[g.past<0],"eff")
    res["past72_rises"]=reg(g[g.past>0],"past"); res["past72_falls"]=reg(g[g.past<0],"past")
    res["past24_d"]=reg(d,"past"); res["last1z_d"]=reg(d,"z1"); res["maxz_d"]=reg(d,"maxz")
    out["regs"] = pd.DataFrame(res).T
    # per coin momentum 72
    pc = {}
    for coin, s in g.groupby("coin"):
        pc[coin] = pd.concat([reg(s,"past").add_prefix("past_"), reg(s,"vol").add_prefix("vol_"), reg(s[s.past>0],"g3").add_prefix("g3_")])
    out["per_coin72"] = pd.DataFrame(pc).T
    # vol terciles
    g["volq"] = g.groupby("coin")["vol"].transform(lambda x: pd.qcut(x,3,labels=False))
    out["vol_terc"] = g.groupby("volq")["ex"].agg(["mean","count",lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    H = pd.concat(hr)
    hs = H.groupby("hour")["r"].agg(["mean","std","count"]); hs["t"]=hs["mean"]/hs["std"]*np.sqrt(hs["count"])
    out["hour"] = hs[["mean","t"]]
    ws = H.groupby("wd")["r"].agg(["mean","std","count"]); ws["t"]=ws["mean"]/ws["std"]*np.sqrt(ws["count"])
    out["weekday"] = ws[["mean","t"]]
    # book
    D = []
    for coin in days:
        for w, df in days[coin].items():
            x = df[["day","book_return","coin_return"]].copy(); x["coin"]=coin; x["w"]=w; D.append(x)
    D = pd.concat(D)
    out["book_by_coin"] = D.groupby("coin")[["book_return","coin_return"]].mean()
    out["book_by_window"] = D.groupby(["w"])[["book_return","coin_return"]].mean().T
    out["alloc_mean"] = H.groupby("coin")["alloc"].mean()
    return out
