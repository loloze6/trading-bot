def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    B=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy(); b['coin']=c; b['window']=w
            b['prevhi']=b['high'].rolling(20).max().shift(1)
            b['on']=b['close']>b['prevhi']
            hi20=b['high'].rolling(20).max(); lo20=b['low'].rolling(20).min()
            hi100=b['high'].rolling(100).max(); lo100=b['low'].rolling(100).min()
            b['comp']=1-(hi20-lo20)/(hi100-lo100)
            b['ret20']=b['close']/b['close'].shift(20)-1
            for h in [3,10,20]:
                b[f'f{h}']=b['close'].shift(-h)/b['close']-1
            b['r1']=b['close'].shift(-1)/b['close']-1
            # days since last break (within 10/20 days)
            last=pd.Series(np.where(b['on'],np.arange(len(b)),np.nan)).ffill().values
            b['since']=np.arange(len(b))-last
            b['pos_i']=np.arange(len(b))
            b['year']=pd.to_datetime(b['timestamp']).dt.year
            B.append(b)
    B=pd.concat(B,ignore_index=True)
    for h in [3,10,20]:
        B[f'x{h}']=B[f'f{h}']-B['coin'].map(B[B['pos_i']%h==0].groupby('coin')[f'f{h}'].mean())
    # non-overlapping grid t-stats for break bars
    res={}
    for h in [3,10,20]:
        g=B[(B['pos_i']%h==0)&B['on']][f'x{h}'].dropna()
        res[h]=dict(n=len(g),mean=g.mean(),t=g.mean()/(g.std()/np.sqrt(len(g))))
        gc=B[(B['pos_i']%h==0)&B['on']].dropna(subset=[f'x{h}','comp'])
        sl=stats.linregress(gc['comp'],gc[f'x{h}'])
        res[h].update(slope_comp=sl.slope,t_comp=sl.slope/sl.stderr)
        sl2=stats.linregress(gc['ret20'],gc[f'x{h}'])
        res[h].update(slope_r20=sl2.slope,t_r20=sl2.slope/sl2.stderr)
    out['grid_break']=pd.DataFrame(res).T
    g=B[(B['pos_i']%20==0)&B['on']]
    out['x20_by_coin']=g.groupby('coin')['x20'].agg(['mean','count'])
    out['x20_by_year']=g.groupby('year')['x20'].agg(['mean','count'])
    # hypothetical book: long 1 for K days after any break, daily return r1, mean over coins per day
    hb={}
    for K in [1,5,10,20]:
        B['pos']=((B['since']<K)).astype(float)
        B['g']=B['pos']*B['r1']
        d=B.dropna(subset=['r1'])
        day=d.groupby(['window','timestamp'])['g'].mean()
        cm=B.groupby('coin')['r1'].mean()
        mk=(B['pos']*B['coin'].map(cm)).mean()
        # calmar
        eq=[];v=1.0
        for w in sorted(day.index.get_level_values(0).unique(),key=lambda s:int(s[1:])):
            for r in day.loc[w].values:
                v*=1+r; eq.append(v)
        eq=np.array(eq); dd=(eq/np.maximum.accumulate(eq)-1).min()
        yr=eq[-1]**(365/len(eq))-1
        hb[K]=dict(inpos=B['pos'].mean(),mean=day.mean(),sharpe=day.mean()/day.std()*np.sqrt(365),calmar=yr/abs(dd),mkt=mk,timing=B['g'].mean()-mk)
    out['hyp_hold_after_break']=pd.DataFrame(hb).T
    # forward x20 by comp quartile on grid; by since-break bucket for non-break bars
    g10=B[(B['pos_i']%10==0)].copy()
    g10['sb']=pd.cut(g10['since'],[-1,0,5,10,20,40,1e9])
    out['x10_by_since']=g10.groupby('sb')['x10'].agg(['mean','count'])
    return out
