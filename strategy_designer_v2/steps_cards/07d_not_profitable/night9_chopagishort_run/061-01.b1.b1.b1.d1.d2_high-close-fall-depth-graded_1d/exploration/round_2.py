def explore(data):
    import numpy as np, pandas as pd
    out={}
    def build(H):
        rows=[]
        for coin,ws in data["bars"].items():
            allr=[]
            for w,b in ws.items():
                c=b["close"].values
                for i in range(0,len(b)-H,H): allr.append(c[i+H]/c[i]-1)
            dr=np.mean(allr) if allr else np.nan
            for w,b in ws.items():
                b=b.reset_index(drop=True)
                c=b["close"]; rng=(b.high-b.low).replace(0,np.nan)
                cl=(c-b.low)/rng; r5=c/c.shift(5)-1; r60=c/c.shift(60)-1
                lr=np.log(c).diff(); v30=lr.rolling(30).std()
                vp=v30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
                fwd=c.shift(-H)/c-1
                d=pd.DataFrame(dict(coin=coin,w=w,i=range(len(b)),day=b.timestamp.astype(str).str[:10],
                    regime=b.regime,cl=cl,r5=r5,r60=r60,vp=vp,fwd=fwd))
                d["un"]=-(d.fwd-dr); d["cell"]=d.i//H
                rows.append(d)
        return pd.concat(rows).dropna(subset=["cl","r5","fwd"])
    def summ(sub):
        s=sub.sort_values("i").groupby(["coin","w","cell"]).first().reset_index()
        if len(s)<3: return pd.Series(dict(n=len(s)))
        d=(s.un-s.un.mean()).groupby(s.day).sum(); se=np.sqrt((d**2).sum())/len(s)
        return pd.Series(dict(n=len(s),days=s.day.nunique(),mean_un=s.un.mean(),t=s.un.mean()/se,tot=(-s.fwd).mean()))
    res={}
    for H in [2,5,10]:
        df=build(H); P=df[df.regime!="chop"]
        res[f"H{H}_prof_cl75"]=summ(P[(P.cl>=.75)&(P.r5<0)])
        res[f"H{H}_prof_cl50"]=summ(P[(P.cl>=.5)&(P.r5<0)])
        if H==5:
            A=df[(df.vp>0.5)]
            res["H5_agit_anytrend_cl50_r5neg"]=summ(A[(A.cl>=.5)&(A.r5<0)])
            res["H5_agit_anytrend_r5neg_cl<50"]=summ(A[(A.cl<.5)&(A.r5<0)])
            ch=df[(df.r60.abs()<=.1)]
            res["H5_choppy_calm_cl50_r5neg"]=summ(ch[(ch.vp<=.5)&(ch.cl>=.5)&(ch.r5<0)])
            res["H5_choppy_any_cl50_r5neg"]=summ(ch[(ch.cl>=.5)&(ch.r5<0)])
            res["H5_choppy_any_r5neg_cl<50"]=summ(ch[(ch.cl<.5)&(ch.r5<0)])
            fd=df[(df.r60<-.1)]
            res["H5_falling_cl50_r5neg"]=summ(fd[(fd.cl>=.5)&(fd.r5<0)])
            res["H5_falling_r5neg_cl<50"]=summ(fd[(fd.cl<.5)&(fd.r5<0)])
            rs=df[(df.r60>.1)]
            res["H5_rising_cl50_r5neg"]=summ(rs[(rs.cl>=.5)&(rs.r5<0)])
    out["groups"]=pd.DataFrame(res).T
    # book daily: worst days, contributions by window
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w; D.append(dd)
    D=pd.concat(D)
    book=D.groupby(["w","day"]).book_return.mean()
    hold=D.groupby(["w","day"]).coin_return.mean()
    out["by_window"]=pd.DataFrame({"book_mean":book.groupby(level=0).mean(),"book_sum":book.groupby(level=0).sum(),"hold_mean":hold.groupby(level=0).mean(),"days":book.groupby(level=0).size()})
    return out
