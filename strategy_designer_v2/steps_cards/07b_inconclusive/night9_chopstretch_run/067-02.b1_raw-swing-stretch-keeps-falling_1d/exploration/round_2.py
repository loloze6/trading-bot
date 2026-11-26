def explore(data):
    import numpy as np, pandas as pd
    col='debug_info.components.stretch_below.last_history_value'
    rows=[]
    for coin,ws in data['bars'].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df['close'].values; n=len(c)
            ts=pd.to_datetime(df['timestamp'])
            for h in (5,10):
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,year=ts[i].year,day=ts[i].normalize(),
                        ret=c[i+h]/c[i]-1,reg=df['regime'].iloc[i],
                        s=df[col].iloc[i] if col in df else np.nan))
    d=pd.DataFrame(rows)
    d['ex']=d['ret']-d.groupby(['coin','h'])['ret'].transform('mean')
    sd=d.groupby(['coin','h'])['ret'].transform('std')
    d['str']=d['ex']*np.sign(d['s'])/sd
    ch=d[(d.reg=='unknown')&d.s.notna()].copy()
    def cl(g):
        g=g.dropna(subset=['s','ex'])
        if len(g)<10: return pd.Series({'n':len(g)})
        x=g.s.values; y=g.ex.values; xm=x-x.mean()
        b=(xm*(y-y.mean())).sum()/(xm**2).sum(); a=y.mean()-b*x.mean()
        e=y-a-b*x
        sc=pd.Series(xm*e).groupby(g.day.values).sum()
        G=len(sc); se=np.sqrt((sc**2).sum()*G/(G-1))/(xm**2).sum()
        sm=pd.Series(g.ex.values*np.sign(x)).groupby(g.day.values).sum()
        tm=sm.mean()/(sm.std()/np.sqrt(G))
        return pd.Series({'n':len(g),'days':G,'slope':b,'t_cl':b/se,
                          'dirmean':(g.ex*np.sign(g.s)).mean(),'t_dir_cl':tm,'strength':g['str'].mean()})
    out={}
    out['all_h']=ch.groupby('h').apply(cl)
    out['all_h_year']=ch.groupby(['h','year']).apply(cl)
    out['all_h_coin']=ch.groupby(['h','coin']).apply(cl)
    ch['side']=np.where(ch.s<0,'below','above')
    out['h_side']=ch.groupby(['h','side']).apply(cl)
    return out
