import pandas as pd, numpy as np

def explore(data):
    H=[6,12,18,42,84]
    rows=[]; drift={}; usual={}
    for coin,wins in data["bars"].items():
        for h in H:
            rs=[]
            for w,df in wins.items():
                c=df["close"].values
                idx=np.arange(0,len(c)-h,h)
                rs+=list(c[idx+h]/c[idx]-1)
            drift[(coin,h)]=np.mean(rs); usual[(coin,h)]=np.std(rs)
        for w,df in wins.items():
            c=df["close"].values; f=df["forecast"].fillna(0).values
            raw=df["debug_info.components.panic.last_history_value"].values if "debug_info.components.panic.last_history_value" in df else np.full(len(c),np.nan)
            n=len(c); s=pd.Series(c)
            r360=s.pct_change(360).values
            r42p=s.pct_change(42).values
            lo=df["low"].values
            alloc=df["postRebalance_current_allocation"].values
            for cell in range(0,n,84):
                seg=np.where(f[cell:min(cell+84,n)]>=2)[0]
                if len(seg)==0: continue
                t=cell+seg[0]
                d={"coin":coin,"raw":raw[t],"r360":r360[t],"r42p":r42p[t],"alloc":alloc[t]}
                for h in H:
                    if t+h<n:
                        d[f"x{h}"]=c[t+h]/c[t]-1-drift[(coin,h)]
                        d[f"tot{h}"]=c[t+h]/c[t]-1
                        d[f"s{h}"]=d[f"x{h}"]/usual[(coin,h)]
                rows.append(d)
    D=pd.DataFrame(rows)
    def summ(g):
        r={}
        for h in H:
            x=g[f"x{h}"].dropna()
            r[f"x{h}"]=x.mean(); r[f"t{h}"]=x.mean()/(x.std()/np.sqrt(len(x)))
            r[f"tot{h}"]=g[f"tot{h}"].mean()
        r["s6"]=g["s6"].mean(); r["n"]=len(g); return pd.Series(r)
    out={}
    D["r360s"]=np.sign(D["r360"])
    out["by_60d_sign"]=D.groupby("r360s").apply(summ).round(4)
    D["r42q"]=pd.qcut(D["r42p"],3,labels=False)
    out["by_7d_ret_tercile"]=D.groupby("r42q").apply(summ).round(4)
    neg=D[D["r360"]<0].copy()
    neg["rawq"]=pd.qcut(neg["raw"],3,labels=False,duplicates="drop")
    out["60dneg_by_raw_tercile"]=neg.groupby("rawq").apply(summ).round(4)
    D["rawq"]=pd.qcut(D["raw"],3,labels=False,duplicates="drop")
    out["all_raw_tercile_strength"]=D.groupby("rawq").apply(summ)[["x6","t6","s6","tot6","n"]].round(4)
    # trades
    tr=[]
    for coin,wins in data["trades"].items():
        for w,df in wins.items():
            tr.append(df[["duration_minutes","profit_loss_percent","net_profit_loss_percent"]])
    T=pd.concat(tr)
    out["trades"]=pd.Series({"n":len(T),"mean_dur_days":T.duration_minutes.mean()/1440,
        "mean_pl":T.profit_loss_percent.mean(),"mean_net":T.net_profit_loss_percent.mean(),
        "win":(T.profit_loss_percent>0).mean()})
    # book: deep falls
    dd=[]
    for coin,wins in data["days"].items():
        for w,df in wins.items():
            t=df[["day","book_return","coin_return"]].copy(); t["w"]=w; dd.append(t)
    B=pd.concat(dd).dropna()
    G=B.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    G["wn"]=G["w"].str[1:].astype(int); G=G.sort_values(["wn","day"]).reset_index(drop=True)
    eq=(1+G.book_return).cumprod(); G["dd"]=eq/eq.cummax()-1
    G["mkt20"]=G.groupby("wn")["coin_return"].transform(lambda x:(1+x).rolling(20).apply(np.prod,raw=True)-1)
    out["book_dd_by_window"]=G.groupby("wn").agg(mindd=("dd","min"),mkt=("coin_return","mean"),book=("book_return","mean")).round(4)
    G["mkt_state"]=pd.qcut(G["mkt20"],4,labels=False)
    out["book_by_mkt20_quartile"]=G.groupby("mkt_state")[["book_return","coin_return"]].mean().round(5)
    return out
