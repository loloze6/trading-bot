def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    fc = 'debug_info.components.rsi_below_share.last_history_value'
    rows = []
    drows = []
    for coin, ws in data['bars'].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b['close'].values
            n = len(c)
            lr = np.log(b['close']).diff()
            vol14 = lr.rolling(14).std().values
            r7p = b['close'].pct_change(7).values
            r14p = b['close'].pct_change(14).values
            r30p = b['close'].pct_change(30).values
            for h in (7, 14):
                for t in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, f=b['forecast'].iloc[t],
                                     share=b[fc].iloc[t] if fc in b else np.nan,
                                     pos=b['postRebalance_current_allocation'].iloc[t],
                                     vol=vol14[t], r7p=r7p[t], r14p=r14p[t], r30p=r30p[t],
                                     fwd=c[t + h] / c[t] - 1,
                                     wd=pd.Timestamp(b['timestamp'].iloc[t]).weekday()))
        for w, d in data['days'][coin].items():
            d = d.copy(); d['coin'] = coin; d['w'] = w
            d['wd'] = pd.to_datetime(d['day']).dt.weekday
            d['year'] = pd.to_datetime(d['day']).dt.year
            drows.append(d)
    g = pd.DataFrame(rows)
    D = pd.concat(drows)
    def tab(df, col, q=5):
        df = df.dropna(subset=[col, 'fwd']).copy()
        df['ex'] = df['fwd'] - df.groupby('coin')['fwd'].transform('mean')
        df['bin'] = df.groupby('coin')[col].transform(lambda s: pd.qcut(s.rank(method='first'), q, labels=False))
        r = df.groupby('bin')['ex'].agg(['mean', 'count', 'std'])
        r['t'] = r['mean'] / (r['std'] / np.sqrt(r['count']))
        sp = df.groupby('coin').apply(lambda x: stats.spearmanr(x[col], x['ex'])[0])
        r.loc['spearman_' + '_'.join(f"{k}:{v:.3f}" for k, v in sp.items())] = np.nan
        return r
    g14 = g[g.h == 14]; g7 = g[g.h == 7]
    out['share_quint_fwd14'] = tab(g14, 'share')
    out['r30p_quint_fwd14'] = tab(g14, 'r30p')
    out['r7p_quint_fwd7'] = tab(g7, 'r7p')
    out['r14p_quint_fwd14'] = tab(g14, 'r14p')
    out['vol_tercile_fwd14'] = tab(g14, 'vol', 3)
    out['vol_tercile_fwd7'] = tab(g7, 'vol', 3)
    # signed: past 14d return x vol tercile
    gg = g14.dropna(subset=['vol', 'r14p']).copy()
    gg['ex'] = gg['fwd'] - gg.groupby('coin')['fwd'].transform('mean')
    gg['vt'] = gg.groupby('coin')['vol'].transform(lambda s: pd.qcut(s, 3, labels=False))
    out['mom_corr_by_vol'] = gg.groupby(['coin', 'vt']).apply(lambda x: pd.Series({'sp': stats.spearmanr(x['r14p'], x['ex'])[0], 'n': len(x)}))
    # weekday daily coin returns
    Dd = D.dropna(subset=['coin_return'])
    wk = Dd.groupby('wd')['coin_return'].agg(['mean', 'std', 'count'])
    wk['t'] = wk['mean'] / (wk['std'] / np.sqrt(wk['count']))
    out['weekday_coin'] = wk
    # book by year / by coin
    Db = D.dropna(subset=['book_return'])
    by = Db.groupby(['coin', 'year'])['book_return'].agg(['mean', 'std', 'count'])
    by['sharpe'] = by['mean'] / by['std'] * np.sqrt(365)
    out['book_by_coin_year'] = by
    # book decomposition: market vs timing
    b_all = []
    for coin, ws in data['bars'].items():
        for w, b in ws.items():
            r = b['close'].pct_change().shift(-1)
            b_all.append(pd.DataFrame({'coin': coin, 'pos': b['postRebalance_current_allocation'], 'r': r, 'f': b['forecast']}))
    B = pd.concat(b_all).dropna()
    mu = B.groupby('coin')['r'].transform('mean')
    B['gain'] = B['pos'] * B['r']; B['mkt'] = B['pos'] * mu
    out['decomp'] = B.groupby('coin')[['gain', 'mkt']].mean().assign(timing=lambda x: x.gain - x.mkt, mean_pos=B.groupby('coin')['pos'].mean(), long_share=B.groupby('coin')['pos'].apply(lambda s: (s > 0).mean()))
    # gain by long/short side
    B['side'] = np.sign(B['pos'])
    out['gain_by_side'] = B.groupby(['coin', 'side'])['gain'].agg(['mean', 'count', 'sum'])
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data['trades'].items() for t in ws.values()])
    out['trades_side'] = T.groupby(['coin', 'side'])['net_profit_loss_percent'].agg(['mean', 'median', 'count'])
    # largest book days: coin's prior 14d return around them
    out['book_tail_share'] = pd.Series({'top5pct_sum_share': Db['book_return'].nlargest(int(len(Db) * 0.05)).sum() / Db['book_return'].sum(),
                                        'bottom5pct_sum_share': Db['book_return'].nsmallest(int(len(Db) * 0.05)).sum() / Db['book_return'].sum()})
    return out
