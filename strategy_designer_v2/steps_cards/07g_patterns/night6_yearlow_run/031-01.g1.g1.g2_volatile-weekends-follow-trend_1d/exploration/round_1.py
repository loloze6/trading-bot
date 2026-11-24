import numpy as np, pandas as pd
from scipy import stats

def _prep(df):
    df = df.copy()
    df['ts'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('ts').reset_index(drop=True)
    c = df['close']
    lr = np.log(c).diff()
    df['r1'] = c.pct_change()
    df['vol20'] = lr.rolling(20).std()
    df['volr'] = df['vol20'] / df['vol20'].rolling(60).mean()
    df['ret14'] = c / c.shift(14) - 1
    df['z14'] = (df['ret14'] - df['ret14'].rolling(60, min_periods=20).mean()) / df['ret14'].rolling(60, min_periods=20).std()
    df['zr1'] = df['r1'] / df['vol20']
    df['pos30'] = (c - c.rolling(30).min()) / (c.rolling(30).max() - c.rolling(30).min())
    df['wd'] = df['ts'].dt.weekday
    df['f1'] = c.shift(-1) / c - 1
    df['f2'] = c.shift(-2) / c - 1
    df['f5'] = c.shift(-5) / c - 1
    df['idx'] = np.arange(len(df))
    return df

def _slope(x, y):
    m = ~(np.isnan(x) | np.isnan(y))
    x, y = x[m], y[m]
    if len(x) < 20: return (np.nan, np.nan, len(x))
    r = stats.linregress(x, y)
    return (r.slope, r.slope / r.stderr, len(x))

def explore(data):
    bars = data['bars']
    allb = []
    drift = {}
    for coin in bars:
        parts = []
        g2, g1, g5 = [], [], []
        for w, df in bars[coin].items():
            d = _prep(df); d['coin'] = coin; d['win'] = w
            parts.append(d)
            g1 += list(d['f1'].values[::1]); g2 += list(d['f2'].values[::2]); g5 += list(d['f5'].values[::5])
        drift[coin] = (np.nanmean(g1), np.nanmean(g2), np.nanmean(g5))
        b = pd.concat(parts)
        b['x1'] = b['f1'] - drift[coin][0]; b['x2'] = b['f2'] - drift[coin][1]; b['x5'] = b['f5'] - drift[coin][2]
        allb.append(b)
    B = pd.concat(allb, ignore_index=True)
    out = {}
    # 1 weekday: slope of 2-day excess on z14, by weekday and vol regime
    rows = []
    for k in range(7):
        s = B[B.wd == k]
        for lab, ss in [('hi', s[s.volr > 1]), ('lo', s[s.volr <= 1]), ('all', s)]:
            sl, t, n = _slope(ss['z14'].values, ss['x2'].values)
            rows.append({'wd': k, 'vol': lab, 'slope2d_on_z14': sl, 't': t, 'n': n})
    out['weekday_trend_slope_2d'] = pd.DataFrame(rows)
    # 2 weekday seasonality of 1-day returns
    rows = []
    for k in range(7):
        s = B[B.wd == k]['x1'].dropna()
        rows.append({'wd': k, 'mean_excess_1d': s.mean(), 't': s.mean() / (s.std() / np.sqrt(len(s))), 'n': len(s),
                     'absmean': B[B.wd == k]['f1'].abs().mean()})
    out['weekday_1d'] = pd.DataFrame(rows)
    # 3 after large daily moves: next-day excess by zr1 quintile, by vol regime
    B['zq'] = pd.qcut(B['zr1'], 5, labels=False)
    out['next1d_by_today_move_quintile'] = B.groupby(['zq']).agg(mean_x1=('x1', 'mean'), n=('x1', 'count'), mean_z=('zr1', 'mean')).reset_index()
    # 4 position in 30-day range: 5-day forward on grid idx%5==0
    G5 = B[B.idx % 5 == 0].copy()
    G5['pq'] = pd.qcut(G5['pos30'], 5, labels=False)
    agg = G5.groupby('pq').agg(mean_x5=('x5', 'mean'), sd=('x5', 'std'), n=('x5', 'count'), pos=('pos30', 'mean')).reset_index()
    agg['t'] = agg.mean_x5 / (agg.sd / np.sqrt(agg.n))
    out['fwd5_by_pos30_quintile'] = agg
    sl, t, n = _slope(G5['z14'].values, G5['x5'].values)
    out['fwd5_slope_on_z14_all_days_grid'] = pd.Series({'slope': sl, 't': t, 'n': n})
    # hi-vol only 5-day trend
    h = G5[G5.volr > 1]; l = G5[G5.volr <= 1]
    out['fwd5_slope_z14_hi_lo'] = pd.DataFrame([dict(zip(['slope', 't', 'n'], _slope(h['z14'].values, h['x5'].values)), vol='hi'),
                                                 dict(zip(['slope', 't', 'n'], _slope(l['z14'].values, l['x5'].values)), vol='lo')])
    # 5 Fridays: weekend signed excess by volr bins (graded?)
    F = B[(B.wd == 4)].dropna(subset=['z14', 'x2', 'volr']).copy()
    F['g'] = np.sign(F['z14']) * F['x2']
    F['vq'] = pd.qcut(F['volr'], 4, labels=False)
    a = F.groupby('vq').agg(signed_x2=('g', 'mean'), sd=('g', 'std'), n=('g', 'count'), volr=('volr', 'mean')).reset_index()
    a['t'] = a.signed_x2 / (a.sd / np.sqrt(a.n)); out['fri_signed_weekend_by_volr_quartile'] = a
    F['zq'] = pd.qcut(F['z14'], 5, labels=False)
    out['fri_x2_by_z14_quintile_hivol'] = F[F.volr > 1].groupby('zq').agg(x2=('x2', 'mean'), n=('x2', 'count'), z=('z14', 'mean')).reset_index()
    out['fri_x2_by_z14_quintile_lovol'] = F[F.volr <= 1].groupby('zq').agg(x2=('x2', 'mean'), n=('x2', 'count'), z=('z14', 'mean')).reset_index()
    # per coin hi-vol Friday slope
    rows = []
    for coin, s in F[F.volr > 1].groupby('coin'):
        sl, t, n = _slope(s['z14'].values, s['x2'].values); rows.append({'coin': coin, 'slope': sl, 't': t, 'n': n})
    out['fri_hivol_slope_by_coin'] = pd.DataFrame(rows)
    # by year
    F['year'] = F.ts.dt.year
    rows = []
    for y, s in F[F.volr > 1].groupby('year'):
        sl, t, n = _slope(s['z14'].values, s['x2'].values); rows.append({'year': y, 'slope': sl, 't': t, 'n': n})
    out['fri_hivol_slope_by_year'] = pd.DataFrame(rows)
    # trades
    tr = []
    for coin in data['trades']:
        for w, t_ in data['trades'][coin].items():
            if len(t_): tt = t_.copy(); tt['coin'] = coin; tr.append(tt)
    if tr:
        T = pd.concat(tr)
        out['trades_by_side'] = T.groupby('side').agg(n=('net_profit_loss_percent', 'count'), mean_net=('net_profit_loss_percent', 'mean'),
                                                     mean_gross=('profit_loss_percent', 'mean'), win=('net_profit_loss_percent', lambda s: (s > 0).mean()),
                                                     dur_h=('duration_minutes', lambda s: s.mean() / 60)).reset_index()
    return out
