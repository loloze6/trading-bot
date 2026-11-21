def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=18
    rows=[]; cells=[]
    for coin, wins in data["bars"].items():
        grid=[]
        per=[]
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; hi=b["high"].values; lo=b["low"].values
            n=len(c)
            s=pd.Series(c)
            f=s.shift(-H)/s-1
            minlo=pd.Series(lo).shift(1).rolling(12).min()
            maxhi=pd.Series(hi).shift(1).rolling(12).max()
            S=maxhi-minlo
            br=pd.Series((hi-lo)/c)
            B=pd.Series(hi-lo).rolling(180).mean()
            comp=S/B
            r180=s/s.shift(180)-1
            r6=s/s.shift(6)-1
            r1=s/s.shift(1)-1
            vol=r1.rolling(180).std()
            dn=(s<minlo)
            up=(s>maxhi)
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"f":f,"comp":comp,"r180":r180,"r6":r6,"r1":r1,"vol":vol,"dn":dn,"up":up,
                             "hour":ts.dt.hour,"wd":ts.dt.weekday,"pos":np.arange(n),"coin":coin,"w":w})
            df["cell"]=df["pos"]//H
            per.append(df)
            grid.append(f.iloc[::H].dropna())
        drift=pd.concat(grid).mean(); sd=pd.concat(grid).std()
        for df in per:
            df["u"]=df["f"]-drift; df["z"]=df["u"]/sd
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    G=A[A["pos"]%H==0].dropna(subset=["f","comp","r180"])
    def summ(x,col="u"):
        v=x[col].dropna()
        return pd.Series({"n":len(v),"mean":v.mean(),"t":v.mean()/(v.std()/np.sqrt(len(v))) if len(v)>2 else np.nan,"absz":x["z"].abs().mean()})
    out={}
    G=G.copy(); G["cq"]=G.groupby("coin")["comp"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["grid_by_compression_quintile"]=G.groupby("cq").apply(summ)
    def firstcases(mask, sign):
        X=A[mask & A["f"].notna() & A["comp"].notna() & A["r180"].notna()]
        X=X.groupby(["coin","w","cell"]).head(1).copy()
        X["s"]=sign*X["u"]; X["z"]=sign*X["z"]
        return X
    D=firstcases(A["dn"],-1); U=firstcases(A["up"],1)
    for nm,X in [("down",D),("up",U)]:
        X["trend"]=np.where(X["r180"]>0,"r180+","r180-")
        X["ct"]=X.groupby("coin")["comp"].transform(lambda x: pd.qcut(x,3,labels=False))
        out[f"break_{nm}_by_trend_comptercile"]=X.groupby(["trend","ct"]).apply(lambda x: summ(x,"s"))
        X["vq"]=X.groupby("coin")["vol"].transform(lambda x: pd.qcut(x,3,labels=False))
        out[f"break_{nm}_by_trend_vol"]=X.groupby(["trend","vq"]).apply(lambda x: summ(x,"s"))
    G["r6q"]=G.groupby("coin")["r6"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["grid_by_past1day_return_quintile"]=G.groupby("r6q").apply(summ)
    G["vq"]=G.groupby("coin")["vol"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["grid_by_vol_quintile"]=G.groupby("vq").apply(summ)
    G["tr"]=np.where(G["r180"]>0,"r180+","r180-")
    out["grid_by_trend"]=G.groupby("tr").apply(summ)
    out["grid_by_weekday"]=G.groupby("wd").apply(summ)
    out["grid_by_hour"]=G.groupby("hour").apply(summ)
    # per-coin for down-break r180+
    Dp=D[D["r180"]>0]
    out["down_r180pos_by_coin"]=Dp.groupby("coin").apply(lambda x: summ(x,"s"))
    # book: days
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; dd.append(d)
    Dd=pd.concat(dd)
    out["book_return_by_coin"]=Dd.groupby("coin")[["book_return","coin_return"]].mean()
    # trades
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values() if len(t)])
    out["trades_by_coin"]=tr.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
