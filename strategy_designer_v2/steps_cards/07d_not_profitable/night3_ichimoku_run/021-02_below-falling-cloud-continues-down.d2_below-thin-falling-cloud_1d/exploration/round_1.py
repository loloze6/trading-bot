import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=26
    bars=data["bars"]; days=data["days"]
    # drift per coin: non-overlapping 26-bar returns over all windows
    drift={}; usual={}
    for c in bars:
        r=[]
        for w,b in bars[c].items():
            cl=b["close"].values
            for i in range(0,len(cl)-H,H):
                r.append(cl[i+H]/cl[i]-1)
        drift[c]=np.mean(r); usual[c]=np.std(r)
    cases=[]
    allbar=[]
    for c in bars:
        for w,b in bars[c].items():
            cl=b["close"].values; f=b["forecast"].values
            pos=b["postRebalance_current_allocation"].values
            bir=pd.to_numeric(b.get("debug_info.bars_in_regime"),errors="coerce").values if "debug_info.bars_in_regime" in b else np.full(len(b),np.nan)
            n=len(cl)
            past26=np.full(n,np.nan); past7=np.full(n,np.nan)
            past26[26:]=cl[26:]/cl[:-26]-1; past7[7:]=cl[7:]/cl[:-7]-1
            lr=np.diff(np.log(cl),prepend=np.nan)
            vol20=pd.Series(lr).rolling(20).std().values
            hi=pd.Series(b["high"].values).rolling(26,min_periods=10).max().values
            dd=cl/hi-1
            for i in range(0,n-H,H):
                if f[i]<0:
                    fr=cl[i+H]/cl[i]-1
                    cases.append(dict(coin=c,win=w,f=abs(f[i]),ex=-(fr-drift[c]),tot=-fr,p26=past26[i],p7=past7[i],vol=vol20[i],dd=dd[i],bir=bir[i]))
            nr=np.append(cl[1:]/cl[:-1]-1,np.nan)
            allbar.append(pd.DataFrame(dict(coin=c,win=w,pos=pos,g=pos*nr,nr=nr,act=(f<0))))
    C=pd.DataFrame(cases); A=pd.concat(allbar)
    out={}
    out["cases_by_coin"]=C.groupby("coin").agg(n=("ex","size"),ex=("ex","mean"),tot=("tot","mean"))
    out["drift_usual"]=pd.DataFrame({"drift":drift,"usual":usual})
    for col in ["f","p26","p7","vol","dd","bir"]:
        d=C.dropna(subset=[col])
        if len(d)>20:
            q=pd.qcut(d[col].rank(method="first"),3,labels=["lo","mid","hi"])
            g=d.groupby(q).agg(n=("ex","size"),ex=("ex","mean"),tot=("tot","mean"),mean_x=(col,"mean"))
            g["spearman_tot"]=stats.spearmanr(d[col],d["tot"])[0]
            out["by_"+col]=g
    # book by window
    D=[]
    for c in days:
        for w,d in days[c].items():
            D.append(d.assign(coin=c,win=w))
    D=pd.concat(D)
    bw=D.groupby("win").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    act=A.groupby("win").agg(short_share=("pos",lambda x:(x<0).mean()),gain=("g","mean"))
    out["by_window"]=bw.join(act).round(5)
    out["active_bar_gain"]=pd.Series({"mean_gain_active":A.loc[A.pos<0,"g"].mean(),"mean_nr_active":A.loc[A.pos<0,"nr"].mean(),"mean_nr_all":A["nr"].mean(),"short_share":(A.pos<0).mean(),"mean_pos_when_short":A.loc[A.pos<0,"pos"].mean()})
    return out
