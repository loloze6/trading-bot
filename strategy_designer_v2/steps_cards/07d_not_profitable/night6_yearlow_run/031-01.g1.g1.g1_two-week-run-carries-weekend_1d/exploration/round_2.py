def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]; days=data["days"]
    out={}
    rows=[]; cs=[]; allfri=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            d=days[c][w].reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]).dt.normalize()
            al=b["postRebalance_current_allocation"].values
            prev=np.r_[0,al[:-1]]
            dd=pd.DataFrame({"day":pd.to_datetime(d["day"]).dt.normalize(),"br":d["book_return"].values,"cr":d["coin_return"].values})
            m=pd.DataFrame({"day":ts,"prev":prev,"al":al})
            dd=dd.merge(m,on="day",how="left")
            # long-only: zero days held short and the day a short was opened
            lo=dd["br"].where(~((dd["prev"]<0)|(dd["al"]<0)),0.0)
            so=dd["br"].where(~((dd["prev"]>0)|(dd["al"]>0)),0.0)
            dd["lo"]=lo; dd["so"]=so; dd["coin"]=c; dd["wn"]=int(w[1:])
            rows.append(dd)
            cl=b["close"].values; wk=pd.to_datetime(b["timestamp"]).dt.weekday.values
            r14=pd.Series(cl).pct_change(14).values
            for i in range(len(b)-2):
                if wk[i]!=4: continue
                allfri.append(dict(coin=c,ret2=cl[i+2]/cl[i]-1,r14=r14[i],f=b["forecast"].iat[i]))
    D=pd.concat(rows)
    def bookstats(col):
        B=D.groupby(["wn","day"])[col].mean().dropna().reset_index().sort_values(["wn","day"])
        r=B[col]; v=(1+r).cumprod(); mdd=(v/v.cummax()-1).min()
        yr=v.iat[-1]**(365/len(r))-1
        return pd.Series(dict(mean=r.mean(),sharpe=r.mean()/r.std()*np.sqrt(365),yearly=yr,maxdd=mdd,calmar=yr/abs(mdd)))
    out["books"]=pd.DataFrame({k:bookstats(k) for k in ["br","lo","so"]})
    F=pd.DataFrame(allfri)
    F["s"]=np.sign(F["r14"])
    def g(x): return pd.Series(dict(n=len(x),mean=x["ret2"].mean(),t=x["ret2"].mean()/(x["ret2"].std()/np.sqrt(len(x)))))
    out["all_fridays_weekend_ret"]=g(F)
    out["fridays_by_r14_sign"]=F.groupby("s").apply(g)
    F["q"]=pd.qcut(F["r14"],5,labels=False)
    out["fridays_by_r14_q"]=F.groupby("q").apply(g)
    # long side: graded inside positive forecast?
    P=F[F["f"]>0].copy(); P["q"]=pd.qcut(P["f"],3,labels=False)
    out["long_by_f_tercile"]=P.groupby("q").apply(g)
    # non-friday weekend-like 2-day returns after positive r14 (condition without the Friday)
    return out
