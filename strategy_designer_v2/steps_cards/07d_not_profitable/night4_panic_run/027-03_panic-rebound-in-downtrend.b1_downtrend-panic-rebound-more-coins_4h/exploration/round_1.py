import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H=[6,18,42,84]
    rows=[]
    drift={}
    for coin,wins in data["bars"].items():
        # coin mean h-return on non-overlapping grid over all windows
        for h in H:
            rs=[]
            for w,df in wins.items():
                c=df["close"].values
                idx=np.arange(0,len(c)-h,h)
                rs+=list(c[idx+h]/c[idx]-1)
            drift[(coin,h)]=np.mean(rs) if rs else np.nan
        for w,df in wins.items():
            c=df["close"].values; f=df["forecast"].fillna(0).values
            raw=df.get("debug_info.components.panic.last_history_value")
            raw=raw.values if raw is not None else np.full(len(c),np.nan)
            n=len(c)
            r180=pd.Series(c).pct_change(180).shift(6).values
            r540=pd.Series(c).pct_change(540).values
            r6=pd.Series(c).pct_change(6).values
            hi=df["high"].values; lo=df["low"].values
            rng=pd.Series(hi-lo).rolling(180).mean().values
            for cell in range(0,n,84):
                seg=np.where(f[cell:min(cell+84,n)]>=2)[0]
                if len(seg)==0: continue
                t=cell+seg[0]
                d={"coin":coin,"w":w,"year":df["timestamp"].iloc[t].year if hasattr(df["timestamp"].iloc[t],'year') else pd.Timestamp(df["timestamp"].iloc[t]).year,
                   "fc":f[t],"raw":raw[t],"r180":r180[t],"r540":r540[t],"r6":r6[t]}
                for h in H:
                    if t+h<n:
                        d[f"x{h}"]=c[t+h]/c[t]-1-drift[(coin,h)]
                        d[f"tot{h}"]=c[t+h]/c[t]-1
                rows.append(d)
    D=pd.DataFrame(rows)
    out={}
    def summ(g):
        res={}
        for h in H:
            x=g[f"x{h}"].dropna()
            res[f"m{h}"]=x.mean(); res[f"t{h}"]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        res["n"]=len(g); return pd.Series(res)
    out["all"]=summ(D)
    D["r180q"]=pd.qcut(D["r180"],4,labels=False)
    out["by_prior30d_quartile"]=D.groupby("r180q").apply(summ)
    D["r540s"]=np.sign(D["r540"])
    out["by_90d_sign"]=D.groupby("r540s").apply(summ)
    D["rawq"]=pd.qcut(D["raw"],3,labels=False,duplicates="drop")
    out["by_raw_tercile"]=D.groupby("rawq").apply(summ)
    D["r6q"]=pd.qcut(D["r6"],3,labels=False)
    out["by_24h_ret_tercile"]=D.groupby("r6q").apply(summ)
    out["by_year"]=D.groupby("year").apply(summ)
    out["corr_raw_x84"]=D[["raw","x84"]].corr().iloc[0,1]
    out["corr_r180_x84"]=D[["r180","x84"]].corr().iloc[0,1]
    # book: daily mean over coins, per window
    dd=[]
    for coin,wins in data["days"].items():
        for w,df in wins.items():
            t=df[["day","book_return","coin_return"]].copy(); t["w"]=w; dd.append(t)
    B=pd.concat(dd).dropna()
    G=B.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    G["wn"]=G["w"].str[1:].astype(int); G=G.sort_values(["wn","day"])
    eq=(1+G["book_return"]).cumprod(); dd_=eq/eq.cummax()-1
    out["book_maxdd"]=dd_.min()
    G["yr"]=pd.to_datetime(G["day"]).dt.year
    out["book_by_window"]=G.groupby("wn")[["book_return","coin_return"]].agg(["mean"]).round(5)
    return out
