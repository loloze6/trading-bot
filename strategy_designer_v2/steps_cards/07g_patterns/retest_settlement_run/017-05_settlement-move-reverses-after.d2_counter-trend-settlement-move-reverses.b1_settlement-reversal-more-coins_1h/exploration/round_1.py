def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data['bars'].items():
        parts = []
        for w, b in wins.items():
            ts = pd.to_datetime(b['timestamp'], utc=True)
            s = pd.Series(b['close'].astype(float).values)
            v = pd.Series(b['volume'].astype(float).values)
            df = pd.DataFrame({'coin': coin, 'w': w,
                               'hc': (ts + pd.Timedelta(hours=1)).dt.hour.values,
                               'year': ts.dt.year.values,
                               'pos': np.arange(len(s))})
            df['r1'] = s.pct_change().values
            df['r2'] = (s / s.shift(2) - 1).values
            df['r24'] = (s / s.shift(24) - 1).values
            df['f1'] = (s.shift(-1) / s - 1).values
            df['f8'] = (s.shift(-8) / s - 1).values
            df['f24'] = (s.shift(-24) / s - 1).values
            lr = np.log(s).diff()
            df['vr'] = (lr.rolling(24).std() / lr.rolling(168).std()).values
            df['volrel'] = (v / v.rolling(168, min_periods=48).median()).values
            df['alloc'] = b['postRebalance_current_allocation'].astype(float).values
            df['fc'] = b['forecast'].astype(float).values
            parts.append(df)
        d = pd.concat(parts, ignore_index=True)
        sd = d['r1'].std()
        for c, k in [('f1', 1), ('f8', 8), ('f24', 24), ('r2', 2), ('r24', 24)]:
            d[c + 'n'] = d[c] / (sd * np.sqrt(k))
        d['f8n'] = d['f8n'] - d['f8n'].mean()
        d['f24n'] = d['f24n'] - d['f24n'].mean()
        d['f1n'] = d['f1n'] - d['f1n'].mean()
        rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def st(x):
        x = x.dropna()
        n = len(x)
        return pd.Series({'mean': x.mean(), 't': x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan, 'n': n})

    out = {}
    # next-hour return (drift removed, vol-normalised) by the hour the next bar starts
    out['next1h_by_start_hour'] = D.groupby('hc')['f1n'].apply(st).unstack()
    # reversal of 2h move over next 8h, by anchor hour (hour next bar starts)
    D['rev8'] = -np.sign(D['r2']) * D['f8n']
    out['rev8_of_2h_by_anchor_hour'] = D.groupby('hc')['rev8'].apply(st).unstack()
    A = D[D['r2'] * D['r24'] < 0].copy()
    A['tr8'] = np.sign(A['r24']) * A['f8n']
    out['against_trend_trend8_by_anchor'] = A.groupby('hc')['tr8'].apply(st).unstack()
    # volume by bar start hour
    D['hs'] = (D['hc'] - 1) % 24
    out['volrel_by_start_hour'] = D.groupby('hs')['volrel'].median()
    # 24h grid: past 24h return quintile -> next 24h
    G = D[(D['pos'] % 24 == 0)].dropna(subset=['r24n', 'f24n', 'vr']).copy()
    G['q'] = pd.qcut(G['r24n'], 5, labels=False)
    out['next24_by_past24_quintile'] = G.groupby('q')['f24n'].apply(st).unstack()
    G['vq'] = pd.qcut(G['vr'], 3, labels=False)
    G['mom'] = np.sign(G['r24']) * G['f24n']
    out['momentum24_by_volratio_tercile'] = G.groupby('vq')['mom'].apply(st).unstack()
    G2 = D[(D['pos'] % 8 == 0)].dropna(subset=['r2n', 'f8n']).copy()
    G2['q'] = pd.qcut(G2['r2n'], 5, labels=False)
    out['next8_by_past2_quintile_grid8'] = G2.groupby('q')['f8n'].apply(st).unstack()
    # book gross gain by hour
    D['g'] = D['alloc'] * D['f1']
    out['gross_gain_by_hour_bps'] = (D.groupby('hs')['g'].mean() * 1e4)
    out['gross_mean_bps_all'] = float(D['g'].mean() * 1e4)
    # trades
    T = []
    for coin, wins in data['trades'].items():
        for w, t in wins.items():
            if len(t):
                T.append(t.assign(coin=coin))
    T = pd.concat(T, ignore_index=True)
    T['eh'] = pd.to_datetime(T['entry_time'], utc=True).dt.hour
    out['trades_by_side'] = T.groupby('side')[['profit_loss_percent', 'net_profit_loss_percent', 'duration_minutes']].mean().assign(n=T.groupby('side').size())
    out['trades_by_entry_hour'] = T.groupby('eh')[['profit_loss_percent', 'net_profit_loss_percent']].mean().assign(n=T.groupby('eh').size())
    # book daily by weekday and year
    Ds = []
    for coin, wins in data['days'].items():
        for w, dd in wins.items():
            Ds.append(dd.assign(coin=coin, w=w))
    Ds = pd.concat(Ds, ignore_index=True)
    bk = Ds.groupby(['w', 'day'])[['book_return', 'coin_return']].mean().reset_index()
    bk['wd'] = pd.to_datetime(bk['day']).dt.weekday
    bk['year'] = pd.to_datetime(bk['day']).dt.year
    out['book_by_weekday'] = bk.groupby('wd')['book_return'].apply(st).unstack()
    out['book_by_year'] = bk.groupby('year')[['book_return', 'coin_return']].mean()
    return out
