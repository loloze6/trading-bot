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
            ret60=b.close/b.close.shift(60)-1
            d=pd.DataFrame({"coin":c,"wn":int(w[1:]),"pos":np.arange(len(b)),"a":b.postRebalance_current_allocation,"fc":b.forecast,"z":z,"ret20":ret20,"ret60":ret60})
            for h in [1,3,5]:
                d[f"f{h}"]=b.close.shift(-h)/b.close-1
            d["g"]=d.a*d.f1
            br.append(d)
    X=pd.concat(ignore_index=True,objs=br)
    X["mu"]=X.coin.map(X.groupby("coin").f1.mean())
    sig=X[X.fc>0].copy()
    sig["zb"]=pd.cut(sig.z,[-99,-3,-2,-1.5,-1,0],labels=["<-3","-3..-2","-2..-1.5","-1.5..-1","-1..0"])
    out["by_z_bin"]=sig.groupby("zb").apply(lambda d:pd.Series({"n":len(d),"ex1":(d.f1-d.mu).mean(),"t1":(d.f1-d.mu).mean()/(d.f1-d.mu).std()*np.sqrt(len(d)),"ex3":(d.f3-3*d.mu).mean(),"ex5":(d.f5-5*d.mu).mean(),"alloc":d.a.mean(),"gain":d.g.mean()})).round(5)
    sig["r60q"]=pd.qcut(sig.ret60,4,labels=False,duplicates="drop")
    out["by_ret60_q"]=sig.groupby("r60q").apply(lambda d:pd.Series({"n":len(d),"r60":d.ret60.mean(),"ex1":(d.f1-d.mu).mean(),"t1":(d.f1-d.mu).mean()/(d.f1-d.mu).std()*np.sqrt(len(d)),"ex5":(d.f5-5*d.mu).mean(),"gain":d.g.mean()})).round(5)
    dd=X[X.wn.isin([15,16,17])]
    a2=dd[dd.a.abs()>0.01].dropna(subset=["g"])
    out["dd_windows_active"]=pd.Series({"n":len(a2),"gain":a2.g.mean(),"sum_gain":a2.g.sum(),"alloc":a2.a.mean(),"share_down20":(a2.ret20<0).mean(),"mean_ret60":a2.ret60.mean(),"mean_z_sig":a2[a2.fc>0].z.mean()})
    out["dd_windows_by_coin"]=a2.groupby("coin").agg(n=("g","size"),sum_g=("g","sum"),r60=("ret60","mean")).round(4)
    rest=X[~X.wn.isin([15,16,17])]; a3=rest[rest.a.abs()>0.01].dropna(subset=["g"])
    out["other_windows_active"]=pd.Series({"n":len(a3),"gain":a3.g.mean(),"mean_ret60":a3.ret60.mean()})
    return out
