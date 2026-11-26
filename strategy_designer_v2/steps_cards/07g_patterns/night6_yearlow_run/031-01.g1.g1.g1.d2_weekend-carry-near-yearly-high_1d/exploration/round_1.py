import pandas as pd, numpy as np
from scipy import stats

def _clt(df, col, key='ts'):
    # day-clustered t of mean: average per day across coins
    g = df.groupby(key)[col].mean()
    n = len(g)
    if n < 3: return (np.nan, n)
    return (g.mean()/(g.std(ddof=1)/np.sqrt(n)), n)

def explore(data):
    rows = []; fri = []
    for coin, wins in data["bars"].items():
        # coin mean 1-bar and 2-bar return over all windows (non-overlapping grid)
        r1all=[]; r2all=[]
        for w, b in wins.items():
            c = b['close'].values
            r1all += list(c[1:]/c[:-1]-1)
            idx = np.arange(0, len(c)-2, 2)
            r2all += list(c[idx+2]/c[idx]-1)
        m1=np.mean(r1all); m2=np.mean(r2all); s2=np.std(r2all)
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            ts = pd.to_datetime(b['timestamp'])
            c = b['close']
            r = c.pct_change()
            vol = r.rolling(30, min_periods=15).std()
            d = pd.DataFrame({'ts':ts.dt.normalize(), 'wd':ts.dt.weekday,
                              'r':r, 'nxt':c.shift(-1)/c-1, 'nxt2':c.shift(-2)/c-1,
                              'ret14':c/c.shift(14)-1, 'ret7':c/c.shift(7)-1,
                              'z':r/vol.shift(1), 'vol':vol,
                              'prox':b.get('debug_info.components.near_high.last_history_value'),
                              'alloc':b['postRebalance_current_allocation'],
                              'coin':coin,'win':w})
            d['ex1']=d['nxt']-m1; d['ex2']=(d['nxt2']-m2); d['ex2n']=d['ex2']/s2
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # weekday of next-day return (return of day wd+1 measured from wd close)
    wdtab=[]
    for wd in range(7):
        s=A[A.wd==wd].dropna(subset=['ex1'])
        t,n=_clt(s,'ex1'); wdtab.append([wd, s['ex1'].mean(), t, n])
    out['next-day excess return by weekday of signal bar']=pd.DataFrame(wdtab,columns=['wd','mean_ex','t_day','days'])
    F = A[(A.wd==4)].dropna(subset=['ex2','ret14']).copy()
    F['up']=F.ret14>0
    tab=[]
    for k,s in F.groupby('up'):
        t,n=_clt(s,'ex2'); tab.append([k,s.ex2.mean(),t,n,len(s)])
    out['Fri weekend excess by 14d up']=pd.DataFrame(tab,columns=['up','mean','t','days','cases'])
    F['q14']=pd.qcut(F.ret14,5,labels=False)
    tab=[]
    for k,s in F.groupby('q14'):
        t,n=_clt(s,'ex2'); tab.append([k,s.ret14.mean(),s.ex2.mean(),t,n])
    out['Fri weekend excess by ret14 quintile']=pd.DataFrame(tab,columns=['q','ret14','mean','t','days'])
    F['q7']=pd.qcut(F.ret7,5,labels=False)
    tab=[]
    for k,s in F.groupby('q7'):
        t,n=_clt(s,'ex2'); tab.append([k,s.ret7.mean(),s.ex2.mean(),t,n])
    out['Fri weekend excess by ret7 quintile']=pd.DataFrame(tab,columns=['q','ret7','mean','t','days'])
    Fv=F.dropna(subset=['vol']).copy(); Fv['qv']=Fv.groupby('coin')['vol'].transform(lambda x: pd.qcut(x,3,labels=False))
    tab=[]
    for k,s in Fv.groupby('qv'):
        t,n=_clt(s,'ex2'); tab.append([k,s.ex2.mean(),s.ex2n.mean(),t,n])
    out['Fri weekend excess by vol tercile']=pd.DataFrame(tab,columns=['q','mean','strength','t','days'])
    P=F.dropna(subset=['prox']).copy(); P['qp']=pd.qcut(P.prox,5,labels=False,duplicates='drop')
    tab=[]
    for k,s in P.groupby('qp'):
        t,n=_clt(s,'ex2'); tab.append([k,s.prox.mean(),s.ex2.mean(),t,n])
    out['active Fri weekend excess by proximity quintile']=pd.DataFrame(tab,columns=['q','prox','mean','t','days'])
    # weekend excess by year
    F['yr']=F.ts.dt.year
    tab=[]
    for k,s in F[F.up].groupby('yr'):
        t,n=_clt(s,'ex2'); tab.append([k,s.ex2.mean(),t,n])
    out['up-Fri weekend excess by year']=pd.DataFrame(tab,columns=['yr','mean','t','days'])
    tab=[]
    for k,s in F.groupby('coin'):
        a=s[s.up].ex2; b=s[~s.up].ex2
        tab.append([k,a.mean(),b.mean(),stats.ttest_ind(a,b,equal_var=False).statistic,len(a),len(b)])
    out['by coin weekend excess up vs down']=pd.DataFrame(tab,columns=['coin','up','down','welch_t','n_up','n_dn'])
    # large moves next day, all days
    Z=A.dropna(subset=['z','ex1']).copy(); Z['qz']=pd.qcut(Z.z,7,labels=False)
    tab=[]
    for k,s in Z.groupby('qz'):
        t,n=_clt(s,'ex1'); tab.append([k,s.z.mean(),s.ex1.mean(),t,n])
    out['next-day excess by today z-move septile']=pd.DataFrame(tab,columns=['q','z','mean','t','days'])
    # Friday's own return vs weekend
    tab=[]
    Fz=F.dropna(subset=['z']).copy(); Fz['qz']=pd.qcut(Fz.z,5,labels=False)
    for k,s in Fz.groupby('qz'):
        t,n=_clt(s,'ex2'); tab.append([k,s.z.mean(),s.ex2.mean(),t,n])
    out['Fri weekend excess by Friday z-move']=pd.DataFrame(tab,columns=['q','z','mean','t','days'])
    return out
