def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        gr=[]
        for w,b in ws.items():
            c=b["close"].values
            gr+=list(c[48::48]/c[:-48:48][:len(c[48::48])]-1)
        drift[coin]=np.nanmean(gr)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].values; v=b["volume"].values; n=len(b)
            wd=ts.dt.weekday.values; hr=ts.dt.hour.values
            for t in np.where((wd==6)&(hr==23))[0]:
                if t-720<0 or t+48>=n: continue
                vwe=v[t-47:t+1].mean(); vwd=v[t-167:t-47].mean()
                lr=np.diff(np.log(c[t-720:t+1]))
                rows.append(dict(coin=coin,rwe=c[t]/c[t-48]-1,ratio=vwd/vwe if vwe>0 else np.nan,
                    f48=c[t+48]/c[t]-1,fc=b["forecast"].values[t],vol=np.std(lr),
                    alloc=b["postRebalance_current_allocation"].values[t]))
    d=pd.DataFrame(rows)
    d["drift"]=d["coin"].map(drift)
    g=d.groupby("coin")
    d["z"]=d["rwe"]/g["rwe"].transform("std")
    d["s"]=-d["z"]*d["ratio"]
    d["un"]=np.sign(d["s"])*(d["f48"]-d["drift"])
    d["tot"]=np.sign(d["s"])*d["f48"]
    d["unfc"]=np.sign(d["fc"])*(d["f48"]-d["drift"])
    d["vq"]=g["vol"].transform(lambda x:pd.qcut(x,3,labels=["lowvol","midvol","highvol"]))
    d["sq"]=pd.qcut(d["s"].abs(),4,labels=False)
    d["fq"]=pd.qcut(d["fc"].abs().rank(method="first"),4,labels=False)
    out={}
    out["fc_sign_agrees_minus_z_by_fcq"]=d.groupby("fq").apply(lambda q:(np.sign(q.fc)==np.sign(-q.z)).mean())
    def agg(q):
        return pd.Series({"un_bp":q.un.mean()*1e4,"t":q.un.mean()/(q.un.std()/np.sqrt(len(q))),"tot_bp":q.tot.mean()*1e4,"n":len(q)})
    out["raw_signal_by_abs_s_quartile"]=d.groupby("sq").apply(agg)
    out["raw_signal_by_vol"]=d.groupby("vq").apply(agg)
    out["raw_top_half_s_by_vol"]=d[d.sq>=2].groupby("vq").apply(agg)
    out["fc_signal_by_vol"]=d.groupby("vq").apply(lambda q:pd.Series({"un_bp":q.unfc.mean()*1e4,"n":len(q)}))
    out["mean_usual_move_by_vol"]=d.groupby("vq")["f48"].std()
    return out
