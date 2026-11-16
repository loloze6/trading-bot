def explore(data):
    import pandas as pd, numpy as np
    bars=data["bars"]
    rows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.copy()
            col='debug_info.components.run.post_pipeline_value'
            b['s']=pd.to_numeric(b[col],errors='coerce') if col in b.columns else np.nan
            b['nxt']=b['close'].shift(-1)/b['close']-1
            b['a']=b['postRebalance_current_allocation']
            b['gain']=b['a']*b['nxt']
            b['r30']=b['close']/b['close'].shift(30)-1
            b['r10']=b['close']/b['close'].shift(10)-1
            b['f10']=b['close'].shift(-10)/b['close']-1
            b['grid']=(np.arange(len(b))%10==0)
            b['coin']=c; b['wn']=int(w[1:])
            b['year']=pd.to_datetime(b['timestamp']).dt.year
            rows.append(b)
    B=pd.concat(rows)
    out={}
    mu=B[B.grid].groupby('coin')['f10'].mean()
    B['ex10']=B['f10']-B['coin'].map(mu)
    T=B[B.regime=='trending']
    G=T[T.grid].dropna(subset=['ex10','r30'])
    tt=lambda x:x.mean()/x.std()*np.sqrt(len(x))
    Gp=G[G.r30>0].copy(); Gp['b']=pd.qcut(Gp['r30'],5)
    out['trending grid r30>0 quintiles ex10']=Gp.groupby('b')['ex10'].agg(['size','mean',tt])
    Gp['rb']=pd.qcut(Gp['r10'],4)
    out['trending r30>0 grid ex10 by r10 quartile']=Gp.groupby('rb')['ex10'].agg(['size','mean',tt])
    Gn=G[G.r30<=0]
    out['trending r30<=0 grid ex10']=pd.Series({'n':len(Gn),'mean':Gn['ex10'].mean(),'t':tt(Gn['ex10'])})
    S=T[T.a<0]
    out['short bars by year']=S.groupby('year').agg(n=('gain','size'),gain_sum=('gain','sum'),mean=('gain','mean'))
    L=T[T.a>0]
    out['long bars by year']=L.groupby('year').agg(n=('gain','size'),gain_sum=('gain','sum'),mean=('gain','mean'))
    out['short gain t']=pd.Series({'n':len(S),'mean':S['gain'].mean(),'t':tt(S['gain'].dropna()),'mean_alloc':S['a'].mean()})
    out['long gain t']=pd.Series({'n':len(L),'mean':L['gain'].mean(),'t':tt(L['gain'].dropna()),'mean_alloc':L['a'].mean()})
    big=L[L.r30>0.4]; mid=L[(L.r30>0.07)&(L.r30<=0.4)]
    out['long r30>0.4 vs mid']=pd.Series({'n_big':len(big),'mean_big':big['gain'].mean(),'std_big':big['gain'].std(),'n_mid':len(mid),'mean_mid':mid['gain'].mean(),'std_mid':mid['gain'].std(),'alloc_big':big['a'].mean(),'alloc_mid':mid['a'].mean()})
    return out
