def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    col = 'debug_info.components.fail_exc.last_history_value'
    H = [1, 3, 5, 10, 20]
    drift = {}; usual = {}
    for c, ws in data['bars'].items():
        for h in H:
            rs = []
            for w, b in ws.items():
                cl = b['close'].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    rows = []
    for c, ws in data['bars'].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b['close'].values; n = len(cl)
            raw = b[col].fillna(0).values if col in b else np.zeros(n)
            year = pd.to_datetime(b['timestamp']).dt.year.values
            mom20 = pd.Series(cl).pct_change(20).values
            mom60 = pd.Series(cl).pct_change(60).values
            vol20 = pd.Series(cl).pct_change().rolling(20).std().values
            first = np.r_[raw[0] > 0, (raw[1:] > 0) & (raw[:-1] <= 0)]
            for h in H:
                seen = set()
                for t in np.where(raw > 0)[0]:
                    g = t // h
                    if g in seen or t + h >= n: continue
                    seen.add(g)
                    r = cl[t + h] / cl[t] - 1
                    rows.append(dict(coin=c, win=w, h=h, year=year[t], exc=raw[t], first=first[t],
                                     r=r, unus=r - drift[(c, h)], strength=(r - drift[(c, h)]) / usual[(c, h)],
                                     mom20=mom20[t], mom60=mom60[t], vol20=vol20[t]))
    d = pd.DataFrame(rows)
    def summ(g):
        return pd.Series({'n': len(g), 'mean_unus_long': g.unus.mean(),
                          't': g.unus.mean() / (g.unus.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          'mean_raw': g.r.mean(), 'strength_long': g.strength.mean()})
    out = {}
    out['by_horizon'] = d.groupby('h').apply(summ)
    d5 = d[d.h == 5].copy()
    out['h5_by_coin'] = d5.groupby('coin').apply(summ)
    out['h5_by_year'] = d5.groupby('year').apply(summ)
    d5['excq'] = pd.qcut(d5.exc, 5, labels=False, duplicates='drop')
    out['h5_by_exc_quintile'] = d5.groupby('excq').apply(lambda g: pd.concat([summ(g), pd.Series({'exc_mean': g.exc.mean()})]))
    d5['m20q'] = pd.qcut(d5.mom20, 4, labels=False, duplicates='drop')
    out['h5_by_mom20_q'] = d5.groupby('m20q').apply(lambda g: pd.concat([summ(g), pd.Series({'m20': g.mom20.mean()})]))
    d5['m60s'] = np.sign(d5.mom60)
    out['h5_by_mom60_sign'] = d5.groupby('m60s').apply(summ)
    d5['vq'] = pd.qcut(d5.vol20, 3, labels=False, duplicates='drop')
    out['h5_by_vol_tercile'] = d5.groupby('vq').apply(summ)
    out['h5_first_bar_vs_later'] = d5.groupby('first').apply(summ)
    reg = {}
    for h in H:
        x = d[d.h == h]
        s = stats.linregress(x.exc, x.r)
        reg[h] = dict(slope=s.slope, t=s.slope / s.stderr, n=len(x))
    out['slope_r_on_exc_by_h'] = pd.DataFrame(reg).T
    d20 = d[d.h == 20].copy()
    d20['excq'] = pd.qcut(d20.exc, 5, labels=False, duplicates='drop')
    out['h20_by_exc_quintile'] = d20.groupby('excq').apply(summ)
    out['h10_by_coin'] = d[d.h == 10].groupby('coin').apply(summ)
    return out
