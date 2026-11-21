def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    hr = []
    for coin, wins in data['bars'].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df['close'].values.astype(float); v = df['volume'].values.astype(float)
            ts = pd.to_datetime(df['timestamp'])
            n = len(c)
            lr = np.full(n, np.nan); lr[1:] = np.log(c[1:] / c[:-1])
            hr.append(pd.DataFrame({'coin': coin, 'hour': ts.dt.hour.values, 'wd': ts.dt.dayofweek.values, 'lr': lr}))
            fc = df['forecast'].values
            alloc = df['postRebalance_current_allocation'].values
            for i in range(0, n, 72):
                if i + 72 > n - 1 or i < 168:
                    continue
                p = lr[i-167:i+1]
                if np.any(~np.isfinite(p)):
                    continue
                a = np.abs(p); sa = a.sum()
                if sa <= 0:
                    continue
                vv = v[i-167:i+1]; sv = vv.sum()
                rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, wd=ts.iloc[i].dayofweek,
                    r7=c[i]/c[i-168]-1, r3=c[i]/c[i-72]-1, r1=c[i]/c[i-24]-1,
                    eff=abs(p.sum())/sa, maxsh=a.max()/sa, top5=np.sort(a)[-5:].sum()/sa,
                    vtop5=(np.sort(vv)[-5:].sum()/sv) if sv > 0 else np.nan,
                    upfrac=(p > 0).mean(), rv=p.std(),
                    fwd=c[i+72]/c[i]-1, fwd24=c[i+24]/c[i]-1, fc=fc[i], alloc=alloc[i]))
    g = pd.DataFrame(rows)
    g['ex'] = g['fwd'] - g.groupby('coin')['fwd'].transform('mean')
    g['ex24'] = g['fwd24'] - g.groupby('coin')['fwd24'].transform('mean')
    feats = ['r7', 'r3', 'r1', 'eff', 'maxsh', 'top5', 'vtop5', 'upfrac', 'rv']
    for f in feats:
        g['z_'+f] = g.groupby('coin')[f].transform(lambda s: (s - s.mean())/s.std())
    # signed grind: r7 sign * eff, and r7 * eff
    g['sgn_eff'] = np.sign(g['r7']) * g['eff']
    g['r7_x_maxsh'] = g['z_r7'] * g['z_maxsh']
    g['r7_x_vtop5'] = g['z_r7'] * g['z_vtop5']
    g['r7_x_eff'] = g['z_r7'] * g['z_eff']
    for f in ['sgn_eff', 'r7_x_maxsh', 'r7_x_vtop5', 'r7_x_eff']:
        g['z_'+f] = g.groupby('coin')[f].transform(lambda s: (s - s.mean())/s.std())

    def ols(y, X):
        d = pd.concat([y, X], axis=1).dropna()
        Y = d.iloc[:, 0].values; Xm = np.column_stack([np.ones(len(d)), d.iloc[:, 1:].values])
        b, *_ = np.linalg.lstsq(Xm, Y, rcond=None)
        res = Y - Xm @ b
        s2 = res @ res / (len(Y) - Xm.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.inv(Xm.T @ Xm)))
        return b[1:], (b / se)[1:], len(Y)

    uni = []
    for f in feats + ['sgn_eff']:
        for y in ['ex', 'ex24']:
            b, t, nn = ols(g[y], g[['z_'+f]])
            uni.append(dict(feat=f, y=y, slope_bps=b[0]*1e4, t=t[0], n=nn))
    uni = pd.DataFrame(uni)
    multi = []
    for f in ['eff', 'maxsh', 'top5', 'vtop5', 'upfrac', 'rv', 'r7_x_maxsh', 'r7_x_vtop5', 'r7_x_eff']:
        b, t, nn = ols(g['ex'], g[['z_r7', 'z_'+f]])
        multi.append(dict(feat=f, slope_r7_bps=b[0]*1e4, t_r7=t[0], slope_f_bps=b[1]*1e4, t_f=t[1], n=nn))
    multi = pd.DataFrame(multi)
    # tercile table r7 x eff (within coin)
    g['r7t'] = g.groupby('coin')['r7'].transform(lambda s: pd.qcut(s, 3, labels=False))
    g['efft'] = g.groupby('coin')['eff'].transform(lambda s: pd.qcut(s, 3, labels=False))
    g['mst'] = g.groupby('coin')['maxsh'].transform(lambda s: pd.qcut(s, 3, labels=False))
    tab1 = g.groupby(['r7t', 'efft'])['ex'].agg(['mean', 'count', lambda s: s.mean()/s.std()*np.sqrt(len(s))]).rename(columns={'<lambda_0>': 't'})
    tab1['mean'] *= 1e4
    tab2 = g.groupby(['r7t', 'mst'])['ex'].agg(['mean', 'count', lambda s: s.mean()/s.std()*np.sqrt(len(s))]).rename(columns={'<lambda_0>': 't'})
    tab2['mean'] *= 1e4
    # per coin slopes r7 and rv
    pc = []
    for coin, s in g.groupby('coin'):
        b, t, nn = ols(s['ex'], s[['z_r7']]); b2, t2, _ = ols(s['ex'], s[['z_rv']]); b3, t3, _ = ols(s['ex'], s[['z_r7', 'z_eff']])
        pc.append(dict(coin=coin, r7_bps=b[0]*1e4, t_r7=t[0], rv_bps=b2[0]*1e4, t_rv=t2[0], eff_given_r7_t=t3[1], n=nn))
    pc = pd.DataFrame(pc)
    # by year r7 slope
    yr = []
    for y_, s in g.groupby('year'):
        b, t, nn = ols(s['ex'], s[['z_r7']])
        yr.append(dict(year=y_, r7_bps=b[0]*1e4, t=t[0], n=nn, mean_ex_pos_fc=s.loc[s.fc > 0, 'ex'].mean()*1e4, mean_ex_zero=s.loc[s.fc == 0, 'ex'].mean()*1e4))
    yr = pd.DataFrame(yr)
    # hour of day
    H = pd.concat(hr).dropna()
    H['exh'] = H['lr'] - H.groupby('coin')['lr'].transform('mean')
    hod = H.groupby('hour')['exh'].agg(['mean', 'count', 'std'])
    hod['t'] = hod['mean']/hod['std']*np.sqrt(hod['count']); hod['mean_bps'] = hod['mean']*1e4
    hod = hod[['mean_bps', 't', 'count']]
    # book by weekday
    D = []
    for coin, wins in data['days'].items():
        for w, d in wins.items():
            dd = d.copy(); dd['coin'] = coin; D.append(dd)
    D = pd.concat(D).dropna(subset=['book_return', 'coin_return'])
    D['wd'] = pd.to_datetime(D['day']).dt.dayofweek
    bw = D.groupby('wd').agg(book_bps=('book_return', lambda s: s.mean()*1e4), coin_bps=('coin_return', lambda s: s.mean()*1e4), n=('book_return', 'count'))
    bw['coin_t'] = D.groupby('wd')['coin_return'].apply(lambda s: (s - D['coin_return'].mean()).mean()/s.std()*np.sqrt(len(s)))
    return {'univariate': uni, 'r7_plus_feature': multi, 'r7_tercile_x_eff_tercile': tab1,
            'r7_tercile_x_maxshare_tercile': tab2, 'per_coin': pc, 'by_year': yr, 'hour_of_day': hod, 'book_weekday': bw}
