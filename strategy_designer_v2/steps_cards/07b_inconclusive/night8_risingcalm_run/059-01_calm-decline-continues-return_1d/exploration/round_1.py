def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    fc = 'forecast'
    out = {}
    def ols_t(x, y):
        x = np.asarray(x, float); y = np.asarray(y, float)
        m = ~(np.isnan(x) | np.isnan(y)); x, y = x[m], y[m]
        if len(x) < 10: return (np.nan, np.nan, len(x))
        r = stats.linregress(x, y)
        return (r.slope, r.slope / r.stderr if r.stderr > 0 else np.nan, len(x))
    rows = []
    for H in [1, 3, 5, 10, 20]:
        for coin, wins in bars.items():
            # coin mean H return over all windows
            allr = []
            for w, df in wins.items():
                c = df['close'].values
                idx = np.arange(0, len(c) - H, H)
                allr += list(c[idx + H] / c[idx] - 1)
            mu = np.mean(allr) if allr else np.nan
            for w, df in wins.items():
                c = df['close'].values
                n = len(c)
                idx = np.arange(0, n - H, H)
                r = c[idx + H] / c[idx] - 1
                lr = np.log(df['close']).diff()
                sd30 = lr.rolling(30).std().values
                ret14 = df['close'].pct_change(14).values
                ret60 = df['close'].pct_change(60).values
                z = ret14 / sd30
                year = pd.to_datetime(df['timestamp']).dt.year.values
                for k, i in enumerate(idx):
                    rows.append(dict(H=H, coin=coin, w=w, year=year[i], f=df[fc].values[i],
                                     calm=df['regime'].values[i] != 'chop', z=z[i], t60=ret60[i],
                                     ex=r[k] - mu))
    R = pd.DataFrame(rows)
    # main measure by horizon
    hz = []
    for H, g in R.groupby('H'):
        s = g[(g.f < 0) & g.calm]
        sl, t, n = ols_t(s.f, s.ex)
        a = g[g.calm & (g.z < 0)]
        sl2, t2, n2 = ols_t(a.z, a.ex)
        b = g[g.calm]
        sl3, t3, n3 = ols_t(b.z, b.ex)
        c = g[~g.calm & (g.z < 0)]
        sl4, t4, n4 = ols_t(c.z, c.ex)
        hz.append(dict(H=H, slope_f=sl, t_f=t, n_f=n, slope_zneg_calm=sl2, t_zneg=t2, n_zneg=n2,
                       t_z_allcalm=t3, n_allcalm=n3, t_zneg_agit=t4, n_agit=n4,
                       mean_ex_fneg=s.ex.mean()))
    out['by_horizon'] = pd.DataFrame(hz)
    g5 = R[(R.H == 5) & (R.f < 0) & R.calm].copy()
    def grp(key):
        res = []
        for k, s in g5.groupby(key):
            sl, t, n = ols_t(s.f, s.ex)
            res.append(dict(key=k, slope=sl, t=t, n=n, mean_ex=s.ex.mean(),
                            t_mean=s.ex.mean() / (s.ex.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan))
        return pd.DataFrame(res)
    out['by_coin'] = grp('coin')
    out['by_window'] = grp('w')
    out['by_year'] = grp('year')
    g5['trend'] = pd.cut(g5.t60, [-np.inf, -0.10, 0.10, np.inf], labels=['falling', 'choppy', 'rising'])
    out['by_trend'] = grp('trend')
    g5['fq'] = pd.qcut(g5.f, 5, labels=False)
    out['by_forecast_quintile'] = g5.groupby('fq').agg(f_mean=('f', 'mean'), ex_mean=('ex', 'mean'),
                                                       n=('ex', 'size'), ex_std=('ex', 'std'))
    # zq on all calm z<0
    a = R[(R.H == 5) & R.calm & (R.z < 0)].copy()
    a['zq'] = pd.qcut(a.z, 5, labels=False)
    out['calm_zneg_quintile_H5'] = a.groupby('zq').agg(z_mean=('z', 'mean'), ex_mean=('ex', 'mean'), n=('ex', 'size'))
    a = R[(R.H == 10) & R.calm & (R.z < 0)].copy()
    a['zq'] = pd.qcut(a.z, 5, labels=False)
    out['calm_zneg_quintile_H10'] = a.groupby('zq').agg(z_mean=('z', 'mean'), ex_mean=('ex', 'mean'), n=('ex', 'size'))
    return out
