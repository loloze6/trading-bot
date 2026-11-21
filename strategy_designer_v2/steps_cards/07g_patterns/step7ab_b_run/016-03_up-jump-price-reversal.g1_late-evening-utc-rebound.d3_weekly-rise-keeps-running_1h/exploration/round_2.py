def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data['bars'].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df['close'].values.astype(float); v = df['volume'].values.astype(float)
            ts = pd.to_datetime(df['timestamp'])
            n = len(c)
            lr = np.full(n, np.nan); lr[1:] = np.log(c[1:] / c[:-1])
            for i in range(0, n, 24):
                if i < 168 or i + 72 > n - 1:
                    continue
                p = lr[i-167:i+1]; q = lr[i-23:i+1]
                if np.any(~np.isfinite(p)):
                    continue
                a = np.abs(p); sa = a.sum(); aq = np.abs(q); sq = aq.sum()
                if sa <= 0 or sq <= 0:
                    continue
                vq = v[i-23:i+1]; vw = v[i-167:i+1]
                rows.append(dict(coin=coin, win=w, wnum=int(w[1:]), year=ts.iloc[i].year, g72=(i % 72 == 0),
                    r7=c[i]/c[i-168]-1, r1=c[i]/c[i-24]-1,
                    eff=abs(p.sum())/sa, seff=p.sum()/sa, maxsh1=aq.max()/sq,
                    vrat1=vq.mean()/vw.mean() if vw.mean() > 0 else np.nan,
                    fwd24=c[i+24]/c[i]-1, fwd72=c[i+72]/c[i]-1))
    g = pd.DataFrame(rows)
    g['ex24'] = g['fwd24'] - g.groupby('coin')['fwd24'].transform('mean')
    g['ex72'] = g['fwd72'] - g.groupby('coin')['fwd72'].transform('mean')
    for f in ['r7', 'r1', 'eff', 'seff', 'maxsh1', 'vrat1']:
        g['z_'+f] = g.groupby('coin')[f].transform(lambda s: (s - s.mean())/s.std())
    g['r1_x_maxsh'] = g['z_r1']*g['z_maxsh1']; g['r1_x_vrat'] = g['z_r1']*g['z_vrat1']
    def ols(d, y, xs):
        d = d[[y]+xs].dropna()
        Y = d[y].values; X = np.column_stack([np.ones(len(d))]+[d[x].values for x in xs])
        b, *_ = np.linalg.lstsq(X, Y, rcond=None); r = Y - X@b
        se = np.sqrt(np.diag(r@r/(len(Y)-X.shape[1])*np.linalg.inv(X.T@X)))
        return b[1:], (b/se)[1:], len(Y)
    out = {}
    # 1-day reversal on daily grid
    res = []
    for name, xs in [('r1', ['z_r1']), ('r1+maxsh+int', ['z_r1', 'z_maxsh1', 'r1_x_maxsh']), ('r1+vrat+int', ['z_r1', 'z_vrat1', 'r1_x_vrat'])]:
        b, t, nn = ols(g, 'ex24', xs)
        res.append(dict(model=name, **{f'b{k}_bps': b[k]*1e4 for k in range(len(b))}, **{f't{k}': t[k] for k in range(len(t))}, n=nn))
    out['day_reversal_daily_grid'] = pd.DataFrame(res)
    # quintiles of r1 vs ex24
    g['r1q'] = g.groupby('coin')['r1'].transform(lambda s: pd.qcut(s, 5, labels=False))
    q = g.groupby('r1q')['ex24'].agg(['mean', 'std', 'count']); q['t'] = q['mean']/q['std']*np.sqrt(q['count']); q['mean_bps'] = q['mean']*1e4
    q['mean_abs_r1_bps'] = g.groupby('r1q')['r1'].apply(lambda s: s.abs().mean()*1e4)
    out['r1_quintile_next_day'] = q[['mean_bps', 't', 'count', 'mean_abs_r1_bps']]
    # per coin and by half of windows, r1 reversal
    pc = []
    for k, s in g.groupby('coin'):
        b, t, nn = ols(s, 'ex24', ['z_r1']); b2, t2, _ = ols(s[s.g72], 'ex72', ['z_seff']); b3, t3, _ = ols(s[s.g72], 'ex72', ['z_eff'])
        pc.append(dict(coin=k, r1_bps=b[0]*1e4, t_r1=t[0], seff72_bps=b2[0]*1e4, t_seff72=t2[0], eff72_bps=b3[0]*1e4, t_eff72=t3[0], n=nn))
    out['per_coin'] = pd.DataFrame(pc)
    hh = []
    for k, s in g.groupby(g.wnum <= 12):
        b, t, nn = ols(s, 'ex24', ['z_r1']); b2, t2, n2 = ols(s[s.g72], 'ex72', ['z_seff']); b3, t3, _ = ols(s[s.g72], 'ex72', ['z_eff'])
        hh.append(dict(first_half=k, r1_bps=b[0]*1e4, t_r1=t[0], n=nn, seff72_bps=b2[0]*1e4, t_seff72=t2[0], eff72_bps=b3[0]*1e4, t_eff72=t3[0], n72=n2))
    out['by_half'] = pd.DataFrame(hh)
    yy = []
    for k, s in g.groupby('year'):
        b, t, nn = ols(s, 'ex24', ['z_r1']); b3, t3, _ = ols(s[s.g72], 'ex72', ['z_eff'])
        yy.append(dict(year=k, r1_bps=b[0]*1e4, t_r1=t[0], eff72_bps=b3[0]*1e4, t_eff72=t3[0], n=nn))
    out['by_year'] = pd.DataFrame(yy)
    # efficiency: unsigned vs signed, split by direction of r7, on 72 grid
    s72 = g[g.g72].copy()
    s72['up'] = s72['r7'] > 0
    s72['effq'] = s72.groupby(['coin', 'up'])['eff'].transform(lambda s: pd.qcut(s, 3, labels=False))
    e = s72.groupby(['up', 'effq'])['ex72'].agg(['mean', 'std', 'count']); e['t'] = e['mean']/e['std']*np.sqrt(e['count']); e['mean_bps'] = e['mean']*1e4
    out['eff_tercile_by_direction_72'] = e[['mean_bps', 't', 'count']]
    return out
