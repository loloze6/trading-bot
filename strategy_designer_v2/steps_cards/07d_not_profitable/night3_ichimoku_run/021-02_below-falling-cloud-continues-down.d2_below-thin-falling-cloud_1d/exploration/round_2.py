import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=26
    bars=data["bars"]; days=data["days"]
    drift={}; usual={}
    for c in bars:
        r=[]
        for w,b in bars[c].items():
            cl=b["close"].values
            for i in range(0,len(cl)-H,H):
                r.append(cl[i+H]/cl[i]-1)
        drift[c]=np.mean(r); usual[c]=np.std(r)
    cases=[]; up=[]
    for c in bars:
        for w,b in bars[c].items():
            cl=b["close"].values; f=b["forecast"].values
            hi=pd.Series(b["high"].values); lo=pd.Series(b["low"].values)
            n=len(cl)
            ten=(hi.rolling(9).max()+lo.rolling(9).min())/2
            kij=(hi.rolling(26).max()+lo.rolling(26).min())/2
            sa=((ten+kij)/2).shift(26); sb=((hi.rolling(52).max()+lo.rolling(52).min())/2).shift(26)
            top=np.maximum(sa,sb).values; bot=np.minimum(sa,sb).values; mid=((sa+sb)/2).values
            slope=np.full(n,np.nan); slope[26:]=mid[26:]/mid[:-26]-1
            width=(top-bot)/cl
            p7=np.full(n,np.nan); p7[7:]=cl[7:]/cl[:-7]-1
            p26=np.full(n,np.nan); p26[26:]=cl[26:]/cl[:-26]-1
            for i in range(0,n-H,H):
                fr=cl[i+H]/cl[i]-1
                if f[i]<0:
                    cases.append(dict(coin=c,win=w,f=abs(f[i]),p7=p7[i],p26=p26[i],ex=-(fr-drift[c]),tot=-fr))
                if np.isfinite(slope[i]) and cl[i]>top[i] and slope[i]>0:
                    up.append(dict(coin=c,width=width[i],ex=fr-drift[c],tot=fr,str=(fr-drift[c])/usual[c]))
    C=pd.DataFrame(cases); U=pd.DataFrame(up)
    out={}
    d=C.dropna(subset=["p7"])
    d["fq"]=pd.qcut(d.f.rank(method="first"),2,labels=["thick","thin"])
    d["pq"]=pd.qcut(d.p7.rank(method="first"),2,labels=["fell7","rose7"])
    out["f_x_p7"]=d.groupby(["fq","pq"]).agg(n=("ex","size"),ex=("ex","mean"),tot=("tot","mean"))
    out["p7_tstat"]=pd.Series({"spearman_p7_ex":stats.spearmanr(d.p7,d.ex)[0],"spearman_p7_ex_p":stats.spearmanr(d.p7,d.ex)[1],"spearman_f_ex_p":stats.spearmanr(d.f,d.ex)[1],"t_tot_rose7":stats.ttest_1samp(d.loc[d.pq=="rose7","tot"],0)[0]})
    if len(U):
        out["above_rising_cloud"]=pd.Series({"n":len(U),"ex":U.ex.mean(),"t_ex":U.ex.mean()/U.ex.std()*np.sqrt(len(U)),"tot":U.tot.mean(),"strength":U["str"].mean(),"spearman_thin_ex":stats.spearmanr(-U.width,U.ex)[0] if len(U)>5 else np.nan})
    # book falls: chained daily book return per window, worst windows' drawdown, and coin moves during
    D=[]
    for c in days:
        for w,dd in days[c].items(): D.append(dd.assign(coin=c,win=w))
    D=pd.concat(D)
    bk=D.groupby(["win","day"]).agg(b=("book_return","mean"),m=("coin_return","mean")).reset_index()
    order=sorted(bk.win.unique(),key=lambda s:int(s[1:]))
    rows=[]
    for w in order:
        x=bk[bk.win==w].dropna()
        v=(1+x.b).cumprod(); mdd=(v/v.cummax()-1).min()
        rows.append(dict(win=w,book_tot=v.iloc[-1]-1,coin_tot=(1+x.m).prod()-1,mdd=mdd))
    out["window_falls"]=pd.DataFrame(rows).set_index("win").sort_values("mdd").head(8).round(4)
    return out
