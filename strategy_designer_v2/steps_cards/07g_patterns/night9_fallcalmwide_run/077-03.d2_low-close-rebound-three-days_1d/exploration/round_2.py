def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]
            r=c.pct_change()
            s30=r.rolling(30,min_periods=20).std()
            rng=(h-l)
            clv=np.where(rng>0,(c-(h+l)/2)/(rng/2),0.0)
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),"day":ts.dt.floor("D"),
                "clv":clv,"width":(rng/c)/s30,"r0z":r/s30,"s30":s30,
                "f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,"f3":c.shift(-3)/c-1,
                "ret20":c/c.shift(20)-1,"ret10":c/c.shift(10)-1,"ret40":c/c.shift(40)-1,
                "year":ts.dt.year})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for hz in (1,2,3):
        g=D[D["pos"]%hz==0]
        drift=g.groupby("coin")[f"f{hz}"].mean()
        D[f"x{hz}"]=D[f"f{hz}"]-D["coin"].map(drift)
    D["volrank"]=D.groupby("coin")["s30"].rank(pct=True)
    D["agit"]=(D["volrank"]>0.5).astype(int)
    def ct(df,col,sign=1):
        df=df.dropna(subset=[col])
        v=sign*df[col]; m=v.mean()
        dev=(v-m).groupby(df["day"]).sum(); Dn=len(dev)
        se=np.sqrt((dev**2).sum()*Dn/(Dn-1))/len(v)
        return pd.Series({"mean":round(m,5),"t_day":round(m/se,2),"n":len(v),"days":Dn})
    res={}
    # trend pullback: graded signal = -clv * sign(trend20) * width
    out={}
    for hz in (1,2,3):
        G=D[D["pos"]%hz==0].dropna(subset=["ret20","clv"])
        up=G[(G["ret20"]>0)&(G["clv"]<0)]; dn=G[(G["ret20"]<0)&(G["clv"]>0)]
        out[f"h{hz} up-trend low close long"]=ct(up,f"x{hz}",1)
        out[f"h{hz} down-trend high close short"]=ct(dn,f"x{hz}",-1)
    res["trend pullback, day-clustered"]=pd.DataFrame(out).T
    G=D.dropna(subset=["ret20","clv","x1"])
    # graded: within up-trend low closes, by clv tercile and by trend strength
    out={}
    for side,sub,sg in (("upLow",G[(G.ret20>0)&(G.clv<0)],1),("dnHigh",G[(G.ret20<0)&(G.clv>0)],-1)):
        sub=sub.assign(cq=pd.qcut(sub["clv"].abs(),3,labels=False),tq=pd.qcut(sub["ret20"].abs(),3,labels=False))
        for q in range(3):
            out[f"{side} |clv| q{q}"]=ct(sub[sub.cq==q],"x1",sg)
            out[f"{side} |trend20| q{q}"]=ct(sub[sub.tq==q],"x1",sg)
        for a in (0,1):
            out[f"{side} agit{a}"]=ct(sub[sub.agit==a],"x1",sg)
        for y in sorted(sub.year.unique()):
            out[f"{side} y{y}"]=ct(sub[sub.year==y],"x1",sg)
    res["pullback graded/regime/year"]=pd.DataFrame(out).T
    # high-vol up-day fade short, by trend and year
    out={}
    hv=G[G.volrank>2/3]
    for nm,sub in (("all",hv),("trend+",hv[hv.ret20>0]),("trend-",hv[hv.ret20<0])):
        u=sub[sub.r0z>0]
        out[f"hv upday short {nm}"]=ct(u,"x1",-1)
        dd=sub[sub.r0z<0]
        out[f"hv downday long {nm}"]=ct(dd,"x1",1)
    u=hv[hv.r0z>0].assign(q=lambda x: pd.qcut(x.r0z,3,labels=False))
    for q in range(3): out[f"hv upday short r0z q{q}"]=ct(u[u.q==q],"x1",-1)
    for y in sorted(hv.year.unique()): out[f"hv upday short y{y}"]=ct(hv[(hv.r0z>0)&(hv.year==y)],"x1",-1)
    res["high-vol up-day fade"]=pd.DataFrame(out).T
    # coin breadth of pullback
    sub=G[(G.ret20>0)&(G.clv<0)]
    res["upLow by coin"]=sub.groupby("coin")["x1"].agg(["mean","count"]).round(5)
    sub=G[(G.ret20<0)&(G.clv>0)]
    res["dnHigh by coin (short sign)"]=(-sub.groupby("coin")["x1"].mean()).round(5)
    return res
