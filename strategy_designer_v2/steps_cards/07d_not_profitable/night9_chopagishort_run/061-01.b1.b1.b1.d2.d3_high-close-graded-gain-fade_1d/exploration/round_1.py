def explore(data):
    import numpy as np, pandas as pd
    H=5
    out={}
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        rets=[]
        for w,b in ws.items():
            c=b["close"].values
            for i in range(0,len(c)-H,H):
                rets.append(c[i+H]/c[i]-1)
        drift[coin]=(np.mean(rets),np.std(rets))
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]
            rng=(h-l).replace(0,np.nan)
            loc=(c-l)/rng
            r1=c.pct_change()
            mabs=r1.abs().rolling(20,min_periods=10).mean()
            g=r1/mabs
            fwd=c.shift(-H)/c-1
            inprof=(b["regime"]!="chop")
            ret5p=c/c.shift(5)-1
            ret10p=c/c.shift(10)-1
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"loc":loc,"r1":r1,"g":g,"fwd":fwd,
                             "prof":inprof,"regime":b["regime"],"fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],
                             "ret5p":ret5p,"ret10p":ret10p,"year":pd.to_datetime(b["timestamp"]).dt.year,"ts":b["timestamp"]})
            df["cell"]=df["pos"]//H
            df["unus"]=-(df["fwd"]-drift[coin][0])
            df["str"]=df["unus"]/drift[coin][1]
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    D=D[D["fwd"].notna()]
    def meas(mask,name):
        s=D[mask].sort_values("pos").groupby(["coin","w","cell"]).head(1)
        if len(s)<3: return {"name":name,"n":len(s)}
        s=s.assign(day=s["ts"].astype(str).str[:10])
        d=s.groupby("day")["unus"].mean()
        t=d.mean()/(d.std()/np.sqrt(len(d))) if len(d)>2 else np.nan
        return {"name":name,"n":len(s),"days":len(d),"unus":s["unus"].mean(),"total_short":(-s["fwd"]).mean(),"str":s["str"].mean(),"t":t}
    P=D["prof"]; up=D["r1"]>0
    res=[]
    res.append(meas(P&(D["loc"]>=0.8)&up,"tested loc>=.8 up"))
    res.append(meas(P&(D["loc"]>=0.8)&up&(D["g"]<1),"tested & gain<1usual"))
    res.append(meas(P&(D["loc"]>=0.8)&up&(D["g"]>=1),"loc>=.8 gain>=1"))
    res.append(meas(P&(D["loc"]>=0.6)&up,"loc>=.6 up"))
    res.append(meas(P&(D["loc"]>=0.6)&up&(D["g"]<1),"loc>=.6 up gain<1"))
    res.append(meas(P&(D["loc"]>=0.5),"loc>=.5 any"))
    res.append(meas(P&up,"prof up any loc"))
    res.append(meas(P&up&(D["g"]<1),"prof up gain<1 any loc"))
    res.append(meas(P&(D["loc"]>=0.8)&up&(D["g"]<1)&(D["g"]>0),"loc.8 gain0-1"))
    res.append(meas(P&~((D["loc"]>=0.8)&up),"prof no signal"))
    res.append(meas(P,"prof all bars"))
    res.append(meas(~P&(D["loc"]>=0.8)&up,"outside prof loc.8 up"))
    res.append(meas(~P&(D["loc"]>=0.8)&up&(D["g"]<1),"outside prof loc.8 up g<1"))
    res.append(meas(~P,"outside prof all"))
    res.append(meas(P&(D["loc"]>=0.8)&up&(D["ret5p"]>0),"tested & 5d up"))
    res.append(meas(P&(D["loc"]>=0.8)&up&(D["ret5p"]<=0),"tested & 5d down"))
    res.append(meas(P&(D["loc"]>=0.6)&up&(D["ret10p"]>0),"loc.6 & 10d up"))
    res.append(meas(P&(D["loc"]>=0.6)&up&(D["ret10p"]<=0),"loc.6 & 10d down"))
    out["cases"]=pd.DataFrame(res)
    # profile share
    out["share_prof_bars"]=float(P.mean())
    out["share_signal_in_prof"]=float(((D["loc"]>=0.8)&up)[P].mean())
    # by year for tested
    s=D[P&(D["loc"]>=0.6)&up].sort_values("pos").groupby(["coin","w","cell"]).head(1)
    out["loc6_by_year"]=s.groupby("year")["unus"].agg(["count","mean"])
    out["loc6_by_coin"]=s.groupby("coin")["unus"].agg(["count","mean"])
    # gain buckets in prof loc>=.6 up
    s2=s.copy(); s2["gb"]=pd.cut(s2["g"],[0,0.5,1,1.5,2,100])
    out["loc6_gain_bucket"]=s2.groupby("gb")["unus"].agg(["count","mean"])
    # book falls
    br=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            br.append(d.assign(coin=coin,w=w))
    B=pd.concat(br)
    B["wn"]=B["w"].str[1:].astype(int)
    daily=B.groupby(["wn","day"])["book_return"].mean().dropna().sort_index()
    v=(1+daily).cumprod(); dd=v/v.cummax()-1
    out["book_maxdd"]=float(dd.min())
    out["book_yearly"]=float(v.iloc[-1]**(365/len(v))-1)
    # dd by window
    out["dd_by_window"]=dd.groupby(level=0).min()
    out["ret_by_window"]=(1+daily).groupby(level=0).prod()-1
    # trades by coin
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): tr.append(t.assign(coin=coin,w=w))
    T=pd.concat(tr)
    out["trades_pl"]=T.groupby("w")["net_profit_loss_percent"].agg(["count","mean","min"])
    out["n_trades"]=len(T)
    return out
