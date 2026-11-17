def explore(data):
    import numpy as np, pandas as pd
    out = {}
    fc = 'debug_info.components.rsi_below_age.last_history_value'
    # per-window book vs coin daily returns
    rows = []
    for coin in data['days']:
        for w, d in data['days'][coin].items():
            b = data['bars'][coin][w]
            rows.append({'coin': coin, 'w': int(w[1:]), 'book_mean': d['book_return'].mean(),
                         'coin_mean': d['coin_return'].mean(),
                         'short_share': (b['postRebalance_current_allocation'] < 0).mean(),
                         'mean_alloc': b['postRebalance_current_allocation'].mean()})
    pw = pd.DataFrame(rows)
    out['by_window'] = pw.groupby('w')[['book_mean', 'coin_mean', 'short_share', 'mean_alloc']].mean()
    # bar-level gain decomposition
    allb = []
    for coin in data['bars']:
        cm_parts = []
        for w, b in data['bars'][coin].items():
            b = b.copy()
            b['r1'] = b['close'].shift(-1) / b['close'] - 1
            b['coin'] = coin; b['w'] = w
            # trend state known at close: 30-day and 90-day returns, within window
            b['ret30'] = b['close'] / b['close'].shift(30) - 1
            b['ret90'] = b['close'] / b['close'].shift(90) - 1
            b['ma100'] = b['close'] / b['close'].rolling(100, min_periods=50).mean() - 1
            b['ret7'] = b['close'] / b['close'].shift(7) - 1
            allb.append(b)
    B = pd.concat(allb)
    B['pos'] = B['postRebalance_current_allocation']
    B['gain'] = B['pos'] * B['r1']
    cmean = B.groupby('coin')['r1'].mean()
    B['cm'] = B['coin'].map(cmean)
    B['drift'] = B['pos'] * B['cm']
    B['timing'] = B['gain'] - B['drift']
    s = B[B['pos'] < 0]
    out['decomp_all'] = pd.Series({'gain_mean_all_bars': B['gain'].mean(), 'drift': B['drift'].mean(),
                                   'timing': B['timing'].mean(), 'n_short_bars': len(s),
                                   'short_share': (B['pos'] < 0).mean()})
    s = s.copy()
    s['run'] = -s[fc]
    s['runb'] = pd.cut(s['run'], [0, 5, 10, 20, 35, 61])
    out['short_by_run'] = s.groupby('runb').agg(n=('gain', 'size'), gain=('gain', 'mean'),
                                                r1=('r1', 'mean'), pos=('pos', 'mean'))
    for col in ['ret30', 'ret90', 'ma100', 'ret7']:
        q = pd.qcut(s[col], 4, duplicates='drop')
        out['short_by_' + col] = s.groupby(q).agg(n=('gain', 'size'), gain=('gain', 'mean'), r1=('r1', 'mean'))
    # fees
    T = pd.concat([pd.concat(list(data['trades'][c].values())) for c in data['trades']])
    out['trades'] = pd.Series({'n': len(T), 'pl_mean': T['profit_loss_percent'].mean(),
                               'net_mean': T['net_profit_loss_percent'].mean(),
                               'win': (T['profit_loss_percent'] > 0).mean(),
                               'dur_days_mean': T['duration_minutes'].mean() / 1440})
    return out
