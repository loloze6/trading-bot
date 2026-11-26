def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # ---- book daily returns
    recs = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"]=c; dd["w"]=w
            recs.append(dd)
    D = pd.concat(recs)
    D["wn"]=D["w"].str[1:].astype(int)
    bk = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().reset_index().sort_values(["wn","day"])
    bk = bk.dropna(subset=["book_return"])
    v = (1+bk["book_return"]).cumprod()
    dd_ = v/v.cummax()-1
    bk["dd"]=dd_.values
    bk["year"]=pd.to_datetime(bk["day"]).dt.year
    out["book_by_year"]=bk.groupby("year").agg(mean=("book_return","mean"),sd=("book_return","std"),n=("book_return","size"),min_dd=("dd","min"),coin=("coin_return","mean"))
    out["book_by_window"]=bk.groupby("wn").agg(sum=("book_return","sum"),min_dd=("dd","min"))
    out["max_dd"]=float(dd_.min())
    # worst days
    bk["rank"]=bk["book_return"].rank()
    # per coin contribution to book by year
    D["year"]=pd.to_datetime(D["day"]).dt.year
    out["coin_year_bookret_sum"]=D.pivot_table(index="year",columns="coin",values="book_return",aggfunc="sum")
    # ---- cases
    rows=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"])
            cl=b["close"].values
            r=pd.Series(cl).pct_change()
            vol=r.rolling(20).std()
            vr=vol/vol.rolling(60).mean()
            ret14=pd.Series(cl)/pd.Series(cl).shift(14)-1
            for i in range(len(b)-2):
                if ts[i].dayofweek==4:
                    f=b["forecast"].iloc[i]; a=b["postRebalance_current_allocation"].iloc[i]
                    rows.append(dict(coin=c,w=w,year=ts[i].year,f=f,a=a,ret2=cl[i+2]/cl[i]-1,
                                     vr=vr.iloc[i],r14=ret14.iloc[i],vol=vol.iloc[i],
                                     prior1=cl[i]/cl[i-1]-1 if i>0 else np.nan,
                                     reg=b["regime"].iloc[i]))
    C=pd.DataFrame(rows)
    mu=C.groupby("coin")["ret2"].mean()
    C["ex"]=C["ret2"]-C["coin"].map(mu)
    act=C[C["f"]!=0].copy()
    act["side"]=np.sign(act["f"])
    act["g"]=act["side"]*act["ret2"]
    act["gex"]=act["side"]*act["ex"]
    act["pnl"]=act["a"]*act["ret2"]
    def agg(g):
        return pd.Series(dict(n=len(g),g=g["g"].mean(),t=g["g"].mean()/g["g"].std()*np.sqrt(len(g)),pnl=g["pnl"].mean(),absa=g["a"].abs().mean(),worst=g["pnl"].min()))
    out["by_side"]=act.groupby("side").apply(agg)
    act["absf_q"]=pd.qcut(act["f"].abs(),4,labels=False)
    out["by_absf"]=act.groupby("absf_q").apply(agg)
    act["vr_q"]=pd.qcut(act["vr"],4,labels=False)
    out["by_vr"]=act.groupby("vr_q").apply(agg)
    out["vr_q_edges"]=act.groupby("vr_q")["vr"].agg(["min","max"])
    out["by_year"]=act.groupby("year").apply(agg)
    out["by_coin"]=act.groupby("coin").apply(agg)
    out["by_side_year_pnl"]=act.pivot_table(index="year",columns="side",values="pnl",aggfunc="sum")
    # agreement of 14d direction with last day
    act["agree1"]=np.sign(act["prior1"])==act["side"]
    out["by_agree1"]=act.groupby("agree1").apply(agg)
    # other Fridays without signal (low vol) gain if traded by r14 sign
    oth=C[(C["f"]==0)].dropna(subset=["r14"]).copy()
    oth["g"]=np.sign(oth["r14"])*oth["ret2"]
    out["other_fridays_r14sign"]=pd.Series(dict(n=len(oth),g=oth["g"].mean(),t=oth["g"].mean()/oth["g"].std()*np.sqrt(len(oth))))
    # pnl tails
    out["pnl_quantiles"]=act["pnl"].quantile([0.01,0.05,0.5,0.95,0.99])
    return out
