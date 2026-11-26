def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    wins = sorted(data["bars"][coins[0]].keys(), key=lambda w:int(w[1:]))
    # book daily returns
    rows=[]
    for c in coins:
        for w in wins:
            d=data["days"][c].get(w)
            if d is None: continue
            t=d[["day","book_return","coin_return"]].copy(); t["coin"]=c; t["w"]=w
            rows.append(t)
    D=pd.concat(rows)
    B=D.groupby(["w","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).reset_index()
    B["wn"]=B.w.str[1:].astype(int); B=B.sort_values(["wn","day"]).dropna(subset=["br"])
    B["year"]=pd.to_datetime(B.day).dt.year
    v=(1+B.br).cumprod(); peak=v.cummax(); dd=v/peak-1
    B["dd"]=dd.values
    i=int(np.argmin(dd.values)); pk=int(np.argmax(v.values[:i+1]))
    out["deepest fall"]=pd.Series({"depth":dd.values[i],"days_long":i-pk,"peak_window":B.w.values[pk],"trough_window":B.w.values[i]})
    out["by window"]=B.groupby("w").agg(book_sum=("br","sum"),coin_mean=("cr","mean"),min_dd=("dd","min"),n=("br","size")).reindex(wins)
    out["by year"]=B.groupby("year").agg(book_sum=("br","sum"),coin_sum=("cr","sum"),n=("br","size"))
    # cases
    cs=[]; held=[]
    for c in coins:
        drs=[]
        for w in wins:
            b=data["bars"][c].get(w)
            if b is None: continue
            cl=b.close.values; n=len(cl)
            for k in range(0,n-5,5): drs.append(cl[k+5]/cl[k]-1)
        drift=np.mean(drs); usual=np.std(drs,ddof=1)
        for w in wins:
            b=data["bars"][c].get(w)
            if b is None: continue
            b=b.reset_index(drop=True)
            cl=b.close; r1=cl.pct_change()
            ret10=cl/cl.shift(10)-1; ret5=cl/cl.shift(5)-1; ret1=r1
            vol20=r1.rolling(20).std()
            vr=b["debug_info.components.vol_dryup.last_history_value"]
            f=b.forecast.values; n=len(b)
            alloc=b.postRebalance_current_allocation
            g=(cl.shift(-1)/cl-1)*alloc
            held.append(pd.DataFrame({"g":g,"alloc":alloc,"ret10":ret10,"ret5":ret5,"vol20":vol20,"coin":c,"regime":b.regime,"r1":r1}))
            for k in range(0,n-5,5):
                for j in range(k,min(k+5,n-5)):
                    if f[j]<=-2:
                        r5=cl[j+5]/cl[j]-1
                        cs.append(dict(coin=c,w=w,ts=str(b.timestamp[j])[:10],u=drift-r5,f=f[j],ret10=ret10[j],ret5=ret5[j],r1=ret1[j],vol=vol20[j],vr=vr[j],usual=usual))
                        break
    C=pd.DataFrame(cs)
    vm=C.groupby("coin").vol.transform("median"); C["volrel"]=C.vol/vm
    def tab(col,q=3):
        x=C.dropna(subset=[col]).copy(); x["b"]=pd.qcut(x[col],q,labels=False,duplicates="drop")
        return x.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),mean_u=("u","mean"),n=("u","size"),t=("u",lambda s:s.mean()/(s.std()/np.sqrt(len(s)))))
    out["cases overall"]=pd.Series({"n":len(C),"mean_u":C.u.mean(),"days":C.ts.nunique()})
    out["by ret10"]=tab("ret10"); out["by ret5"]=tab("ret5"); out["by r1"]=tab("r1")
    out["by volrel"]=tab("volrel"); out["by forecast"]=tab("f")
    out["by coin"]=C.groupby("coin").u.agg(["mean","size"])
    out["by window cases"]=C.groupby("w").u.agg(["mean","size"]).reindex(wins)
    H=pd.concat(held); H=H[H.alloc.abs()>1e-9].dropna(subset=["g"])
    out["worst position days"]=pd.Series({"n_in":len(H),"mean_g":H.g.mean(),"share_loss_from_worst5pct":H.g[H.g<H.g.quantile(0.05)].sum()/H.g.sum()})
    H["vb"]=pd.qcut(H.vol20/H.groupby("coin").vol20.transform("median"),3,labels=False)
    out["held gain by vol"]=H.groupby("vb").g.agg(["mean","std","size"])
    out["held by alloc size"]=H.groupby(pd.qcut(H.alloc.abs(),3,labels=False)).g.agg(["mean","std","size"])
    return out
