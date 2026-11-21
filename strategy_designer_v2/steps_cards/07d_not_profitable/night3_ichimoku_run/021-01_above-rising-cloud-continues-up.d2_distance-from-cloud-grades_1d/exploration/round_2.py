def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 26
    rows = []; drift = {}
    def mid(h, l, n): return (h.rolling(n).max() + l.rolling(n).min()) / 2
    for coin, ws in data['bars'].items():
        rets = []
        for w, b in ws.items():
            c = b['close'].values
            for i in range(0, len(b) - H, H):
                rets.append(c[i+H]/c[i]-1)
        drift[coin] = np.mean(rets)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            h, l, cl = b['high'], b['low'], b['close']
            tk = mid(h, l, 9); kj = mid(h, l, 26); sb = mid(h, l, 52)
            sa = ((tk + kj) / 2).shift(26); sbb = sb.shift(26)
            top = np.maximum(sa, sbb); bot = np.minimum(sa, sbb)
            thick = (top - bot) / cl
            topslope = top / top.shift(26) - 1
            dist = cl / top - 1
            r26 = cl.pct_change(26)
            vol = cl.pct_change().rolling(26).std()
            a = b['postRebalance_current_allocation']
            c = cl.values
            for i in range(0, len(b) - H, H):
                r = c[i+H]/c[i]-1
                rows.append(dict(coin=coin, w=w, f=b['forecast'].iloc[i], r=r, ex=r-drift[coin],
                                 dist=dist.iloc[i], thick=thick.iloc[i], tslope=topslope.iloc[i],
                                 r26=r26.iloc[i], vol=vol.iloc[i], a=a.iloc[i]))
    df = pd.DataFrame(rows)
    out = {}
    out['n_with_cloud'] = int(df['dist'].notna().sum())
    d = df.dropna(subset=['dist', 'tslope'])
    d = d.assign(above=(d['dist'] > 0).astype(int), rising=(d['tslope'] > 0).astype(int))
    out['above_x_rising'] = d.groupby(['above', 'rising']).agg(n=('r', 'size'), mean_r=('r', 'mean'), mean_ex=('ex', 'mean'))
    # slope of ex on cloud slope, within above and below
    for s in [1, 0]:
        x = d[d.above == s]
        sl = stats.linregress(x['tslope'], x['ex'])
        out[f'ex_on_cloudslope_above{s}'] = f"slope={sl.slope:.4f} t={sl.slope/sl.stderr:.2f} n={len(x)}"
        sl = stats.linregress(x['r26'].fillna(0), x['ex'])
        out[f'ex_on_r26_above{s}'] = f"slope={sl.slope:.4f} t={sl.slope/sl.stderr:.2f} n={len(x)}"
    # cloud slope quintiles
    d['sq'] = pd.qcut(d['tslope'].rank(method='first'), 5, labels=False)
    out['by_cloudslope_quintile'] = d.groupby('sq').agg(n=('r', 'size'), tslope=('tslope', 'mean'), mean_r=('r', 'mean'), mean_ex=('ex', 'mean'), share_above=('above', 'mean'))
    # thickness among above
    xa = d[d.above == 1].copy()
    xa['tq'] = pd.qcut(xa['thick'].rank(method='first'), 3, labels=False)
    out['above_by_thickness'] = xa.groupby('tq').agg(n=('r', 'size'), thick=('thick', 'mean'), mean_r=('r', 'mean'), mean_ex=('ex', 'mean'))
    # by coin, side
    out['by_coin_above'] = d.groupby(['coin', 'above'])['r'].mean().unstack()
    # long-only daily book proxy: position = max(alloc,0) applied to daily returns
    rec = []
    for coin, ws in data['bars'].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            dr = b['close'].pct_change()
            a = b['postRebalance_current_allocation'].shift(1)
            rec.append(pd.DataFrame(dict(lo=(a.clip(lower=0) * dr), full=a * dr, hold=dr)).dropna())
    R = pd.concat(rec)
    sh = lambda x: x.mean() / x.std() * np.sqrt(365)
    out['bar_level_sharpe'] = pd.Series({k: sh(R[k]) for k in ['lo', 'full', 'hold']})
    out['bar_level_mean_bps'] = R.mean() * 1e4
    return out
