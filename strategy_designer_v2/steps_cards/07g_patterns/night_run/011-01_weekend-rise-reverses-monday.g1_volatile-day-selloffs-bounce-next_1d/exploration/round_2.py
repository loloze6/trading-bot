def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            r=c.pct_change()
            sd=r.rolling(60,min_periods=60).std()
            z=r/sd
            nxt=c.shift(-1)/c-1
            vr=np.log(b["volume"]/b["volume"].rolling(60,min_periods=30).mean())
            rng=(h-l)/c/sd
            cl=(c-l)/(h-l).replace(0,np.nan)
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"sd":sd,"nxt":nxt,"vr":vr,"rng":rng,"cl":cl,
                            "wd":pd.to_datetime(b["timestamp"]).dt.dayofweek,"alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    cm=D.groupby("coin")["nxt"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(cm)
    E=D.dropna(subset=["z","ex","vr"]).copy()
    out={}
    def tab(g):
        return pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    F=E[E["z"]<-1].copy()
    F["zb"]=pd.qcut(F["z"],2,labels=["big","small"])
    F["vb"]=pd.qcut(F["vr"],3,labels=False)
    out["falls z-half x volume tercile"]=tab(F.groupby(["zb","vb"])["ex"])
    # regression of ex on z and vr within falls
    X=np.column_stack([np.ones(len(F)),F["z"],F["vr"]]); y=F["ex"].values
    beta,res,_,_=np.linalg.lstsq(X,y,rcond=None)
    e=y-X@beta; s2=e@e/(len(y)-3); cov=s2*np.linalg.inv(X.T@X)
    out["falls OLS ex~z+logvolratio"]=pd.DataFrame({"beta":beta,"t":beta/np.sqrt(np.diag(cov))},index=["c","z","vr"])
    # volume effect by coin in falls: corr
    out["falls corr(vr,ex) by coin"]=F.groupby("coin").apply(lambda x: pd.Series({"n":len(x),"corr":x["vr"].corr(x["ex"])}))
    # volume effect in rises
    R=E[E["z"]>1].copy(); R["vb"]=pd.qcut(R["vr"],3,labels=False)
    out["rises by volume tercile"]=tab(R.groupby("vb")["ex"])
    # all days: volume tercile regardless of direction, signed by -sign(z)
    E["vb"]=E.groupby("coin")["vr"].transform(lambda s: pd.qcut(s,3,labels=False))
    E["rev"]=-np.sign(E["z"])*E["ex"]
    out["all days: reversal-signed ex by volume tercile"]=tab(E.groupby("vb")["rev"])
    # close location within falls
    F2=F.dropna(subset=["cl"]).copy(); F2["cb"]=pd.qcut(F2["cl"],3,labels=False)
    out["falls by close-location tercile (0=near low)"]=tab(F2.groupby("cb")["ex"])
    # falls vol tercile by year halves
    F["late"]=np.where(F["w"].str[1:].astype(int)<=12,"w1-12","w13-24")
    F["vq"]=pd.qcut(F["sd"],3,labels=False)
    out["falls vol tercile x window half"]=tab(F.groupby(["late","vq"])["ex"])
    # book: largest gain/loss days
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    DD=pd.concat(dd)
    bk=DD.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index().dropna()
    q=bk["book_return"].quantile([0.01,0.99])
    top=bk[bk.book_return>=q[0.99]]; bot=bk[bk.book_return<=q[0.01]]
    out["book top1% / bottom1%"]=pd.DataFrame({"n":[len(top),len(bot)],"book":[top.book_return.mean(),bot.book_return.mean()],
        "coins":[top.coin_return.mean(),bot.coin_return.mean()],"share_of_total_sum":[top.book_return.sum()/bk.book_return.sum(),bot.book_return.sum()/bk.book_return.sum()]})
    return out
