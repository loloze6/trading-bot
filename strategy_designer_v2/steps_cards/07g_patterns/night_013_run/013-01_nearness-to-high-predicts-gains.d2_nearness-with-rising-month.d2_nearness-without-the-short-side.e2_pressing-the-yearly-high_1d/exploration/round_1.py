def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=7
    rows=[]
    drows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            fwd=c.shift(-H)/c-1
            past7=c/c.shift(7)-1
            past28=c/c.shift(28)-1
            r1=c.pct_change()
            vol20=r1.rolling(20).std()
            v=b["volume"].astype(float)
            vr=v/v.rolling(20).mean()
            hi30=c.rolling(30).max().shift(1)
            brk=(c/hi30-1)
            hi90=c.rolling(90).max()
            d90=c/hi90-1
            raw=b.get("debug_info.components.dist_high.last_history_value")
            df=pd.DataFrame({"coin":coin,"w":w,"fwd":fwd,"fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],
                             "past7":past7,"past28":past28,"vol20":vol20,"vr":vr,"brk":brk,"d90":d90,
                             "raw":raw if raw is not None else np.nan})
            df=df.iloc[::H]
            rows.append(df)
        for w,d in data["days"][coin].items():
            d=d.reset_index(drop=True)
            dd=pd.DataFrame({"coin":coin,"w":w,"br":d["book_return"],"cr":d["coin_return"],
                             "wd":pd.to_datetime(d["day"]).dt.dayofweek,"yr":pd.to_datetime(d["day"]).dt.year})
            dd["cr_next3"]=(1+d["coin_return"]).rolling(3).apply(np.prod,raw=True).shift(-3)-1
            drows.append(dd)
    g=pd.concat(rows).dropna(subset=["fwd"])
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    def qt(col,q=5):
        x=g.dropna(subset=[col]).copy()
        x["q"]=x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),q,labels=False))
        o=x.groupby("q")["ex"].agg(["mean","count","std"])
        o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
        return o[["mean","t","count"]].round(4)
    res={}
    for col in ["fc","raw","past7","past28","vol20","vr","brk","d90","alloc"]:
        res["q_"+col]=qt(col)
    D=pd.concat(drows).dropna(subset=["cr"])
    wd=D.groupby("wd")["cr"].agg(["mean","count","std"]); wd["t"]=wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    res["weekday_coin"]=wd.round(5)
    yb=D.groupby("yr")[["br","cr"]].mean().round(5); res["year_book_vs_coin"]=yb
    D2=D.dropna(subset=["br"])
    lo=D2["br"].quantile(0.02); hi=D2["br"].quantile(0.98)
    res["after_book_extremes"]=pd.DataFrame({
        "big_loss_next3":[D2.loc[D2.br<=lo,"cr_next3"].mean(),(D2.br<=lo).sum()],
        "big_gain_next3":[D2.loc[D2.br>=hi,"cr_next3"].mean(),(D2.br>=hi).sum()],
        "all_next3":[D2["cr_next3"].mean(),len(D2)]}).round(4)
    # big coin daily moves -> next 3 days
    z=D.copy(); z["zs"]=z.groupby("coin")["cr"].transform(lambda s:(s-s.mean())/s.std())
    z["b"]=pd.cut(z["zs"],[-99,-2,-1,1,2,99])
    o=z.groupby("b")["cr_next3"].agg(["mean","count","std"]); o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    res["after_big_day"]=o.round(4)
    return res
