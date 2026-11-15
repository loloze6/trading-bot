def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; drows=[]
    raw='debug_info.components.above_ma.last_history_value'
    for coin,wins in data["bars"].items():
        rets=[]
        for w,b in wins.items():
            c=b['close'].values
            rets.append(pd.Series(c).pct_change().dropna())
        mu=pd.concat(rets).mean()
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b['close']
            r1=c.pct_change()
            df=pd.DataFrame({
              'coin':coin,'win':w,
              'fc':b['forecast'],'dist':b[raw] if raw in b else np.nan,
              'alloc':b['postRebalance_current_allocation'],
              'past20':c/c.shift(20)-1,'past5':c/c.shift(5)-1,
              'vol20':r1.rolling(20).std(),
              'f20':c.shift(-20)/c-1-20*mu,'f5':c.shift(-5)/c-1-5*mu,
              'pos':np.arange(len(b))})
            rows.append(df)
        for w,d in data["days"][coin].items():
            d=d.copy(); d['coin']=coin; d['win']=w; drows.append(d)
    A=pd.concat(rows)
    g20=A[A.pos%20==0].dropna(subset=['f20'])
    g5=A[A.pos%5==0].dropna(subset=['f5'])
    out={}
    def tab(df,col,y,q=5):
        d=df.dropna(subset=[col,y]).copy()
        d['b']=d.groupby('coin')[col].transform(lambda s: pd.qcut(s.rank(method='first'),q,labels=False))
        t=d.groupby('b')[y].agg(['mean','count','std'])
        t['t']=t['mean']/(t['std']/np.sqrt(t['count']))
        t['hit']=d.groupby('b')[y].apply(lambda s:(s>0).mean())
        return t.drop(columns='std').round(4)
    out['f20 by dist quintile (per coin)']=tab(g20,'dist','f20')
    out['f20 by past20 quintile']=tab(g20,'past20','f20')
    out['f5 by past5 quintile']=tab(g5,'past5','f5')
    out['f20 by vol20 quintile']=tab(g20,'vol20','f20')
    pos=g20[g20.fc>0].copy()
    out['f20 by forecast quintile (fc>0)']=tab(pos,'fc','f20')
    out['f20 fc==0 vs >0']=g20.groupby(g20.fc>0)['f20'].agg(['mean','count']).round(4)
    D=pd.concat(drows); D['ts']=pd.to_datetime(D['day'])
    D['wd']=D.ts.dt.dayofweek; D['yr']=D.ts.dt.year
    out['coin_return by weekday']=D.groupby('wd')['coin_return'].agg(['mean','count']).round(5)
    out['book by year']=D.groupby('yr')[['book_return','coin_return']].mean().round(5)
    # book extremes
    Dd=D.dropna(subset=['book_return'])
    q=Dd.book_return.quantile([0.01,0.99])
    out['book tail days count & coin ret']=pd.DataFrame({
      'n':[ (Dd.book_return<q.iloc[0]).sum(), (Dd.book_return>q.iloc[1]).sum()],
      'coin_ret':[Dd.coin_return[Dd.book_return<q.iloc[0]].mean(),Dd.coin_return[Dd.book_return>q.iloc[1]].mean()]},index=['worst1%','best1%']).round(4)
    # timing vs market
    a=A.groupby('coin')['alloc'].mean()
    out['mean alloc by coin']=a.round(3)
    # drawdown by coin of book
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            t=t.copy(); t['coin']=coin; tr.append(t)
    T=pd.concat(tr)
    T['dur_d']=T.duration_minutes/1440
    T['db']=pd.qcut(T.dur_d.rank(method='first'),4,labels=False)
    out['trades by duration quartile']=T.groupby('db').agg(n=('dur_d','size'),dur=('dur_d','mean'),pl=('net_profit_loss_percent','mean'),win=('net_profit_loss_percent',lambda s:(s>0).mean())).round(3)
    return out
