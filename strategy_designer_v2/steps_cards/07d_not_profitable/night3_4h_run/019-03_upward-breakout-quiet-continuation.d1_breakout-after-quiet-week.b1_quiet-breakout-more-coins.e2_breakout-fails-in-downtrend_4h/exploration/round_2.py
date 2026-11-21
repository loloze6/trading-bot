import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars=data["bars"]; days=data["days"]
    out={}
    rows=[]; age=[]
    for coin in bars:
        allr=[]; r1=[]
        for w,b in bars[coin].items():
            c=b["close"].values
            idx=np.arange(0,len(c)-72,72)
            allr+=list(c[idx+72]/c[idx]-1); r1+=list(c[1:]/c[:-1]-1)
        drift=np.mean(allr); m1=np.mean(r1)
        for w,b in bars[coin].items():
            b=b.reset_index(drop=True)
            c=b["close"].values; h=b["high"].values; l=b["low"].values; n=len(c)
            pos=b["postRebalance_current_allocation"].fillna(0).values
            nxt=np.r_[c[1:]/c[:-1]-1,np.nan]
            fc=b["forecast"].fillna(0).values
            # bars since position opened
            a=np.zeros(n,int); 
            for i in range(1,n):
                a[i]=a[i-1]+1 if pos[i]!=0 and pos[i-1]!=0 else 0
            for i in range(n-1):
                if pos[i]!=0:
                    age.append((min(a[i]//72,3),pos[i]*nxt[i],pos[i]*m1))
            ret30=pd.Series(c).pct_change(180).values
            ret90=pd.Series(c).pct_change(540).values
            rng=(pd.Series(h).rolling(12).max()-pd.Series(l).rolling(12).min())/pd.Series(c)
            rngq=(rng/rng.rolling(180).mean()).shift(1).values
            ent=np.where((fc<0)&(np.r_[0,fc[:-1]]==0))[0]
            for i in ent:
                if i+72>=n: continue
                fr=c[i+72]/c[i]-1
                rows.append(dict(coin=coin,wn=int(w[1:]),tot=-fr,unus=-(fr-drift),ret30=ret30[i],ret90=ret90[i],rngq=rngq[i]))
    E=pd.DataFrame(rows)
    A=pd.DataFrame(age,columns=["agecell","gain","mkt"])
    out["gain_by_age_72bar_cells"]=A.groupby("agecell").agg(n=("gain","size"),gain_sum=("gain","sum"),mkt_sum=("mkt","sum"),gain_mean=("gain","mean"))
    x=E.dropna(subset=["ret30","rngq"]).copy()
    x["q30"]=pd.qcut(x.ret30,4,labels=False); x["qr"]=pd.qcut(x.rngq,2,labels=False)
    out["ret30_x_range"]=x.groupby(["q30","qr"]).agg(n=("tot","size"),tot=("tot","mean"),unus=("unus","mean"),t=("tot",lambda s:s.mean()/s.std()*np.sqrt(len(s))))
    y=E.dropna(subset=["ret90"]).copy(); y["deep"]=y.ret90<-0.42
    out["deep90_by_window"]=y[y.deep].groupby("wn").agg(n=("tot","size"),tot=("tot","mean"))
    z=E.dropna(subset=["rngq"]).copy(); z["qr"]=pd.qcut(z.rngq,4,labels=False)
    out["range_by_year_half"]=z.assign(late=z.wn>12).groupby(["late","qr"]).agg(n=("tot","size"),tot=("tot","mean"),t=("tot",lambda s:s.mean()/s.std()*np.sqrt(len(s))))
    out["corr_tot"]=pd.Series({k:stats.spearmanr(E[k],E.tot,nan_policy="omit").correlation for k in ["ret30","ret90","rngq"]})
    # book drawdown windows
    dd=[]
    for coin in days:
        for w,d in days[coin].items():
            dd.append(d.assign(wn=int(w[1:]))[["wn","day","book_return","coin_return"]])
    D=pd.concat(dd).dropna().groupby(["wn","day"]).mean().reset_index()
    D=D.sort_values(["wn","day"])
    v=(1+D.book_return).cumprod(); D["dd"]=v/v.cummax()-1
    out["dd_by_window"]=D.groupby("wn").agg(book=("book_return","sum"),coin=("coin_return","sum"),mindd=("dd","min"))
    return out
