import numpy as np, pandas as pd

def _clt(df, col):
    d = df.dropna(subset=[col])
    if len(d) < 5: return (np.nan, np.nan, len(d), 0)
    m = d[col].mean()
    g = (d[col]-m).groupby(d['day']).sum()
    G = len(g)
    se = np.sqrt((g**2).sum()*G/(G-1))/len(d) if G>1 else np.nan
    return (m, m/se if se else np.nan, len(d), G)

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        allc = []
        for w, b in wins.items():
            c = b['close'].values
            allc.append(pd.Series(c).pct_change().dropna())
        cmean = pd.concat(allc).mean()
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            b['coin']=coin; b['win']=w
            ts = pd.to_datetime(b['timestamp'])
            b['day']=ts.dt.floor('D'); b['wd']=ts.dt.weekday; b['yr']=ts.dt.year
            b['r1']=b['close'].pct_change()
            rng=b['high']-b['low']
            b['rm']=rng/rng.rolling(20).mean()
            b['cl']=(b['close']-b['low'])/rng.replace(0,np.nan)
            b['tr60']=b['close']/b['close'].shift(60)-1
            vol=b['r1'].rolling(20).std()
            b['z']=b['r1']/vol.shift(1)
            b['f1']=b['close'].shift(-1)/b['close']-1
            b['x1']=b['f1']-cmean
            b['f3']=b['close'].shift(-3)/b['close']-1-3*cmean
            b['pos']=b['postRebalance_current_allocation']
            b['pg']=b['pos']*b['f1']
            rows.append(b)
    P = pd.concat(rows, ignore_index=True)
    P['trend']=np.where(P['tr60']< -0.10,'falling',np.where(P['tr60']>0.10,'rising','choppy'))
    P.loc[P['tr60'].isna(),'trend']='na'
    out={}
    # 1 up days by trend x range multiple bucket
    up=P[(P['r1']>0)&P['rm'].notna()].copy()
    up['rmb']=pd.cut(up['rm'],[0,0.8,1.2,1.5,2.0,99],labels=['<0.8','0.8-1.2','1.2-1.5','1.5-2','>2'])
    res=[]
    for (t,k),g in up.groupby(['trend','rmb'],observed=True):
        m,tt,n,G=_clt(g,'x1'); res.append([t,k,m,tt,n,G])
    out['up_days_next_excess_by_trend_rm']=pd.DataFrame(res,columns=['trend','rm','mean','t','n','days'])
    # 2 down days
    dn=P[(P['r1']<0)&P['rm'].notna()].copy()
    dn['rmb']=pd.cut(dn['rm'],[0,0.8,1.2,1.5,2.0,99],labels=['<0.8','0.8-1.2','1.2-1.5','1.5-2','>2'])
    res=[]
    for (t,k),g in dn.groupby(['trend','rmb'],observed=True):
        m,tt,n,G=_clt(g,'x1'); res.append([t,k,m,tt,n,G])
    out['down_days_next_excess_by_trend_rm']=pd.DataFrame(res,columns=['trend','rm','mean','t','n','days'])
    # 3 z-score of day return, by trend
    zz=P[P['z'].notna()].copy()
    zz['zb']=pd.cut(zz['z'],[-99,-2,-1,0,1,2,99])
    res=[]
    for (t,k),g in zz.groupby(['trend','zb'],observed=True):
        m,tt,n,G=_clt(g,'x1'); m3,t3,_,_=_clt(g,'f3'); res.append([t,str(k),m,tt,n,G,m3,t3])
    out['next_by_trend_dayz']=pd.DataFrame(res,columns=['trend','z','m1','t1','n','days','m3_overl','t3_overl'])
    # 4 weekday
    res=[]
    for (t,k),g in P[P['trend']!='na'].groupby(['trend','wd']):
        m,tt,n,G=_clt(g,'x1'); res.append([t,k,m,tt,n])
    out['weekday_next_by_trend']=pd.DataFrame(res,columns=['trend','wd_of_signal','mean','t','n'])
    # 5 wide up days in falling: closeloc bucket
    fu=up[(up['trend']=='falling')&(up['rm']>=1.5)].copy()
    fu['clb']=pd.cut(fu['cl'],[0,0.33,0.66,0.9,1.01])
    res=[]
    for k,g in fu.groupby('clb',observed=True):
        m,tt,n,G=_clt(g,'x1'); m3,t3,_,_=_clt(g,'f3'); res.append([str(k),m,tt,n,m3,t3])
    out['falling_wide_up_by_closeloc']=pd.DataFrame(res,columns=['cl','m1','t1','n','m3','t3'])
    # 6 by year for falling wide up
    res=[]
    for k,g in fu.groupby('yr'):
        m,tt,n,G=_clt(g,'x1'); res.append([k,m,tt,n])
    out['falling_wide_up_by_year']=pd.DataFrame(res,columns=['yr','m1','t1','n'])
    # 7 close location all days by trend (any day), next return
    cc=P[P['cl'].notna()&(P['trend']!='na')].copy()
    cc['clb']=pd.cut(cc['cl'],[-0.01,0.1,0.33,0.66,0.9,1.01])
    res=[]
    for (t,k),g in cc.groupby(['trend','clb'],observed=True):
        m,tt,n,G=_clt(g,'x1'); res.append([t,str(k),m,tt,n])
    out['closeloc_all_days_by_trend']=pd.DataFrame(res,columns=['trend','cl','mean','t','n'])
    # 8 book: largest days
    D=[]
    for coin,wins in data['days'].items():
        for w,d in wins.items():
            d=d.copy(); d['coin']=coin; D.append(d)
    D=pd.concat(D)
    bd=D.groupby('day')['book_return'].mean().dropna()
    out['book_daily_summary']=pd.Series({'n':len(bd),'mean':bd.mean(),'sd':bd.std(),
        'top10_sum':bd.nlargest(10).sum(),'bot10_sum':bd.nsmallest(10).sum(),'total_sum':bd.sum()})
    return out
