def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # 1-day next returns by weekday of the day the return is earned
    rows = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy()
            x['day'] = pd.to_datetime(x['day'])
            x['wd'] = x['day'].dt.dayofweek
            x['year'] = x['day'].dt.year
            x['coin'] = coin; x['win'] = w
            rows.append(x[['coin', 'win', 'wd', 'year', 'coin_return', 'book_return']])
    d = pd.concat(rows, ignore_index=True).dropna(subset=['coin_return'])
    d['ex'] = d['coin_return'] - d.groupby('coin')['coin_return'].transform('mean')
    g = d.groupby('wd')['ex'].agg(['mean', 'std', 'count']); g['t'] = g['mean'] / (g['std'] / np.sqrt(g['count']))
    g['book_mean'] = d.groupby('wd')['book_return'].mean()
    out['day_ret_by_weekday'] = g
    # by year: Sunday and Tuesday excess
    py = d.pivot_table(index='year', columns='wd', values='ex', aggfunc='mean')
    out['weekday_by_year_mean'] = py
    # 5-day grid fwd by start weekday, by year halves
    H = 5; rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b['close'].astype(float)
            fwd = c.shift(-H) / c - 1
            hi90 = c.rolling(90, min_periods=60).max()
            near = c / hi90 - 1
            r20 = c / c.shift(20) - 1
            ts = pd.to_datetime(b['timestamp'])
            x = pd.DataFrame({'coin': coin, 'fwd': fwd, 'near': near, 'r20': r20,
                              'wd': ts.dt.dayofweek, 'year': ts.dt.year}).iloc[::H]
            rows.append(x)
    g5 = pd.concat(rows, ignore_index=True).dropna(subset=['fwd'])
    g5['ex'] = g5['fwd'] - g5.groupby('coin')['fwd'].transform('mean')
    g5['late'] = g5['year'] >= 2022
    t = g5.groupby(['late', 'wd'])['ex'].agg(['mean', 'count']); out['grid_wd_by_period'] = t.unstack(0)
    # near quintiles by period and coins
    x = g5.dropna(subset=['near']).copy()
    x['q'] = x.groupby('coin')['near'].transform(lambda s: pd.qcut(s.rank(method='first'), 5, labels=False))
    gg = x.groupby(['late', 'q'])['ex'].agg(['mean', 'std', 'count'])
    gg['t'] = gg['mean'] / (gg['std'] / np.sqrt(gg['count']))
    out['near_q_by_period'] = gg
    x['q1'] = x['q'] == 1
    out['near_q1_coins_negative_share'] = float((x[x.q1].groupby('coin')['ex'].mean() < 0).mean())
    # graded: rank corr near vs ex in the lower half of near
    lo = x[x['q'] <= 1]
    out['spearman_near_ex_lowhalf'] = str(stats.spearmanr(lo['near'], lo['ex']))
    hi = x[x['q'] >= 1]
    out['spearman_near_ex_upper'] = str(stats.spearmanr(hi['near'], hi['ex']))
    # book: largest gain/loss days by weekday
    bk = d.groupby(['win', 'wd', 'year']).size()
    dd = d.copy()
    lo_cut, hi_cut = dd['book_return'].quantile([0.02, 0.98])
    out['book_extreme_days_wd'] = pd.DataFrame({
        'big_loss': dd[dd.book_return <= lo_cut].groupby('wd').size(),
        'big_gain': dd[dd.book_return >= hi_cut].groupby('wd').size()})
    return out
