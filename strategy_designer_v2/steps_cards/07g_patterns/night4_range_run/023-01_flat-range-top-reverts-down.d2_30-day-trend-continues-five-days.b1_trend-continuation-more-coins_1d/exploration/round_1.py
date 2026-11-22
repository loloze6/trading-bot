def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            d=df.reset_index(drop=True).copy()
            c=d["close"]; h=d["high"]; l=d["low"]
            d["ret30"]=c/c.shift(30)-1
            hh=h.rolling(30).max(); ll=l.rolling(30).min()
            d["nmr"]=(c-c.shift(30)).abs()/(hh-ll)
            d["rpos"]=(c-(hh+ll)/2)/(hh-ll)
            d["ret1"]=c/c.shift(1)-1
            d["ret5b"]=c/c.shift(5)-1
            d["vol20"]=d["ret1"].rolling(20).std()
            d["fwd5"]=c.shift(-5)/c-1
            d["wd"]=pd.to_datetime(d["timestamp"]).dt.dayofweek
            d["yr"]=pd.to_datetime(d["timestamp"]).dt.year
            g=d.iloc[::5].copy()
            g["coin"]=coin; g["win"]=w
            rows.append(g)
    G=pd.concat(rows,ignore_index=True)
    G=G.dropna(subset=["fwd5"])
    G["drift"]=G.groupby("coin")["fwd5"].transform("mean")
    G["un"]=G["fwd5"]-G["drift"]
    out={}
    def summ(gb,col="y"):
        r=gb[col].agg(["count","mean","std"])
        r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
        return r.round(4)
    T=G[(G.regime=="trending")&(G.forecast!=0)].copy()
    T["y"]=T["un"]*np.sign(T["forecast"])
    T["fq"]=pd.qcut(T["forecast"].abs(),5,labels=False,duplicates="drop")
    out["trend: dir unusual by |fc| quintile"]=summ(T.groupby("fq"))
    T["side"]=np.where(T.forecast>0,"long","short")
    out["trend: dir unusual by side"]=summ(T.groupby("side"))
    out["trend: dir unusual by year"]=summ(T.groupby("yr"))
    # non-trending: does range position predict reversion?
    N=G[(G.regime!="trending")].dropna(subset=["rpos","nmr"]).copy()
    N["y"]=N["un"]
    N["rq"]=pd.qcut(N["rpos"],5,labels=False,duplicates="drop")
    out["nontrend: unusual by range-pos quintile"]=summ(N.groupby("rq"))
    A=G.dropna(subset=["ret30","nmr"]).copy()
    A["nq"]=pd.qcut(A["nmr"],5,labels=False,duplicates="drop")
    A["y"]=A["un"]*np.sign(A["ret30"])
    out["all: dir(30d) unusual by nmr quintile"]=summ(A.groupby("nq"))
    # short-term moves
    B=G.dropna(subset=["ret5b","vol20"]).copy()
    B["z5"]=B["ret5b"]/(B["vol20"]*np.sqrt(5))
    B["zq"]=pd.qcut(B["z5"],5,labels=False,duplicates="drop")
    B["vq"]=B.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    B["y"]=B["un"]
    out["all: unusual by past-5d z quintile"]=summ(B.groupby("zq"))
    out["all: unusual by vol tercile (in-coin)"]=summ(B.groupby("vq"))
    B["y"]=B["un"]*np.sign(B["ret5b"])
    out["all: dir(5d) unusual by vol tercile x regime"]=summ(B.groupby(["vq","regime"]))
    # weekday on daily coin returns
    dd=[]
    for coin,wins in data["days"].items():
        for w,df in wins.items():
            x=df.copy(); x["coin"]=coin; dd.append(x)
    D=pd.concat(dd,ignore_index=True)
    D["wd"]=pd.to_datetime(D["day"]).dt.dayofweek
    D["y"]=D["coin_return"]
    out["daily coin ret by weekday"]=summ(D.dropna(subset=["y"]).groupby("wd"))
    D["y"]=D["book_return"]
    out["daily book ret by weekday"]=summ(D.dropna(subset=["y"]).groupby("wd"))
    # trades
    tr=[]
    for coin,wins in data["trades"].items():
        for w,df in wins.items():
            if len(df): x=df.copy(); x["coin"]=coin; tr.append(x)
    TR=pd.concat(tr,ignore_index=True)
    TR["y"]=TR["net_profit_loss_percent"]
    TR["dq"]=pd.qcut(TR["duration_minutes"],4,labels=False,duplicates="drop")
    out["trades by side"]=summ(TR.groupby("side"))
    out["trades by duration quartile"]=summ(TR.groupby("dq"))
    out["trade dur days by quartile"]=(TR.groupby("dq")["duration_minutes"].median()/1440).round(1)
    return out
