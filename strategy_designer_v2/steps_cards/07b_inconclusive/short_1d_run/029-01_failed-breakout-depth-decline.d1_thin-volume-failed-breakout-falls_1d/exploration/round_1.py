import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H=5
    rows=[]; allf=[]; drift={}; usual={}
    comp='debug_info.components.thin_failed_breakout.last_history_value'
    for coin, wins in data["bars"].items():
        rets=[]
        for w,df in wins.items():
            c=df['close'].values
            for i in range(0,len(c)-H,H): rets.append(c[i+H]/c[i]-1)
        drift[coin]=np.mean(rets); usual[coin]=np.std(rets)
    for coin, wins in data["bars"].items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df['close'].values; v=df['volume'].values; n=len(c)
            f=df['forecast'].fillna(0).values
            hi=pd.Series(c).shift(1).rolling(20).max().values
            vr=(pd.Series(v)/pd.Series(v).rolling(20).mean()).values
            yr=pd.to_datetime(df['timestamp']).dt.year.values
            for s in range(0,n,H):
                # tested cases
                done=False; doneA=False
                for t in range(s,min(s+H,n)):
                    if t+H>=n: break
                    fwd=[c[t+k]/c[t]-1 for k in (1,2,3,5,10) if t+k<n]
                    if not done and t>0 and f[t]-f[t-1]<=-2:
                        done=True
                        r=c[t+H]/c[t]-1
                        r10=c[t+10]/c[t]-1 if t+10<n else np.nan
                        rows.append(dict(coin=coin,w=w,year=yr[t],raw=df[comp].iloc[t] if comp in df else np.nan,
                          fc=f[t],un=-(r-drift[coin]),tot=-r,un10=-(r10-2*drift[coin]),
                          r1=-(c[t+1]/c[t]-1-drift[coin]/5), st=-(r-drift[coin])/usual[coin]))
                    if not doneA and t>=24:
                        for j in (t-1,t-2,t-3):
                            if j>=0 and not np.isnan(hi[j]) and c[j]>hi[j] and c[t]<hi[j] and all(c[k]>=hi[j] for k in range(j,t)):
                                doneA=True
                                r=c[t+H]/c[t]-1
                                allf.append(dict(coin=coin,year=yr[t],vr=vr[j],un=-(r-drift[coin]),
                                    depth=(hi[j]-c[t])/hi[j]))
                                break
    R=pd.DataFrame(rows); A=pd.DataFrame(allf)
    def agg(g,col='un'):
        x=g[col].dropna(); return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out={}
    out['tested overall']=agg(R)
    out['tested by coin']=R.groupby('coin').apply(agg)
    out['tested by year']=R.groupby('year').apply(agg)
    out['tested 10d']=agg(R,'un10'); out['tested 1d']=agg(R,'r1')
    out['forecast values']=R['fc'].round(2).value_counts().head(10)
    R['rq']=pd.qcut(R['raw'].rank(method='first'),3,labels=['low','mid','high'])
    out['tested by raw thinness tercile']=R.groupby('rq').apply(agg)
    A['vq']=pd.qcut(A['vr'].rank(method='first'),4,labels=['q1thin','q2','q3','q4heavy'])
    out['all failures by vol quartile']=A.groupby('vq').apply(agg)
    out['all failures overall']=agg(A)
    out['all failures thin vs heavy (vr<1)']=A.groupby(A['vr']<1).apply(agg)
    A['dq']=pd.qcut(A['depth'].rank(method='first'),3,labels=['shallow','mid','deep'])
    out['all failures by depth']=A.groupby('dq').apply(agg)
    out['all failures by year']=A.groupby('year').apply(agg)
    out['drift5 by coin']=pd.Series(drift)
    return out
