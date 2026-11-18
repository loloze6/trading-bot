def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    fc = 'debug_info.components.up_shock.post_pipeline_value'
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].values.astype(float); v = b['volume'].values.astype(float)
            n = len(b)
            r1 = np.full(n, np.nan); r1[:-1] = c[1:]/c[:-1]-1
            r25 = np.full(n, np.nan); r25[:-5] = c[5:]/c[1:-4]-1
            r5 = np.full(n, np.nan); r5[:-5] = c[5:]/c[:-5]-1
            past = np.full(n, np.nan); past[1:] = c[1:]/c[:-1]-1
            vrel = v / pd.Series(v).rolling(20, min_periods=10).mean().shift(1).values
            f = b[fc].values.astype(float)
            fsm = pd.Series(f).rolling(5, min_periods=1).mean().values
            pos = b['postRebalance_current_allocation'].values
            prev = b['previous_allocation'].values
            d = pd.DataFrame({'coin': coin, 'win': w, 'f': f, 'fsm': fsm, 'r1': r1, 'r25': r25,
                              'r5': r5, 'vrel': vrel, 'pos': pos, 'chg': np.abs(pos-prev),
                              'grid5': (np.arange(n) % 5 == 0)})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for col in ['r1', 'r25', 'r5']:
        D['ex_'+col] = D[col] - D.groupby('coin')[col].transform('mean')
    A = D[D['f'] > 0].copy()
    A['vq'] = pd.qcut(A['vrel'], 3, labels=['thin', 'mid', 'heavy'])
    A['fq'] = pd.cut(A['f'], [0, 6, 20.1], labels=['small', 'large'])
    def summ(g):
        return pd.Series({'n': len(g),
                          'ex_next_day': g['ex_r1'].mean(),
                          't_next': stats.ttest_1samp(g['ex_r1'].dropna(), 0).statistic,
                          'ex_days2to5': g['ex_r25'].mean(),
                          't_2to5': stats.ttest_1samp(g['ex_r25'].dropna(), 0).statistic})
    out['active_by_volume'] = A.groupby('vq', observed=True).apply(summ)
    out['active_by_volume_and_size'] = A.groupby(['fq', 'vq'], observed=True).apply(summ)
    # slow forecast on 5-day grid
    G = D[D['grid5'] & D['ex_r5'].notna()]
    G2 = G.copy(); G2['sq'] = pd.cut(G2['fsm'], [-0.1, 0.001, 2, 5, 20.1], labels=['0', '0-2', '2-5', '5+'])
    out['slow_forecast_grid'] = G2.groupby('sq', observed=True).agg(n=('ex_r5', 'size'), ex5=('ex_r5', 'mean'))
    s1 = stats.linregress(G['fsm'], G['ex_r5']); s0 = stats.linregress(G['f'], G['ex_r5'])
    out['slope_t'] = pd.Series({'raw_f_t': s0.slope/s0.stderr, 'smooth5_t': s1.slope/s1.stderr})
    out['turnover'] = pd.Series({'mean_abs_change': D['chg'].mean(),
                                 'share_days_traded': (D['chg'] > 0.01).mean()})
    # year split of active next-day vs days2-5
    yrs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            yrs.append(pd.to_datetime(b['timestamp']).dt.year.values)
    D['year'] = np.concatenate(yrs)
    A2 = D[D['f'] > 0]
    out['active_by_year'] = A2.groupby('year').agg(n=('ex_r1', 'size'), next=('ex_r1', 'mean'), d2to5=('ex_r25', 'mean'))
    return out
