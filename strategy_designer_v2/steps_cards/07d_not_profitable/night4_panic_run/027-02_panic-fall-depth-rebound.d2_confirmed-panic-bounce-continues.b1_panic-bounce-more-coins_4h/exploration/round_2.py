import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=84; rows=[]; drift={}
    for coin,ws in data["bars"].items():
        g=[]
        for w,b in ws.items():
            c=b["close"].values
            if len(c)>H: g+=list(c[H::H]/c[:-H:H]-1)
        drift[coin]=np.nanmean(g) if g else np.nan
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            h=b["high"];l=b["low"];c=b["close"]
            r6=h.rolling(6).max()-l.rolling(6).min()
            base=r6.rolling(180,min_periods=30).mean()
            mult=(r6/base).shift(6)
            fall=c.shift(6)/c.shift(12)-1
            bounce=c/c.shift(6)-1
            prior=c.shift(12)/c.shift(186)-1
            f84=c.shift(-H)/c-1
            panic=(mult>=3)&(fall<0)
            d=pd.DataFrame({"panic":panic,"mult":mult,"bounce":bounce,"prior":prior,"f84":f84,
                            "cell":np.arange(len(c))//H,"fc":b["forecast"]})
            d=d[d.panic].groupby("cell").head(1); d["coin"]=coin; d["w"]=w; rows.append(d)
    D=pd.concat(rows); D["ex"]=D.f84-D.coin.map(drift); D=D.dropna(subset=["ex"])
    out={}
    D["absprior"]=D.prior.abs()
    Dp=D.dropna(subset=["prior"])
    s=stats.linregress(Dp.absprior,Dp.ex); out["slope_ex_on_absprior"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(Dp)})
    s=stats.linregress(Dp.prior,Dp.ex); out["slope_ex_on_prior"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(Dp)})
    Dp=Dp.copy(); Dp["apq"]=pd.qcut(Dp.absprior,4,labels=False)
    out["by_absprior_q"]=Dp.groupby("apq").agg(n=("ex","size"),ex=("ex","mean"),tot=("f84","mean"),fcpos=("fc",lambda x:(x>0).mean()))
    Dp["mq"]=pd.qcut(Dp["mult"],2,labels=False); Dp["pq"]=pd.qcut(Dp.prior,3,labels=False)
    out["mult_x_prior_ex"]=Dp.pivot_table(index="pq",columns="mq",values="ex",aggfunc="mean")
    out["mult_x_prior_n"]=Dp.pivot_table(index="pq",columns="mq",values="ex",aggfunc="size")
    s=stats.linregress(D["mult"],D.ex); out["slope_ex_on_mult"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(D)})
    # trades
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; T.append(t)
    T=pd.concat(T)
    out["trades"]=pd.Series({"n":len(T),"mean_gross":T.profit_loss_percent.mean(),"mean_net":T.net_profit_loss_percent.mean(),
        "win":(T.net_profit_loss_percent>0).mean(),"median_net":T.net_profit_loss_percent.median(),
        "days_mean":T.duration_minutes.mean()/1440,"t_net":T.net_profit_loss_percent.mean()/(T.net_profit_loss_percent.std()/np.sqrt(len(T)))})
    T["fq"]=pd.qcut(T.entry_forecast.rank(method="first"),4,labels=False)
    out["trades_by_entry_fc_q"]=T.groupby("fq").agg(n=("net_profit_loss_percent","size"),net=("net_profit_loss_percent","mean"),fc=("entry_forecast","mean"))
    # book drawdowns: per-day mean over coins within each window; chain
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x[["day","book_return","coin_return"]].copy(); x["w"]=w; dd.append(x)
    X=pd.concat(dd)
    Bk=X.groupby(["w","day"]).agg(book=("book_return","mean"),coin=("coin_return","mean")).dropna().reset_index()
    Bk["wn"]=Bk.w.str[1:].astype(int); Bk=Bk.sort_values(["wn","day"])
    v=(1+Bk.book).cumprod(); dw=v/v.cummax()-1
    out["book_maxdd"]=dw.min()
    Bk["dd"]=dw.values
    out["by_window"]=Bk.groupby("wn").agg(book=("book","mean"),coin=("coin","mean"),mindd=("dd","min"),days=("book","size"))
    return out
