def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out={}
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d['coin']=coin; d['win']=w; D.append(d)
    D=pd.concat(D); D['ts']=pd.to_datetime(D['day']); D['wd']=D.ts.dt.dayofweek
    Dc=D.dropna(subset=['coin_return'])
    # weekday t-stats and per-coin consistency
    wt=Dc.groupby('wd')['coin_return'].agg(['mean','std','count'])
    wt['t']=wt['mean']/(wt['std']/np.sqrt(wt['count']))
    out['weekday coin ret t']=wt.drop(columns='std').round(5)
    out['weekday mean by coin']=Dc.pivot_table(index='coin',columns='wd',values='coin_return',aggfunc='mean').round(4)
    # Welch weekend(Fri+Sat) vs rest
    a=Dc.coin_return[Dc.wd.isin([4,5])]; b=Dc.coin_return[~Dc.wd.isin([4,5])]
    out['FriSat minus rest']=pd.Series({'diff':a.mean()-b.mean(),'t':stats.ttest_ind(a,b,equal_var=False).statistic,'nA':len(a),'nB':len(b)}).round(5)
    # timing decomposition
    rows=[]
    for coin,wins in data["bars"].items():
        mu=pd.concat([w['close'].pct_change().dropna() for w in wins.values()]).mean()
        for w,bb in wins.items():
            bb=bb.reset_index(drop=True)
            c=bb['close']; r=c.pct_change()
            al=bb['postRebalance_current_allocation']
            fc=bb['forecast']
            # bars since forecast turned positive
            on=(fc>0).astype(int)
            grp=(on.diff()!=0).cumsum()
            age=on.groupby(grp).cumcount()*on
            df=pd.DataFrame({'coin':coin,'win':w,'pos':np.arange(len(bb)),'fc':fc,'age':age,
              'alloc':al,'gain':al*r.shift(-1),'mkt':al*mu,
              'r1':r,'absz':r/r.rolling(20).std().shift(1),
              'f5':c.shift(-5)/c-1-5*mu,'f20':c.shift(-20)/c-1-20*mu,
              'vol60':r.rolling(60).std()})
            rows.append(df)
    A=pd.concat(rows)
    out['decomp gain vs market part (per bar)']=pd.Series({'gain':A.gain.mean(),'market':A.mkt.mean()}).round(6)
    # returns after large daily moves, by z quintile, non-overlap 5 grid
    g5=A[A.pos%5==0].dropna(subset=['f5','absz']).copy()
    g5['b']=pd.qcut(g5.absz.rank(method='first'),5,labels=False)
    t=g5.groupby('b')['f5'].agg(['mean','std','count']); t['t']=t['mean']/(t['std']/np.sqrt(t['count']))
    t['z']=g5.groupby('b')['absz'].mean()
    out['f5 by prior-day z quintile']=t.drop(columns='std').round(4)
    # age of above-SMA spell, grid 20
    g20=A[(A.pos%20==0)&(A.fc>0)].dropna(subset=['f20']).copy()
    g20['ab']=pd.cut(g20.age,[-1,20,60,120,10000],labels=['<=20','21-60','61-120','>120'])
    t=g20.groupby('ab')['f20'].agg(['mean','std','count']); t['t']=t['mean']/(t['std']/np.sqrt(t['count']))
    t['hit']=g20.groupby('ab')['f20'].apply(lambda s:(s>0).mean())
    out['f20 by spell age (fc>0)']=t.drop(columns='std').round(4)
    # vol60 tercile x position gain
    Ab=A.dropna(subset=['gain','vol60']).copy()
    Ab=Ab[Ab.alloc>0]
    Ab['vb']=Ab.groupby('coin')['vol60'].transform(lambda s:pd.qcut(s.rank(method='first'),3,labels=False))
    t=Ab.groupby('vb')['gain'].agg(['mean','std','count']); t['t']=t['mean']/(t['std']/np.sqrt(t['count']))
    out['position daily gain by vol60 tercile (alloc>0)']=t.drop(columns='std').round(5)
    # book drawdown per window: deepest fall per coin
    dd=[]
    for (coin,w),d in D.groupby(['coin','win']):
        v=d.book_value.values; m=np.maximum.accumulate(v); dd.append({'coin':coin,'dd':(v/m-1).min()})
    out['worst window drawdown by coin']=pd.DataFrame(dd).groupby('coin').dd.agg(['min','mean']).round(3)
    return out
