def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 26
    fc = 'debug_info.components.cloud_pos.last_history_value'
    rows = []; pos = []; drift = {}
    for coin, ws in data['bars'].items():
        rets = []
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b['close'].values
            for i in range(0, len(b) - H, H):
                rets.append(c[i+H]/c[i]-1)
        drift[coin] = np.mean(rets)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b['close'].values
            n = len(b)
            # recompute features
            hi, lo = b['high'], b['low']
            ret52 = b['close'].pct_change(52)
            ma = b['close'].rolling(100, min_periods=50).mean()
            for i in range(0, n - H, H):
                r = c[i+H]/c[i]-1
                rows.append(dict(coin=coin, w=w, f=b['forecast'].iloc[i], raw=b[fc].iloc[i] if fc in b else np.nan,
                                 alloc=b['postRebalance_current_allocation'].iloc[i], r=r, ex=r-drift[coin],
                                 r52=ret52.iloc[i]))
            g = b['postRebalance_current_allocation'].shift(1)
            dr = b['close'].pct_change()
            pos.append(pd.DataFrame(dict(coin=coin, w=w, a=g, dr=dr)))
    df = pd.DataFrame(rows)
    P = pd.concat(pos).dropna()
    out = {}
    df['side'] = np.sign(df['f'])
    out['grid_by_side'] = df.groupby('side').agg(n=('r','size'), mean_r=('r','mean'), mean_ex=('ex','mean'))
    df['fq'] = pd.qcut(df['f'].rank(method='first'), 5, labels=False)
    out['grid_by_forecast_quintile'] = df.groupby('fq').agg(n=('r','size'), f=('f','mean'), raw=('raw','mean'), mean_r=('r','mean'), mean_ex=('ex','mean'))
    # raw distance quintile
    d2 = df.dropna(subset=['raw'])
    d2 = d2.assign(rq=pd.qcut(d2['raw'].rank(method='first'), 5, labels=False))
    out['grid_by_raw_quintile'] = d2.groupby('rq').agg(n=('r','size'), raw=('raw','mean'), mean_r=('r','mean'), mean_ex=('ex','mean'))
    # gains by position side (bar level)
    P['g'] = P['a']*P['dr']
    P['side'] = np.sign(P['a'])
    out['bar_gain_by_side'] = P.groupby('side').agg(n=('g','size'), mean_gain_bps=('g', lambda x: x.mean()*1e4), mean_alloc=('a','mean'), coin_dr_bps=('dr', lambda x: x.mean()*1e4))
    out['bar_gain_by_coin_side'] = P.groupby(['coin','side'])['g'].sum().unstack()
    # book by window
    win = []
    for coin, ws in data['days'].items():
        for w, d in ws.items():
            win.append(d.assign(coin=coin, w=w))
    D = pd.concat(win)
    bw = D.groupby('w').agg(book=('book_return','mean'), coin=('coin_return','mean'))
    bw['book_sum'] = D.groupby('w')['book_return'].sum()/6
    bw['coin_sum'] = D.groupby('w')['coin_return'].sum()/6
    out['by_window'] = bw[['book_sum','coin_sum']]
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data['trades'].items() for w, t in ws.items()])
    out['trades_by_side'] = T.groupby('side').agg(n=('net_profit_loss_percent','size'), net=('net_profit_loss_percent','mean'), gross=('profit_loss_percent','mean'), dur_days=('duration_minutes', lambda x: x.mean()/1440))
    # long-only vs short slope
    for s in [1,-1]:
        x = df[df.side==s]
        sl = stats.linregress(x['f'], x['ex'])
        out[f'slope_side{s}'] = f"slope={sl.slope:.5f} t={sl.slope/sl.stderr:.2f} n={len(x)}"
    df['tr'] = np.sign(df['r52'])
    out['by_52d_trend_and_side'] = df.groupby(['tr','side']).agg(n=('r','size'), mean_r=('r','mean'))
    return out
