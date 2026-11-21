def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    out={}
    H=26
    gr=[]; feats={}
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            h,l,cl=b.high,b.low,b.close
            t=(h.rolling(9).max()+l.rolling(9).min())/2; k=(h.rolling(26).max()+l.rolling(26).min())/2
            sa=((t+k)/2).shift(26); sb=((h.rolling(52).max()+l.rolling(52).min())/2).shift(26)
            top=np.maximum(sa,sb); bot=np.minimum(sa,sb)
            mid=(sa+sb)/2
            fwd=cl.shift(-H)/cl-1
            df=pd.DataFrame({'fwd':fwd,'f':b.forecast,'ext':cl/top-1,'thick':(top-bot)/cl,
                'past':cl/cl.shift(26)-1,'past52':cl/cl.shift(52)-1,'slope':mid/mid.shift(26)-1,
                'dist_hi':cl/h.rolling(26).max()-1,'vol':np.log(cl).diff().rolling(20).std()})
            df['coin']=c; df['wn']=int(w[1:])
            feats[(c,w)]=df.assign(ts=pd.to_datetime(b.timestamp))
            gr.append(df.iloc[::H])
    G=pd.concat(gr).dropna(subset=['fwd'])
    drift=G.groupby('coin')['fwd'].mean()
    G['ex']=G['fwd']-G['coin'].map(drift)
    A=G[G.f>0].copy()
    def qt(x,col,nq=4):
        x=x.dropna(subset=[col]); q=pd.qcut(x[col].rank(method='first'),nq,labels=False)
        g=x.groupby(q)['ex']
        return pd.DataFrame({'n':g.size(),'mean':g.mean(),'median':g.median(),
            't':g.mean()/(g.std()/np.sqrt(g.size())),'xm':x.groupby(q)[col].mean()})
    for col in ['ext','slope','thick','dist_hi','past52']:
        out['active_'+col]=qt(A,col)
    # all grid bars above cloud (ext>0) regardless of slope
    U=G[G.ext>0]
    out['above_cloud_ext']=qt(U,'ext')
    out['above_cloud_slope']=qt(U,'slope')
    # ext scaled by vol
    G['ext_v']=G['ext']/(G['vol']*np.sqrt(26))
    out['all_extv_quint']=qt(G,'ext_v',5)
    # trades with entry features
    tr=[]
    for c in data['trades']:
        for w,T in data['trades'][c].items():
            if len(T)==0: continue
            F=feats[(c,w)].set_index('ts')
            T=T.copy(); et=pd.to_datetime(T.entry_time)
            idx=F.index.get_indexer(et,method='nearest')
            for col in ['ext','thick','past','slope','dist_hi','vol']:
                T[col]=F[col].values[idx]
            T['wn']=int(w[1:]); T['coin']=c; tr.append(T)
    T=pd.concat(tr)
    T['pl']=T.net_profit_loss_percent
    out['trade_rho']=pd.Series({col:stats.spearmanr(T[col],T['pl'],nan_policy='omit')[0] for col in ['ext','thick','past','slope','dist_hi','vol']})
    x=T.dropna(subset=['ext']); q=pd.qcut(x.ext.rank(method='first'),4,labels=False)
    out['trades_by_ext']=x.groupby(q).agg(n=('pl','size'),mean=('pl','mean'),med=('pl','median'),win=('pl',lambda s:(s>0).mean()),ext=('ext','mean'))
    # fall windows 15-21: per coin book cum vs hold
    rows=[]
    for c in days:
        for w,d in days[c].items():
            wn=int(w[1:])
            if 15<=wn<=21:
                rows.append({'coin':c,'wn':wn,'book':(1+d.book_return.fillna(0)).prod()-1,'hold':(1+d.coin_return.fillna(0)).prod()-1})
    R=pd.DataFrame(rows)
    out['fall_by_coin']=R.groupby('coin')[['book','hold']].mean()
    out['fall_trades']=T[(T.wn>=15)&(T.wn<=21)].groupby('coin').agg(n=('pl','size'),mean=('pl','mean'),ext=('ext','mean'),past=('past','mean'))
    # entries features of fall-window trades vs others
    out['trade_by_period']=T.assign(fall=(T.wn>=15)&(T.wn<=21)).groupby('fall').agg(n=('pl','size'),mean=('pl','mean'),med=('pl','median'),ext=('ext','median'),past=('past','median'),thick=('thick','median'))
    return out
