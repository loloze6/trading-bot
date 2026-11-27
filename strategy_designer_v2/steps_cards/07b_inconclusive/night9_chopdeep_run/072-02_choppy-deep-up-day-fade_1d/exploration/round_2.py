def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            hi=c.rolling(20,min_periods=20).max()
            sd=r1.rolling(20,min_periods=20).std()
            depth=(c-hi)/hi/sd
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"day":b["timestamp"].astype(str).str[:10],
                "r1":r1,"depth":depth,"tr60":c/c.shift(60)-1,"fc":b["forecast"].astype(float),
                "pp":pd.to_numeric(b.get("debug_info.components.depth.post_pipeline_value"),errors="coerce"),
                "f1":c.shift(-1)/c-1,"f3":c.shift(-3)/c-1})
            rows.append(d)
    D=pd.concat(rows)
    for h in [1,3]:
        m=D[D.pos%h==0].groupby("coin")["f%d"%h].mean()
        D["x%d"%h]=-(D["f%d"%h]-D.coin.map(m))
    def tt(s,days):
        g=s.groupby(days).sum()
        return pd.Series({"mean%":s.mean()*100,"n":len(s),"days":g.size,"t":g.mean()/(g.std()/np.sqrt(len(g)))})
    out={}
    act=D[(D.fc<0)&D.x1.notna()].copy()
    # thirds on standardised pipeline value vs raw depth
    for col in ["pp","depth"]:
        q=pd.qcut(act[col].rank(method="first"),3,labels=["deep","mid","shallow"])
        out["thirds_on_"+col]=act.groupby(q).agg(val=(col,"mean"),x1=("x1",lambda s:s.mean()*100),n=("x1","size"))
    out["corr_pp_depth"]=float(act[["pp","depth"]].corr().iloc[0,1])
    # robustness without w16
    res={}
    for lab,s in [("all",act),("ex_w16",act[act.w!="w16"])]:
        res[lab+"_fc"]=tt(s.x1*(-s.fc/10),s.day)
        res[lab+"_rawdepth"]=tt(s.x1*(-s.depth),s.day)
    out["robust"]=pd.DataFrame(res).T
    ch=D[(D.tr60.abs()<=0.10)&(D.depth<0)].copy()
    res2={}
    for lab,s in [("all",ch),("ex_w16",ch[ch.w!="w16"])]:
        for h in [1,3]:
            ss=s[s.pos%h==0].dropna(subset=["x%d"%h])
            res2[f"{lab}_bothsides_h{h}"]=tt(ss["x%d"%h]*(-ss.depth),ss.day)
            u=ss[ss.r1>0]
            res2[f"{lab}_up_h{h}"]=tt(u["x%d"%h]*(-u.depth),u.day)
    out["raw_depth_t"]=pd.DataFrame(res2).T
    ch["year"]=ch.day.str[:4]
    u=ch[(ch.r1>0)&ch.x1.notna()]
    out["up_by_year"]=u.groupby("year").apply(lambda s:pd.Series({"wt":(s.x1*-s.depth).mean()*100,"n":len(s)}))
    return out
