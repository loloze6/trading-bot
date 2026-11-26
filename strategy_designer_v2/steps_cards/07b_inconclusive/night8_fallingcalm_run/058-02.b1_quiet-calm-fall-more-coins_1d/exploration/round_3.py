import numpy as np, pandas as pd

def _tday(df, col):
    df = df.dropna(subset=[col])
    nd = df['day'].nunique()
    if len(df) < 5 or nd < 3: return np.nan, nd
    m = df[col].mean()
    s = (df[col] - m).groupby(df['day']).sum()
    se = np.sqrt((s**2).sum()) / len(df)
    return (m / se if se > 0 else np.nan), nd

def _agg(g, col='um5'):
    tt, nd = _tday(g, col)
    return pd.Series(dict(n=len(g), days=nd, um=g[col].mean(), um_t=tt, tot=g['tot'].mean()))

def _grp(df, key, col='um5'):
    res = {}
    for k, g in df.groupby(key, observed=True):
        res[k] = _agg(g, col)
    return pd.DataFrame(res).T if res else pd.DataFrame()

def explore(data):
    H = 5
    rows = []
    for coin, wins in data['bars'].items():
        allr = []
        for w, b in wins.items():
            c = b['close'].values
            for i in range(0, len(b) - H, H):
                allr.append(c[i+H]/c[i]-1)
        drift = np.mean(allr) if allr else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].values; v = b['volume'].values.astype(float)
            ts = pd.to_datetime(b['timestamp'])
            for i in range(0, len(b) - H, H):
                if i < 90: continue
                r30 = c[i]/c[i-30]-1
                base = v[max(0, i-365):i-29].mean()
                vr = v[i-29:i+1].mean()/base if base > 0 else np.nan
                rows.append(dict(coin=coin, win=w, year=ts[i].year, day=ts[i].normalize(),
                                 f=float(b['forecast'].iloc[i]), regime=b['regime'].iloc[i],
                                 r30=r30, vr=vr, um5=drift-(c[i+H]/c[i]-1), tot=-(c[i+H]/c[i]-1)))
    d = pd.DataFrame(rows).dropna(subset=['vr'])
    out = {}
    for name, sub in [('profile', d[d['regime']=='unknown']), ('outside', d[d['regime']!='unknown'])]:
        sub = sub[sub['r30'] < 0].copy()
        if len(sub) < 12: continue
        sub['vq'] = pd.qcut(sub['vr'].rank(method='first'), 3, labels=['quiet','mid','heavy'])
        sub['rq'] = pd.qcut(sub['r30'].rank(method='first'), 2, labels=['deep','shallow'])
        out[f'{name}_falls_by_volume'] = _grp(sub, 'vq')
        sub['cell'] = sub['rq'].astype(str) + '_' + sub['vq'].astype(str)
        out[f'{name}_falls_depth_x_volume'] = _grp(sub, 'cell')
        out[f'{name}_falls_vr_by_year'] = _grp(sub.assign(k=sub['year'].astype(str)+'_'+sub['vq'].astype(str)), 'k')
    return out
