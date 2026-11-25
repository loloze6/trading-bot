def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]; days=data["days"]
    rows=[]
    for c in bars:
        ws=sorted(bars[c].keys(), key=lambda w:int(w[1:]))
        a=pd.concat([bars[c][w].assign(w=w,coin=c) for w in ws],ignore_index=True)
        a['ts']=pd.to_datetime(a['timestamp'])
        r=a['close'].pct_change()
        a['tr60']=a['close']/a['close'].shift(60)-1
        v30=r.rolling(30).std()
        a['agit']=v30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
        a['rng']=(a['high']-a['low'])/a['close']
        a['rngrel']=a['rng']/a['rng'].rolling(20).mean().shift(1)
        a['cl']=(a['close']-a['low'])/(a['high']-a['low'])
        a['ret1']=a['close']/a['open']-1
        gc=a.groupby('w')['close']
        a['fwd']=gc.shift(-1)/a['close']-1
        a['fwd2']=gc.shift(-2)/a['close']-1
        a['fwd3']=gc.shift(-3)/a['close']-1
        a['pos']=a['postRebalance_current_allocation']
        a['gain']=a['pos']*a['fwd']
        a['k']=a.groupby('w').cumcount()
        a['dayk']=a['ts'].dt.floor('D')
        rows.append(a)
    A=pd.concat(rows,ignore_index=True)
    A=A[A['fwd'].notna()].copy()
    for h,col in [(1,'fwd'),(2,'fwd2'),(3,'fwd3')]:
        dr=A.groupby('coin')[col].mean()
        A['ex'+str(h)]=A[col]-A['coin'].map(dr)
    A['rq']=pd.qcut(A['rngrel'],4,labels=['r1','r2','r3','r4'])
    A['clb']=pd.cut(A['cl'],[-0.01,0.25,0.5,1.01],labels=['low','mid','high'])
    def ct(df,col):
        d=df.dropna(subset=[col]).groupby('dayk')[col].agg(['sum','size'])
        n=d['size'].sum(); m=d['sum'].sum()/n
        dev=df.dropna(subset=[col]).groupby('dayk')[col].apply(lambda x:(x-m).sum())
        se=np.sqrt((dev**2).sum())/n
        return m, m/se, len(d), n
    out={}
    res=[]
    for cb in ['low','mid','high']:
        for q in ['r1','r2','r3','r4']:
            s=A[(A['clb']==cb)&(A['rq']==q)]
            m,t,nd,n=ct(s,'ex1')
            res.append(dict(cl=cb,rq=q,n=n,ex1=m,t_day=t,fwd=s['fwd'].mean(),pos=s['pos'].mean(),gain=s['gain'].mean()))
    out['cl_x_rangerel']=pd.DataFrame(res)
    # horizons on nonoverlapping grid, strong case cl<0.5 and r4
    res=[]
    for h in [1,2,3]:
        g=A[A['k']%h==0]
        for name,s in [('low_r4',g[(g['cl']<0.5)&(g['rq']=='r4')]),('low_r34',g[(g['cl']<0.5)&(g['rq'].isin(['r3','r4']))]),('low_all',g[g['cl']<0.5]),('high_r4',g[(g['cl']>=0.5)&(g['rq']=='r4')])]:
            m,t,nd,n=ct(s,'ex'+str(h))
            res.append(dict(h=h,case=name,n=n,days=nd,ex=m,t_day=t))
    out['horizons']=pd.DataFrame(res)
    # low_r4 by year and by window
    s=A[(A['cl']<0.5)&(A['rq']=='r4')]
    out['lowr4_by_year']=s.groupby(s['ts'].dt.year)['ex1'].agg(['size','mean'])
    out['lowr4_by_window']=s.groupby('w')['ex1'].agg(['size','mean'])
    # on low-close days, gain by range quartile split by trend
    L=A[A['cl']<0.5].copy()
    L['tr']=np.where(L['tr60']>0.1,'rising',np.where(L['tr60']<-0.1,'falling','choppy'))
    out['low_rq_trend']=L.groupby(['tr','rq'])['ex1'].agg(['size','mean']).unstack()
    # book: days in position split by whether the position came from r4 day
    out['gain_share']=pd.Series({'gain_all_low':L['gain'].sum(),'gain_r4':L.loc[L['rq']=='r4','gain'].sum(),'gain_r12':L.loc[L['rq'].isin(['r1','r2']),'gain'].sum(),'n_pos_bars':(L['pos'].abs()>0.001).sum(),'n_pos_r12':((L['pos'].abs()>0.001)&L['rq'].isin(['r1','r2'])).sum()})
    # worst window w14 drawdown: what profile/range
    D=[]
    for c in days:
        for w in days[c]:
            d=days[c][w].copy(); d['coin']=c; d['w']=w; D.append(d)
    D=pd.concat(D)
    bk=D.groupby(['w','day'])['book_return'].mean().dropna()
    out['worst_book_days_share_from_r12']=None
    worst=bk.nsmallest(40).reset_index()
    A['day']=A['ts'].dt.strftime('%Y-%m-%d')
    D['day']=pd.to_datetime(D['day']).dt.strftime('%Y-%m-%d')
    # positions held into worst days: previous bar's case
    A['nextday']=(A['ts']+pd.Timedelta(days=1)).dt.strftime('%Y-%m-%d')
    W=A.merge(worst[['w','day']].assign(day=lambda x:pd.to_datetime(x['day']).dt.strftime('%Y-%m-%d')),left_on=['w','nextday'],right_on=['w','day'])
    W=W[W['pos'].abs()>0.001]
    out['worst40_held_from']=W.groupby('rq').agg(n=('gain','size'),gain=('gain','sum'),cl=('cl','mean'))
    del out['worst_book_days_share_from_r12']
    return out
