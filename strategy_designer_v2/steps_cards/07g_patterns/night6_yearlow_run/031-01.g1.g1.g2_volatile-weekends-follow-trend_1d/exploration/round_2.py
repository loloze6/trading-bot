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
    df['day'] = df['ts'].dt.floor('D')
    return df

def _ct(vals, days):
    s = pd.Series(vals).groupby(np.asarray(days)).sum()
    s = s.dropna()
    if len(s) < 10: return (np.nan, np.nan, len(s))
    return (s.mean(), s.mean() / (s.std() / np.sqrt(len(s))), len(s))

def explore(data):
    bars = data['bars']
    allb = []
    for coin in bars:
        parts = []; g1, g2, g5 = [], [], []
        for w, df in bars[coin].items():
            d = _prep(df); d['coin'] = coin; d['win'] = w; parts.append(d)
            g1 += list(d['f1'].values); g2 += list(d['f2'].values[::2]); g5 += list(d['f5'].values[::5])
        b = pd.concat(parts)
        b['x1'] = b['f1'] - np.nanmean(g1); b['x2'] = b['f2'] - np.nanmean(g2); b['x5'] = b['f5'] - np.nanmean(g5)
        b['sd2'] = np.nanstd(g2)
        allb.append(b)
    B = pd.concat(allb, ignore_index=True)
    B['year'] = B.ts.dt.year
    out = {}
    # A: 14-day trend on 2-day excess, day-clustered, by weekday and vol; signed product z14*x2 (capped z)
    B['zc'] = B['z14'].clip(-2, 2)
    B['p2'] = B['zc'] * B['x2']
    rows = []
    for k in range(7):
        for lab, m in [('hi', B.volr > 1), ('lo', B.volr <= 1), ('all', B.volr.notna())]:
            s = B[(B.wd == k) & m].dropna(subset=['p2'])
            mu, t, n = _ct(s['p2'].values, s['day'].values)
            rows.append({'wd': k, 'vol': lab, 'mean_zx2_perday': mu, 't_day': t, 'days': n})
    out['A_trend2d_weekday_vol_dayclustered'] = pd.DataFrame(rows)
    # A2: all-days 2-day grid trend, by volr quartile (graded by vol?)
    G2 = B[B.idx % 2 == 0].dropna(subset=['p2', 'volr']).copy()
    G2['vq'] = pd.qcut(G2['volr'], 4, labels=False)
    rows = []
    for q, s in G2.groupby('vq'):
        mu, t, n = _ct(s['p2'].values, s['day'].values); rows.append({'vq': q, 'volr': s.volr.mean(), 'mean': mu, 't_day': t, 'days': n})
    out['A2_trend2d_grid_by_volr_q'] = pd.DataFrame(rows)
    # A3: Wed+Thu trend by year (robustness)
    s0 = B[B.wd.isin([2, 3])].dropna(subset=['p2'])
    rows = []
    for y, s in s0.groupby('year'):
        mu, t, n = _ct(s['p2'].values, s['day'].values); rows.append({'year': y, 'mean': mu, 't_day': t, 'days': n})
    out['A3_wedthu_trend_by_year'] = pd.DataFrame(rows)
    # A4: Wed+Thu trend by coin
    rows = []
    for c, s in s0.groupby('coin'):
        sl = stats.linregress(s['zc'], s['x2']); rows.append({'coin': c, 'slope': sl.slope, 't': sl.slope / sl.stderr, 'n': len(s)})
    out['A4_wedthu_trend_by_coin'] = pd.DataFrame(rows)
    # A5: quintiles of z14 on Thursday, 2-day excess
    th = B[B.wd == 3].dropna(subset=['z14', 'x2']).copy()
    th['zq'] = pd.qcut(th['z14'], 5, labels=False)
    out['A5_thu_x2_by_z14_q'] = th.groupby('zq').agg(x2=('x2', 'mean'), n=('x2', 'count'), z=('z14', 'mean')).reset_index()
    # B: weekday 1-day excess, day-clustered (mean over coins per day)
    rows = []
    for k in range(7):
        s = B[B.wd == k].dropna(subset=['x1'])
        m = s.groupby('day')['x1'].mean()
        rows.append({'wd': k, 'mean': m.mean(), 't_day': m.mean() / (m.std() / np.sqrt(len(m))), 'days': len(m)})
    out['B_weekday_1d_dayclustered'] = pd.DataFrame(rows)
    rows = []
    for y, s in B[B.wd == 4].dropna(subset=['x1']).groupby('year'):
        m = s.groupby('day')['x1'].mean(); rows.append({'year': y, 'fri_mean': m.mean(), 't': m.mean() / (m.std() / np.sqrt(len(m))), 'days': len(m)})
    out['B2_friday_1d_by_year'] = pd.DataFrame(rows)
    # C: next-day after large down day, graded, day-clustered
    B['zq'] = pd.qcut(B['zr1'], 10, labels=False)
    rows = []
    for q, s in B.dropna(subset=['x1', 'zq']).groupby('zq'):
        m = s.groupby('day')['x1'].mean(); rows.append({'decile': q, 'z': s.zr1.mean(), 'mean_x1': m.mean(), 't_day': m.mean() / (m.std() / np.sqrt(len(m))), 'days': len(m)})
    out['C_next1d_by_zr1_decile'] = pd.DataFrame(rows)
    # D: book positions: gain on long vs short bars, Friday long/short by z14 sign
    F = B[(B.wd == 4) & (B.volr > 1)].dropna(subset=['z14', 'x2'])
    rows = []
    for lab, s in [('z>0', F[F.z14 > 0]), ('z<0', F[F.z14 < 0])]:
        m = s.groupby('day')['x2'].mean(); rows.append({'side': lab, 'mean_x2': m.mean(), 't_day': m.mean() / (m.std() / np.sqrt(len(m))), 'days': len(m)})
    out['D_fri_hivol_x2_by_sign'] = pd.DataFrame(rows)
    # E: pos30 graded on 5-day grid day-clustered
    G5 = B[B.idx % 5 == 0].dropna(subset=['pos30', 'x5']).copy()
    G5['pc'] = G5['pos30'] - 0.5
    G5['p5'] = G5['pc'] * G5['x5']
    mu, t, n = _ct(G5['p5'].values, G5['day'].values)
    out['E_pos30_x5_product'] = pd.Series({'mean': mu, 't_day': t, 'days': n})
    return out
