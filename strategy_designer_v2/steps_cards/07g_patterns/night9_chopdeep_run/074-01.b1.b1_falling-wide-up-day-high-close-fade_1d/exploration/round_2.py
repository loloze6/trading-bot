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
        allc = [pd.Series(b['close'].values).pct_change().dropna() for b in wins.values()]
        cmean = pd.concat(allc).mean()
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            b['coin']=coin; b['win']=w
            ts = pd.to_datetime(b['timestamp'])
            b['day']=ts.dt.floor('D'); b['yr']=ts.dt.year
            b['r1']=b['close'].pct_change()
            rng=b['high']-b['low']
            b['rm']=rng/rng.rolling(20).mean()
            b['cl']=(b['close']-b['low'])/rng.replace(0,np.nan)
            b['tr60']=b['close']/b['close'].shift(60)-1
            sd30=b['r1'].rolling(30).std()
            b['agit']=sd30.rolling(120,min_periods=60).apply(lambda a:(a<=a[-1]).mean(),raw=True)
            b['x1']=b['close'].shift(-1)/b['close']-1-cmean
            b['x2']=b['close'].shift(-2)/b['close']-1-2*cmean
            b['x3']=b['close'].shift(-3)/b['close']-1-3*cmean
            b['g3']=(np.arange(len(b))%3==0)
            rows.append(b)
    P = pd.concat(rows, ignore_index=True)
    P['trend']=np.where(P['tr60']< -0.10,'falling',np.where(P['tr60']>0.10,'rising','choppy'))
    P.loc[P['tr60'].isna(),'trend']='na'
    P['ag']=np.where(P['agit']>0.5,'agit','calm'); P.loc[P['agit'].isna(),'ag']='na'
    out={}
    # A: choppy low-close days
    ch=P[(P['trend']=='choppy')&P['cl'].notna()].copy()
    ch['clb']=pd.cut(ch['cl'],[-0.01,0.05,0.1,0.2,0.33,1.01])
    res=[]
    for k,g in ch.groupby('clb',observed=True):
        a=_clt(g,'x1'); b2=_clt(g,'x2'); res.append([str(k),a[0],a[1],a[2],b2[0],b2[1]])
    out['choppy_cl_fine']=pd.DataFrame(res,columns=['cl','m1','t1','n','m2','t2'])
    lo=ch[ch['cl']<=0.1]
    res=[]
    for k,g in lo.groupby('ag'):
        a=_clt(g,'x1'); res.append(['ag_'+k,a[0],a[1],a[2]])
    for k,g in lo.groupby('yr'):
        a=_clt(g,'x1'); res.append(['yr_'+str(k),a[0],a[1],a[2]])
    for k,g in lo.groupby(lo['r1']<0):
        a=_clt(g,'x1'); res.append(['down_day_'+str(k),a[0],a[1],a[2]])
    out['choppy_lowclose_splits']=pd.DataFrame(res,columns=['grp','m1','t1','n'])
    # graded: in choppy, next return vs (1-cl) correlation across all days
    c2=ch.dropna(subset=['x1'])
    out['choppy_corr_lowness_next']=pd.Series({'spearman':pd.Series(1-c2['cl']).corr(c2['x1'],method='spearman'),'n':len(c2)})
    # B: rising wide up days continuation, by agitation, non-overlap 3d
    ru=P[(P['trend']=='rising')&(P['r1']>0)&P['rm'].notna()].copy()
    ru['rmb']=pd.cut(ru['rm'],[0,1.2,1.5,2,3,99])
    res=[]
    for (a_,k),g in ru.groupby(['ag','rmb'],observed=True):
        a=_clt(g,'x1'); b3=_clt(g[g['g3']],'x3'); res.append([a_,str(k),a[0],a[1],a[2],b3[0],b3[1],b3[2]])
    out['rising_up_by_ag_rm']=pd.DataFrame(res,columns=['ag','rm','m1','t1','n','m3_nonov','t3','n3'])
    wr=ru[ru['rm']>=2]
    res=[]
    for k,g in wr.groupby('yr'):
        a=_clt(g,'x1'); b3=_clt(g,'x3'); res.append([k,a[0],a[1],a[2],b3[0]])
    out['rising_wide_up_by_year']=pd.DataFrame(res,columns=['yr','m1','t1','n','m3_ov'])
    # C: falling up days, width grading, by agitation
    fu=P[(P['trend']=='falling')&(P['r1']>0)&P['rm'].notna()].copy()
    fu['rmb']=pd.cut(fu['rm'],[0,1.2,1.5,2,3,99])
    res=[]
    for (a_,k),g in fu.groupby(['ag','rmb'],observed=True):
        a=_clt(g,'x1'); res.append([a_,str(k),a[0],a[1],a[2]])
    out['falling_up_by_ag_rm']=pd.DataFrame(res,columns=['ag','rm','m1','t1','n'])
    return out
