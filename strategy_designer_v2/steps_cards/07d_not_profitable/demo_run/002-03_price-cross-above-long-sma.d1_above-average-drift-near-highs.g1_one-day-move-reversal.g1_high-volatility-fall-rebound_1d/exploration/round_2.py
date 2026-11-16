def explore(data):
    import numpy as np, pandas as pd
    out = {}
    br=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            r=b.close.pct_change()
            vol=r.rolling(20).std()
            z=r/vol
            ret20=(b.close/b.close.shift(20)-1)/(vol*np.sqrt(20))
            sma50=b.close.rolling(50).mean()
            d=pd.DataFrame({"coin":c,"w":w,"pos":np.arange(len(b)),"a":b.postRebalance_current_allocation,"fc":b.forecast,"z":z,"ret20":ret20,"abv50":(b.close>sma50).where(sma50.notna()),"reg":b.regime})
            for h in [1,2,3,5]:
                d[f"f{h}"]=b.close.shift(-h)/b.close-1
            d["g"]=d.a*d.f1
            br.append(d)
    X=pd.concat(ignore_index=True,objs=br)
    mu=X.groupby("coin").f1.mean()
    X["mu"]=X.coin.map(mu)
    sig=X[(X.fc>0)].copy()
    out["n_signal"]=len(sig)
    # horizons, excess over coin mean daily x h
    rows={}
    for h in [1,2,3,5]:
        s=sig[f"f{h}"]-h*sig.mu
        s=s.dropna()
        rows[h]={"mean_ex":s.mean(),"t":s.mean()/s.std()*np.sqrt(len(s)),"n":len(s)}
    out["signal_horizons"]=pd.DataFrame(rows).T.round(5)
    sig["fcq"]=pd.qcut(sig.fc,3,labels=False,duplicates="drop")
    sig["tr"]=np.where(sig.ret20>0,"up20","down20")
    g=sig.groupby(["tr","fcq"])
    out["trend_x_fc"]=g.apply(lambda d:pd.Series({"n":len(d),"ex1":(d.f1-d.mu).mean(),"t1":(d.f1-d.mu).mean()/(d.f1-d.mu).std()*np.sqrt(len(d)),"ex3":(d.f3-3*d.mu).mean(),"alloc":d.a.mean(),"gain":d.g.mean()})).round(5)
    out["above50_x_fc"]=sig.groupby(["abv50","fcq"]).apply(lambda d:pd.Series({"n":len(d),"ex1":(d.f1-d.mu).mean(),"t1":(d.f1-d.mu).mean()/(d.f1-d.mu).std()*np.sqrt(len(d)),"alloc":d.a.mean(),"gain":d.g.mean()})).round(5)
    # allocation held on worst gain bars
    act=X[X.a.abs()>0.01].dropna(subset=["g"])
    worst=act.nsmallest(50,"g")
    out["worst50_gain_bars"]=pd.Series({"mean_g":worst.g.mean(),"mean_a":worst.a.mean(),"mean_fc":worst.fc.mean(),"share_fc0":(worst.fc==0).mean(),"share_down20":(worst.ret20<0).mean(),"mean_z":worst.z.mean(),"share_above50":worst.abv50.mean()})
    # allocation held with forecast 0 (lingering)
    out["active_fc0"]=pd.Series({"n":int(((act.fc==0)).sum()),"gain":act[act.fc==0].g.mean(),"alloc":act[act.fc==0].a.mean()})
    # book drawdown
    rows=[]
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd=d[["day","book_return"]].copy(); dd["w"]=int(w[1:]); rows.append(dd)
    D=pd.concat(rows).groupby(["w","day"]).book_return.mean().dropna().reset_index().sort_values(["w","day"])
    eq=(1+D.book_return).cumprod(); dd=eq/eq.cummax()-1
    D["dd"]=dd.values
    out["maxdd"]=dd.min()
    out["dd_by_window_min"]=D.groupby("w").dd.min().round(4).nsmallest(8)
    return out
