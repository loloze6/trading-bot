import numpy as np, pandas as pd
from scipy import stats

FC = 'debug_info.components.range_pos.post_pipeline_value'
RC = 'debug_info.components.range_pos.last_history_value'

def _grid(data, h):
    rows = []
    for coin, wins in data['bars'].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df['close'].values
            ts = pd.to_datetime(df['timestamp'])
            lr = pd.Series(c).pct_change()
            sd30 = lr.rolling(30).std()
            # agitation: share of past year's 30d swings at or below today's (within window, approx)
            agit = sd30.rolling(365, min_periods=120).apply(lambda a: (a <= a[-1]).mean(), raw=True).values
            tr60 = pd.Series(c).pct_change(60).values
            hi20 = pd.Series(c).rolling(20).max().values
            lo20 = pd.Series(c).rolling(20).min().values
            pos = (c - lo20) / (hi20 - lo20)
            for i in range(0, len(df) - h, h):
                rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, f=df[FC].iloc[i], raw=df[RC].iloc[i],
                                 pos=pos[i], r=c[i+h]/c[i]-1, tr=tr60[i], ag=agit[i], day=ts.iloc[i].floor('D')))
    g = pd.DataFrame(rows).dropna(subset=['f', 'r'])
    g['drift'] = g.groupby('coin')['r'].transform('mean')
    g['x'] = g['r'] - g['drift']
    g['xw'] = g['r'] - g.groupby(['coin', 'win'])['r'].transform('mean')
    return g

def _slope(g, xcol='f', ycol='x'):
    g = g.dropna(subset=[xcol, ycol])
    if len(g) < 10 or g[xcol].std() == 0:
        return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
    res = stats.linregress(g[xcol], g[ycol])
    return pd.Series(dict(n=len(g), slope=res.slope, t=res.slope/res.stderr))

def explore(data):
    out = {}
    g = _grid(data, 5)
    out['h5 standardised forecast'] = _slope(g, 'f')
    out['h5 raw range position'] = _slope(g, 'raw')
    out['h5 forecast, window-demeaned return'] = _slope(g, 'f', 'xw')
    out['h5 raw, window-demeaned return'] = _slope(g, 'raw', 'xw')
    g['agit'] = np.where(g['ag'] > 0.5, 'agitated', np.where(g['ag'].notna(), 'calm', 'na'))
    out['h5 by agitation'] = g.groupby('agit').apply(_slope)
    # raw position bins
    g['pb'] = pd.cut(g['raw'], [-20.01, -19.99, -10, 0, 10, 19.99, 20.01],
                     labels=['at low', 'low', 'mid-low', 'mid-high', 'high', 'at high'])
    out['h5 by raw position bin'] = g.groupby('pb')['x'].agg(['count', 'mean', 'std']).assign(
        t=lambda d: d['mean']/(d['std']/np.sqrt(d['count'])))
    # day-clustered t of signed unusual move
    g['sx'] = np.sign(g['f'])*g['x']
    d = g.groupby('day')['sx'].sum()
    nd = len(d)
    out['h5 signed move, day-clustered'] = pd.Series(dict(cases=len(g), days=nd, mean=g['sx'].mean(),
        t=g['sx'].sum()/np.sqrt(((d - d.mean()*0)**2).sum())))
    # per-window share of positive slopes for h3
    g3 = _grid(data, 3)
    out['h3 by year'] = g3.groupby('year').apply(_slope)
    out['h5 window-level: coin window mean return vs mean forecast'] = _slope(
        g.groupby(['coin', 'win']).agg(f=('f', 'mean'), x=('r', 'mean')).reset_index(), 'f', 'x')
    return out
