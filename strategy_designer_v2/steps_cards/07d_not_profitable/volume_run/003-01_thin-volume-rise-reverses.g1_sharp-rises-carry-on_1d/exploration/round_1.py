def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    fc = 'debug_info.components.up_shock.post_pipeline_value'
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].values
            n = len(b)
            r1 = np.full(n, np.nan); r1[:-1] = c[1:]/c[:-1]-1
            d = pd.DataFrame({'coin': coin, 'win': w,
                              'f': b[fc].values if fc in b else np.nan,
                              'pos': b['postRebalance_current_allocation'].values,
                              'r1': r1})
            for k in range(1, 6):
                # return on day k after the shock bar: close[t+k]/close[t+k-1]-1
                rk = np.full(n, np.nan)
                if n > k:
                    rk[:n-k] = c[k:]/c[k-1:-1]-1 if k > 1 else r1[:n-1]
                d[f'd{k}'] = rk
            r5 = np.full(n, np.nan); r5[:-5] = c[5:]/c[:-5]-1
            d['r5'] = r5
            d['gain'] = d['pos']*d['r1']
            pv = b['total_portfolio_value'].values; pr = b['postRebalance_total_value'].values
            d['fee'] = (pv - pr)/pv
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D['bucket'] = pd.cut(D['f'], [-0.1, 0.001, 2, 6, 10, 15, 20.1],
                         labels=['0', '0-2', '2-6', '6-10', '10-15', '15-20'])
    coinmean = D.groupby('coin')['r1'].transform('mean')
    D['ex1'] = D['r1'] - coinmean
    g = D.groupby('bucket', observed=True)
    out['by_forecast_bucket'] = pd.DataFrame({
        'n': g.size(),
        'mean_pos': g['pos'].mean(),
        'next_day_excess': g['ex1'].mean(),
        'd2': g['d2'].mean(), 'd3': g['d3'].mean(), 'd4': g['d4'].mean(), 'd5': g['d5'].mean(),
        'r5': g['r5'].mean(),
        'gain_sum': g['gain'].sum(), 'fee_sum': g['fee'].sum()})
    out['totals'] = pd.Series({
        'gain_sum': D['gain'].sum(), 'fee_sum': D['fee'].sum(),
        'share_bars_pos>0': (D['pos'] > 0.01).mean(),
        'mean_pos': D['pos'].mean(),
        'coin_mean_daily': D['r1'].mean()})
    act = D[D['f'] > 0]
    out['next_day_t_active'] = pd.Series({
        'mean_ex1': act['ex1'].mean(),
        't': stats.ttest_1samp(act['ex1'].dropna(), 0).statistic,
        'n': act['ex1'].notna().sum()})
    out['by_coin'] = D.groupby('coin').agg(gain=('gain', 'sum'), fee=('fee', 'sum'),
                                          ex1_active=('ex1', lambda s: s[D.loc[s.index, 'f'] > 0].mean()))
    # days data
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x['coin'] = coin; x['win'] = w; dd.append(x)
    DD = pd.concat(dd, ignore_index=True)
    out['book_by_coin_daily'] = DD.groupby('coin').agg(book=('book_return', 'mean'), coin=('coin_return', 'mean'))
    return out
