import numpy as np, pandas as pd, json, ast
from scipy import stats

def _parse(v):
    if isinstance(v, dict): return v
    if isinstance(v, str):
        for f in (json.loads, ast.literal_eval):
            try: return f(v)
            except Exception: pass
    return None

def _raw(v):
    d = _parse(v)
    if not isinstance(d, dict): return np.nan
    c = d.get('quiet_fall')
    if isinstance(c, dict):
        try: return float(c.get('last_history_value'))
        except Exception: return np.nan
    return np.nan

def _tday(df, col):
    df = df.dropna(subset=[col])
    nd = df['day'].nunique()
    if len(df) < 5 or nd < 3: return np.nan, nd
    m = df[col].mean()
    s = (df[col] - m).groupby(df['day']).sum()
    se = np.sqrt((s**2).sum()) / len(df)
    return (m / se if se > 0 else np.nan), nd

def _agg(g, col='um_short'):
    tt, nd = _tday(g, col)
    return pd.Series(dict(n=len(g), days=nd, um=g[col].mean(), um_t=tt,
                          tot=g['tot_short'].mean() if 'tot_short' in g else np.nan,
                          absf=g['absf'].mean()))

def _grp(df, key, col='um_short'):
    res = {}
    for k, g in df.groupby(key, observed=True):
        res[k] = _agg(g, col)
    return pd.DataFrame(res).T if res else pd.DataFrame()

def explore(data):
    rows = []
    Hs = [1, 3, 5, 10, 20]
    for coin, wins in data['bars'].items():
        allr = {h: [] for h in Hs}
        for w, b in wins.items():
            c = b['close'].values
            for h in Hs:
                for i in range(0, len(b) - h, h):
                    allr[h].append(c[i+h]/c[i]-1)
        drift = {h: (np.mean(allr[h]) if allr[h] else np.nan) for h in Hs}
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].values
            ts = pd.to_datetime(b['timestamp'])
            raw = b['debug_info.components'].map(_raw) if 'debug_info.components' in b else pd.Series(np.nan, index=b.index)
            H = 5
            for i in range(0, len(b) - H, H):
                r = dict(coin=coin, win=w, year=ts[i].year, day=ts[i].normalize(),
                         f=float(b['forecast'].iloc[i]), regime=b['regime'].iloc[i],
                         raw=raw.iloc[i], r30=(c[i]/c[i-30]-1 if i >= 30 else np.nan))
                for h in Hs:
                    if i + h < len(b):
                        r[f'um{h}'] = drift[h] - (c[i+h]/c[i]-1)
                    else:
                        r[f'um{h}'] = np.nan
                r['tot_short'] = -(c[i+H]/c[i]-1)
                r['drift5'] = drift[5]
                # coin's market move: own 5-day previous
                r['r5past'] = c[i]/c[i-5]-1 if i >= 5 else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    d['um_short'] = d['um5']
    d['absf'] = (-d['f']).clip(lower=0)
    cs = d[d['f'] < 0].copy()
    cs['main'] = cs['um_short'] * cs['absf'] / 10
    out = {}
    tm, nd = _tday(cs, 'main'); tu, _ = _tday(cs, 'um_short')
    out['overall'] = pd.Series(dict(n=len(cs), days=nd, main=cs['main'].mean(), main_t=tm,
                                    um=cs['um_short'].mean(), um_t=tu, tot=cs['tot_short'].mean(),
                                    drift5=cs['drift5'].mean(), raw_nonnull=cs['raw'].notna().mean()))
    hz = {}
    for h in Hs:
        t, n = _tday(cs, f'um{h}')
        hz[f'{h}d'] = dict(um=cs[f'um{h}'].mean(), t=t, days=n, per_day=cs[f'um{h}'].mean()/h)
    out['cases_by_horizon'] = pd.DataFrame(hz).T
    cs['fq'] = pd.qcut(cs['absf'].rank(method='first'), 4, labels=['q1small','q2','q3','q4large'])
    out['by_forecast_quartile'] = _grp(cs, 'fq')
    out['by_coin'] = _grp(cs, 'coin')
    out['by_year'] = _grp(cs, 'year')
    out['by_window'] = _grp(cs, 'win')
    cc = cs.dropna(subset=['r30']).copy()
    if len(cc) > 9:
        cc['r30q'] = pd.qcut(cc['r30'].rank(method='first'), 3, labels=['deep','mid','shallow'])
        out['cases_by_r30_tercile'] = _grp(cc, 'r30q')
    cc2 = cs.dropna(subset=['r5past']).copy()
    cc2['r5q'] = pd.qcut(cc2['r5past'].rank(method='first'), 3, labels=['fell5','mid5','rose5'])
    out['cases_by_past5d'] = _grp(cc2, 'r5q')
    prof = d[d['regime'] == 'unknown'].dropna(subset=['r30']).copy()
    prof['r30q'] = pd.qcut(prof['r30'].rank(method='first'), 4, labels=['q1deep','q2','q3','q4'])
    out['profile_all_by_r30'] = _grp(prof, 'r30q')
    oth = d[d['regime'] != 'unknown'].dropna(subset=['r30']).copy()
    oth['r30q'] = pd.qcut(oth['r30'].rank(method='first'), 4, labels=['q1deep','q2','q3','q4'])
    out['outside_profile_by_r30'] = _grp(oth, 'r30q')
    out['corr'] = pd.Series(dict(
        spearman_absf_um=stats.spearmanr(cs['absf'], cs['um_short'], nan_policy='omit')[0],
        spearman_r30_um=stats.spearmanr(cc['r30'], cc['um_short'], nan_policy='omit')[0] if len(cc) > 5 else np.nan,
        n_profile_grid=len(prof), n_out_grid=len(oth)))
    out['regimes'] = d['regime'].value_counts()
    return out
