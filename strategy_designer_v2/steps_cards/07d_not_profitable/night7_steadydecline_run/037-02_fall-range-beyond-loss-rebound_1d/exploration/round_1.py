def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    days=data["days"]; bars=data["bars"]
    coins=list(bars.keys())
    out={}
    # per-bar table
    rows=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.copy().reset_index(drop=True)
            r=b.close.pct_change()
            fall=(-r).clip(lower=0)*100
            rng=(b.high-b.low)/b.close.shift(1)*100
            exc=(rng-fall).clip(lower=0)
            nxt=b.close.shift(-1)/b.close-1
            tr60=b.close/b.close.shift(60)-1
            tr20=b.close/b.close.shift(20)-1
            vol30=r.rolling(30).std()
            d=pd.DataFrame({"coin":c,"w":w,"r":r,"fall":fall,"exc":exc,"prod":fall*exc,"nxt":nxt,
                "fc":b.forecast,"alloc":b.postRebalance_current_allocation,"tr60":tr60,"tr20":tr20,"vol30":vol30,
                "vrank":vol30.rank(pct=True)})
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    drift=A.groupby("coin").nxt.mean()
    A["unus"]=A.nxt-A.coin.map(drift)
    A["pos"]=A.alloc.abs()>1e-6
    A["case"]=A.fc>0
    out["share_case_pos"]=pd.Series({"case":A.case.mean(),"pos":A.pos.mean(),"pos_given_nocase":A.loc[~A.case,"pos"].mean(),
        "alloc_case":A.loc[A.case,"alloc"].mean(),"alloc_nocase_pos":A.loc[(~A.case)&A.pos,"alloc"].mean()})
    A["gain"]=A.alloc*A.nxt
    out["gain_by_case"]=A.groupby("case").agg(n=("gain","size"),gain=("gain","mean"),nxt=("nxt","mean"),unus=("unus","mean"))
    # trend buckets
    A["trend"]=pd.cut(A.tr60,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    A["tr20b"]=pd.cut(A.tr20,[-9,-0.1,0,0.1,99])
    g=A.groupby(["trend","case"]).agg(n=("nxt","size"),nxt=("nxt","mean"),unus=("unus","mean"),gain=("gain","mean"),
        t=("unus",lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    out["by_trend60_case"]=g
    g=A.groupby(["tr20b","case"]).agg(n=("nxt","size"),nxt=("nxt","mean"),gain=("gain","mean"),
        t=("unus",lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    out["by_tr20_case"]=g
    A["vq"]=pd.qcut(A.vrank,[0,0.5,1],labels=["calmer","agitated"])
    out["by_vol_case"]=A.groupby(["vq","case"]).agg(n=("nxt","size"),nxt=("nxt","mean"),gain=("gain","mean"),
        t=("unus",lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    # forecast strength quintile among cases
    C=A[A.case].copy()
    C["fq"]=pd.qcut(C.fc,4,labels=False,duplicates="drop")
    out["by_fc_quart"]=C.groupby("fq").agg(n=("nxt","size"),fc=("fc","mean"),nxt=("nxt","mean"),gain=("gain","mean"),
        t=("unus",lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    # holding: return after case days 1..3
    # book daily, drawdown
    bk=[]
    for w in sorted({w for c in coins for w in days[c]},key=lambda s:int(s[1:])):
        dd=[days[c][w].set_index("day")[["book_return","coin_return"]] for c in coins if w in days[c]]
        m=pd.concat(dd,axis=1,keys=range(len(dd)))
        br=m.xs("book_return",axis=1,level=1).mean(axis=1); cr=m.xs("coin_return",axis=1,level=1).mean(axis=1)
        bk.append(pd.DataFrame({"w":w,"br":br.values,"cr":cr.values}))
    B=pd.concat(bk,ignore_index=True).dropna()
    v=(1+B.br).cumprod(); peak=v.cummax(); B["dd"]=v/peak-1
    out["maxdd"]=B.dd.min()
    out["book_by_window"]=B.groupby("w",sort=False).agg(br=("br","sum"),cr=("cr","sum"),mindd=("dd","min"))
    # in book drawdown episodes: days with dd < -0.15 vs others
    B["deep"]=B.dd<-0.15
    out["deep_days"]=B.groupby("deep").agg(n=("br","size"),br=("br","mean"),cr=("cr","mean"))
    # loss decomposition: position gains on case bars vs carried bars by trend
    out["gain_pos_trend"]=A[A.pos].groupby(["trend","case"]).gain.agg(["size","mean","sum"])
    return out
