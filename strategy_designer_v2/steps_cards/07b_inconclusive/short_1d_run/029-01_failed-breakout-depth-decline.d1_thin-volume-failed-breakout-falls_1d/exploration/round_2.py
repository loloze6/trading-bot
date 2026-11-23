import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H=5
    drift={}; usual={}
    comp='debug_info.components.thin_failed_breakout.last_history_value'
    for coin, wins in data["bars"].items():
        rets=[]
        for w,df in wins.items():
            c=df['close'].values
            for i in range(0,len(c)-H,H): rets.append(c[i+H]/c[i]-1)
        drift[coin]=np.mean(rets); usual[coin]=np.std(rets)
    rows=[]; allf=[]
    for coin, wins in data["bars"].items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df['close'].values; v=df['volume'].values; n=len(c)
            f=df['forecast'].fillna(0).values
            raw=df[comp].values if comp in df else np.full(n,np.nan)
            hi=pd.Series(c).shift(1).rolling(20).max().values
            vr=(pd.Series(v)/pd.Series(v).rolling(20).mean()).values
            for s in range(0,n,H):
                done=False; doneA=False
                for t in range(s,min(s+H,n)):
                    if t+H>=n: break
                    r=c[t+H]/c[t]-1
                    if not done and t>0 and f[t]-f[t-1]<=-2:
                        done=True
                        rows.append(dict(coin=coin,raw=raw[t],un=-(r-drift[coin]),tot=-r,st=-(r-drift[coin])/usual[coin]))
                    if not doneA and t>=24:
                        for j in (t-1,t-2,t-3):
                            if j>=0 and not np.isnan(hi[j]) and c[j]>hi[j] and c[t]<hi[j] and all(c[k]>=hi[j] for k in range(j,t)):
                                doneA=True
                                allf.append(dict(coin=coin,vr=vr[j],un=-(r-drift[coin]),thin=max(0,1-vr[j])))
                                break
    R=pd.DataFrame(rows).dropna(subset=['raw']); A=pd.DataFrame(allf).dropna()
    out={}
    sp=stats.spearmanr(R['raw'],R['un']); out['tested: spearman raw vs unusual']=pd.Series(dict(rho=sp[0],p=sp[1],n=len(R)))
    med=R['raw'].median()
    a=R[R.raw>med]['un']; b=R[R.raw<=med]['un']
    out['tested: raw upper half minus lower half']=pd.Series(dict(diff=a.mean()-b.mean(),t=stats.ttest_ind(a,b,equal_var=False)[0],na=len(a),nb=len(b)))
    out['tested: strength mean']=R['st'].mean()
    out['tested: share of cases with raw==0']=(R['raw']<=0).mean()
    th=A[A.vr<1]['un']; hv=A[A.vr>=1]['un']
    out['all failures thin minus heavy']=pd.Series(dict(diff=th.mean()-hv.mean(),t=stats.ttest_ind(th,hv,equal_var=False)[0],nt=len(th),nh=len(hv)))
    sp2=stats.spearmanr(A['vr'],A['un']); out['all failures spearman volratio vs unusual']=pd.Series(dict(rho=sp2[0],p=sp2[1],n=len(A)))
    out['all failures thin by coin']=A[A.vr<1].groupby('coin')['un'].agg(['count','mean'])
    return out
