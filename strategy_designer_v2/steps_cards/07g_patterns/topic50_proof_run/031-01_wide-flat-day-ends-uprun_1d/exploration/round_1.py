import pandas as pd, numpy as np

def _feat(df):
    d = df.copy().reset_index(drop=True)
    o,h,l,c = d['open'],d['high'],d['low'],d['close']
    rng = (h-l)
    d['rng'] = rng
    d['rr'] = rng / rng.rolling(20).mean()
    d['flat'] = 1 - (c-o).abs()/rng.replace(0,np.nan)
    d['clv'] = (c-l)/rng.replace(0,np.nan)
    d['r1'] = c.pct_change()
    d['r5'] = c/c.shift(5)-1
    d['r20'] = c/c.shift(20)-1
    d['r60'] = c/c.shift(60)-1
    d['vol20'] = d['r1'].rolling(20).std()
    d['volrel'] = d['vol20']/d['r1'].rolling(60).std()
    d['fwd5'] = c.shift(-5)/c-1
    d['fwd1'] = c.shift(-1)/c-1
    d['pos'] = np.arange(len(d))
    d['cell'] = d['pos']//5
    d['ts'] = pd.to_datetime(d['timestamp'])
    d['dayk'] = d['ts'].dt.floor('D')
    d['wd'] = d['ts'].dt.weekday
    return d

def _t(x, days):
    x = np.asarray(x, float); m = ~np.isnan(x)
    x = x[m]; dk = np.asarray(days)[m]
    if len(x) < 3: return (len(x), np.nan, np.nan, 0)
    mu = x.mean()
    s = pd.Series(x-mu).groupby(dk).sum()
    se = np.sqrt((s**2).sum())/len(x)
    return (len(x), mu, mu/se if se>0 else np.nan, len(s))

def explore(data):
    rows=[]
    for coin, wins in data['bars'].items():
        for w, df in wins.items():
            d=_feat(df); d['coin']=coin; d['win']=w
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    grid = A[A['pos']%5==0].dropna(subset=['fwd5'])
    drift = grid.groupby('coin')['fwd5'].agg(['mean','std'])
    A['ex5'] = A['fwd5'] - A['coin'].map(drift['mean'])
    A['z5'] = A['ex5']/A['coin'].map(drift['std'])
    G = A[(A['pos']%5==0)].dropna(subset=['ex5','rr','r5','flat'])
    out={}
    out['drift_by_coin']=drift
    def cases(mask, sign=1):
        sub=A[mask & A['ex5'].notna()]
        sub=sub.groupby(['coin','win','cell']).head(1)
        n,mu,t,nd=_t(sign*sub['ex5'], sub['dayk'])
        return pd.Series({'n':n,'mean_ex5':mu,'t':t,'days':nd,'z':(sign*sub['z5']).mean()})
    up=A['r5']>0; dn=A['r5']<0
    wide=A['rr']>=1.5; flat=A['flat']>=0.9; narrow=A['rr']<0.8
    C={}
    C['wideflat_after_up (long dir)']=cases(up&wide&flat)
    C['wideflat_after_down (long dir)']=cases(dn&wide&flat)
    C['narrowflat_after_up']=cases(up&narrow&flat)
    C['narrowflat_after_down']=cases(dn&narrow&flat)
    C['wide_closehigh_after_up']=cases(up&wide&(A['clv']>0.8))
    C['wide_closelow_after_up']=cases(up&wide&(A['clv']<0.2))
    C['wide_closehigh_after_down']=cases(dn&wide&(A['clv']>0.8))
    C['wide_closelow_after_down']=cases(dn&wide&(A['clv']<0.2))
    C['wide_any']=cases(wide)
    C['wide_flat_rr>=2']=cases(wide&flat&(A['rr']>=2))
    out['conditional_cases_long_direction']=pd.DataFrame(C).T
    # graded grid bins
    for col in ['rr','flat','clv','r1','r5','r20','r60','volrel']:
        g=G.dropna(subset=[col]).copy()
        g['q']=pd.qcut(g[col],5,labels=False,duplicates='drop')
        res=g.groupby('q').apply(lambda s: pd.Series(dict(zip(['n','mean','t','days'],_t(s['ex5'],s['dayk']))) | {'feat_mean':s[col].mean()}))
        out['grid_ex5_by_'+col]=res
    g=G.copy(); g['q']=pd.qcut(g['rr'],3,labels=False); g['s']=np.sign(g['r5'])
    out['grid_ex5_by_rr_x_r5sign']=g.groupby(['s','q']).apply(lambda s: pd.Series(dict(zip(['n','mean','t','days'],_t(s['ex5'],s['dayk'])))))
    # weekday on 1-day returns (all bars)
    a=A.dropna(subset=['fwd1'])
    out['fwd1_by_weekday']=a.groupby('wd').apply(lambda s: pd.Series(dict(zip(['n','mean','t','days'],_t(s['fwd1'],s['dayk'])))))
    # regime/trades summary
    tr=[]
    for coin,wins in data['trades'].items():
        for w,t in wins.items():
            if len(t): t=t.copy(); t['coin']=coin; t['win']=w; tr.append(t)
    if tr:
        T=pd.concat(tr)
        out['trades_by_coin']=T.groupby('coin')['net_profit_loss_percent'].agg(['count','mean','median'])
        out['trades_by_win']=T.groupby('win')['net_profit_loss_percent'].agg(['count','mean'])
    return out
