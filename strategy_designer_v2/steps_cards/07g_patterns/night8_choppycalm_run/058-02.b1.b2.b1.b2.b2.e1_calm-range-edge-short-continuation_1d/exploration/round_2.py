import numpy as np, pandas as pd

def ct(df, col):
    d = df.dropna(subset=[col])
    n = len(d)
    if n < 5: return (n, np.nan, np.nan, 0)
    m = d[col].mean()
    s = (d[col]-m).groupby(d['day']).sum()
    G = len(s)
    se = np.sqrt((s**2).sum()/n**2 * G/(G-1)) if G > 1 else np.nan
    return (n, m, m/se if se else np.nan, G)

def tab(df, by, col):
    rows = []
    for k, g in df.groupby(by, observed=True):
        n, m, t, G = ct(g, col)
        rows.append(dict(key=str(k), n=n, mean_pct=m*100, t=t, days=G))
    return pd.DataFrame(rows)

def build(data):
    frames = []
    for coin, wins in data['bars'].items():
        for w, b in wins.items():
            b = b.sort_values('timestamp').reset_index(drop=True).copy()
            b['coin'] = coin; b['win'] = w; b['i'] = np.arange(len(b))
            c = b['close']
            b['ret1'] = c.pct_change()
            for h in (2, 5, 10):
                b[f'fwd{h}'] = c.shift(-h)/c - 1
            hh = b['high'].rolling(20, min_periods=20).max()
            ll = b['low'].rolling(20, min_periods=20).min()
            b['rp'] = (c-ll)/(hh-ll)
            b['sd20'] = b['ret1'].rolling(20, min_periods=15).std()
            b['width'] = (hh-ll)/c/(b['sd20']*np.sqrt(20))
            b['vr'] = b['ret1'].rolling(10, min_periods=8).std()/b['ret1'].rolling(60, min_periods=40).std()
            b['tr60'] = c/c.shift(60)-1
            b['r20'] = c/c.shift(20)-1
            b['day'] = pd.to_datetime(b['timestamp']).dt.floor('D')
            b['calm'] = np.where(b['regime'] == 'unknown', 'calm', 'agit')
            b['trend'] = np.select([b['tr60'] > .1, b['tr60'] < -.1], ['rising', 'falling'], 'choppy')
            b.loc[b['tr60'].isna(), 'trend'] = 'na'
            frames.append(b)
    return pd.concat(frames, ignore_index=True)

def explore(data):
    B = build(data)
    out = {}
    for h in (2, 5, 10):
        g = B[B['i'] % h == 0].copy()
        dr = g.groupby('coin')[f'fwd{h}'].mean()
        g['ex'] = g[f'fwd{h}'] - g['coin'].map(dr)
        g['side'] = np.sign(g['rp'] - 0.5)
        g['sx'] = g['ex']*g['side']
        g['rpq'] = pd.cut(g['rp'], [-0.01, .2, .4, .6, .8, 1.01], labels=['q1','q2','q3','q4','q5'])
        if h == 5:
            out['h5_rp_calm'] = tab(g, ['calm', 'rpq'], 'ex')
            out['h5_rp_agit_trend'] = tab(g[g.calm == 'agit'], ['trend', 'rpq'], 'ex')
            g['wq'] = pd.qcut(g['width'], 4, labels=['narrow','w2','w3','wide'])
            out['h5_signed_by_width_calm'] = tab(g, ['calm', 'wq'], 'sx')
            g['vq'] = pd.qcut(g['vr'], 4, labels=['contract','v2','v3','expand'])
            out['h5_signed_by_volratio'] = tab(g, ['calm', 'vq'], 'sx')
            g['r20q'] = pd.qcut(g['r20'], 5, labels=['r1','r2','r3','r4','r5'])
            out['h5_r20_agit'] = tab(g[g.calm == 'agit'], ['trend', 'r20q'], 'ex')
        out[f'h{h}_signed_calm_trend'] = tab(g, ['calm', 'trend'], 'sx')
    # book's largest days
    D = []
    for coin, wins in data['days'].items():
        for w, d in wins.items():
            d = d.copy(); d['coin'] = coin; d['win'] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(['win', 'day'])[['book_return', 'coin_return']].mean().reset_index().dropna()
    q = bk['book_return'].quantile([.05, .95])
    top = bk[bk.book_return >= q[.95]]; bot = bk[bk.book_return <= q[.05]]
    out['book_extremes'] = pd.DataFrame({
        'n': [len(top), len(bot)],
        'book_mean': [top.book_return.mean(), bot.book_return.mean()],
        'coin_mean': [top.coin_return.mean(), bot.coin_return.mean()],
        'share_total_gain': [top.book_return.sum()/bk.book_return.sum(), bot.book_return.sum()/bk.book_return.sum()]},
        index=['top5', 'bottom5'])
    bk['cq'] = pd.qcut(bk['coin_return'], 5, labels=['c1','c2','c3','c4','c5'])
    out['book_by_market_day'] = bk.groupby('cq', observed=True)['book_return'].agg(['count', 'mean'])
    return out
