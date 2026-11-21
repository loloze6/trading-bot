def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows96=[]; rows24=[]
    for coin, wins in data["bars"].items():
        g96=[]; g24=[]
        for w, b in wins.items():
            c=b["close"].astype(float).reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r24=c/c.shift(24)-1
            scale=r24.abs().rolling(720,min_periods=360).mean()
            z=r24/scale
            r720=c/c.shift(720)-1
            r168=c/c.shift(168)-1
            hv=np.log(c).diff().rolling(720,min_periods=360).std()
            f96=c.shift(-96)/c-1
            f24=c.shift(-24)/c-1
            d=pd.DataFrame({"z":z,"r720":r720,"r168":r168,"hv":hv,"f96":f96,"f24":f24,
                            "hour":ts.dt.hour,"wd":ts.dt.weekday,"year":ts.dt.year})
            g96.append(d.iloc[::96].assign(win=w))
            g24.append(d.iloc[::24].assign(win=w))
        a=pd.concat(g96); a=a.dropna(subset=["f96"])
        a["u"]=(a.f96-a.f96.mean())/a.f96.std(); a["coin"]=coin
        a["hvq"]=pd.qcut(a.hv.rank(method="first"),3,labels=["lowvol","midvol","highvol"])
        rows96.append(a)
        e=pd.concat(g24); e=e.dropna(subset=["f24"])
        e["u"]=(e.f24-e.f24.mean())/e.f24.std(); e["coin"]=coin
        rows24.append(e)
    A=pd.concat(rows96); E=pd.concat(rows24)
    def summ(df,keys,col="u"):
        g=df.groupby(keys,observed=True)[col]
        out=g.agg(["mean","count","std"])
        out["t"]=out["mean"]/(out["std"]/np.sqrt(out["count"]))
        return out.drop(columns="std").round(3)
    A["zb"]=pd.cut(A.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    A["reg"]=np.where(A.r720<0,"down30","up30")
    E["zb"]=pd.cut(E.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    E["reg"]=np.where(E.r720<0,"down30","up30")
    A["r168b"]=pd.cut(A.r168.groupby(A.coin).rank(pct=True),[0,.1,.3,.7,.9,1])
    A["r720b"]=pd.cut(A.r720.groupby(A.coin).rank(pct=True),[0,.1,.3,.7,.9,1])
    res={}
    res["96h_by_z_regime"]=summ(A.dropna(subset=["z","r720"]),["reg","zb"])
    res["24h_by_z_regime"]=summ(E.dropna(subset=["z","r720"]),["reg","zb"])
    res["96h_by_7d_ret_pct"]=summ(A.dropna(subset=["r168"]),["r168b"])
    res["96h_by_30d_ret_pct"]=summ(A.dropna(subset=["r720"]),["r720b"])
    res["96h_by_vol"]=summ(A.dropna(subset=["hv"]),["hvq"])
    res["24h_by_weekday"]=summ(E,["wd"])
    res["96h_by_coin_regime"]=summ(A.dropna(subset=["r720"]),["coin","reg"])
    res["96h_by_year"]=summ(A,["year"])
    # trades
    T=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    T=pd.concat(T)
    T["hrs"]=T.duration_minutes/60
    res["trades_by_coin"]=T.groupby("coin").agg(n=("net_profit_loss_percent","size"),
        mean_net=("net_profit_loss_percent","mean"),mean_gross=("profit_loss_percent","mean"),
        hit=("net_profit_loss_percent",lambda x:(x>0).mean()),hrs=("hrs","median")).round(3)
    T["fb"]=pd.qcut(T.entry_forecast.rank(method="first"),4,labels=["q1deep","q2","q3","q4shallow"])
    res["trades_by_entry_forecast"]=T.groupby("fb").agg(n=("net_profit_loss_percent","size"),
        mean_gross=("profit_loss_percent","mean"),med=("profit_loss_percent","median")).round(3)
    return res
