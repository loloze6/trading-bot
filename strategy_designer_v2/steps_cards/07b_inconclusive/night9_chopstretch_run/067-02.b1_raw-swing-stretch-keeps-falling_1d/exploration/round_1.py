def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    col='debug_info.components.stretch_below.last_history_value'
    rows=[]
    for coin,ws in data['bars'].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df['close'].values; n=len(c)
            ts=pd.to_datetime(df['timestamp'])
            for h in (3,5,10,20):
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,i=i,year=ts[i].year,day=ts[i].normalize(),
                        ret=c[i+h]/c[i]-1,reg=df['regime'].iloc[i],
                        s=df[col].iloc[i] if col in df else np.nan))
    d=pd.DataFrame(rows)
    d['ex']=d['ret']-d.groupby(['coin','h'])['ret'].transform('mean')
    ch=d[(d.reg=='unknown')&d.s.notna()].copy()
    out={}
    def reg(g):
        if len(g)<10: return pd.Series({'n':len(g)})
        r=stats.linregress(g.s,g.ex)
        return pd.Series({'n':len(g),'slope':r.slope,'t':r.slope/r.stderr,'mean_ex':g.ex.mean(),'t_mean':g.ex.mean()/(g.ex.std()/np.sqrt(len(g)))})
    ch['side']=np.where(ch.s<0,'below','above')
    out['by_h_side']=ch.groupby(['h','side']).apply(reg)
    out['by_h_all']=ch.groupby('h').apply(reg)
    c10=ch[ch.h==10].copy()
    c10['q']=pd.qcut(c10.s,5,labels=False)
    out['quint10']=c10.groupby('q').agg(n=('ex','size'),s=('s','mean'),ex=('ex','mean'),ret=('ret','mean'))
    c5=ch[ch.h==5].copy(); c5['q']=pd.qcut(c5.s,5,labels=False)
    out['quint5']=c5.groupby('q').agg(n=('ex','size'),s=('s','mean'),ex=('ex','mean'))
    b10=c10[c10.s<0]
    out['below10_coin']=b10.groupby('coin').apply(reg)
    out['below10_year']=b10.groupby('year').apply(reg)
    out['all10_coin']=c10.groupby('coin').apply(reg)
    out['share_choppy']=float((d[d.h==10].reg=='unknown').mean())
    return out
