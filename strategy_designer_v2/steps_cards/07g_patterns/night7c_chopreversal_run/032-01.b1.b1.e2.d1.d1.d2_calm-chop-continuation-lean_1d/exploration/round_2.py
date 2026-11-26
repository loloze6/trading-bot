def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            s30=r1.rolling(30).std()
            s90=r1.rolling(90,min_periods=40).std()
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"r1":r1,"r1z":r1/s30.shift(1),
                            "n1":c.shift(-1)/c-1,"n3":c.shift(-3)/c-1,"n7":c.shift(-7)/c-1,
                            "vr":s30/s90,"r30":c/c.shift(30)-1,"year":ts.dt.year,
                            "s30":s30,"pos":b["postRebalance_current_allocation"].astype(float)})
            d["i"]=np.arange(len(d))
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    f=lambda x: pd.Series({"mean":x.mean(),"n":len(x),"t":x.mean()/x.std()*np.sqrt(len(x))})
    out={}
    for h,col in [(1,"n1"),(3,"n3")]:
        G=A[A.i%h==0].dropna(subset=[col,"r1z"]).copy()
        dr=G.groupby("coin")[col].mean()
        G["ex"]=G[col]-G.coin.map(dr)
        G["zb"]=pd.cut(G.r1z,[-99,-3,-2,-1.5,-1,0,1,1.5,2,3,99])
        out[f"excess next {h}d by today z"]=G.groupby("zb")["ex"].apply(f).unstack()
        if h==1:
            L=G[G.r1z<=-1.5]
            out["after z<=-1.5: excess next 1d by coin"]=L.groupby("coin")["ex"].apply(f).unstack()
            out["after z<=-1.5: by year"]=L.groupby("year")["ex"].apply(f).unstack()
            L=L.copy(); L["vrb"]=pd.qcut(L.vr,3,labels=["calm","mid","wide"])
            out["after z<=-1.5: by vr"]=L.groupby("vrb")["ex"].apply(f).unstack()
            L["tr"]=np.where(L.r30>0,"r30 up","r30 down")
            out["after z<=-1.5: by r30 sign"]=L.groupby("tr")["ex"].apply(f).unstack()
            # graded: regression of ex on r1z among down days
            Dn=G[G.r1z<0].dropna(subset=["ex"])
            sl=np.polyfit(Dn.r1z,Dn.ex,1)[0]
            res=Dn.ex-np.polyval(np.polyfit(Dn.r1z,Dn.ex,1),Dn.r1z)
            se=res.std()/np.sqrt(((Dn.r1z-Dn.r1z.mean())**2).sum())
            out["down days: slope ex on z, t, n"]=f"{sl:.5f}, t {sl/se:.2f}, n {len(Dn)}"
            Up=G[G.r1z>0]
            p=np.polyfit(Up.r1z,Up.ex,1); res=Up.ex-np.polyval(p,Up.r1z)
            se=res.std()/np.sqrt(((Up.r1z-Up.r1z.mean())**2).sum())
            out["up days: slope ex on z, t, n"]=f"{p[0]:.5f}, t {p[0]/se:.2f}, n {len(Up)}"
            # was the book positioned on those rebound days?
            L2=A[(A.r1z<=-1.5)].dropna(subset=["n1"])
            out["book pos after big down day"]=f"mean pos {L2.pos.mean():.3f}, share long {(L2.pos>0).mean():.2f}, share short {(L2.pos<0).mean():.2f}, n {len(L2)}"
    # book: before/after largest daily losses
    bd=[]
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dd=d.reset_index(drop=True).copy(); dd["coin"]=coin; dd["w"]=w
            dd["nb"]=dd.book_return.shift(-1); dd["pc"]=dd.coin_return.shift(1)
            bd.append(dd)
    B=pd.concat(bd).dropna(subset=["book_return","nb"])
    q=B.book_return.quantile([0.02,0.98])
    out["book next day after its worst 2% days"]=f(B[B.book_return<=q.iloc[0]].nb).to_string()
    out["book next day after its best 2% days"]=f(B[B.book_return>=q.iloc[1]].nb).to_string()
    return out
