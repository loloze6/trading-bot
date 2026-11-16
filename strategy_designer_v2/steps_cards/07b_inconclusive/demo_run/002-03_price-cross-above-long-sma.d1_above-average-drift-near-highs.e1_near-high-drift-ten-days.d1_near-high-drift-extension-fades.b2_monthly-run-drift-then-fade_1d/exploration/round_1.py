import numpy as np, pandas as pd
from scipy import stats

def _s(df):
    col = 'debug_info.components.run.post_pipeline_value'
    if col in df.columns:
        return pd.to_numeric(df[col], errors='coerce')
    out = []
    for v in df['debug_info.components']:
        try:
            out.append(float(v['run']['post_pipeline_value']))
        except Exception:
            out.append(np.nan)
    return pd.Series(out, index=df.index)

def explore(data):
    bars = data["bars"]
    rows = []
    for coin in bars:
        # coin mean h-bar returns over all windows, for several h
        for h in (5, 10, 20, 30):
            pass
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            s = _s(df)
            c = df['close'].values
            yr = pd.to_datetime(df['timestamp']).dt.year.values
            for h in (5, 10, 20, 30):
                for i in range(0, len(df) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=yr[i],
                                     reg=df['regime'].iat[i], s=s.iat[i],
                                     f=df['forecast'].iat[i],
                                     r=c[i+h]/c[i]-1))
    R = pd.DataFrame(rows)
    R['ex'] = R['r'] - R.groupby(['coin','h'])['r'].transform('mean')
    T = R[(R.reg == 'trending')].dropna(subset=['s'])
    out = {}
    T10 = T[T.h == 10].copy()
    bins = [-np.inf, -4, -2, 0, 2, 4, 6, 8, 11, 14, 17, np.inf]
    T10['sb'] = pd.cut(T10.s, bins)
    out['tiers_h10'] = T10.groupby('sb', observed=True)['ex'].agg(['count','mean','std']).assign(
        t=lambda d: d['mean']/(d['std']/np.sqrt(d['count'])))
    def slope(d, x):
        d = d.dropna(subset=[x,'ex'])
        if len(d) < 10: return (np.nan, np.nan, len(d))
        r = stats.linregress(d[x], d['ex'])
        return (r.slope, r.slope/r.stderr, len(d))
    res = []
    for h in (5, 10, 20, 30):
        d = T[T.h == h]
        a = slope(d, 's'); b = slope(d, 'f')
        a2 = slope(d[d.s < 8], 's'); a3 = slope(d[d.s >= 8], 's')
        res.append(dict(h=h, n=a[2], slope_s=a[0], t_s=a[1], t_f=b[1],
                        t_s_below8=a2[1], n_below8=a2[2], t_s_above8=a3[1], n_above8=a3[2]))
    out['slopes_by_h'] = pd.DataFrame(res)
    pc = []
    for coin, d in T10.groupby('coin'):
        a = slope(d, 's'); b = slope(d, 'f')
        pc.append(dict(coin=coin, n=a[2], t_s=a[1], t_f=b[1], mean_ex=d.ex.mean(),
                       hi=d[d.s>=14].ex.mean(), n_hi=(d.s>=14).sum()))
    out['per_coin_h10'] = pd.DataFrame(pc)
    py = []
    for y, d in T10.groupby('year'):
        a = slope(d, 's')
        py.append(dict(year=y, n=a[2], t_s=a[1], mean_ex=d.ex.mean(),
                       hi=d[d.s>=14].ex.mean(), n_hi=(d.s>=14).sum(),
                       mid=d[(d.s>=8)&(d.s<14)].ex.mean()))
    out['per_year_h10'] = pd.DataFrame(py)
    out['s_quantiles'] = T10.s.describe(percentiles=[.1,.25,.5,.75,.9,.95])
    # non-trending: does s-like relation exist? (use raw 30d return)
    out['share_trending_grid'] = float((R[R.h==10].reg=='trending').mean())
    return out
