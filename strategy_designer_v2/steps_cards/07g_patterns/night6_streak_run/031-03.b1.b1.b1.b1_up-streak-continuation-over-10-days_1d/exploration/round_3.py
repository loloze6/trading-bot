import numpy as np, pandas as pd

def _slope(G, xcol, ycol='z'):
    d = G[[xcol, ycol, 'day']].dropna()
    if len(d) < 30: return np.nan, np.nan, len(d), 0
    x = (d[xcol] - d[xcol].mean()) / d[xcol].std()
    y = d[ycol] - d[ycol].mean()
    b = (x*y).sum() / (x*x).sum()
    e = y - b*x
    s = (x*e).groupby(d['day']).sum()
    D = len(s)
    se = np.sqrt(D/(D-1) * (s**2).sum()) / (x*x).sum()
    return round(b, 4), round(b/se, 2), len(d), D

def explore(data):
    out = {}
    for H in [5, 10, 20]:
        recs = []
        for coin, wins in data['bars'].items():
            rows = []
            for w, b in wins.items():
                b = b.sort_values('timestamp').reset_index(drop=True)
                c = b['close'].astype(float)
                r1 = c.pct_change()
                vol = r1.rolling(30).std()
                df = pd.DataFrame({'day': pd.to_datetime(b['timestamp']).dt.floor('D'),
                                   'fwd': c.shift(-H)/c - 1, 'pos': np.arange(len(c))})
                for L in [10, 30]:
                    df[f'm{L}'] = (c/c.shift(L) - 1) / (vol*np.sqrt(L))
                rows.append(df)
            cd = pd.concat(rows, ignore_index=True)
            gd = cd[(cd['pos'] % H == 0) & cd['fwd'].notna()]
            drift, sd = gd['fwd'].mean(), gd['fwd'].std()
            cd['z'] = (cd['fwd'] - drift)/sd; cd['coin'] = coin
            recs.append(cd)
        A = pd.concat(recs, ignore_index=True)
        rows = []
        for col in ['m10', 'm30']:
            for off in sorted(set([0, H//3, 2*H//3])):
                G = A[(A['pos'] % H == off) & A['fwd'].notna()].copy()
                G['yr'] = G['day'].dt.year
                b, t, n, D = _slope(G, col)
                bp, tp, _, _ = _slope(G[G[col] > 0], col)
                bn, tn, _, _ = _slope(G[G[col] <= 0], col)
                yrs = [ _slope(g, col)[0] for _, g in G.groupby('yr')]
                rows.append({'var': col, 'off': off, 'b': b, 't': t, 'n': n, 'days': D,
                             'b_posside': bp, 't_posside': tp, 'b_negside': bn, 't_negside': tn,
                             'yrs_pos_of': f"{sum(1 for y in yrs if y > 0)}/{len(yrs)}"})
        out[f'H{H}'] = pd.DataFrame(rows)
    return out
