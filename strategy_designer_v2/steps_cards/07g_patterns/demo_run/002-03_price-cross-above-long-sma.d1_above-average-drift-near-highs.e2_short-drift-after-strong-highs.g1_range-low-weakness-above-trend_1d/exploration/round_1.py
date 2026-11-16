def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; drows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            lo=c.rolling(20).min(); hi=c.rolling(20).max()
            rp=(c-lo)/(hi-lo)
            r1=c.pct_change()
            vol=r1.rolling(20).std()
            p5=c/c.shift(5)-1; p20=c/c.shift(20)-1
            f5=c.shift(-5)/c-1
            ts=pd.to_datetime(b["timestamp"])
            idx=np.arange(0,len(b),5)
            g=pd.DataFrame({"coin":coin,"w":w,"rp":rp.iloc[idx].values,"vol":vol.iloc[idx].values,
                "p5":p5.iloc[idx].values,"p20":p20.iloc[idx].values,"f5":f5.iloc[idx].values,
                "fc":b["forecast"].iloc[idx].values,"reg":b["regime"].iloc[idx].values,
                "wd":ts.dt.weekday.iloc[idx].values,"year":ts.dt.year.iloc[idx].values})
            rows.append(g)
        for w,d in data["days"][coin].items():
            d=d.copy(); d["coin"]=coin; d["w"]=w
            d["wd"]=pd.to_datetime(d["day"]).dt.weekday
            # position at end of previous day
            b=data["bars"][coin][w]
            pos=b.groupby(pd.to_datetime(b["timestamp"]).dt.floor("D"))["postRebalance_current_allocation"].last()
            d["pos_prev"]=pd.Series(pos.values).shift(1).values[:len(d)] if len(pos)==len(d) else np.nan
            drows.append(d)
    G=pd.concat(rows); G=G.dropna(subset=["f5"])
    G["ex"]=G["f5"]-G.groupby("coin")["f5"].transform("mean")
    D=pd.concat(drows)
    out={}
    def summ(df,key):
        a=df.groupby(key)["ex"].agg(["mean","count","std"])
        a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"])); return a.drop(columns="std").round(4)
    G["rpq"]=pd.cut(G["rp"],[-.01,.2,.4,.6,.8,1.01])
    out["rangepos x regime"]=summ(G,["reg","rpq"])
    G["p5q"]=G.groupby("coin")["p5"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["past5 quintile x regime"]=summ(G,["reg","p5q"])
    G["p20q"]=G.groupby("coin")["p20"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["past20 quintile x regime"]=summ(G,["reg","p20q"])
    G["vq"]=G.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    out["vol tercile"]=summ(G,["vq"])
    out["coin x regime"]=summ(G,["coin","reg"])
    out["year"]=summ(G,["year"])
    D2=D.dropna(subset=["coin_return"])
    D2["cex"]=D2["coin_return"]-D2.groupby("coin")["coin_return"].transform("mean")
    a=D2.groupby("wd")["cex"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["weekday daily coin excess"]=a.round(5)
    m=D2.groupby("coin")["coin_return"].mean()
    D2["mkt"]=D2["pos_prev"]*D2["coin"].map(m)
    out["book mean"]=float(D2["book_return"].mean())
    out["book market part"]=float(D2["mkt"].mean())
    out["mean pos_prev"]=float(D2["pos_prev"].mean())
    D2["side"]=np.sign(D2["pos_prev"].fillna(0))
    out["book by side"]=D2.groupby("side")[["book_return","coin_return"]].agg(["mean","count"]).round(5)
    out["book by coin"]=D2.groupby("coin")["book_return"].agg(["mean","std","count"]).round(5)
    return out
