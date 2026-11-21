def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    out={}
    # book daily
    rows=[]
    for c in days:
        for w,d in days[c].items():
            b=bars[c][w].copy()
            b['day']=pd.to_datetime(b['timestamp']).dt.floor('D')
            al=b.groupby('day')['postRebalance_current_allocation'].last()
            dd=d.copy(); dd['day']=pd.to_datetime(dd['day']).dt.floor('D')
            dd['alloc_prev']=dd['day'].map(al).shift(1)
            dd['coin']=c; dd['w']=w
            rows.append(dd)
    D=pd.concat(rows)
    D['wn']=D['w'].str[1:].astype(int)
    cm=D.groupby('coin')['coin_return'].mean()
    D['mkt']=D['alloc_prev']*D['coin'].map(cm)
    bk=D.groupby(['wn','day']).agg(book=('book_return','mean'),hold=('coin_return','mean'),
        alloc=('alloc_prev','mean'),mkt=('mkt','mean')).dropna().sort_index()
    s=lambda x: x.mean()/x.std()*np.sqrt(365)
    out['summary']=pd.Series({'book_mean':bk.book.mean(),'hold_mean':bk.hold.mean(),'book_sh':s(bk.book),
        'hold_sh':s(bk.hold),'mean_alloc':bk.alloc.mean(),'mkt_part':bk.mkt.mean(),
        'timing':bk.book.mean()-bk.mkt.mean(),'share_days_in':(bk.alloc>0.01).mean(),'ndays':len(bk)})
    # by window
    g=bk.groupby(level=0)
    out['by_window']=pd.DataFrame({'book':g.book.mean()*1e4,'hold':g.hold.mean()*1e4,'alloc':g.alloc.mean(),
        'book_cum':g.book.apply(lambda x:(1+x).prod()-1),'hold_cum':g.hold.apply(lambda x:(1+x).prod()-1)})
    # drawdowns
    eq=(1+bk.book).cumprod(); peak=eq.cummax(); ddn=eq/peak-1
    bk['dd']=ddn.values
    # identify episodes
    ep=[];i=0;v=ddn.values;n=len(v)
    in_dd=False
    for j in range(n):
        if v[j]<0 and not in_dd: st=j;in_dd=True
        if in_dd and (v[j]==0 or j==n-1):
            seg=v[st:j+1]; k=st+seg.argmin()
            ep.append((seg.min(),st,k,j)); in_dd=False
    ep=sorted(ep)[:6]
    er=[]
    for depth,st,k,e in ep:
        sub=bk.iloc[st:k+1]
        er.append({'depth':depth,'days_to_trough':k-st+1,'win_start':sub.index[0][0],'win_trough':sub.index[-1][0],
                   'alloc':sub.alloc.mean(),'hold_cum':(1+sub.hold).prod()-1,'book_cum':(1+sub.book).prod()-1})
    out['falls']=pd.DataFrame(er)
    # grid analysis
    H=26; gr=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            h,l,cl=b.high,b.low,b.close
            t=(h.rolling(9).max()+l.rolling(9).min())/2; k=(h.rolling(26).max()+l.rolling(26).min())/2
            sa=((t+k)/2).shift(26); sb=((h.rolling(52).max()+l.rolling(52).min())/2).shift(26)
            top=np.maximum(sa,sb); bot=np.minimum(sa,sb)
            fwd=cl.shift(-H)/cl-1
            df=pd.DataFrame({'fwd':fwd,'f':b.forecast,'ext':cl/top-1,'thick':(top-bot)/cl,
                'past':cl/cl.shift(26)-1,'vol':np.log(cl).diff().rolling(20).std(),
                'past7':cl/cl.shift(7)-1,'alloc':b.postRebalance_current_allocation})
            df=df.iloc[::H]; df['coin']=c; df['wn']=int(w[1:]); gr.append(df)
    G=pd.concat(gr).dropna(subset=['fwd'])
    drift=G.groupby('coin')['fwd'].mean()
    G['ex']=G['fwd']-G['coin'].map(drift)
    A=G[G.f>0].copy(); I=G[G.f<=0]
    out['active_vs_not']=pd.DataFrame({'n':[len(A),len(I)],'fwd':[A.fwd.mean(),I.fwd.mean()],'ex':[A.ex.mean(),I.ex.mean()],
        'fwd_t':[stats.ttest_1samp(A.fwd,0)[0],stats.ttest_1samp(I.fwd,0)[0]]},index=['active','flat'])
    res={}
    for col in ['f','ext','thick','past','vol','past7']:
        x=A.dropna(subset=[col])
        q=pd.qcut(x[col].rank(method='first'),4,labels=False)
        gg=x.groupby(q)
        res[col]=pd.Series(gg['ex'].mean().values,index=[f'q{i+1}' for i in range(4)])
        res[col+'_rho']=pd.Series([stats.spearmanr(x[col],x['ex'])[0]],index=['rho'])
    out['active_quartile_ex']=pd.DataFrame({k:v for k,v in res.items() if not k.endswith('rho')})
    out['active_rho']=pd.Series({k:v.iloc[0] for k,v in res.items() if k.endswith('rho')})
    # whole-sample (all grid) graded by past return and ext
    x=G.dropna(subset=['ext','past'])
    for col in ['ext','past']:
        q=pd.qcut(x[col].rank(method='first'),5,labels=False)
        out['all_quint_'+col]=x.groupby(q).agg(n=('ex','size'),ex=('ex','mean'),fwd=('fwd','mean'),xm=(col,'mean'))
    # trades
    T=pd.concat([data['trades'][c][w] for c in data['trades'] for w in data['trades'][c]])
    out['trades']=pd.Series({'n':len(T),'mean_net':T.net_profit_loss_percent.mean(),'win':(T.net_profit_loss_percent>0).mean(),
        'med_days':T.duration_minutes.median()/1440})
    return out
