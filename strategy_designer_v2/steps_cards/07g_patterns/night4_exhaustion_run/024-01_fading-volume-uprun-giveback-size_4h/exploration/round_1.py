def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=18
    rows=[]; hourrows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float); v=df["volume"].astype(float)
            r=c.pct_change()
            sd=r.rolling(180,min_periods=60).std()
            up=(r>0).astype(int); dn=(r<0).astype(int)
            # signed streak length
            s=np.zeros(len(df))
            for i in range(1,len(df)):
                if r.iloc[i]>0: s[i]=s[i-1]+1 if s[i-1]>0 else 1
                elif r.iloc[i]<0: s[i]=s[i-1]-1 if s[i-1]<0 else -1
                else: s[i]=0
            g4=(c/c.shift(4)-1)/sd
            g6=(c/c.shift(6)-1)/sd
            g18=(c/c.shift(18)-1)/sd
            fade=v.rolling(2).mean()/v.rolling(4).mean()
            vrel=v/v.rolling(180,min_periods=60).mean()
            fwd=c.shift(-H)/c-1
            fwd6=c.shift(-6)/c-1
            ts=pd.to_datetime(df["timestamp"])
            idx=np.arange(0,len(df),H)
            sub=pd.DataFrame({"coin":coin,"w":w,"streak":s[idx],"g4":g4.values[idx],"g6":g6.values[idx],
                "g18":g18.values[idx],"fade":fade.values[idx],"vrel":vrel.values[idx],"sd":sd.values[idx],
                "fwd":fwd.values[idx],"fc":df["forecast"].values[idx],
                "pos":df["postRebalance_current_allocation"].values[idx]})
            rows.append(sub)
            hourrows.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour,"wd":ts.dt.weekday,"r1":r.shift(-1),"absr":r.abs(),"vrel":vrel}))
    G=pd.concat(rows).dropna(subset=["fwd"])
    drift=G.groupby("coin")["fwd"].mean(); usual=G.groupby("coin")["fwd"].std()
    G["ex"]=G["fwd"]-G["coin"].map(drift)
    G["z"]=G["ex"]/G["coin"].map(usual)
    def summ(g):
        x=g["z"].dropna(); e=g["ex"].dropna()
        return pd.Series({"n":len(x),"mean_ex%":100*e.mean(),"mean_z":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    G["sbin"]=pd.cut(G["streak"],[-99,-5,-3,-1,0,2,4,99])
    out["streak_len"]=G.groupby("sbin").apply(summ)
    G["fadebin"]=np.where(G["fade"]<1,"fade","rise")
    out["streak_x_fade"]=G[G["streak"].abs()>=3].groupby([np.sign(G["streak"]),"fadebin"]).apply(summ)
    for k in ["g4","g18","vrel","sd"]:
        G[k+"q"]=G.groupby("coin")[k].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
        out[k+"_quint"]=G.groupby(k+"q").apply(summ)
    G["vq"]=G["vrelq"]
    out["g18_by_vrel_hi_lo"]=G[G["vq"].isin([0,4])].groupby(["vq","g18q"]).apply(summ)
    out["coin"]=G.groupby("coin").apply(summ)
    G["fcb"]=pd.cut(G["fc"],[-21,-5,-0.01,0.01,21])
    out["fc_bin"]=G.groupby("fcb").apply(summ)
    Hh=pd.concat(hourrows).dropna()
    hz=Hh.groupby("hour")["r1"].agg(["count","mean","std"]); hz["t"]=hz["mean"]/(hz["std"]/np.sqrt(hz["count"]))
    out["hour_next_bar"]=hz
    wz=Hh.groupby("wd")["r1"].agg(["count","mean","std"]); wz["t"]=wz["mean"]/(wz["std"]/np.sqrt(wz["count"]))
    out["weekday_next_bar"]=wz
    D=pd.concat([d.assign(coin=c,w=w) for c,ws in data["days"].items() for w,d in ws.items()])
    out["book_by_coin"]=D.groupby("coin")[["book_return","coin_return"]].mean()*100
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    out["trades"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
