def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            b["ts"] = pd.to_datetime(b["timestamp"]); b["day"] = b["ts"].dt.floor("D")
            b["pos"] = b["postRebalance_current_allocation"].shift(1)
            b["fc_prev"] = b["forecast"].shift(1)
            b["r1"] = b["close"].pct_change()
            b["bk"] = b["postRebalance_total_value"].pct_change()
            b["ret30"] = b["close"]/b["close"].shift(30)-1
            b["ret60"] = b["close"]/b["close"].shift(60)-1
            b["vol30"] = b["r1"].rolling(30).std()*np.sqrt(30)
            b["z30"] = b["ret30"]/b["vol30"]
            b["coin"]=c; b["win"]=w; b["i"]=np.arange(len(b))
            rows.append(b[["coin","win","day","i","pos","fc_prev","r1","bk","close","forecast","ret30","ret60","z30"]])
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["r1"].mean(); B["mu"]=B.coin.map(mu)
    B["tim"] = B.bk - B.pos*B.mu
    D = B.dropna(subset=["bk","pos"])
    D = D.assign(state=np.where(D.pos.abs()<1e-9,"flat",np.where(D.fc_prev>0,"held_fc>0","held_fc==0")))
    nd = D.groupby(["win","day"]).ngroups
    nc = D.groupby(["win","day"])["coin"].transform("size")
    D = D.assign(wbk=D.bk/nc, wtim=D.tim/nc)
    st = D.groupby("state").agg(n=("bk","size"), mean_bk=("bk","mean"), mean_tim=("tim","mean"), mean_pos=("pos","mean"))
    st["contrib_bk_per_day"] = D.groupby("state")["wbk"].sum()/nd
    st["contrib_tim_per_day"] = D.groupby("state")["wtim"].sum()/nd
    out["by_state"] = st.round(5)
    def clus(g):
        pdd = g.groupby("day")["ab"].sum(); Dn=len(pdd); m=g.ab.mean()
        se=np.sqrt((pdd**2).sum()*Dn/(Dn-1))/len(g); return m, m/se, Dn
    res=[]; slopes=[]
    for h in [10,20,30]:
        rr=[]
        for (c,w),g in B.groupby(["coin","win"]):
            g=g.reset_index(drop=True); fwd=g.close.shift(-h)/g.close-1
            idx=np.arange(0,len(g),h)
            rr.append(pd.DataFrame({"coin":c,"day":g.day.iloc[idx].values,"fwd":fwd.iloc[idx].values,
              "z30":g.z30.iloc[idx].values,"ret30":g.ret30.iloc[idx].values,"ret60":g.ret60.iloc[idx].values}))
        R=pd.concat(rr).dropna()
        R["ab"]=R.fwd-R.coin.map(R.groupby("coin").fwd.mean())
        R["yr"]=pd.to_datetime(R.day).dt.year
        R["half"]=np.where(R.yr<=2021,"2018-21","2022-25")
        for var in ["z30","ret60"]:
            R["q"]=pd.qcut(R[var],5,labels=False)
            for q,g in R.groupby("q"):
                m,t,Dn=clus(g); res.append({"h":h,"var":var,"q":q,"n":len(g),"days":Dn,"mean_ab":m,"t":t,"med_var":g[var].median()})
        for half,G in R.groupby("half"):
            G=G.copy(); G["q"]=pd.qcut(G.z30,5,labels=False)
            hi=G[G.q==4]; lo=G[G.q==0]
            for nm,g in [("hi",hi),("lo",lo)]:
                m,t,Dn=clus(g); slopes.append({"h":h,"half":half,"grp":nm,"n":len(g),"mean_ab":m,"t":t})
        # strength per case: ab/usual move, slope of ab on z30
        x=R.z30.clip(-4,4); y=R.ab
        b=np.cov(x,y)[0,1]/x.var(); e=y-y.mean()-b*(x-x.mean())
        sc=(e*(x-x.mean())).groupby(R.day).sum(); se=np.sqrt((sc**2).sum())/((x-x.mean())**2).sum()
        slopes.append({"h":h,"half":"all","grp":"slope_ab_on_z30","n":len(R),"mean_ab":b,"t":b/se})
        # top quintile z30 by coin sign
        R["q"]=pd.qcut(R.z30,5,labels=False)
        if h==10:
            top=R[R.q==4]
            out["top_z30_by_coin_h10"]=top.groupby("coin").ab.agg(["mean","size"]).round(4)
            out["usual_move"]=pd.Series({"h10_std":R.groupby("coin").fwd.std().mean()})
    out["quintiles"]=pd.DataFrame(res).round(4)
    out["halves_and_slope"]=pd.DataFrame(slopes).round(4)
    return out
