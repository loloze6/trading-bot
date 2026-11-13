import pandas as pd, numpy as np
from scipy import stats

def wstats(df, col='ex', w='w'):
    if len(df) < 3: return pd.Series({'n': len(df), 'wmean': np.nan, 't': np.nan, 'hit': np.nan})
    x = df[col].values; ww = df[w].values
    m = np.sum(ww*x)/np.sum(ww); n = len(x)
    se = np.sqrt(np.sum(ww**2*(x-m)**2)*n/(n-1))/np.sum(ww)
    return pd.Series({'n': n, 'wmean': m, 't': m/se if se > 0 else np.nan, 'hit': (x > 0).mean()})

def explore(data):
    rows = []
    btc = {}
    for wk, b in data['bars']['BTCUSD'].items():
        b = b.copy()
        b['bf'] = b['close'].shift(-10)/b['close'] - 1
        btc[wk] = b.set_index('timestamp')['bf']
    for coin, wins in data['bars'].items():
        allf = []
        for wk, b in wins.items():
            allf.append((b['close'].shift(-10)/b['close'] - 1).dropna())
        hold = pd.concat(allf).mean()
        for wk, b in wins.items():
            b = b.reset_index(drop=True).copy()
            sp = b['debug_info.components.sma_cross_down.last_history_value']
            b['fwd'] = b['close'].shift(-10)/b['close'] - 1
            b['mom20'] = b['close']/b['close'].shift(20) - 1
            b['dsp'] = sp - sp.shift(10)
            b['vol'] = np.log(b['close']).diff().rolling(20).std()
            b['sp'] = sp
            b['ts'] = pd.to_datetime(b['timestamp'])
            b['bf'] = b['timestamp'].map(btc.get(wk, pd.Series(dtype=float)))
            s = b.iloc[::10]
            s = s[(s['forecast'] < 0) & s['fwd'].notna()]
            for _, r in s.iterrows():
                rows.append({'coin': coin, 'win': wk, 'year': r['ts'].year, 'f': r['forecast'], 'w': abs(r['forecast']),
                             'ex': -(r['fwd'] - hold), 'mom20': r['mom20'], 'dsp': r['dsp'], 'vol': r['vol'], 'sp': r['sp'],
                             'bf': r['bf'], 'fwd': r['fwd']})
    d = pd.DataFrame(rows)
    out = {}
    out['all'] = wstats(d).to_frame().T
    out['by_coin'] = d.groupby('coin').apply(wstats)
    out['by_year'] = d.groupby('year').apply(wstats)
    out['by_window'] = d.groupby('win').apply(wstats)
    d['terc'] = pd.qcut(d['w'].rank(method='first'), 3, labels=['low', 'mid', 'high'])
    out['by_tercile'] = d.groupby('terc').apply(wstats)
    d['mom_neg'] = np.where(d['mom20'] < 0, 'mom20<0', 'mom20>=0')
    out['by_mom20'] = d.dropna(subset=['mom20']).groupby('mom_neg').apply(wstats)
    d['sp_dir'] = np.where(d['dsp'] < 0, 'spread widening', 'spread narrowing')
    out['by_spread_dir'] = d.dropna(subset=['dsp']).groupby('sp_dir').apply(wstats)
    dv = d.dropna(subset=['vol']).copy()
    dv['volq'] = pd.qcut(dv['vol'], 3, labels=['lowvol', 'midvol', 'highvol'])
    out['by_vol'] = dv.groupby('volq').apply(wstats)
    db = d.dropna(subset=['bf']).copy()
    db['bdir'] = np.where(db['bf'] < 0, 'BTC fwd down', 'BTC fwd up')
    out['by_btc_fwd'] = db.groupby('bdir').apply(wstats)
    nb = db[db['coin'] != 'BTCUSD'].copy()
    nb['ex_vs_btc'] = -(nb['fwd'] - nb['bf'])
    out['nonBTC_vs_BTC'] = wstats(nb, 'ex_vs_btc').to_frame().T
    out['ex_sd'] = float(d['ex'].std())
    out['corr_ex_btcfwd'] = float(db['ex'].corr(-db['bf']))
    out['mom_x_spread'] = d.dropna(subset=['mom20', 'dsp']).groupby(['mom_neg', 'sp_dir']).apply(wstats)
    return out
