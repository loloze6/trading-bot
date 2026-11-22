import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=18
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r=c.pct_change()
            am=r.abs().rolling(180,min_periods=45).mean()
            sd18=r.rolling(180,min_periods=45).std()*np.sqrt(H)
            # streaks
            dn=(r<0).values; up=(r>0).values
            n=len(c); dstart=np.full(n,np.nan); ustart=np.full(n,np.nan)
            dlen=np.zeros(n); ulen=np.zeros(n)
            for i in range(1,n):
                if dn[i]:
                    dlen[i]=dlen[i-1]+1; dstart[i]=dstart[i-1] if dlen[i-1]>0 else c.iloc[i-1]
                if up[i]:
                    ulen[i]=ulen[i-1]+1; ustart[i]=ustart[i-1] if ulen[i-1]>0 else c.iloc[i-1]
            dd=np.where(dlen>0,(1-c.values/dstart)/am.values,0)
            ud=np.where(ulen>0,(c.values/ustart-1)/am.values,0)
            past18=(c/c.shift(H)-1)/sd18
            past6=(c/c.shift(6)-1)/(am*np.sqrt(6))
            volr=v.rolling(3).mean()/v.shift(3).rolling(18).mean()
            vlev=r.rolling(30).std()/r.rolling(180,min_periods=45).std()
            fwd=c.shift(-H)/c-1
            ts=pd.to_datetime(b["timestamp"])
            idx=np.arange(0,n,H)
            d=pd.DataFrame({"coin":coin,"w":w,"fwd":fwd.values[idx],"dd":dd[idx],"ud":ud[idx],
                "dlen":dlen[idx],"ulen":ulen[idx],"past18":past18.values[idx],"past6":past6.values[idx],
                "volr":volr.values[idx],"vlev":vlev.values[idx],"sd18":sd18.values[idx],
                "fc":b["forecast"].values[idx],"hour":ts.dt.hour.values[idx],"wd":ts.dt.weekday.values[idx],
                "year":ts.dt.year.values[idx]})
            rows.append(d)
    g=pd.concat(rows).dropna(subset=["fwd"])
    g["drift"]=g.groupby("coin")["fwd"].transform("mean")
    g["u"]=g["fwd"]-g["drift"]
    g["us"]=g["u"]/g["sd18"]
    def tab(key,q=None):
        x=g.dropna(subset=[key]).copy()
        k=pd.qcut(x[key].rank(method="first"),q,labels=False) if q else x[key]
        o=x.groupby(k)["u"].agg(["mean","count","std"])
        o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
        o["key_mean"]=x.groupby(k)[key].mean()
        return o.drop(columns="std").round(5)
    out={}
    out["n_cases"]=len(g)
    out["by_past18_quint"]=tab("past18",5)
    out["by_past6_quint"]=tab("past6",5)
    out["by_vollevel_quint"]=tab("vlev",5)
    out["by_volume_ratio_quint"]=tab("volr",5)
    out["by_dlen"]=tab("dlen").head(10)
    out["by_ulen"]=tab("ulen").head(10)
    out["by_hour"]=tab("hour")
    out["by_weekday"]=tab("wd")
    out["by_year"]=tab("year")
    # deep down streak, split by volume fade
    deep=g[g["dd"]>np.nanpercentile(g.loc[g.dd>0,"dd"],75)]
    s=deep.groupby(deep["volr"]<1)["u"].agg(["mean","count"])
    out["deep_down_by_volfade"]=s
    deepu=g[g["ud"]>np.nanpercentile(g.loc[g.ud>0,"ud"],75)]
    out["deep_up_by_volfade"]=deepu.groupby(deepu["volr"]<1)["u"].agg(["mean","count"])
    # interaction: past18 quintile x vol level high/low
    x=g.dropna(subset=["past18","vlev"]).copy()
    x["pq"]=pd.qcut(x["past18"].rank(method="first"),5,labels=False)
    x["vh"]=x["vlev"]>x["vlev"].median()
    out["past18_x_volhigh"]=x.pivot_table(index="pq",columns="vh",values="u",aggfunc="mean").round(5)
    # book days
    dl=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            dd_=d.copy(); dd_["coin"]=coin; dd_["w"]=w; dl.append(dd_)
    D=pd.concat(dl).dropna(subset=["book_return"])
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    out["book_by_weekday"]=D.groupby("wd")[["book_return","coin_return"]].mean().round(5)
    out["book_by_coin"]=D.groupby("coin")[["book_return","coin_return"]].agg(["mean"]).round(5)
    q=D["book_return"].quantile([0.01,0.99])
    out["coin_ret_on_book_extremes"]=pd.DataFrame({"low1pct":D.loc[D.book_return<=q.iloc[0],["book_return","coin_return"]].mean(),
        "high1pct":D.loc[D.book_return>=q.iloc[1],["book_return","coin_return"]].mean()})
    return out
