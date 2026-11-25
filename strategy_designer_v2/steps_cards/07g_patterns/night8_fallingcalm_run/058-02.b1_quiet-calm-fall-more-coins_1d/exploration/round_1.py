def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values.astype(float); v=b["volume"].values.astype(float)
            n=len(b)
            fwd=np.full(n,np.nan); fwd[:n-H]=c[H:]/c[:n-H]-1
            r1=np.full(n,np.nan); r1[1:]=c[1:]/c[:-1]-1
            r30=np.full(n,np.nan); r30[30:]=c[30:]/c[:-30]-1
            r5p=np.full(n,np.nan); r5p[5:]=c[5:]/c[:-5]-1
            vs=pd.Series(v); vr=(vs.rolling(5).mean()/vs.rolling(30).mean()).values
            vol20=pd.Series(r1).rolling(20).std().values
            rng=((b["high"]-b["low"])/b["close"]).values
            clv=((b["close"]-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)).values
            col="debug_info.components.quiet_fall.last_history_value"
            qf=b[col].values if col in b else np.full(n,np.nan)
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,n,H):
                rows.append(dict(coin=coin,w=w,fwd=fwd[i],r1=r1[i],r30=r30[i],r5p=r5p[i],vr=vr[i],
                    vol20=vol20[i],rng=rng[i],clv=clv[i],qf=qf[i],fc=b["forecast"].iloc[i],
                    reg=b["regime"].iloc[i],wd=ts.iloc[i].dayofweek,yr=ts.iloc[i].year,day=ts.iloc[i].normalize()))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby("coin")["fwd"].transform("mean")
    d["ex"]=d["fwd"]-d["drift"]
    d=d.dropna(subset=["ex"])
    def tab(g,key):
        out=g.groupby(key)["ex"].agg(["mean","count","std"])
        out["t"]=out["mean"]/(out["std"]/np.sqrt(out["count"]))
        return out.drop(columns="std")
    res={}
    res["regime"]=tab(d,"reg")
    fc=d[d.reg=="unknown"].copy()
    fc["q_r30"]=pd.qcut(fc["r30"],4,labels=False,duplicates="drop")
    res["fallcalm_by_r30"]=tab(fc.dropna(subset=["r30"]),"q_r30")
    fc["q_vr"]=pd.qcut(fc["vr"],4,labels=False,duplicates="drop")
    res["fallcalm_by_vr5_30"]=tab(fc.dropna(subset=["vr"]),"q_vr")
    fc["q_r1"]=pd.qcut(fc["r1"],4,labels=False,duplicates="drop")
    res["fallcalm_by_r1"]=tab(fc.dropna(subset=["r1"]),"q_r1")
    fc["q_r5"]=pd.qcut(fc["r5p"],4,labels=False,duplicates="drop")
    res["fallcalm_by_r5p"]=tab(fc.dropna(subset=["r5p"]),"q_r5")
    ot=d[d.reg!="unknown"].copy()
    ot["q_r30"]=pd.qcut(ot["r30"],5,labels=False)
    res["other_by_r30"]=tab(ot.dropna(subset=["r30"]),"q_r30")
    d["q_r1"]=pd.qcut(d["r1"],5,labels=False)
    res["all_by_r1"]=tab(d.dropna(subset=["r1"]),"q_r1")
    d["q_r5"]=pd.qcut(d["r5p"],5,labels=False)
    res["all_by_r5p"]=tab(d.dropna(subset=["r5p"]),"q_r5")
    d["q_vol"]=pd.qcut(d["vol20"],5,labels=False)
    res["all_by_vol20"]=tab(d.dropna(subset=["vol20"]),"q_vol")
    d["q_vr"]=pd.qcut(d["vr"],5,labels=False)
    res["all_by_vr5_30"]=tab(d.dropna(subset=["vr"]),"q_vr")
    d["q_clv"]=pd.qcut(d["clv"],5,labels=False)
    res["all_by_clv"]=tab(d.dropna(subset=["clv"]),"q_clv")
    res["all_by_wd"]=tab(d,"wd")
    res["all_by_year"]=tab(d,"yr")
    # book daily
    br=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd[["day","book_return","coin_return"]].copy(); x["w"]=w; x["coin"]=coin; br.append(x)
    B=pd.concat(br).dropna()
    bk=B.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    bk["wd"]=pd.to_datetime(bk["day"]).dt.dayofweek
    res["book_by_wd"]=bk.groupby("wd")[["book_return","coin_return"]].mean()
    res["book_by_window"]=bk.groupby("w")[["book_return","coin_return"]].agg(["mean","count"])
    q=bk["book_return"]
    top=bk[q>=q.quantile(0.99)]; bot=bk[q<=q.quantile(0.01)]
    res["book_top_bottom"]=pd.DataFrame({"n":[len(top),len(bot)],"book":[top.book_return.mean(),bot.book_return.mean()],"coin":[top.coin_return.mean(),bot.coin_return.mean()]},index=["top1%","bot1%"])
    res["corr_book_coin"]=float(bk[["book_return","coin_return"]].corr().iloc[0,1])
    return res
