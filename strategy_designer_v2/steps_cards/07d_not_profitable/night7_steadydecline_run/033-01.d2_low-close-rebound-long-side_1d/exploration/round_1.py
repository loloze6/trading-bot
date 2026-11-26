def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]; trades=data["trades"]
    rows=[]; gaps=[]
    for c in bars:
        ws=sorted(bars[c].keys(), key=lambda w:int(w[1:]))
        allc=[]
        prev_end=None
        for w in ws:
            b=bars[c][w].copy()
            b['ts']=pd.to_datetime(b['timestamp'])
            if prev_end is not None: gaps.append((b['ts'].iloc[0]-prev_end).days)
            prev_end=b['ts'].iloc[-1]
            b['w']=w; b['coin']=c
            allc.append(b)
        a=pd.concat(allc,ignore_index=True)
        # indicators on the concatenated closes (indicators only)
        r=a['close'].pct_change()
        a['tr60']=a['close']/a['close'].shift(60)-1
        v30=r.rolling(30).std()
        a['agit']=v30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
        a['rng']=(a['high']-a['low'])/a['close']
        a['rngrel']=a['rng']/a['rng'].rolling(20).mean().shift(1)
        a['ret1']=a['close']/a['open']-1
        a['ret3']=a['close']/a['close'].shift(3)-1
        a['cl']=(a['close']-a['low'])/(a['high']-a['low'])
        # forward within window
        a['fwd']=a.groupby('w')['close'].shift(-1)/a['close']-1
        a['pos']=a['postRebalance_current_allocation']
        a['gain']=a['pos']*a['fwd']
        rows.append(a)
    A=pd.concat(rows,ignore_index=True)
    A=A[A['fwd'].notna()]
    drift=A.groupby('coin')['fwd'].mean()
    A['ex']=A['fwd']-A['coin'].map(drift)
    A['trend']=np.where(A['tr60']>0.10,'rising',np.where(A['tr60']<-0.10,'falling','choppy'))
    A.loc[A['tr60'].isna(),'trend']='na'
    A['ag']=np.where(A['agit'].isna(),'na',np.where(A['agit']>0.5,'agit','calm'))
    A['prof']=A['trend']+'_'+A['ag']
    out={}
    out['gap_days_between_windows']=pd.Series(gaps).describe()
    def g(df,key):
        x=df.groupby(key).agg(n=('ex','size'),ex=('ex','mean'),sd=('ex','std'),fwd=('fwd','mean'),gain=('gain','mean'),pos=('pos','mean'))
        x['t']=x['ex']/(x['sd']/np.sqrt(x['n'])); return x.drop(columns='sd')
    A['clb']=pd.cut(A['cl'],[-0.01,0.1,0.2,0.3,0.4,0.5,0.7,1.01])
    out['by_cl']=g(A,'clb')
    L=A[A['cl']<0.5].copy(); H=A[A['cl']>=0.5].copy()
    L['rq']=pd.qcut(L['rngrel'],4,labels=['r1','r2','r3','r4']); H['rq']=pd.qcut(H['rngrel'],4,labels=['r1','r2','r3','r4'])
    out['low_by_rangerel']=g(L,'rq'); out['high_by_rangerel']=g(H,'rq')
    L['d1']=pd.qcut(L['ret1'],4,labels=['q1dn','q2','q3','q4up'])
    out['low_by_dayreturn']=g(L,'d1')
    out['low_by_profile']=g(L,'prof'); out['high_by_profile']=g(H,'prof')
    out['low_by_trend']=g(L,'trend'); out['high_by_trend']=g(H,'trend')
    out['low_by_year']=g(L,A.loc[L.index,'ts'].dt.year)
    # book daily
    D=[]
    for c in days:
        for w in days[c]:
            d=days[c][w].copy(); d['coin']=c; d['w']=w; D.append(d)
    D=pd.concat(D)
    bk=D.groupby(['w','day'])['book_return'].mean().dropna().reset_index()
    bk['wn']=bk['w'].str[1:].astype(int); bk=bk.sort_values(['wn','day'])
    v=(1+bk['book_return']).cumprod(); dd=v/v.cummax()-1
    out['book_maxdd']=float(dd.min())
    bk['dd']=dd.values
    out['book_by_window']=bk.groupby('wn').agg(mean=('book_return','mean'),sd=('book_return','std'),mindd=('dd','min'))
    # trades
    T=pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c]])
    out['trades']=pd.Series({'n':len(T),'gross_mean':T['profit_loss_percent'].mean(),'net_mean':T['net_profit_loss_percent'].mean(),'dur_days_mean':T['duration_minutes'].mean()/1440})
    # turnover: allocation change on regime bars
    A['dalloc']=(A['pos']-A['previous_allocation']).abs()
    out['turnover']=pd.Series({'mean_abs_alloc_change':A['dalloc'].mean(),'mean_abs_pos':A['pos'].abs().mean(),'gross_gain_mean':A['gain'].mean()})
    return out
