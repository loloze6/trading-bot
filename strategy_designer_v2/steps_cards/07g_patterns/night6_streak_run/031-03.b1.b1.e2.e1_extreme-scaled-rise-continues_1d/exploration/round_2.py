import numpy as np, pandas as pd
from scipy import stats

def ctstat(dev, day):
    df = pd.DataFrame({'d': dev, 'day': day}).dropna()
    N = len(df)
    if N < 5: return np.nan, np.nan, N, 0
    m = df.d.mean()
    g = df.groupby('day').d.agg(['sum', 'count'])
    D = len(g)
    if D < 3: return m, np.nan, N, D
    r = g['sum'] - g['count'] * m
    var = D / (D - 1) * (r ** 2).sum() / N ** 2
    return m, m / np.sqrt(var), N, D

def explore(data):
    out = {}
    # 1. longer horizons after scaled rises (vs10 and vs30)
    res = []
    for H in [5, 10, 20, 30]:
        rows = []
        for coin, wins in data['bars'].items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b['close'].astype(float)
                r1 = c.pct_change()
                vol60 = r1.rolling(60, min_periods=20).std()
                vs = (c / c.shift(10) - 1) / (vol60 * np.sqrt(10))
                v30 = (c / c.shift(30) - 1) / (vol60 * np.sqrt(30))
                fwd = c.shift(-H) / c - 1
                ts = pd.to_datetime(b['timestamp'])
                for i in range(0, len(b), H):
                    if np.isnan(fwd.iloc[i]): continue
                    rows.append(dict(coin=coin, day=ts.iloc[i].normalize(), fwd=fwd.iloc[i], vs=vs.iloc[i],
                                     v30=v30.iloc[i], sd=None, yr=ts.iloc[i].year, win=w))
        df = pd.DataFrame(rows)
        drift = df.groupby('coin').fwd.mean()
        usual = df.groupby('coin').fwd.std()
        df['dev'] = df.fwd - df.coin.map(drift)
        df['str'] = df.dev / df.coin.map(usual)
        for col in ['vs', 'v30']:
            d = df.dropna(subset=[col])
            for lo, hi in [(-10, -0.9487), (-0.9487, 0), (0, 0.9487), (0.9487, 1.5), (1.5, 10)]:
                s = d[(d[col] > lo) & (d[col] <= hi)]
                m, t, n, D = ctstat(s.dev.values, s.day.values)
                res.append(dict(H=H, measure=col, bin=f'({lo},{hi}]', mean_dev=m, strength=s['str'].mean(), t=t, n=n, days=D))
            # graded slope: rank correlation of measure with dev inside measure >0
            p = d[d[col] > 0]
            rho, pv = stats.spearmanr(p[col], p.dev)
            res.append(dict(H=H, measure=col + ' spearman>0', bin='', mean_dev=rho, strength=np.nan, t=pv, n=len(p), days=np.nan))
    out['horizons'] = pd.DataFrame(res)
    # 2. weekday, pooled by day (mean across coins per day), by year halves
    dl = []
    for coin, wins in data['days'].items():
        for w, d in wins.items():
            dd = d.copy(); dd['coin'] = coin; dd['win'] = w; dl.append(dd)
    D = pd.concat(dl)
    D['day'] = pd.to_datetime(D['day'])
    D['wd'] = D.day.dt.weekday
    D['yr'] = D.day.dt.year
    daym = D.groupby(['day']).agg(cr=('coin_return', 'mean'), br=('book_return', 'mean'))
    daym['wd'] = daym.index.weekday; daym['yr'] = daym.index.year
    out['weekday day-pooled'] = daym.groupby('wd').agg(cr=('cr', 'mean'), cr_sd=('cr', 'std'), br=('br', 'mean'), br_sd=('br', 'std'), n=('cr', 'count')).assign(
        cr_t=lambda x: x.cr / x.cr_sd * np.sqrt(x.n), br_t=lambda x: x.br / x.br_sd * np.sqrt(x.n))
    daym['early'] = daym.yr <= 2021
    g = daym.groupby(['early', 'wd']).cr.agg(['mean', 'std', 'count'])
    g['t'] = g['mean'] / g['std'] * np.sqrt(g['count'])
    out['weekday coin by era (early<=2021)'] = g
    # 3. book: largest gain/loss days, which weekday, and the coin's prior 10d scaled rise
    bk = daym.br.dropna()
    q_hi, q_lo = bk.quantile(0.95), bk.quantile(0.05)
    out['book top5% days by weekday'] = daym[daym.br >= q_hi].wd.value_counts().sort_index()
    out['book bottom5% days by weekday'] = daym[daym.br <= q_lo].wd.value_counts().sort_index()
    # 4. after book's largest days: next 10 days book mean
    daym['next10'] = daym.br[::-1].rolling(10, min_periods=5).sum()[::-1].shift(-1)
    out['book next10 after top/bottom'] = pd.DataFrame({'after_top': [daym[daym.br >= q_hi].next10.mean()],
                                                       'after_bottom': [daym[daym.br <= q_lo].next10.mean()],
                                                       'all': [daym.next10.mean()]})
    return out
