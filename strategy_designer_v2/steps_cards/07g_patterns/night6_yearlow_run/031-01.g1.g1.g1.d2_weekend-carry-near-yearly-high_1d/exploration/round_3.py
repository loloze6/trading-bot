import pandas as pd, numpy as np

def _slope(df, x, y, key='ts'):
    d=df.dropna(subset=[x,y])
    if len(d)<30: return (np.nan,np.nan,0,len(d))
    xv=d[x]-d[x].mean(); b=(xv*d[y]).sum()/(xv**2).sum()
    a=d[y].mean()-b*d[x].mean(); res=d[y]-a-b*d[x]
    sc=(xv*res).groupby(d[key]).sum(); G=len(sc)
    se=np.sqrt((sc**2).sum()*G/(G-1))/(xv**2).sum()
    return b, b/se, G, len(d)

def _clt(df,col,key='ts'):
    n=len(df); m=df[col].mean(); dev=(df[col]-m).groupby(df[key]).sum(); G=len(dev)
    se=np.sqrt((dev**2).sum()*G/(G-1))/n
    return m/se, G

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        r1all=[]; 
        for w,b in wins.items():
            c=b['close'].values; r1all+=list(c[1:]/c[:-1]-1)
        m1=np.mean(r1all); s1=np.std(r1all)
        for w,b in wins.items():
            b=b.reset_index(drop=True); ts=pd.to_datetime(b['timestamp']); c=b['close']
            r=c.pct_change(); vol=r.rolling(30,min_periods=15).std()
            d=pd.DataFrame({'ts':ts.dt.normalize(),'wd':ts.dt.weekday,'coin':coin,'yr':ts.dt.year,
               'd1':c.shift(-1)/c-1-m1,'ret14':c/c.shift(14)-1,'ret7':c/c.shift(7)-1,'vol':vol})
            d['ret14n']=d.ret14/(d.vol*np.sqrt(14)); d['ret7n']=d.ret7/(d.vol*np.sqrt(7))
            d['d1n']=d.d1/s1
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    out={}
    tab=[]
    for wd in range(7):
        s=A[A.wd==wd]
        for x in ['ret14n','ret7n']:
            b,t,G,n=_slope(s,x,'d1'); tab.append([wd,x,b,t,G,n])
    out['next-day excess slope on trend, by weekday of signal bar']=pd.DataFrame(tab,columns=['wd','x','slope','t','days','n'])
    TF=A[A.wd.isin([3,4])].dropna(subset=['ret14n','d1']).copy()
    tab=[]
    for lab,s in [('<=2021',TF[TF.yr<=2021]),('>=2022',TF[TF.yr>=2022])]:
        b,t,G,n=_slope(s,'ret14n','d1'); tab.append([lab,b,t,G,n])
    for coin,s in TF.groupby('coin'):
        b,t,G,n=_slope(s,'ret14n','d1'); tab.append([coin,b,t,G,n])
    out['Thu+Fri next-day slope on ret14n by half and coin']=pd.DataFrame(tab,columns=['grp','slope','t','days','n'])
    TF['q']=pd.qcut(TF.ret14n,5,labels=False)
    tab=[]
    for k,s in TF.groupby('q'):
        t,G=_clt(s,'d1'); tab.append([k,s.ret14n.mean(),s.d1.mean(),s.d1n.mean(),t,G])
    out['Thu+Fri next-day excess by ret14n quintile']=pd.DataFrame(tab,columns=['q','ret14n','mean','strength','t','days'])
    O=A[~A.wd.isin([3,4])]
    b,t,G,n=_slope(O,'ret14n','d1'); out['other weekdays next-day slope']=f"slope {b:.5f} t {t:.2f} days {G} n {n}"
    return out
