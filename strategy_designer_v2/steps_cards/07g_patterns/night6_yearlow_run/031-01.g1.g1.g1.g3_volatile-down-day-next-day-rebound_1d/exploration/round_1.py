import numpy as np, pandas as pd
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3 or x.std() == 0: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def _summ(df, by, col='ex1'):
    g = df.dropna(subset=[col]).groupby(by)[col]
    out = pd.DataFrame({'n': g.size(), 'mean%': g.mean()*100, 't': g.apply(_t)})
    return out

def explore(data):
    rows = []
    for coin, wins in data['bars'].items():
        for w, b in wins.items():
            b = b.sort_values('timestamp').reset_index(drop=True)
            c = b['close']; r = c.pct_change()
            sd = r.rolling(20, min_periods=15).std()
            d = pd.DataFrame({'coin': coin, 'win': w, 'ts': pd.to_datetime(b['timestamp'])})
            d['r'] = r; d['z'] = r / sd.shift(1)
            d['sd20'] = sd
            d['f1'] = c.shift(-1)/c - 1
            d['f3'] = c.shift(-3)/c - 1
            d['pos'] = np.arange(len(b))
            d['regime'] = b['regime'].values
            d['fc'] = b['forecast'].values
            rng = (b['high'] - b['low']).replace(0, np.nan)
            d['clv'] = (c - b['low']) / rng
            d['wick'] = (np.minimum(b['open'], c) - b['low']) / rng
            lo30 = b['low'].rolling(30, min_periods=20).min().shift(1)
            d['dlo30'] = (c/lo30 - 1) / sd
            d['r5'] = c / c.shift(5) - 1
            d['z5'] = d['r5'] / (sd*np.sqrt(5))
            d['vol_c'] = b['volume'] / b['volume'].rolling(20, min_periods=10).mean().shift(1)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby('coin')['f1'].mean()
    D['ex1'] = D['f1'] - D['coin'].map(mu1)
    D['wd'] = D['ts'].dt.weekday; D['yr'] = D['ts'].dt.year
    D['vol'] = np.where(D['regime'] == 'mean_reversion', 'hi', 'other')
    D['zb'] = pd.cut(D['z'], [-np.inf, -2.5, -1.5, -0.75, 0, 0.75, 1.5, 2.5, np.inf])
    res = {}
    res['z bucket x vol regime'] = _summ(D, ['vol', 'zb'])
    dn = D[D['z'] < 0]
    res['falls: corr z vs ex1 by vol'] = dn.dropna(subset=['ex1','z']).groupby('vol').apply(lambda g: pd.Series({'n': len(g), 'r': g['z'].corr(g['ex1']), 't': g['z'].corr(g['ex1'])*np.sqrt(len(g)-2)}))
    big = D[D['z'] <= -1.5]
    res['big falls by vol x clv third'] = _summ(big.assign(clvb=pd.cut(big['clv'], [0, .33, .66, 1.0], include_lowest=True)), ['vol', 'clvb'])
    res['big falls by vol x volume surge'] = _summ(big.assign(vb=pd.qcut(big['vol_c'], 3, labels=['lowV','midV','hiV'])), ['vol', 'vb'])
    res['big falls by 5d z tercile'] = _summ(big.assign(b5=pd.qcut(big['z5'], 3, labels=['deep','mid','shallow'])), ['b5'])
    res['big falls by dist to 30d low'] = _summ(big.assign(bl=pd.qcut(big['dlo30'], 3, labels=['below/at','near','far'])), ['bl'])
    res['big falls by weekday'] = _summ(big, ['wd'])
    res['big falls by coin'] = _summ(big, ['coin'])
    res['big falls by year'] = _summ(big, ['yr'])
    # all bars: clv effect
    res['all bars clv quintile'] = _summ(D.assign(cb=pd.qcut(D['clv'], 5, labels=False)), ['vol', 'cb'])
    res['all bars weekday'] = _summ(D, ['wd'])
    # 3-day horizon grid after big falls
    g3 = D[D['pos'] % 3 == 0].copy()
    mu3 = g3.groupby('coin')['f3'].mean()
    g3['ex3'] = g3['f3'] - g3['coin'].map(mu3)
    res['3d grid: z bucket x vol'] = _summ(g3, ['vol', 'zb'], 'ex3')
    # book: largest days
    dd = []
    for coin, wins in data['days'].items():
        for w, t in wins.items():
            dd.append(t.assign(coin=coin))
    DD = pd.concat(dd)
    br = DD['book_return'].dropna()
    res['book day ret quantiles %'] = (br.quantile([.001, .01, .05, .5, .95, .99, .999])*100)
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data['trades'].items() for t in ws.values()])
    tr['fb'] = pd.qcut(tr['entry_forecast'], 4, labels=False, duplicates='drop')
    res['trades by entry forecast q'] = tr.groupby('fb')['net_profit_loss_percent'].agg(['size','mean','median'])
    res['trades duration days'] = (tr['duration_minutes']/1440).describe()
    return res
