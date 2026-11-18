import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=3
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            cl=b.close; hi=b.high; lo=b.low; v=b.volume
            r1=cl.pct_change()
            f=pd.DataFrame({
              'coin':c,'win':w,
              'fwd':cl.shift(-H)/cl-1,
              'r1':r1,'r5':cl/cl.shift(5)-1,'r20':cl/cl.shift(20)-1,
              'vol20':r1.rolling(20).std(),
              'dhi':cl/hi.shift(1).rolling(20).max()-1,
              'dlo':cl/lo.shift(1).rolling(20).min()-1,
              'comp':1-(hi.rolling(10).max()-lo.rolling(10).min())/(hi.rolling(40).max()-lo.rolling(40).min()),
              'vrat':v.rolling(5).mean()/v.rolling(30).mean(),
              'rng':(hi-lo)/cl,
              'wd':pd.to_datetime(b.timestamp).dt.weekday,
              'fc':b.forecast,'pos':b.postRebalance_current_allocation})
            f=f.iloc[::H]
            rows.append(f)
    d=pd.concat(rows).dropna(subset=['fwd'])
    d['ex']=d.fwd-d.groupby('coin').fwd.transform('mean')
    d['absfwd']=d.fwd.abs()
    out={}
    out['n_grid']=len(d)
    summ=[]
    for k in ['r1','r5','r20','vol20','dhi','dlo','comp','vrat','rng']:
        x=d.dropna(subset=[k]).copy()
        x['q']=x.groupby('coin')[k].transform(lambda s: pd.qcut(s.rank(method='first'),5,labels=False))
        g=x.groupby('q').ex.mean()
        ga=x.groupby('q').absfwd.mean()
        rho,p=stats.spearmanr(x[k],x.ex)
        rho2,p2=stats.spearmanr(x[k],x.absfwd)
        tq=stats.ttest_ind(x.ex[x.q==4],x.ex[x.q==0],equal_var=False)
        summ.append(dict(f=k,n=len(x),q1=g[0],q3=g[2],q5=g[4],t_q5q1=tq.statistic,rho=rho,p=p,absq1=ga[0],absq5=ga[4],rho_abs=rho2,p_abs=p2))
    out['feature_quintiles_ex3d']=pd.DataFrame(summ).round(4)
    wd=d.groupby('wd').ex.agg(['mean','count','std']); wd['t']=wd['mean']/(wd['std']/np.sqrt(wd['count']))
    out['weekday']=wd.round(4)
    # by coin: break vs not
    d['brk']=d.dhi>0
    out['brk_by_coin']=d.groupby(['coin','brk']).ex.agg(['mean','count']).unstack().round(4)
    # book daily
    dd=[]
    for c,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x['coin']=c; x['win']=w; dd.append(x)
    D=pd.concat(dd)
    out['book_by_coin']=D.groupby('coin')[['book_return','coin_return']].agg(['mean','std']).round(5)
    out['book_by_window']=D.groupby('win').book_return.agg(['mean','count']).round(5).T
    return out
