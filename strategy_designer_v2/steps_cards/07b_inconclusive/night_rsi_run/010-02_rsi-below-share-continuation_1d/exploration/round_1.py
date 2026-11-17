def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    col='debug_info.components.rsi_below_share.last_history_value'
    out={}
    def grid(h):
        rows=[]
        for c,ws in data["bars"].items():
            for w,b in ws.items():
                b=b.reset_index(drop=True)
                cl=b['close'].values
                for i in range(0,len(b)-h,h):
                    rows.append(dict(coin=c,win=w,year=pd.Timestamp(b['timestamp'].iloc[i]).year,
                        f=b['forecast'].iloc[i],share=b[col].iloc[i] if col in b else np.nan,
                        r=cl[i+h]/cl[i]-1))
        g=pd.DataFrame(rows)
        g['ex']=g['r']-g.groupby('coin')['r'].transform('mean')
        g['p']=g['f']/10*g['ex']
        return g
    def tt(s):
        s=s.dropna(); return pd.Series(dict(n=len(s),mean=s.mean(),t=s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan))
    g=grid(14)
    out['all14']=tt(g['p'])
    out['by_coin']=g.groupby('coin')['p'].apply(tt).unstack()
    out['by_year']=g.groupby('year')['p'].apply(tt).unstack()
    g['side']=np.where(g['f']>0,'long','short')
    out['by_side']=g.groupby('side')['p'].apply(tt).unstack()
    g['fq']=pd.qcut(g['f'].abs(),4,labels=False,duplicates='drop')
    out['by_absf_q']=g.groupby('fq')['p'].apply(tt).unstack()
    g['sq']=pd.qcut(g['share'],5,labels=False,duplicates='drop')
    out['ex_by_share_q']=g.groupby('sq').agg(n=('ex','size'),share=('share','mean'),ex=('ex','mean'),r=('r','mean'))
    rh={}
    for h in [3,7,21,28,42]:
        gh=grid(h); s=tt(gh['p']); rh[h]=s
        rh[h]['spearman_share']=stats.spearmanr(gh['share'],gh['ex'],nan_policy='omit')[0]
    out['by_horizon']=pd.DataFrame(rh).T
    # market regime: coin's past 60-day return sign at grid
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True); cl=b['close']
            m=cl/cl.shift(60)-1
            for i in range(0,len(b)-14,14):
                rows.append(m.iloc[i])
    g['m60']=rows
    g['trend']=np.where(g['m60'].isna(),'na',np.where(g['m60']>0,'up60','down60'))
    out['by_trend']=g.groupby(['trend','side'])['p'].apply(tt).unstack()
    return out
