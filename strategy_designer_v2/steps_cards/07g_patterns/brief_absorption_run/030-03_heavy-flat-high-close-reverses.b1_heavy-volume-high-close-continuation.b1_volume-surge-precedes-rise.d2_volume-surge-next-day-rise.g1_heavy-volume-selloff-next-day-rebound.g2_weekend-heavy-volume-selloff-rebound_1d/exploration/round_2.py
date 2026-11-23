def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].reset_index(drop=True); allr.append((c.shift(-1)/c-1).dropna())
        cm=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r0=c/c.shift(1)-1
            d=pd.DataFrame(index=b.index)
            d["coin"]=coin; d["w"]=w
            d["r1"]=c.shift(-1)/c-1-cm
            d["r3"]=c.shift(-3)/c-1-3*cm
            d["pos"]=np.arange(len(b))
            d["r0"]=r0
            v20=r0.rolling(20).std()
            d["z"]=r0/v20
            d["v20"]=v20
            d["vr"]=b["volume"]/b["volume"].shift(1).rolling(20).mean()
            rg=(b["high"]-b["low"]).replace(0,np.nan)
            d["clv"]=(2*c-b["high"]-b["low"])/rg
            d["rng"]=rg/c/v20
            d["r5"]=c/c.shift(5)-1
            d["z5"]=d["r5"]/(v20*np.sqrt(5))
            d["r20"]=c/c.shift(20)-1
            d["z20"]=d["r20"]/(v20*np.sqrt(20))
            ts=pd.to_datetime(b["timestamp"])
            d["wd"]=ts.dt.weekday.values
            d["alloc"]=b["postRebalance_current_allocation"].values
            d["fc"]=b["forecast"].values
            d["yr"]=ts.dt.year.values
            d["gain"]=d["alloc"]*(c.shift(-1)/c-1)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def g(df,col,key="r1"):
        x=df.dropna(subset=[col,key]).groupby(col,observed=True)[key]
        o=x.agg(["mean","count","std"]); o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
        o["mean"]*=100; return o[["mean","t","count"]].round(3)
    def g2(df,a,b_,key="r1"):
        return df.dropna(subset=[a,b_,key]).groupby([a,b_],observed=True)[key].agg(lambda s:f"{100*s.mean():.3f}|t{s.mean()/(s.std()/np.sqrt(len(s))):.2f}|n{len(s)}").unstack()
    out={}
    def safe(name,f):
        try: out[name]=f()
        except Exception as e: out[name]="ERR "+str(e)[:80]
    safe("by_weekday",lambda:g(D,"wd"))
    D["zb"]=pd.cut(D["z"],[-99,-2,-1,-0.3,0.3,1,2,99])
    safe("by_z_day",lambda:g(D,"zb"))
    D["we"]=D["wd"].isin([5,6])
    safe("z_x_weekend",lambda:g2(D,"zb","we"))
    D["vrb"]=pd.qcut(D["vr"],3,labels=["lowV","midV","highV"])
    D["clvb"]=pd.cut(D["clv"],[-1.01,-0.6,-0.2,0.2,0.6,1.01])
    safe("clv_x_vol",lambda:g2(D,"clvb","vrb"))
    safe("z_x_vol",lambda:g2(D,"zb","vrb"))
    D["rngb"]=pd.qcut(D["rng"],5)
    safe("by_range_norm",lambda:g(D,"rngb"))
    D["z5b"]=pd.cut(D["z5"],[-99,-2,-1,-0.3,0.3,1,2,99])
    safe("by_z5",lambda:g(D,"z5b"))
    D["z20b"]=pd.cut(D["z20"],[-99,-2,-1,-0.3,0.3,1,2,99])
    safe("by_z20",lambda:g(D,"z20b"))
    D["v20b"]=D.groupby("coin")["v20"].transform(lambda s:pd.qcut(s,3,labels=False,duplicates="drop"))
    safe("by_vol_tercile",lambda:g(D,"v20b"))
    safe("z_x_voltercile",lambda:g2(D,"zb","v20b"))
    N3=D[D["pos"]%3==0]
    safe("r3_by_z",lambda:g(N3,"zb","r3"))
    safe("r3_by_z5",lambda:g(N3,"z5b","r3"))
    safe("by_coin_down_day",lambda:g2(D[D["z"]<-1],"coin","we"))
    safe("by_year_bigdown",lambda:g(D[D["z"]<-1],"yr"))
    D["fcb"]=pd.cut(D["fc"],[-0.01,0.01,5,10,15,20.1])
    safe("r1_by_forecast",lambda:g(D,"fcb"))
    safe("gain_by_weekday",lambda:g(D,"wd","gain"))
    br=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd=d.copy(); dd["wd"]=pd.to_datetime(dd["day"]).dt.weekday.values; dd["w"]=w; dd["coin"]=coin; br.append(dd)
    B=pd.concat(br,ignore_index=True)
    safe("book_by_weekday",lambda:g(B.rename(columns={"book_return":"r1"}),"wd"))
    safe("coin_by_weekday",lambda:g(B.rename(columns={"coin_return":"r1"}),"wd"))
    return out
