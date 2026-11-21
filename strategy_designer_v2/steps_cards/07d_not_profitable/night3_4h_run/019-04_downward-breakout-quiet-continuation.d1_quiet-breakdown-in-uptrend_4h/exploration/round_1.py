def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=18
    rows=[]; drift={}; usual={}
    for c,wd in data["bars"].items():
        rs=[]
        for w,b in wd.items():
            cl=b["close"].values
            idx=np.arange(0,len(cl)-H,H)
            rs+=list(cl[idx+H]/cl[idx]-1)
        drift[c]=np.mean(rs); usual[c]=np.std(rs)
    for c,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True)
            cl=b["close"]; lo=b["low"]; hi=b["high"]
            lo12=lo.shift(1).rolling(12).min(); hi12=hi.shift(1).rolling(12).max()
            S=hi12-lo12; B=(hi-lo).shift(1).rolling(180).mean()
            ratio=S/B
            r180=cl/cl.shift(180)-1
            r30d=r180; r7=cl/cl.shift(42)-1
            fwd=cl.shift(-H)/cl-1
            fwd6=cl.shift(-6)/cl-1
            dnb=(cl<lo12); upb=(cl>hi12)
            depth=(lo12-cl)/cl
            yr=pd.to_datetime(b["timestamp"]).dt.year
            grid=np.arange(len(b))//H
            df=pd.DataFrame({"c":c,"w":w,"cell":grid,"dn":dnb,"up":upb,"ratio":ratio,"r180":r180,"r7":r7,"fwd":fwd,"fwd6":fwd6,"depth":depth,"yr":yr})
            df=df.dropna(subset=["fwd","ratio","r180"])
            for side,col in [("dn","dn"),("up","up")]:
                d=df[df[col]].groupby("cell").first().reset_index()
                d["side"]=side
                rows.append(d)
    X=pd.concat(rows)
    X["drift"]=X["c"].map(drift); X["usual"]=X["c"].map(usual)
    X["tot_short"]=-X["fwd"]; X["unu_short"]=-(X["fwd"]-X["drift"])
    out={}
    def summ(g,col):
        return pd.Series({"n":len(g),"mean":g[col].mean(),"t":g[col].mean()/(g[col].std()/np.sqrt(len(g))) if len(g)>2 else np.nan})
    dn=X[X.side=="dn"]; up=X[X.side=="up"]
    dn["r180q"]=pd.qcut(dn["r180"],5,labels=False)
    out["down_break_short_total_by_r180_quintile"]=dn.groupby("r180q").apply(lambda g: pd.Series({"n":len(g),"r180_med":g.r180.median(),"short_total":g.tot_short.mean(),"t":summ(g,"tot_short")["t"],"short_unusual":g.unu_short.mean()}))
    dn["ratioq"]=pd.qcut(dn["ratio"],5,labels=False)
    out["down_break_short_total_by_narrowness_q(0=narrowest)"]=dn.groupby("ratioq").apply(lambda g: pd.Series({"n":len(g),"ratio_med":g.ratio.median(),"short_total_pos_r180":g[g.r180>0].tot_short.mean(),"short_total_neg_r180":g[g.r180<=0].tot_short.mean(),"short6_all":(-g.fwd6).mean()}))
    up["r180q"]=pd.qcut(up["r180"],5,labels=False)
    out["up_break_long_total_by_r180_quintile"]=up.groupby("r180q").apply(lambda g: pd.Series({"n":len(g),"r180_med":g.r180.median(),"long_total":g.fwd.mean(),"t":summ(g,"fwd")["t"],"long_unusual":(g.fwd-g.drift).mean()}))
    up["ratioq"]=pd.qcut(up["ratio"],5,labels=False)
    out["up_break_long_by_narrowness_q"]=up.groupby("ratioq").apply(lambda g: pd.Series({"n":len(g),"ratio_med":g.ratio.median(),"long_total":g.fwd.mean(),"long_total_pos_r180":g[g.r180>0].fwd.mean(),"absmove":g.fwd.abs().mean()}))
    # abs move after narrow vs not, all bars
    out["down_break_pos_r180_by_year"]=dn[dn.r180>0].groupby("yr").apply(lambda g: summ(g,"tot_short"))
    out["down_break_pos_r180_by_coin"]=dn[dn.r180>0].groupby("c").apply(lambda g: summ(g,"tot_short"))
    # book
    dd=[]
    for c,wd in data["days"].items():
        for w,d in wd.items():
            d=d.copy(); d["c"]=c; d["w"]=w; dd.append(d)
    D=pd.concat(dd); D["yr"]=pd.to_datetime(D["day"]).dt.year
    out["book_by_year"]=D.groupby("yr").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","count"))
    T=[]
    for c,wd in data["trades"].items():
        for w,t in wd.items():
            t=t.copy(); t["c"]=c; T.append(t)
    T=pd.concat(T)
    out["trades"]=T.groupby("side").agg(n=("net_profit_loss_percent","count"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur_h=("duration_minutes",lambda x:x.mean()/60),win=("profit_loss_percent",lambda x:(x>0).mean()))
    return out
