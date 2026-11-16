def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars=data["bars"]; days=data["days"]; trades=data["trades"]
    rows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.copy()
            s=None
            col='debug_info.components.run.post_pipeline_value'
            if col in b.columns: s=b[col]
            elif 'debug_info.components' in b.columns:
                def g(x):
                    try:
                        if isinstance(x,str):
                            import json; x=json.loads(x)
                        return x['run']['post_pipeline_value']
                    except Exception: return np.nan
                s=b['debug_info.components'].apply(g)
            b['s']=pd.to_numeric(s,errors='coerce') if s is not None else np.nan
            b['nxt']=b['close'].shift(-1)/b['close']-1
            b['gain']=b['postRebalance_current_allocation']*b['nxt']
            b['r30']=b['close']/b['close'].shift(30)-1
            b['r10']=b['close']/b['close'].shift(10)-1
            b['vol20']=b['close'].pct_change().rolling(20).std()
            b['coin']=c; b['w']=w; b['wn']=int(w[1:])
            b['year']=pd.to_datetime(b['timestamp']).dt.year
            rows.append(b)
    B=pd.concat(rows)
    out={}
    out['s nonmissing share']=float(B['s'].notna().mean())
    out['regime share']=B['regime'].value_counts(normalize=True)
    # book daily pooled
    D=[]
    for c in days:
        for w,d in days[c].items():
            d=d.copy(); d['coin']=c; d['wn']=int(w[1:]); D.append(d)
    D=pd.concat(D)
    P=D.groupby(['wn','day']).agg(book=('book_return','mean'),coin=('coin_return','mean')).reset_index().sort_values(['wn','day'])
    P=P.dropna()
    eq=(1+P['book']).cumprod(); dd=eq/eq.cummax()-1
    P['dd']=dd.values; P['year']=pd.to_datetime(P['day']).dt.year
    out['book by window']=P.groupby('wn').agg(book_sum=('book','sum'),coin_sum=('coin','sum'),min_dd=('dd','min'))
    out['book by year']=P.groupby('year').agg(book_mean=('book','mean'),coin_mean=('coin','mean'),n=('book','size'))
    out['maxdd']=float(dd.min())
    # gain by s bucket in trending
    T=B[B['regime']=='trending'].copy()
    T['sb']=pd.cut(T['s'],[-30,-5,-2,0,2,5,8,14,30])
    out['gain by s bucket']=T.groupby('sb').agg(n=('gain','size'),mean_gain=('gain','mean'),sum_gain=('gain','sum'),alloc=('postRebalance_current_allocation','mean'),nxt=('nxt','mean'))
    T['r30b']=pd.qcut(T['r30'],6)
    out['gain by r30 sextile']=T.groupby('r30b').agg(n=('gain','size'),mean_gain=('gain','mean'),sum_gain=('gain','sum'),alloc=('postRebalance_current_allocation','mean'),nxt=('nxt','mean'))
    T['vb']=pd.qcut(T['vol20'],5)
    out['gain by vol20 quintile']=T.groupby('vb').agg(n=('gain','size'),mean_gain=('gain','mean'),sum_gain=('gain','sum'),alloc=('postRebalance_current_allocation','mean'),nxt=('nxt','mean'))
    out['gain by coin']=B.groupby('coin').agg(mean_gain=('gain','mean'),alloc=('postRebalance_current_allocation','mean'),short_share=('postRebalance_current_allocation',lambda x:(x<0).mean()))
    B['side']=np.sign(B['postRebalance_current_allocation'])
    out['gain by side']=B.groupby('side').agg(n=('gain','size'),mean_gain=('gain','mean'),sum_gain=('gain','sum'),nxt=('nxt','mean'))
    tr=pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()])
    out['trades']=pd.Series({'n':len(tr),'gross_mean':tr['profit_loss_percent'].mean(),'net_mean':tr['net_profit_loss_percent'].mean(),'comm_sum':tr['total_commission'].sum(),'dur_days_med':tr['duration_minutes'].median()/1440})
    # deepest fall: worst 30 days of pooled book
    P['b30']=P.groupby('wn')['book'].transform(lambda x:x.rolling(20).sum())
    worst=P.nsmallest(1,'b30')
    out['worst 20d book sum']=float(worst['b30'].iloc[0]); out['worst window']=int(worst['wn'].iloc[0])
    return out
