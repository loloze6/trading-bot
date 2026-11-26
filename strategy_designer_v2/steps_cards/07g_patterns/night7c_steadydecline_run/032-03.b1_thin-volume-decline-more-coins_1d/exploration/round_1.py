import numpy as np, pandas as pd
from scipy import stats

def _clt(df, col):
    # day-clustered t of mean of col
    d = df.dropna(subset=[col])
    if len(d) < 5: return np.nan, len(d), 0
    m = d[col].mean()
    g = (d[col]-m).groupby(d['day']).sum()
    G = len(g)
    se = np.sqrt((g**2).sum()*G/(G-1))/len(d)
    return m/se if se>0 else np.nan, len(d), G

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b['close']; v = b['volume']
            rng = (b['high']-b['low'])/c
            r1 = c.pct_change()
            f = pd.DataFrame({'coin':coin,'win':w,'day':pd.to_datetime(b['timestamp']).dt.floor('D')})
            f['ret28'] = c/c.shift(28)-1
            f['ret5p'] = c/c.shift(5)-1
            f['ret1'] = r1
            f['ret90'] = c/c.shift(90)-1
            v28 = v.rolling(28).mean(); v90 = v.shift(28).rolling(90).mean()
            f['vratio'] = np.log(v28/v90)
            r28 = rng.rolling(28).mean(); r90 = rng.shift(28).rolling(90).mean()
            f['rratio'] = np.log(r28/r90)
            f['vol28'] = r1.rolling(28).std()
            f['maxdd1_28'] = r1.rolling(28).min()
            f['fwd5'] = c.shift(-5)/c-1
            f['fwd1'] = c.shift(-1)/c-1
            f['fc'] = b['forecast']
            f['wd'] = f['day'].dt.weekday
            f['grid'] = (np.arange(len(b))%5==0)
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    G = A[A.grid & A.fwd5.notna()].copy()
    drift = G.groupby('coin')['fwd5'].mean()
    G['ex5'] = G['fwd5'] - G['coin'].map(drift)
    sd = G.groupby('coin')['fwd5'].std()
    G['z5'] = G['ex5']/G['coin'].map(sd)
    out = {}
    out['drift_by_coin'] = pd.DataFrame({'drift':drift,'sd':sd,'n':G.groupby('coin').size()})
    def tab(D, key, q=5):
        D = D.dropna(subset=[key,'ex5']).copy()
        D['b'] = pd.qcut(D[key], q, labels=False, duplicates='drop')
        res = []
        for k, g in D.groupby('b'):
            t, n, nd = _clt(g, 'ex5')
            res.append({'bin':k,'key_mean':g[key].mean(),'ex5':g['ex5'].mean(),'raw5':g['fwd5'].mean(),'t':t,'n':n,'days':nd})
        return pd.DataFrame(res)
    dec = G[G.ret28<0]
    out['all_by_ret28'] = tab(G,'ret28')
    out['dec_by_ret28'] = tab(dec,'ret28')
    out['dec_by_vratio'] = tab(dec,'vratio')
    out['dec_by_rratio'] = tab(dec,'rratio')
    out['all_by_ret5p'] = tab(G,'ret5p')
    out['all_by_ret90'] = tab(G,'ret90')
    out['all_by_vol28'] = tab(G,'vol28')
    out['all_by_vratio'] = tab(G,'vratio')
    out['all_by_rratio'] = tab(G,'rratio')
    out['all_by_maxdd1'] = tab(G,'maxdd1_28')
    # calm vs panic in decline: slope of ex5 on ret28
    res=[]
    for lab, g in [('calm',dec[dec.rratio<dec.rratio.median()]),('panic',dec[dec.rratio>=dec.rratio.median()])]:
        g=g.dropna(subset=['ret28','ex5'])
        s=stats.linregress(g['ret28'],g['ex5'])
        res.append({'grp':lab,'slope':s.slope,'t':s.slope/s.stderr,'n':len(g),'ex5':g.ex5.mean()})
    out['dec_slope_ret28_calm_panic']=pd.DataFrame(res)
    # weekday, daily
    D1 = A.dropna(subset=['fwd1']).copy()
    d1 = D1.groupby('coin')['fwd1'].transform('mean'); D1['ex1']=D1['fwd1']-d1
    res=[]
    for k,g in D1.groupby('wd'):
        t,n,nd=_clt(g.rename(columns={'ex1':'x'}),'x')
        res.append({'wd':k,'ex1':g.ex1.mean(),'t':t,'n':n})
    out['weekday_next1']=pd.DataFrame(res)
    # by year
    G['yr']=G['day'].dt.year
    res=[]
    for k,g in dec.assign(yr=dec['day'].dt.year).groupby('yr'):
        t,n,nd=_clt(g,'ex5'); res.append({'yr':k,'ex5':g.ex5.mean(),'t':t,'n':n})
    out['dec_by_year']=pd.DataFrame(res)
    return out
