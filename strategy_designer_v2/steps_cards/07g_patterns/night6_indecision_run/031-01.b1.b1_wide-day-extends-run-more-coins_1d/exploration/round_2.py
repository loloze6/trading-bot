import numpy as np, pandas as pd

def _t(df, col='ex'):
    d = df.dropna(subset=[col])
    n = len(d)
    if n < 5: return (n, np.nan, np.nan, 0)
    m = d[col].mean()
    s = (d[col]-m).groupby(d['day']).sum()
    se = np.sqrt((s**2).sum())/n
    return (n, m, m/se if se>0 else np.nan, d['day'].nunique())

def _tab(df, by, col='ex'):
    rows = {}
    for k, g in df.groupby(by, observed=True):
        n, m, t, nd = _t(g, col)
        rows[k] = {'n': n, 'days': nd, 'mean_%': round(100*m,3) if m==m else m, 't': round(t,2) if t==t else t}
    return pd.DataFrame(rows).T

def _build(data, H):
    recs = []
    for coin, wins in data['bars'].items():
        cg = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c, h, l, o = b['close'], b['high'], b['low'], b['open']
            ts = pd.to_datetime(b['timestamp'])
            f = pd.DataFrame({
                'day': ts.dt.floor('D'), 'year': ts.dt.year,
                'ret5': c/c.shift(5)-1,
                'r1': c/c.shift(1)-1,
                'rr': (h-l)/(h-l).rolling(20).mean(),
                'cl': (c-l)/(h-l).replace(0,np.nan),
                'fwd': c.shift(-H)/c-1,
            })
            f = f.iloc[::H]
            f['coin']=coin; f['w']=w
            cg.append(f)
        cf = pd.concat(cg)
        cf['ex'] = cf['fwd'] - cf['fwd'].mean()
        recs.append(cf)
    d = pd.concat(recs).dropna(subset=['fwd','ret5','rr','cl'])
    d['run'] = np.where(d['ret5']>0,'up5','down5')
    d['rrq'] = pd.qcut(d['rr'],5,labels=False)
    d['clq'] = pd.qcut(d['cl'],5,labels=False)
    d['wide'] = np.where(d['rrq']>=3,'wide','narrow')
    d['cl3'] = pd.qcut(d['cl'],3,labels=['nearLow','mid','nearHigh'])
    return d

def explore(data):
    out = {}
    d3 = _build(data, 3)
    out['3d: run x wide x closeloc'] = _tab(d3, ['run','wide','cl3'])
    out['3d: year, up5 & rrq4'] = _tab(d3[(d3.run=='up5')&(d3.rrq==4)], 'year')
    out['3d: year, down5 & clq4'] = _tab(d3[(d3.run=='down5')&(d3.clq==4)], 'year')
    # graded: within down5, slope of ex on cl
    for nm, sub in [('down5', d3[d3.run=='down5']), ('up5', d3[d3.run=='up5']), ('all', d3)]:
        x = sub['cl']-sub['cl'].mean(); y = sub['ex']
        b = (x*y).sum()/(x*x).sum()
        e = y - y.mean() - b*x
        s = (x*e).groupby(sub['day']).sum()
        se = np.sqrt((s**2).sum())/(x*x).sum()
        out[f'slope ex on closeloc {nm}'] = f'b={b:.4f} t={b/se:.2f} n={len(sub)} days={sub.day.nunique()}'
        x = sub['rr']-sub['rr'].mean()
        b = (x*y).sum()/(x*x).sum(); e = y-y.mean()-b*x
        s = (x*e).groupby(sub['day']).sum(); se = np.sqrt((s**2).sum())/(x*x).sum()
        out[f'slope ex on rangeratio {nm}'] = f'b={b:.4f} t={b/se:.2f}'
    d6 = _build(data, 6)
    out['6d: run x wide x closeloc'] = _tab(d6, ['run','wide','cl3'])
    # book
    bd = []
    for coin, wins in data['days'].items():
        for w, g in wins.items():
            g = g.copy(); g['coin']=coin; g['w']=w; bd.append(g)
    bd = pd.concat(bd).dropna(subset=['book_return'])
    daily = bd.groupby('day')[['book_return','coin_return']].mean()
    out['book daily mean/sd, coin mean'] = f"book {daily.book_return.mean():.5f}/{daily.book_return.std():.5f}, coins {daily.coin_return.mean():.5f}"
    q = daily['book_return']
    top = q.nlargest(int(len(q)*0.05)).sum(); bot = q.nsmallest(int(len(q)*0.05)).sum()
    out['book: sum top5% days, bottom5%, total'] = f"{top:.3f}, {bot:.3f}, {q.sum():.3f}"
    daily['year'] = pd.to_datetime(daily.index).year
    out['book by year'] = daily.groupby('year').agg(book=('book_return','mean'), coin=('coin_return','mean'), n=('book_return','size'))
    # coins' returns after the book's biggest loss days vs gain days
    daily['next3'] = daily['coin_return'].rolling(3).sum().shift(-3)
    daily['bq'] = pd.qcut(daily['book_return'].rank(method='first'),5,labels=False)
    out['coins next-3d after book quintile'] = daily.groupby('bq')[['book_return','coin_return','next3']].mean()
    return out
