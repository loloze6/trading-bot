def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; allrows=[]
    cm={}
    for c,ws in data["bars"].items():
        rs=[]
        for w,b in ws.items():
            r=b["close"].pct_change().dropna(); rs.append(r)
        cm[c]=pd.concat(rs).mean()
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"].values; n=len(cl)
            ret=np.r_[np.nan, cl[1:]/cl[:-1]-1]
            run=np.zeros(n); cnt=0
            for i in range(1,n):
                if ret[i]>0:
                    run[i]=cnt; cnt=0
                elif ret[i]<0: cnt+=1
                else: cnt=0
            tr=np.full(n,np.nan)
            tr[60:]=cl[60:]/cl[:-60]-1
            for i in range(1,n):
                if run[i]>=1:
                    d={"coin":c,"w":w,"run":run[i],"tr":tr[i],"case":b["forecast"].iloc[i]<0,
                       "day":str(b["timestamp"].iloc[i])[:10],"year":str(b["timestamp"].iloc[i])[:4],
                       "upday":ret[i]}
                    for h in (1,2,3,5):
                        if i+h<n: d[f"u{h}"]=-(cl[i+h]/cl[i]-1-h*cm[c])
                    allrows.append(d)
    A=pd.DataFrame(allrows); C=A[A.case]
    def summ(g,col="u1"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    C["rb"]=pd.cut(C.run,[0,1,2,3,4,30])
    A["rb"]=pd.cut(A.run,[0,1,2,3,4,30])
    A["trb"]=pd.cut(A.tr,[-9,-0.3,-0.1,0.1,9])
    C["upq"]=pd.qcut(C.upday,3,labels=["small","mid","big"])
    out={}
    out["cases_h"]=pd.DataFrame({h:summ(C,f"u{h}") for h in ("u1","u2","u3","u5")}).T
    out["cases_by_run"]=C.groupby("rb").apply(summ)
    out["cases_by_coin"]=C.groupby("coin").apply(summ)
    out["cases_by_window"]=C.groupby("w").apply(summ)
    out["cases_by_year"]=C.groupby("year").apply(summ)
    out["cases_by_upday"]=C.groupby("upq").apply(summ)
    out["all_breaks_by_trend"]=A.groupby("trb").apply(summ)
    out["all_breaks_by_run"]=A.groupby("rb").apply(summ)
    out["noncase_falling_by_run"]=A[(~A.case)&(A.tr<-0.1)].groupby("rb").apply(summ)
    out["cases_u3_by_run"]=C.groupby("rb").apply(lambda g: summ(g,"u3"))
    return out
