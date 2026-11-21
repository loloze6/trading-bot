def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol=r1.rolling(24).std()
            vm=vol.rolling(720,min_periods=100).mean()
            r2=c/c.shift(2)-1
            hr=pd.to_datetime(b["timestamp"]).dt.hour
            sett=((hr+1)%24).isin([0,8,16])
            f=b["forecast"].astype(float)
            out={}
            for h in [2,4,8,16,24,48]:
                out[h]=c.shift(-h)/c-1
            idx=np.where(sett & (f!=0))[0]
            for i in idx:
                d={"coin":coin,"w":w,"f":f.iloc[i],"r2":r2.iloc[i],"z":r2.iloc[i]/vm.iloc[i] if vm.iloc[i]>0 else np.nan,
                   "vr":vol.iloc[i]/vm.iloc[i] if vm.iloc[i]>0 else np.nan,"vol":vol.iloc[i]}
                for h in out: d[f"m{h}"]=out[h].iloc[i]
                rows.append(d)
    df=pd.DataFrame(rows)
    s=np.sign(df["f"])
    for h in [2,4,8,16,24,48]:
        df[f"s{h}"]=s*df[f"m{h}"]*1e4
    res={}
    cols=[f"s{h}" for h in [2,4,8,16,24,48]]
    res["by_horizon_all"]=df[cols].agg(["mean","count"]).T.assign(t=lambda x: df[cols].mean()/df[cols].std()*np.sqrt(df[cols].count()))
    df["fdec"]=pd.qcut(df["f"].abs().rank(method="first"),10,labels=False)
    res["by_absf_decile_bps"]=df.groupby("fdec")[cols].mean().assign(n=df.groupby("fdec").size(), absz=df.groupby("fdec")["z"].apply(lambda x:x.abs().mean()))
    df["vrq"]=pd.qcut(df["vr"].rank(method="first"),5,labels=False)
    res["by_volratio_quint_bps"]=df.groupby("vrq")[["s8","s16","s24"]].mean().assign(vr=df.groupby("vrq")["vr"].mean())
    df["absr2"]=df["r2"].abs()*1e4
    res["by_coin_bps"]=df.groupby("coin")[["s8","s16","s24","absr2"]].mean().assign(n=df.groupby("coin").size())
    # pre-move size in bps deciles
    df["r2dec"]=pd.qcut(df["absr2"].rank(method="first"),10,labels=False)
    res["by_abs_pre_move_decile"]=df.groupby("r2dec")[["absr2","s8","s16","s24"]].mean()
    # trades
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): tt=t.copy(); tt["coin"]=coin; tr.append(tt)
    T=pd.concat(tr)
    res["trades_by_coin"]=T.groupby("coin").agg(n=("side","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur_h=("duration_minutes",lambda x:x.mean()/60))
    return res
