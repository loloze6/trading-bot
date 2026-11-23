def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            fwd=c.shift(-H)/c-1
            past5=c/c.shift(5)-1
            past20=c/c.shift(20)-1
            vol20=r1.rolling(20).std()
            near=c/c.rolling(60,min_periods=30).max()-1
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"fwd":fwd,"p5":past5,"p20":past20,"vol":vol20,
                "near":near,"fc":b["forecast"].astype(float),"pos":b["postRebalance_current_allocation"].astype(float),
                "wd":ts.dt.weekday,"yr":ts.dt.year,"r1":r1})
            df=df.iloc[::H]
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["fwd"])
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    d["volz"]=d["vol"]/d.groupby("coin")["vol"].transform("median")
    def g(col,q=5):
        x=d.dropna(subset=[col]).copy()
        x["b"]=x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),q,labels=False))
        o=x.groupby("b")["ex"].agg(["mean","count","std"])
        o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
        return o[["mean","count","t"]]
    out={}
    out["by_forecast_q"]=g("fc")
    out["by_past5_q"]=g("p5")
    out["by_past20_q"]=g("p20")
    out["by_vol_q"]=g("volz")
    out["by_near_q"]=g("near")
    def tg(col):
        o=d.groupby(col)["ex"].agg(["mean","count","std"]);o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]));return o[["mean","count","t"]]
    out["by_weekday"]=tg("wd")
    # strategy gain per case by year
    d["gain"]=np.sign(d["fc"])*d["ex"]
    o=d.groupby("yr")["gain"].agg(["mean","count","std"]);o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    out["signed_gain_by_year"]=o[["mean","count","t"]]
    # sign of forecast long vs short
    d["side"]=np.sign(d["fc"])
    o=d.groupby("side")["ex"].agg(["mean","count","std"]);o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    out["ex_by_side"]=o[["mean","count","t"]]
    # interaction: p5 x vol
    x=d.dropna(subset=["p5","volz"]).copy()
    x["vb"]=pd.qcut(x["volz"],3,labels=["lowv","midv","hiv"])
    x["pz"]=x["p5"]/(x["vol"]*np.sqrt(5))
    out["corr_p5z_ex_by_vol"]=x.groupby("vb").apply(lambda s: pd.Series({"rho":stats.spearmanr(s["pz"],s["ex"])[0],"n":len(s)}))
    # book daily: worst/best days context
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy();t["coin"]=coin;t["w"]=w;t["c5"]=t["close"].astype(float).pct_change(5).shift(1);dd.append(t)
    D=pd.concat(dd).dropna(subset=["book_return"])
    D["pos_sign"]=np.sign(D["book_return"]*D["coin_return"])
    D["absc"]=D["coin_return"].abs()
    D["cq"]=D.groupby("coin")["coin_return"].transform(lambda s: pd.qcut(s.rank(method="first"),10,labels=False))
    out["book_ret_by_coin_ret_decile"]=D.groupby("cq")["book_return"].agg(["mean","count"])
    return out
