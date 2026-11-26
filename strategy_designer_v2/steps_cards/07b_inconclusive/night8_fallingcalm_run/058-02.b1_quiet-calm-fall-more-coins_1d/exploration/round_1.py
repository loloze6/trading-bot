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
    if not d: return np.nan
    c = d.get('quiet_fall') if isinstance(d, dict) else None
    if isinstance(c, dict):
        x = c.get('last_history_value')
        try: return float(x)
        except Exception: return np.nan
    return np.nan

def _tday(df, col):
    g = df.groupby('day')[col].sum()
    n = len(g)
    if n < 3: return np.nan, n
    m = df[col].mean()
    dev = (df[col] - m)
    s = dev.groupby(df['day']).sum()
    se = np.sqrt((s**2).sum()) / len(df)
    return m / se if se > 0 else np.nan, n

def explore(data):
    H = 5
    rows = []
    drift = {}
    for coin, wins in data['bars'].items():
        allr = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].values
            for i in range(0, len(b) - H, H):
                allr.append(c[i+H]/c[i]-1)
        drift[coin] = np.mean(allr) if allr else np.nan
        usual = np.std(allr, ddof=1) if len(allr) > 2 else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].values
            v = b['volume'].values
            ts = pd.to_datetime(b['timestamp'])
            raw = b['debug_info.components'].map(_raw) if 'debug_info.components' in b else pd.Series(np.nan, index=b.index)
            for i in range(0, len(b) - H, H):
                r30 = c[i]/c[i-30]-1 if i >= 30 else np.nan
                vr = v[i-29:i+1].mean()/v[:i-29].mean() if i >= 50 else np.nan
                rows.append(dict(coin=coin, win=w, year=ts[i].year, day=ts[i].normalize(),
                                 f=b['forecast'].iloc[i], regime=b['regime'].iloc[i],
                                 raw=raw.iloc[i], r30=r30, vr=vr,
                                 fwd=c[i+H]/c[i]-1, drift=drift[coin], usual=usual))
    d = pd.DataFrame(rows)
    d['um_short'] = d['drift'] - d['fwd']
    d['tot_short'] = -d['fwd']
    cs = d[d['f'] < 0].copy()
    cs['absf'] = -cs['f']
    cs['main'] = cs['um_short'] * cs['absf']/10
    out = {}
    t, n = _tday(cs, 'main'); t2, _ = _tday(cs, 'um_short')
    out['overall'] = pd.Series(dict(n=len(cs), days=n, main_mean=cs['main'].mean(), main_t=t,
                                    um_mean=cs['um_short'].mean(), um_t=t2, tot_mean=cs['tot_short'].mean()))
    cs['fq'] = pd.qcut(cs['absf'].rank(method='first'), 4, labels=['q1','q2','q3','q4'])
    def agg(g):
        tt, nd = _tday(g, 'um_short')
        return pd.Series(dict(n=len(g), days=nd, um=g['um_short'].mean(), um_t=tt, tot=g['tot_short'].mean(), absf=g['absf'].mean()))
    out['by_forecast_quartile'] = cs.groupby('fq').apply(agg)
    out['by_coin'] = cs.groupby('coin').apply(agg)
    out['by_year'] = cs.groupby('year').apply(agg)
    out['by_window'] = cs.groupby('win').apply(agg)
    # components: fall depth vs volume ratio inside cases
    cc = cs.dropna(subset=['r30'])
    cc['r30q'] = pd.qcut(cc['r30'].rank(method='first'), 3, labels=['deep','mid','shallow'])
    out['cases_by_r30_tercile'] = cc.groupby('r30q').apply(agg)
    cv = cs.dropna(subset=['vr'])
    cv['vq'] = pd.qcut(cv['vr'].rank(method='first'), 3, labels=['quiet','mid','heavy'])
    out['cases_by_volratio_tercile_inwindow'] = cv.groupby('vq').apply(agg)
    # all grid bars in profile (regime unknown) regardless of forecast, by r30
    prof = d[(d['regime'] == 'unknown')].dropna(subset=['r30']).copy()
    prof['r30q'] = pd.qcut(prof['r30'].rank(method='first'), 4, labels=['q1deep','q2','q3','q4'])
    out['profile_all_by_r30'] = prof.groupby('r30q').apply(agg)
    oth = d[(d['regime'] != 'unknown')].dropna(subset=['r30']).copy()
    oth['r30q'] = pd.qcut(oth['r30'].rank(method='first'), 4, labels=['q1deep','q2','q3','q4'])
    out['outside_profile_by_r30'] = oth.groupby('r30q').apply(agg)
    out['corr'] = pd.Series(dict(
        spearman_absf_um=stats.spearmanr(cs['absf'], cs['um_short'])[0],
        spearman_r30_um_cases=stats.spearmanr(cc['r30'], cc['um_short'])[0],
        spearman_vr_um_cases=stats.spearmanr(cv['vr'], cv['um_short'])[0] if len(cv) > 5 else np.nan,
        raw_nonnull_share=cs['raw'].notna().mean()))
    out['regimes'] = d['regime'].value_counts()
    return out
