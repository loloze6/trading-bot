import pandas as pd, numpy as np

def _feat(df):
    d = df.copy().reset_index(drop=True)
    o,h,l,c = d['open'],d['high'],d['low'],d['close']
    rng=(h-l)
    d['rr']=rng/rng.rolling(20).mean()
    d['flat']=1-(c-o).abs()/rng.replace(0,np.nan)
    d['clv']=(c-l)/rng.replace(0,np.nan)
    d['r1']=c.pct_change()
    for k in [5,10,20,30,60]:
        d['r%d'%k]=c/c.shift(k)-1
    d['vol20']=d['r1'].rolling(20).std()
    d['tz20']=d['r20']/(d['vol20']*np.sqrt(20))
    d['vol30']=d['r1'].rolling(30).std()
    d['agit']=d['vol30'].rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
    d['fwd5']=c.shift(-5)/c-1
    d['fwd10']=c.shift(-10)/c-1
    d['pos']=np.arange(len(d)); d['cell']=d['pos']//5
    d['dayk']=pd.to_datetime(d['timestamp']).dt.floor('D')
    return d

def _t(x, days):
    x=np.asarray(x,float); m=~np.isnan(x); x=x[m]; dk=np.asarray(days)[m]
    if len(x)<3: return (len(x),np.nan,np.nan,0)
    mu=x.mean(); s=pd.Series(x-mu).groupby(dk).sum()
    se=np.sqrt((s**2).sum())/len(x)
    return (len(x),mu,mu/se if se>0 else np.nan,len(s))

def _slope(x,y,days):
    m=~(np.isnan(x)|np.isnan(y)); x=x[m]; y=y[m]; dk=np.asarray(days)[m]
    xc=x-x.mean(); b=(xc*(y-y.mean())).sum()/(xc**2).sum()
    e=y-y.mean()-b*xc
    s=pd.Series(xc*e).groupby(dk).sum()
    se=np.sqrt((s**2).sum())/(xc**2).sum()
    return pd.Series({'n':len(x),'slope':b,'t':b/se,'corr':np.corrcoef(x,y)[0,1]})

def explore(data):
    rows=[]
    for coin,wins in data['bars'].items():
        for w,df in wins.items():
            d=_feat(df); d['coin']=coin; d['win']=w; rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    grid=A[A['pos']%5==0].dropna(subset=['fwd5'])
    dm=grid.groupby('coin')['fwd5'].agg(['mean','std'])
    A['ex5']=A['fwd5']-A['coin'].map(dm['mean'])
    A['z5']=A['ex5']/A['coin'].map(dm['std'])
    G=A[A['pos']%5==0].dropna(subset=['ex5'])
    out={}
    S={}
    for col in ['r5','r10','r20','r30','r60','tz20']:
        S[col]=_slope(G[col].values,G['z5'].values,G['dayk'].values)
    out['slope_z5_on_past_return']=pd.DataFrame(S).T
    # r20 slope by window and coin
    out['r20_slope_by_window']=G.groupby('win').apply(lambda s:_slope(s['r20'].values,s['z5'].values,s['dayk'].values))
    out['r20_slope_by_coin']=G.groupby('coin').apply(lambda s:_slope(s['r20'].values,s['z5'].values,s['dayk'].values))
    # r20 graded by profile
    g=G.dropna(subset=['r60','agit']).copy()
    g['trend']=np.where(g['r60']>0.1,'rising',np.where(g['r60']<-0.1,'falling','choppy'))
    g['ag']=np.where(g['agit']>0.5,'agit','calm')
    out['r20_slope_by_trend']=g.groupby('trend').apply(lambda s:_slope(s['r20'].values,s['z5'].values,s['dayk'].values))
    out['r20_slope_by_agit']=g.groupby('ag').apply(lambda s:_slope(s['r20'].values,s['z5'].values,s['dayk'].values))
    # wide-flat after up: continuation graded by r5 and rr, all bars first per cell
    wf=A[(A['r5']>0)&(A['rr']>=1.5)&(A['flat']>=0.9)&A['ex5'].notna()].groupby(['coin','win','cell']).head(1)
    out['wideflat_up_by_window']=wf.groupby('win')['ex5'].agg(['count','mean'])
    out['wideflat_up_by_coin']=wf.groupby('coin')['ex5'].agg(['count','mean'])
    # wide days (rr>=1.5) after up: slope of z5 on clv and on r5
    wu=A[(A['r5']>0)&(A['rr']>=1.5)&A['ex5'].notna()].groupby(['coin','win','cell']).head(1)
    out['wide_up_slopes']=pd.DataFrame({'clv':_slope(wu['clv'].values,wu['z5'].values,wu['dayk'].values),
                                         'rr':_slope(wu['rr'].values,wu['z5'].values,wu['dayk'].values),
                                         'r5':_slope(wu['r5'].values,wu['z5'].values,wu['dayk'].values)}).T
    wd=A[(A['r5']<0)&(A['rr']>=1.5)&A['ex5'].notna()].groupby(['coin','win','cell']).head(1)
    out['wide_down_slopes']=pd.DataFrame({'clv':_slope(wd['clv'].values,wd['z5'].values,wd['dayk'].values),
                                         'rr':_slope(wd['rr'].values,wd['z5'].values,wd['dayk'].values),
                                         'r5':_slope(wd['r5'].values,wd['z5'].values,wd['dayk'].values)}).T
    # book largest gains/losses days: coin's prior r20
    D=[]
    for coin,wins in data['days'].items():
        for w,dd in wins.items():
            x=dd.copy(); x['coin']=coin; D.append(x)
    D=pd.concat(D).dropna(subset=['book_return'])
    act=D[D['book_return']!=0]
    out['book_active_days']=pd.Series({'n':len(act),'mean':act['book_return'].mean(),
        'share_pos':(act['book_return']>0).mean(),'corr_with_coin':act[['book_return','coin_return']].corr().iloc[0,1]})
    return out
