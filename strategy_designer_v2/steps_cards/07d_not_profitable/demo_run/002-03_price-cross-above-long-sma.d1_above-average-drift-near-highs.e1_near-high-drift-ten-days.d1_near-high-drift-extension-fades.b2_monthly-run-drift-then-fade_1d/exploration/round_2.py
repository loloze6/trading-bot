def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    rows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.copy()
            col='debug_info.components.run.post_pipeline_value'
            b['s']=pd.to_numeric(b[col],errors='coerce') if col in b.columns else np.nan
            b['nxt']=b['close'].shift(-1)/b['close']-1
            b['gain']=b['postRebalance_current_allocation']*b['nxt']
            b['r30']=b['close']/b['close'].shift(30)-1
            b['f10']=b['close'].shift(-10)/b['close']-1
            b['grid']=(np.arange(len(b))%10==0)
            b['coin']=c; b['wn']=int(w[1:])
            b['day']=pd.to_datetime(b['timestamp']).dt.floor('D')
            rows.append(b)
    B=pd.concat(rows)
    out={}
    mu=B[B.grid].groupby('coin')['f10'].mean()
    B['ex10']=B['f10']-B['coin'].map(mu)
    G=B[B.grid & (B.regime=='trending')].dropna(subset=['ex10','r30'])
    G['r30b']=pd.qcut(G['r30'],6)
    out['grid ex10 by r30 sextile']=G.groupby('r30b')['ex10'].agg(['size','mean',lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    G['sb']=pd.cut(G['s'],[-30,-5,0,5,8,14,30])
    out['grid ex10 by s']=G.groupby('sb')['ex10'].agg(['size','mean',lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    U=B[B.grid & (B.regime!='trending')].dropna(subset=['ex10','r30'])
    U['r30b']=pd.qcut(U['r30'],4)
    out['unknown regime ex10 by r30 quartile']=U.groupby('r30b')['ex10'].agg(['size','mean',lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    # pooled book with drawdown, then what held in deep drawdown days
    D=[]
    for c in days:
        for w,d in days[c].items():
            d=d.copy(); d['coin']=c; d['wn']=int(w[1:]); D.append(d)
    D=pd.concat(D)
    P=D.groupby(['wn','day']).agg(book=('book_return','mean')).reset_index().sort_values(['wn','day']).dropna()
    eq=(1+P['book']).cumprod(); P['dd']=(eq/eq.cummax()-1).values
    P['worst']=P['book']<P['book'].quantile(0.05)
    B['dayk']=B['day'].dt.strftime('%Y-%m-%d'); P['dayk']=pd.to_datetime(P['day']).dt.strftime('%Y-%m-%d')
    M=B.merge(P[['wn','dayk','worst','dd']],on=['wn','dayk'])
    M['side']=np.sign(M['postRebalance_current_allocation'])
    out['worst 5pct book days: holding']=M.groupby('worst').agg(long_share=('side',lambda x:(x>0).mean()),short_share=('side',lambda x:(x<0).mean()),alloc=('postRebalance_current_allocation','mean'),r30=('r30','mean'),s=('s','mean'))
    L=M[M.side>0].copy(); L['r30b']=pd.qcut(L['r30'],5)
    out['long bars gain by r30 quintile']=L.groupby('r30b').agg(n=('gain','size'),mean=('gain','mean'),std=('gain','std'),worst1pct=('gain',lambda x:x.quantile(0.01)))
    S=M[M.side<0].copy(); S['r30b']=pd.qcut(S['r30'],4)
    out['short bars gain by r30 quartile']=S.groupby('r30b').agg(n=('gain','size'),mean=('gain','mean'),std=('gain','std'))
    W5=M[M.wn==5]
    out['w5 by coin']=W5.groupby('coin').agg(gain=('gain','sum'),alloc=('postRebalance_current_allocation','mean'),short=('side',lambda x:(x<0).mean()),coinret=('nxt','sum'))
    out['w5 by side']=W5.groupby('side').agg(n=('gain','size'),gain=('gain','sum'))
    # dd by side contribution: sum of gain in days with dd<-0.15
    out['deep dd days (dd<-0.15) by side']=M[M.dd<-0.15].groupby('side').agg(n=('gain','size'),gain=('gain','sum'))
    return out
