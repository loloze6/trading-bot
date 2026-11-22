def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    out={}
    cases=[]; drift={}; usual={}
    for coin,wins in data["bars"].items():
        g=[]
        for w,b in wins.items():
            c=b["close"].values
            for i in range(0,len(c)-H,H): g.append(c[i+H]/c[i]-1)
        drift[coin]=np.mean(g); usual[coin]=np.std(g)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].values
            r1=pd.Series(c).pct_change()
            z=r1/r1.rolling(20).std()
            for s in range(0,len(b),H):
                for i in range(s,min(s+H,len(b))):
                    if abs(f[i])>=2:
                        if i+H<len(b):
                            ret=c[i+H]/c[i]-1
                            cases.append(dict(coin=coin,win=w,side=np.sign(f[i]),f=abs(f[i]),
                              ret=ret,ex=ret-drift[coin],z=z.iloc[i],
                              r1n=c[i+1]/c[i]-1,yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
                        break
    d=pd.DataFrame(cases)
    d["sideex"]=d.side*d.ex
    out["cases_by_side"]=d.groupby("side").agg(n=("ex","size"),mean_ex=("ex","mean"),mean_ret=("ret","mean"),mean_next1=("r1n","mean"),t=("ex",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    d["fq"]=pd.qcut(d.f.rank(method="first"),4,labels=False)
    out["ex_by_side_fq"]=d.pivot_table(index="fq",columns="side",values="ex",aggfunc="mean")
    out["n_by_side_fq"]=d.pivot_table(index="fq",columns="side",values="ex",aggfunc="size")
    out["sideex_by_coin"]=d.groupby("coin").sideex.agg(["size","mean"])
    out["sideex_by_year_side"]=d.pivot_table(index="yr",columns="side",values="ex",aggfunc="mean")
    out["n_by_year_side"]=d.pivot_table(index="yr",columns="side",values="ex",aggfunc="size")
    # book
    rows=[]
    for coin,wins in data["days"].items():
        for w,dd in wins.items():
            x=dd[["day","book_return","coin_return"]].copy(); x["coin"]=coin; x["win"]=w; rows.append(x)
    D=pd.concat(rows)
    B=D.groupby(["win","day"])[["book_return","coin_return"]].mean().reset_index()
    pw=B.groupby("win").agg(book=("book_return","mean"),hold=("coin_return","mean"),bsd=("book_return","std"),n=("book_return","size"))
    pw["year"]=B.groupby("win").day.first().map(lambda x:pd.Timestamp(x).year)
    out["book_by_window"]=pw
    # long vs short book contribution per bar, fees
    pr=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            a=b["postRebalance_current_allocation"].values; c=b["close"].values
            r=np.r_[c[1:]/c[:-1]-1,np.nan]
            fee=(b["total_portfolio_value"].values-b["postRebalance_total_value"].values)/b["total_portfolio_value"].values
            pr.append(pd.DataFrame(dict(a=a,g=a*r,fee=fee,reg=b["regime"].values)))
    P=pd.concat(pr).dropna()
    P["pos"]=np.sign(P.a)
    out["gain_by_pos"]=P.groupby("pos").agg(bars=("g","size"),sum_gain=("g","sum"),mean_gain=("g","mean"),mean_abs_a=("a",lambda x:x.abs().mean()))
    out["fees_total"]=float(P.fee.sum()); out["gross_total"]=float(P.g.sum())
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items(): tr.append(t)
    T=pd.concat(tr)
    out["trades"]=T.groupby("side").agg(n=("profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda x:(x>0).mean()),dur_d=("duration_minutes",lambda x:x.mean()/1440))
    return out
