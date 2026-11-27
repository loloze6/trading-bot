def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            hi=c.rolling(20,min_periods=20).max()
            sd=r.rolling(20,min_periods=20).std()
            depth=(c-hi)/hi/sd
            tr60=c/c.shift(60)-1
            vol30=r.rolling(30,min_periods=20).std()
            n=len(b)
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(n),"r":r,"depth":depth,
                "alloc":b["postRebalance_current_allocation"].astype(float),
                "prev":b["previous_allocation"].astype(float),
                "tr60":tr60,"vrank":vol30.rolling(120,min_periods=60).rank(pct=True)})
            for h in [1,2,3,5]:
                df[f"f{h}"]=c.shift(-h)/c-1
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    out={}
    def q5(s):
        return pd.cut(s.rank(pct=True),[0,.2,.4,.6,.8,1.0001],labels=["q1deep","q2","q3","q4","q5shallow"])
    D["up"]=D.r>0
    drift={h:D[f"f{h}"].mean() for h in [1,2,3,5]}
    out["drift_all_bars"]=pd.Series(drift)
    U=D[D.up & D.depth.notna() & D.f1.notna()].copy()
    U["q"]=q5(U.depth)
    def tt(x):
        x=x.dropna(); 
        return x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
    g=U.groupby("q").agg(n=("f1","size"),depth=("depth","mean"),f1=("f1","mean"),f2=("f2","mean"),f3=("f3","mean"),f5=("f5","mean"))
    out["up_by_depth_q_fwd"]=g
    # non-overlapping h=3 and 5 grid t for deep quintile vs others
    res={}
    for h in [1,3,5]:
        S=U[(U.pos%h)==0]
        for q in ["q1deep","q2","q5shallow"]:
            x=S.loc[S.q==q,f"f{h}"]-drift[h]
            res[(h,q)]=(len(x.dropna()),x.mean(),tt(x))
    out["nonoverlap_excess_by_h_q(n,mean,t)"]=pd.DataFrame(res,index=["n","mean_excess","t"]).T
    Dn=D[(~D.up)&D.depth.notna()&D.f1.notna()].copy()
    Dn["q"]=q5(Dn.depth)
    out["down_by_depth_q"]=Dn.groupby("q").agg(n=("f1","size"),f1=("f1","mean"),f3=("f3","mean"))
    U["trend"]=pd.cut(U.tr60,[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    U["agit"]=np.where(U.vrank>0.5,"agit","calm")
    out["up_q_by_trend_f1"]=U.groupby(["trend","q"]).f1.mean().unstack()
    out["up_q_by_trend_f3"]=U.groupby(["trend","q"]).f3.mean().unstack()
    D["trend"]=pd.cut(D.tr60,[-9,-0.1,0.1,9],labels=["falling","choppy","rising"])
    out["all_bars_by_trend"]=D.groupby("trend")[["f1","f3"]].mean()
    out["up_q_by_agit_f1"]=U.groupby(["agit","q"]).f1.mean().unstack()
    U["upsz"]=pd.cut(U.r.rank(pct=True),[0,1/3,2/3,1.0001],labels=["small","mid","big"])
    out["deep40_by_upsize"]=U[U.q.isin(["q1deep","q2"])].groupby("upsz")[["f1","f3"]].agg(["size","mean"])
    # book gain and turnover
    D["gain"]=D.alloc*D.f1
    D["turn"]=(D.alloc-D.prev).abs()
    D["cost"]=D.turn*0.0011
    out["book_by_trend"]=D.groupby("trend").agg(gain=("gain","mean"),cost=("cost","mean"),held=("alloc",lambda x:(x!=0).mean()))
    out["book_by_window"]=D.groupby("w").agg(gain=("gain","mean"),cost=("cost","mean"),held=("alloc",lambda x:(x!=0).mean()))
    out["mean_abs_alloc_held"]=float(D.loc[D.alloc!=0,"alloc"].abs().mean())
    out["mean_turn_per_held_bar"]=float(D.loc[D.alloc!=0,"turn"].mean())
    # book gain by depth quintile of active bar
    A=D[(D.alloc!=0)&D.depth.notna()].copy(); A["q"]=q5(A.depth)
    out["book_gain_by_depth_q"]=A.groupby("q").agg(gain=("gain","mean"),cost=("cost","mean"),n=("gain","size"))
    # deepest falls: daily book
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd.append(pd.DataFrame({"w":w,"day":d["day"].values,"br":d["book_return"].values,"cr":d["coin_return"].values}))
    DD=pd.concat(dd)
    B=DD.groupby(["w","day"]).agg(br=("br","mean"),cr=("cr","mean")).reset_index()
    out["book_daily_by_window"]=B.groupby("w").agg(br=("br","mean"),cr=("cr","mean"),sd=("br","std"))
    B["cq"]=pd.cut(B.cr.rank(pct=True),[0,.1,.5,.9,1.0001],labels=["coin_bottom10","low","high","coin_top10"])
    out["book_by_coin_day_bucket"]=B.groupby("cq").br.agg(["size","mean"])
    return out
