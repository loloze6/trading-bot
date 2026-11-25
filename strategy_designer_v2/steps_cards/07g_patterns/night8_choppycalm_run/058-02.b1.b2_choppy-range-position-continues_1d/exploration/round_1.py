def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); hi=b["high"].astype(float); lo=b["low"].astype(float)
            hh=hi.rolling(20).max(); ll=lo.rolling(20).min()
            rp=2*(c-ll)/(hh-ll)-1
            r1=c.pct_change()
            vol30=r1.rolling(30).std()
            tr20=c/c.shift(20)-1
            fwd=c.shift(-H)/c-1
            fwd1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"rp":rp,"r1":r1,"vol30":vol30,
                "tr20":tr20,"fwd":fwd,"fwd1":fwd1,"choppy":(b["regime"]!="chop").values,
                "wd":ts.dt.weekday,"yr":ts.dt.year,"fc":b["forecast"],
                "alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    cm=A[A.pos%H==0].groupby("coin")["fwd"].mean()
    A["ex"]=A["fwd"]-A["coin"].map(cm)
    # vol relative: coin's vol30 rank over all its bars (diagnostic)
    A["vrank"]=A.groupby("coin")["vol30"].rank(pct=True)
    A["r1z"]=A["r1"]/A["vol30"]
    G=A[(A.pos%H==0)].dropna(subset=["ex","rp"])
    out={}
    def tab(df,key):
        g=df.groupby(key)["ex"]
        t=g.agg(["count","mean","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"])); return t.round(4)
    G["rpq"]=pd.cut(G.rp,[-1.01,-0.6,-0.2,0.2,0.6,1.01],labels=["b","lb","m","ut","t"])
    out["rp_choppy"]=tab(G[G.choppy],"rpq")
    out["rp_outside"]=tab(G[~G.choppy],"rpq")
    G["vq"]=pd.cut(G.vrank,[0,0.5,1],labels=["calm","agit"])
    out["rp_choppy_by_vol"]=tab(G[G.choppy],["vq","rpq"])
    G["tq"]=pd.qcut(G.tr20,5,labels=False)
    out["tr20_all"]=tab(G,"tq")
    out["tr20_choppy"]=tab(G[G.choppy],"tq")
    G2=G.dropna(subset=["r1z"]).copy()
    G2["zq"]=pd.qcut(G2.r1z,5,labels=False)
    out["r1z_all"]=tab(G2,"zq")
    out["r1z_by_vol"]=tab(G2,["vq","zq"])
    G["vq5"]=pd.qcut(G.vrank,5,labels=False)
    out["vol_level"]=tab(G,"vq5")
    # weekday daily returns (all bars)
    D=A.dropna(subset=["fwd1"]).copy()
    D["cm1"]=D.groupby("coin")["fwd1"].transform("mean")
    D["ex"]=D["fwd1"]-D["cm1"]
    D["wd_next"]=(D["wd"]+1)%7
    out["weekday_nextday"]=tab(D,"wd_next")
    out["year_rp_choppy_slope"]=G[G.choppy].groupby("yr").apply(lambda x: pd.Series({"n":len(x),"corr":x.rp.corr(x.ex)})).round(3)
    # book: days
    dd=[]
    for coin,wins in data["days"].items():
        for w,t in wins.items():
            t=t.copy(); t["coin"]=coin; t["w"]=w; dd.append(t)
    Dd=pd.concat(dd)
    bk=Dd.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book_by_window"]=bk.groupby(level=0).agg(["mean","count"]).round(5)
    big=bk.book_return
    out["book_top_bottom"]=pd.DataFrame({"top20_mean":[big.nlargest(20).mean()],"bot20_mean":[big.nsmallest(20).mean()],
        "coin_on_top":[bk.loc[big.nlargest(20).index,"coin_return"].mean()],"coin_on_bot":[bk.loc[big.nsmallest(20).index,"coin_return"].mean()],
        "corr_book_coin":[bk.book_return.corr(bk.coin_return)]}).round(4)
    # long vs short in book
    P=A.dropna(subset=["fwd1","alloc"])
    P["g"]=P.alloc*P.fwd1
    P["side"]=np.sign(P.alloc)
    out["gain_by_side"]=P.groupby("side")["g"].agg(["count","mean","sum"])
    return out
