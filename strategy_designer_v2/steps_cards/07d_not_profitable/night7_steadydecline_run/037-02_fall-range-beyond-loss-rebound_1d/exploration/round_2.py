def explore(data):
    import pandas as pd, numpy as np
    bars=data["bars"]; days=data["days"]
    coins=list(bars.keys())
    rows=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.copy().reset_index(drop=True)
            r=b.close.pct_change()
            nxt=b.close.shift(-1)/b.close-1
            vol30=r.rolling(30,min_periods=20).std()
            vmed=vol30.expanding(min_periods=20).median()
            tr60=b.close/b.close.shift(60)-1
            tr10=b.close/b.close.shift(10)-1
            rng=(b.high-b.low)/b.close.shift(1)
            d=pd.DataFrame({"coin":c,"w":w,"i":np.arange(len(b)),"r":r,"nxt":nxt,"fc":b.forecast,
                "alloc":b.postRebalance_current_allocation,"chg":(b.postRebalance_current_allocation-b.previous_allocation).abs(),
                "agit":vol30>vmed,"tr60":tr60,"tr10":tr10,"rng":rng})
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    drift=A.groupby("coin").nxt.mean()
    A["unus"]=A.nxt-A.coin.map(drift)
    A["case"]=A.fc>0
    A["strong"]=A.fc>=15
    A["gain"]=A.alloc*A.nxt
    A["fee"]=A.chg*0.0019
    A["net"]=A.gain-A.fee
    A["trend"]=pd.cut(A.tr60,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    tt=lambda x: x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
    out={}
    out["agit_strong"]=A.groupby(["agit","strong","case"]).agg(n=("nxt","size"),unus=("unus","mean"),t=("unus",tt),net=("net","mean"),fee=("fee","mean"))
    out["trend_agit_case"]=A.groupby(["trend","agit","case"]).agg(n=("nxt","size"),unus=("unus","mean"),t=("unus",tt),net=("net","mean"))
    out["fee_vs_gain_by_strength"]=A[A.case].groupby(pd.cut(A.fc,[0,5,10,15,20.1])).agg(n=("nxt","size"),gain=("gain","mean"),fee=("fee","mean"),net=("net","mean"))
    # book-like daily simulation per variant: per coin-window daily net, mean over coins per (w,i)
    def book(mask):
        X=A.copy(); X["v"]=np.where(mask,X.net,0.0)
        X.loc[~mask,"v"]=np.where(mask[~mask],0,-X.loc[~mask,"fee"]*0)  # simplified
        d=X.groupby(["w","i"]).v.mean().reset_index()
        d["wn"]=d.w.str[1:].astype(int); d=d.sort_values(["wn","i"])
        v=(1+d.v.fillna(0)).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(d))-1
        return pd.Series({"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"sharpe":d.v.mean()/d.v.std()*np.sqrt(365),"share_on":mask.mean()})
    out["variants"]=pd.DataFrame({"all":book(A.alloc.abs()>0),
        "agit_only":book((A.alloc.abs()>0)&A.agit),
        "not_choppy":book((A.alloc.abs()>0)&(A.trend!="choppy")),
        "strong_only":book((A.alloc.abs()>0)&(A.fc>=10)),
        "agit_strong":book((A.alloc.abs()>0)&A.agit&(A.fc>=10))}).T
    # deepest fall of actual book: w16/w17 composition
    D=A[A.w.isin(["w16","w17"])]
    out["w16_17_pos"]=D[D.alloc.abs()>0].groupby(["w","agit","trend"]).agg(n=("net","size"),net=("net","mean"),sum=("net","sum"))
    out["w_other_pos"]=A[(~A.w.isin(["w16","w17"]))&(A.alloc.abs()>0)].groupby(["agit","trend"]).agg(n=("net","size"),net=("net","mean"))
    # 10-day trend among cases
    out["tr10_case"]=A[A.case].groupby(pd.cut(A.tr10,[-9,-0.15,-0.05,0,0.05,99])).agg(n=("nxt","size"),unus=("unus","mean"),t=("unus",tt))
    out["tr10_nocase"]=A[~A.case].groupby(pd.cut(A.tr10,[-9,-0.15,-0.05,0,0.05,99])).agg(n=("nxt","size"),unus=("unus","mean"),t=("unus",tt))
    return out
