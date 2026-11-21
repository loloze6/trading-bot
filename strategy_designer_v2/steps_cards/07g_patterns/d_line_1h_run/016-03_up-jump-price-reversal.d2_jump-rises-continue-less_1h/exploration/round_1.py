def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    H = 72
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values.astype(float)
            r1 = np.r_[np.nan, cl[1:]/cl[:-1]-1]
            n = len(cl)
            for i in range(0, n-H, H):
                if i < H: continue
                past = cl[i]/cl[i-H]-1
                fwd = cl[i+H]/cl[i]-1
                rr = r1[i-H+1:i+1]
                gains = np.sort(rr[rr>0])[::-1]
                losses = np.sort(rr[rr<0])
                top3g = gains[:3].sum() if len(gains) else 0
                top3l = losses[:3].sum() if len(losses) else 0
                vol = np.nanstd(rr)
                v = b["volume"].values[i-H+1:i+1].astype(float)
                vs = np.sort(v)[::-1][:3].sum()/max(v.sum(),1e-12)
                rows.append(dict(coin=c, w=w, past=past, fwd=fwd,
                    ups=(rr>0).mean(), top3g=top3g, top3l=top3l, vol=vol, vshare=vs,
                    fc=b["forecast"].iloc[i], pos=b["postRebalance_current_allocation"].iloc[i]))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    def tab(col, sub, q=5):
        s = sub.copy()
        s["b"] = s.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        a = s.groupby("b")["ex"].agg(["mean","count","std"])
        a["t"] = a["mean"]/(a["std"]/np.sqrt(a["count"]))
        return a
    out["past72 quintile -> ex fwd"] = tab("past", g)
    out["vol quintile -> ex fwd"] = tab("vol", g)
    out["upshare quintile -> ex fwd"] = tab("ups", g)
    out["vol-burst share quintile -> ex fwd"] = tab("vshare", g)
    dn = g[g.past<0].copy(); dn["lshare"] = dn["top3l"]/dn["past"]
    out["falls: top3-loss share quintile -> ex fwd"] = tab("lshare", dn)
    up = g[g.past>0].copy(); up["gshare"] = up["top3g"]/up["past"]
    out["rises: top3-gain share quintile -> ex fwd"] = tab("gshare", up)
    # per coin past->fwd corr
    out["per coin corr past,fwd"] = g.groupby("coin").apply(lambda d: pd.Series({"r":stats.spearmanr(d.past,d.fwd)[0],"n":len(d)}))
    # book
    D = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"]=c; d["w"]=w; D.append(d)
    D = pd.concat(D)
    bk = D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book vs hold daily mean,std"] = bk.agg(["mean","std"])
    bk2 = bk.reset_index(); bk2["wn"]=bk2.w.str[1:].astype(int)
    out["book by window sharpe-ish"] = bk2.groupby("wn").agg(book=("book_return","mean"), hold=("coin_return","mean")).describe()
    # position & book: mean position per coin, weekday/hour
    hr=[]
    for c in bars:
        for w,b in bars[c].items():
            cl=b["close"].values.astype(float)
            f=np.r_[cl[1:]/cl[:-1]-1, np.nan]
            ts=pd.to_datetime(b["timestamp"])
            hr.append(pd.DataFrame({"h":ts.dt.hour.values,"wd":ts.dt.weekday.values,"r":f,
                "pos":b["postRebalance_current_allocation"].values,"fc":b["forecast"].values}))
    hr=pd.concat(hr).dropna()
    hr["pg"]=hr.pos*hr.r
    out["mean pos, share in, mean bar ret, pos gain"] = pd.Series({"pos":hr.pos.mean(),"in":(hr.pos>0).mean(),"r":hr.r.mean(),"pg":hr.pg.mean(),"mkt part":hr.pos.mean()*hr.r.mean()})
    a=hr.groupby("wd")["r"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["weekday 1h ret"]=a
    a=hr.groupby("h")["r"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["hour 1h ret"]=a
    return out
