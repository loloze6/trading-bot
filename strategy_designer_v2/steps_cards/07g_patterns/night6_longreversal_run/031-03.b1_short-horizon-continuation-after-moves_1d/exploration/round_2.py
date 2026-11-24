import numpy as np, pandas as pd
from scipy import stats

def _clustered_t(df, col, daycol='day'):
    s = df.dropna(subset=[col])
    m = s[col].mean()
    dev = (s[col] - m).groupby(s[daycol]).sum()
    se = np.sqrt((dev ** 2).sum()) / len(s)
    return m, (m / se if se > 0 else np.nan), len(s), s[daycol].nunique()

def explore(data):
    out = {}
    d = []
    for coin, wins in data['days'].items():
        for w, df in wins.items():
            df = df.copy().reset_index(drop=True)
            df['coin'] = coin; df['w'] = w
            r = df['coin_return']
            sd30 = r.rolling(30, min_periods=20).std().shift(1)
            df['z0'] = r / sd30                 # today's move vs usual (known at close)
            df['f1'] = r.shift(-1)
            df['f3'] = df['close'].shift(-3) / df['close'] - 1
            df['f1z'] = df['f1'] / sd30
            df['f3z'] = df['f3'] / (sd30 * np.sqrt(3))
            df['ret2'] = df['close'] / df['close'].shift(2) - 1
            df['z2'] = df['ret2'] / (sd30 * np.sqrt(2))
            df['vol_rank'] = sd30
            df['wd'] = pd.to_datetime(df['day']).dt.dayofweek
            df['yr'] = pd.to_datetime(df['day']).dt.year
            df['dayn'] = pd.to_datetime(df['day']).astype('int64')
            df['wn'] = int(w[1:])
            d.append(df)
    d = pd.concat(d, ignore_index=True)
    d['day'] = d['dayn']
    # drift removal per coin
    for c in ['f1z', 'f3z']:
        d[c + 'x'] = d[c] - d.groupby('coin')[c].transform('mean')
    # graded buckets, day-clustered t
    d['zb'] = pd.cut(d['z0'], [-99, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 99])
    rows = []
    for b, s in d.groupby('zb', observed=True):
        m1, t1, n, nd = _clustered_t(s, 'f1zx')
        m3, t3, _, _ = _clustered_t(s, 'f3zx')
        rows.append(dict(b=str(b), n=n, days=nd, f1=m1, t1=t1, f3_nonoverlap_not=m3, t3=t3))
    out['next day / 3 days by today z (clustered)'] = pd.DataFrame(rows).round(3)
    # signed reversal measure: -sign... regression slope of f1zx on z0 clipped, clustered
    s = d.dropna(subset=['z0', 'f1zx']).copy()
    s['zc'] = s['z0'].clip(-4, 4)
    X = s['zc'] - s['zc'].mean()
    beta = (X * s['f1zx']).sum() / (X ** 2).sum()
    resid = s['f1zx'] - s['f1zx'].mean() - beta * X
    g = (X * resid).groupby(s['day']).sum()
    se = np.sqrt((g ** 2).sum()) / (X ** 2).sum()
    out['slope f1z on z0 (clustered)'] = pd.Series(dict(beta=beta, t=beta / se, n=len(s), days=s['day'].nunique())).round(4)
    # per coin and per year: reversal = mean of -sign(z0)*f1zx for |z0|>1.5
    s2 = s[s['z0'].abs() > 1.5].copy()
    s2['rev'] = -np.sign(s2['z0']) * s2['f1zx']
    s2['revraw'] = -np.sign(s2['z0']) * s2['f1']
    rows = []
    for k, ss in s2.groupby('coin'):
        m, t, n, nd = _clustered_t(ss, 'rev'); rows.append(dict(k=k, n=n, rev=m, t=t, raw=ss['revraw'].mean()))
    out['reversal |z|>1.5 per coin'] = pd.DataFrame(rows).round(4)
    rows = []
    for k, ss in s2.groupby('yr'):
        m, t, n, nd = _clustered_t(ss, 'rev'); rows.append(dict(k=k, n=n, rev=m, t=t, raw=ss['revraw'].mean()))
    out['reversal |z|>1.5 per year'] = pd.DataFrame(rows).round(4)
    # down vs up side separately graded
    rows = []
    for side, ss in [('down', s2[s2.z0 < 0]), ('up', s2[s2.z0 > 0])]:
        m, t, n, nd = _clustered_t(ss, 'rev'); rows.append(dict(side=side, n=n, days=nd, rev=m, t=t, raw=ss['revraw'].mean()))
    out['reversal by side'] = pd.DataFrame(rows).round(4)
    # by volatility tercile (per coin)
    s2['vt'] = s2.groupby('coin')['vol_rank'].transform(lambda x: pd.qcut(x.rank(method='first'), 3, labels=False))
    rows = []
    for k, ss in s2.groupby('vt'):
        m, t, n, nd = _clustered_t(ss, 'rev'); rows.append(dict(vt=k, n=n, rev=m, t=t, raw=ss['revraw'].mean()))
    out['reversal by vol tercile'] = pd.DataFrame(rows).round(4)
    # weekday, clustered by day
    d['rz'] = d['coin_return'] / d.groupby('coin')['coin_return'].transform('std')
    d['rzx'] = d['rz'] - d.groupby('coin')['rz'].transform('mean')
    rows = []
    for k, ss in d.groupby('wd'):
        m, t, n, nd = _clustered_t(ss, 'rzx'); rows.append(dict(wd=k, n=n, days=nd, ex=m, t=t))
    out['weekday excess z (clustered)'] = pd.DataFrame(rows).round(3)
    # weekday by half of sample
    d['half'] = np.where(d['wn'] <= 12, 'w1-12', 'w13-24')
    rows = []
    for (h, k), ss in d.groupby(['half', 'wd']):
        m, t, n, nd = _clustered_t(ss, 'rzx'); rows.append(dict(half=h, wd=k, ex=m, t=t))
    out['weekday by half'] = pd.DataFrame(rows).round(3)
    # 2-day move reversal
    d['z2b'] = pd.cut(d['z2'], [-99, -2, -1, 1, 2, 99])
    rows = []
    for b, ss in d.groupby('z2b', observed=True):
        m, t, n, nd = _clustered_t(ss, 'f1zx'); rows.append(dict(b=str(b), n=n, f1=m, t=t))
    out['next day by 2-day z'] = pd.DataFrame(rows).round(3)
    return out
