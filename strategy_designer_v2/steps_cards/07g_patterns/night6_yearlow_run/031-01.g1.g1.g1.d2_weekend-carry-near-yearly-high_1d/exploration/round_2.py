import pandas as pd, numpy as np
from scipy import stats

def _clt(df, col, key='ts'):
    g = df.groupby(key)[col].sum()
    # day-clustered: sum deviations per day; t of mean over cases
    n=len(df); m=df[col].mean()
    dev=(df[col]-m).groupby(df[key]).sum()
    G=len(dev)
    if G<3: return (np.nan,G)
    se=np.sqrt((dev**2).sum()*G/(G-1))/n
    return (m/se, G)

def _slope(df, x, y, key='ts'):
    d=df.dropna(subset=[x,y])
    xv=d[x]-d[x].mean(); b=(xv*d[y]).sum()/(xv**2).sum()
    a=d[y].mean()-b*d[x].mean(); res=d[y]-a-b*d[x]
    sc=(xv*res).groupby(d[key]).sum(); G=len(sc)
    se=np.sqrt((sc**2).sum()*G/(G-1))/(xv**2).sum()
    return b, b/se, G, len(d)

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        r2all=[]; r1all=[]
        for w,b in wins.items():
            c=b['close'].values; idx=np.arange(0,len(c)-2,2)
            r2all+=list(c[idx+2]/c[idx]-1); r1all+=list(c[1:]/c[:-1]-1)
        m2=np.mean(r2all); s2=np.std(r2all); m1=np.mean(r1all)
        for w,b in wins.items():
            b=b.reset_index(drop=True); ts=pd.to_datetime(b['timestamp']); c=b['close']
            r=c.pct_change(); vol=r.rolling(30,min_periods=15).std()
            hi=b['high'].rolling(365,min_periods=91).max()
            d=pd.DataFrame({'ts':ts.dt.normalize(),'wd':ts.dt.weekday,'coin':coin,
               'ex2':c.shift(-2)/c-1-m2,'d1':c.shift(-1)/c-1-m1,'d2':c.shift(-2)/c.shift(-1)-1-m1,
               'ret14':c/c.shift(14)-1,'ret30':c/c.shift(30)-1,'ret60':c/c.shift(60)-1,
               'vol':vol,'dist':c/hi-1,
               'bk':b['postRebalance_total_value'].shift(-2)/b['postRebalance_total_value']-1,
               'al':b['postRebalance_current_allocation']})
            d['ret14n']=d.ret14/(d.vol*np.sqrt(14)); d['ret30n']=d.ret30/(d.vol*np.sqrt(30))
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    out={}
    tab=[]
    for wd in range(7):
        s=A[A.wd==wd]
        for x in ['ret14n','ret30n','dist']:
            b,t,G,n=_slope(s,x,'ex2'); tab.append([wd,x,b,t,G,n])
    out['2-day excess slope on trend/dist, by weekday of start']=pd.DataFrame(tab,columns=['wd','x','slope','t','days','n'])
    F=A[A.wd==4].copy()
    tab=[]
    for x in ['ret14n','ret30n','ret60','dist']:
        for y in ['d1','d2']:
            b,t,G,n=_slope(F,x,y); tab.append([x,y,b,t,G,n])
    out['Fri: Sat (d1) vs Sun (d2) slope']=pd.DataFrame(tab,columns=['x','y','slope','t','days','n'])
    # non-Friday days pooled, graded ret14n
    NF=A[A.wd!=4]
    b,t,G,n=_slope(NF,'ret14n','ex2'); out['non-Fri ret14n slope']=f"slope {b:.5f} t {t:.2f} days {G} n {n}"
    F2=F.dropna(subset=['ret30n','ex2']).copy(); F2['q']=pd.qcut(F2.ret30n,5,labels=False)
    tab=[]
    for k,s in F2.groupby('q'):
        t,G=_clt(s,'ex2'); tab.append([k,s.ret30n.mean(),s.ex2.mean(),t,G])
    out['Fri weekend excess by vol-scaled 30d ret quintile']=pd.DataFrame(tab,columns=['q','ret30n','mean','t','days'])
    # half split robustness of Fri ret30n slope
    F2['yr']=F2.ts.dt.year
    tab=[]
    for lab,s in [('<=2021',F2[F2.yr<=2021]),('>=2022',F2[F2.yr>=2022])]:
        b,t,G,n=_slope(s,'ret30n','ex2'); tab.append([lab,b,t,G,n])
    out['Fri ret30n slope by half']=pd.DataFrame(tab,columns=['half','slope','t','days','n'])
    # book: largest gains/losses on active fridays
    act=A[(A.wd==4)&(A.al>0)].dropna(subset=['bk'])
    act=act.assign(q=pd.qcut(act.bk,10,labels=False))
    out['book 2d return deciles on active Fri: mean ret14n, dist, vol']=act.groupby('q')[['bk','ret14n','dist','vol']].mean()
    return out
