import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c)
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,n-7,7):
                rows.append(dict(coin=coin,w=w,day=str(ts.iloc[i])[:10],yr=ts.iloc[i].year,
                    chop=b["regime"].iloc[i]=="unknown",fwd=c[i+7]/c[i]-1,
                    r30=c[i]/c[i-30]-1 if i>=30 else np.nan,
                    r14=c[i]/c[i-14]-1 if i>=14 else np.nan,
                    r1=c[i]/c[i-1]-1 if i>=1 else np.nan,
                    r60=c[i]/c[i-60]-1 if i>=60 else np.nan,
                    fc=b["forecast"].iloc[i]))
    d=pd.DataFrame(rows)
    d["sd"]=d.groupby("coin")["fwd"].transform("std")
    d["un"]=(d["fwd"]-d.groupby("coin")["fwd"].transform("mean"))/d["sd"]
    def slope(g,v):
        g=g.dropna(subset=[v,"un"])
        if len(g)<20: return pd.Series(dict(n=len(g),days=0,beta=np.nan,t=np.nan))
        x=g[v]/g.groupby("coin")[v].transform("std"); x=x-x.mean(); y=g["un"]-g["un"].mean()
        b=(x*y).sum()/(x*x).sum(); e=y-b*x
        u=(x*e).groupby(g["day"]).sum(); G=len(u)
        se=np.sqrt(G/(G-1)*(u**2).sum())/(x*x).sum()
        return pd.Series(dict(n=len(g),days=G,beta=b,t=b/se))
    out={}
    res=[]
    for v in ["r1","r14","r30","r60"]:
        for ch in [True,False]:
            s=slope(d[d.chop==ch],v); s["var"]=v; s["chop"]=ch; res.append(s)
    out["slopes (std units)"]=pd.DataFrame(res)
    # chop r30 slope separately for up and down months, and by year
    c=d[d.chop]
    out["chop r30 slope by sign"]=pd.DataFrame([slope(c[c.r30<0],"r30"),slope(c[c.r30>=0],"r30")],index=["fall","rise"])
    out["chop r30 slope by year"]=c.groupby("yr").apply(lambda g:slope(g,"r30"))
    out["chop r30 slope by window"]=c.groupby("w").apply(lambda g:slope(g,"r30"))
    # book
    br=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; br.append(x)
    B=pd.concat(br).dropna(subset=["book_return"])
    B["yr"]=pd.to_datetime(B["day"]).dt.year
    dB=B.groupby(["w","day"])["book_return"].mean()
    out["book by window"]=dB.groupby(level=0).agg(["count","mean","std","sum"])
    q=B["book_return"]
    top=B[q>q.quantile(0.995)]; bot=B[q<q.quantile(0.005)]
    out["extremes coin_return"]=pd.DataFrame({"top_book":[len(top),top.book_return.mean(),top.coin_return.mean()],
        "bottom_book":[len(bot),bot.book_return.mean(),bot.coin_return.mean()]},index=["n","book","coin"])
    T=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): t=t.copy(); t["coin"]=coin; T.append(t)
    T=pd.concat(T)
    T["dur_d"]=T["duration_minutes"]/1440
    T["db"]=pd.cut(T["dur_d"],[0,7,8,14,30,1000])
    out["trades by duration"]=T.groupby("db")["profit_loss_percent"].agg(["count","mean","median"])
    out["trades by coin"]=T.groupby("coin")["profit_loss_percent"].agg(["count","mean"])
    return out
