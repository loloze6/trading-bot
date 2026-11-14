def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c)
            r1=np.r_[np.nan, c[1:]/c[:-1]-1]
            vol20=pd.Series(r1).rolling(20).std().values
            dcol="debug_info.components.depth.last_history_value"
            depth=b[dcol].values if dcol in b else np.full(n,np.nan)
            ts=pd.to_datetime(b["timestamp"])
            for i in range(n):
                f1=c[i+1]/c[i]-1 if i+1<n else np.nan
                f5=c[i+5]/c[i]-1 if i+5<n else np.nan
                f10=c[i+10]/c[i]-1 if i+10<n else np.nan
                ret5=c[i]/c[i-5]-1 if i>=5 else np.nan
                rows.append((coin,w,i,r1[i],ret5,vol20[i],depth[i],b["forecast"].iloc[i],b["regime"].iloc[i],ts.iloc[i].weekday(),ts.iloc[i].year,f1,f5,f10))
    d=pd.DataFrame(rows,columns="coin w i r1 ret5 vol fdepth fc regime wd yr f1 f5 f10".split())
    d["z1"]=d["r1"]/d["vol"]
    out={}
    def summ(g,col):
        return g[col].agg(["count","mean",lambda x: x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan]).rename(columns={"<lambda_0>":"t"})
    nb10=d[d.i%10==0].copy()
    nb10["coin_mean"]=nb10.groupby("coin")["f10"].transform("mean")
    nb10["x10"]=nb10["f10"]-nb10["coin_mean"]
    nb10["fcb"]=pd.cut(nb10.fc,[-1,0.0001,5,10,21],right=False)
    out["fc_bucket_x10"]=summ(nb10.groupby(["regime","fcb"],observed=True),"x10")
    nb10["dq"]=pd.qcut(nb10.fdepth,5)
    out["depth_q_x10_inregime"]=summ(nb10.groupby("dq",observed=True),"x10")
    # after large daily moves: next-day returns (each day once)
    d["zb"]=pd.cut(d.z1,[-99,-2,-1,1,2,99])
    out["z1_next1"]=summ(d.groupby("zb",observed=True),"f1")
    nb5=d[d.i%5==0].copy()
    nb5["rb"]=pd.qcut(nb5.ret5,5)
    out["ret5_q_next5"]=summ(nb5.groupby("rb",observed=True),"f5")
    nb10["vq"]=pd.qcut(nb10.vol,4)
    out["vol_q_x10"]=summ(nb10.groupby("vq",observed=True),"x10")
    out["wd_next1"]=summ(d.groupby("wd"),"f1")
    out["coin_x10"]=summ(nb10.groupby("coin"),"x10")
    out["yr_x10_fc10"]=summ(nb10[nb10.fc>=10].groupby("yr"),"x10")
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): t=t.copy(); t["coin"]=coin; tr.append(t)
    T=pd.concat(tr)
    T["days"]=T.duration_minutes/1440
    T["db"]=pd.cut(T.days,[0,2,5,10,30,1000])
    out["trades_by_dur"]=T.groupby("db",observed=True)["net_profit_loss_percent"].agg(["count","mean","median"])
    T["efb"]=pd.cut(T.entry_forecast,[0,1,5,10,21])
    out["trades_by_entryfc"]=T.groupby("efb",observed=True)["net_profit_loss_percent"].agg(["count","mean","median"])
    out["regime_share"]=d.regime.value_counts(normalize=True)
    return out
