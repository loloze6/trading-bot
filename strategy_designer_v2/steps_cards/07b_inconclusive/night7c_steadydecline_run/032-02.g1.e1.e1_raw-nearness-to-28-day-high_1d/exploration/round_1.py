import pandas as pd, numpy as np
from scipy import stats

def clustered_slope(df, x, y):
    d = df.dropna(subset=[x, y])
    if len(d) < 30:
        return np.nan, np.nan, len(d)
    X = d[x].values; Y = d[y].values
    xm = X.mean(); b = ((X-xm)*(Y-Y.mean())).sum()/((X-xm)**2).sum()
    a = Y.mean()-b*xm
    e = Y-a-b*X
    g = pd.Series((X-xm)*e).groupby(d['day'].values).sum()
    G = len(g)
    se = np.sqrt((g**2).sum()*G/(G-1))/((X-xm)**2).sum()
    return b, b/se, len(d)

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close']
            hi = c.rolling(28, min_periods=28).max()
            dist = (hi/c - 1)*100
            r28 = c/c.shift(27) - 1
            fc = b['debug_info.components.high_prox.post_pipeline_value']
            for h in (5, 10):
                fwd = c.shift(-h)/c - 1
                idx = np.arange(0, len(b), h)
                for i in idx:
                    rows.append(dict(coin=coin, w=w, h=h, year=pd.Timestamp(b['timestamp'].iloc[i]).year,
                                     day=pd.Timestamp(b['timestamp'].iloc[i]).floor('D'),
                                     fc=fc.iloc[i], dist=dist.iloc[i], r28=r28.iloc[i], fwd=fwd.iloc[i]))
    df = pd.DataFrame(rows).dropna(subset=['fwd'])
    df['ex'] = df['fwd'] - df.groupby(['coin','h'])['fwd'].transform('mean')
    out = {}
    res = []
    for h in (5,10):
        d = df[df.h==h]
        for x in ('fc','dist'):
            s,t,n = clustered_slope(d, x, 'ex'); res.append(dict(h=h, x=x, slope=s, t=t, n=n))
    out['overall slopes (B,C)'] = pd.DataFrame(res)
    d5 = df[df.h==5]
    res=[]
    for k,g in d5.groupby('coin'):
        s,t,n = clustered_slope(g,'fc','ex'); res.append(dict(coin=k,slope=s,t=t,n=n))
    for k,g in d5.groupby('year'):
        s,t,n = clustered_slope(g,'fc','ex'); res.append(dict(coin=str(k),slope=s,t=t,n=n))
    out['fc slope by coin / year h5'] = pd.DataFrame(res)
    res=[]
    for k,g in d5.groupby('w'):
        s,t,n = clustered_slope(g,'fc','ex'); res.append(dict(w=k,slope=s,t=t,n=n, mean_r28=g.r28.mean()))
    out['fc slope by window h5'] = pd.DataFrame(res)
    res=[]
    for h in (5,10):
        d=df[(df.h==h)].dropna(subset=['r28'])
        for lab,g in (('r28 up', d[d.r28>0]), ('r28 down', d[d.r28<=0])):
            s,t,n = clustered_slope(g,'fc','ex'); s2,t2,_=clustered_slope(g,'dist','ex')
            res.append(dict(h=h, side=lab, fc_slope=s, fc_t=t, dist_slope=s2, dist_t=t2, n=n))
    out['by r28 sign'] = pd.DataFrame(res)
    for h in (5,10):
        d=df[df.h==h].dropna(subset=['dist']).copy()
        d['q']=pd.qcut(d['dist'].rank(method='first'),5,labels=False)
        out[f'dist quintiles h{h}']=d.groupby('q').agg(dist_mean=('dist','mean'),ex_mean=('ex','mean'),
                    n=('ex','size'), t=('ex', lambda v: v.mean()/(v.std()/np.sqrt(len(v)))))
        d['fq']=pd.qcut(d['fc'].rank(method='first'),5,labels=False)
        out[f'fc quintiles h{h}']=d.groupby('fq').agg(fc_mean=('fc','mean'),dist_mean=('dist','mean'),ex_mean=('ex','mean'),n=('ex','size'))
    return out
