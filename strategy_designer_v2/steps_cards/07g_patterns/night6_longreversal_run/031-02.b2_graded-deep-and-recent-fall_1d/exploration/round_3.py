import numpy as np, pandas as pd
from scipy import stats

def _cslope(x, y, g):
    # OLS slope with day-clustered standard error
    d = pd.DataFrame(dict(x=x, y=y, g=g)).dropna()
    xm = d.x - d.x.mean(); ym = d.y - d.y.mean()
    b = (xm*ym).sum()/(xm**2).sum()
    e = ym - b*xm
    s = (xm*e).groupby(d.g).sum()
    D = len(s)
    se = np.sqrt((s**2).sum()*D/(D-1))/(xm**2).sum()
    return b, b/se, len(d), D

def _ct(df, col, tcol='ts'):
    d = df.dropna(subset=[col])
    m = d[col].mean()
    s = (d[col]-m).groupby(d[tcol]).sum(); D = len(s)
    se = np.sqrt((s**2).sum()*D/(D-1))/len(d)
    return m, m/se, len(d), D

def explore(data):
    bars = data["bars"]; out = {}
    # A: 7-day and 14-day forward vs vol-scaled 30-day / 14-day return, clustered, grid offsets
    res = []; byy = []
    for H, P in [(7,30),(7,14),(7,60),(14,30),(3,30)]:
        for off in [0, 1, 2, 3]:
            rows = []
            for c, wins in bars.items():
                for w, b in wins.items():
                    cl = b['close'].values; ts = pd.to_datetime(b['timestamp']).values
                    r1 = np.r_[np.nan, cl[1:]/cl[:-1]-1]
                    for i in range(off, len(cl), H):
                        if i+H >= len(cl) or i < max(P,30): continue
                        v = np.nanstd(r1[i-29:i+1])
                        rows.append(dict(coin=c, ts=ts[i], yr=pd.Timestamp(ts[i]).year, w=w,
                                         fwd=cl[i+H]/cl[i]-1, s=(cl[i]/cl[i-P]-1)/(v*np.sqrt(P)),
                                         v=v))
            A = pd.DataFrame(rows)
            A['ex'] = A['fwd'] - A.groupby('coin')['fwd'].transform('mean')
            A['exs'] = A['ex']/(A['v']*np.sqrt(H))
            b, t, n, D = _cslope(A['s'], A['exs'], A['ts'])
            top = A[A.s >= A.s.quantile(0.8)]; bot = A[A.s <= A.s.quantile(0.2)]
            res.append(dict(H=H, P=P, off=off, slope=b, t_clust=t, n=n, days=D,
                            top_ex=top.ex.mean(), bot_ex=bot.ex.mean()))
            if H == 7 and P == 30 and off == 0:
                for y, s in A.groupby('yr'):
                    b2, t2, n2, D2 = _cslope(s['s'], s['exs'], s['ts'])
                    byy.append(dict(yr=y, slope=b2, t=t2, n=n2))
                A['vq'] = pd.qcut(A['v'], 3, labels=False)
                vr = []
                for q, s in A.groupby('vq'):
                    b2, t2, n2, D2 = _cslope(s['s'], s['exs'], s['ts'])
                    vr.append(dict(volq=q, slope=b2, t=t2, n=n2))
                out['A_7_30_by_vol'] = pd.DataFrame(vr)
                # size: top-quintile-in-direction strength
                A['sig'] = np.sign(A['s'])
                A['dirx'] = A['ex']*A['sig']
                m, t3, n3, D3 = _ct(A[A.s.abs() >= A.s.abs().quantile(0.6)], 'dirx')
                out['A_7_30_directional_strongest40pct'] = pd.DataFrame([dict(mean=m, t=t3, n=n3, days=D3,
                    usual_move=A.groupby('coin')['fwd'].std().mean())])
    out['A_grid'] = pd.DataFrame(res)
    out['A_7_30_by_year'] = pd.DataFrame(byy)
    # B: next-day reversal after scaled daily move, clustered by day, by year
    dl = []
    for c, wins in bars.items():
        for w, b in wins.items():
            cl = b['close'].values; ts = pd.to_datetime(b['timestamp']).values
            r = pd.Series(np.r_[np.nan, cl[1:]/cl[:-1]-1])
            v = r.rolling(30, min_periods=20).std().shift(1)
            d = pd.DataFrame(dict(coin=c, ts=ts, r=r, z=(r/v).clip(-5,5), v=v, yr=pd.to_datetime(ts).year))
            d['n1'] = r.shift(-1)
            d['n3'] = pd.Series(cl).shift(-3)/pd.Series(cl)-1
            dl.append(d)
    B = pd.concat(dl, ignore_index=True).dropna(subset=['z','n1'])
    B['ex1'] = B['n1'] - B.groupby('coin')['r'].transform('mean')
    B['ex1s'] = B['ex1']/B['v']
    b, t, n, D = _cslope(B['z'], B['ex1s'], B['ts'])
    rr = [dict(grp='all', slope=b, t=t, n=n, days=D)]
    for y, s in B.groupby('yr'):
        b, t, n, D = _cslope(s['z'], s['ex1s'], s['ts']); rr.append(dict(grp=str(y), slope=b, t=t, n=n, days=D))
    B['vq'] = B.groupby('coin')['v'].transform(lambda x: pd.qcut(x, 3, labels=False))
    for q, s in B.groupby('vq'):
        b, t, n, D = _cslope(s['z'], s['ex1s'], s['ts']); rr.append(dict(grp=f'vol{q}', slope=b, t=t, n=n, days=D))
    out['B_nextday_clustered'] = pd.DataFrame(rr)
    return out
