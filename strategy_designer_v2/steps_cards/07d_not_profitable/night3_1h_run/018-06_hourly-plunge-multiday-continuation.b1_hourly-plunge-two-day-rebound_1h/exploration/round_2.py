def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 48
    drift = {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            rs += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(rs)
    rows = []; bars = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].fillna(0).values
            n = len(c)
            lr = np.log(pd.Series(c)).diff()
            vr = (lr.rolling(168).std() / lr.rolling(720).std()).values
            r168 = pd.Series(c).pct_change(168).values
            pos = b["postRebalance_current_allocation"].fillna(0).values
            g = np.r_[pos[:-1] * (c[1:] / c[:-1] - 1), 0.0]
            wn = int(w[1:])
            bars.append(pd.DataFrame(dict(coin=coin, wn=wn, vr=vr, pos=pos, g=g, f=f)))
            for s in range(0, n - H, H):
                seg = np.where(f[s:s + H] >= 2)[0]
                if len(seg) == 0: continue
                t = s + seg[0]
                if t + H >= n: continue
                fr = c[t + H] / c[t] - 1
                rows.append(dict(coin=coin, wn=wn, f=f[t], ex=fr - drift[coin], tot=fr, vr=vr[t], r168=r168[t]))
    d = pd.DataFrame(rows); B = pd.concat(bars)
    def summ(g):
        return pd.Series(dict(n=len(g), mean_ex=g.ex.mean(), t=g.ex.mean() / (g.ex.std() / np.sqrt(len(g))),
                              mean_tot=g.tot.mean(), rho=stats.spearmanr(g.f, g.ex)[0] if len(g) > 10 else np.nan))
    d["vrq"] = pd.qcut(d.vr, 5, labels=False)
    out["vr_q_by_fall_period"] = d.assign(fall=d.wn.between(12, 16)).groupby(["fall", "vrq"]).apply(summ)
    d["hi"] = d.vr > 1.0
    out["hi_vr_by_forecast"] = d[d.hi].groupby(pd.cut(d[d.hi].f, [0, 2.5, 8.4, 19.99, 20.1])).apply(summ)
    out["vr_by_coin_hi"] = d.groupby(["coin", "hi"]).apply(summ)["mean_ex"].unstack()
    B["vrq"] = pd.cut(B.vr, [0, 0.76, 0.9, 1.03, 1.2, 5], labels=False)
    act = B[B.pos.abs() > 0]
    out["bar_gain_by_vr"] = act.groupby("vrq").agg(bars=("g", "size"), mean_gain_bps=("g", lambda x: x.mean() * 1e4),
                                                   sum_gain=("g", "sum"), mean_pos=("pos", "mean"))
    out["bar_gain_fall_period_by_vr"] = act[act.wn.between(12, 16)].groupby("vrq").agg(bars=("g", "size"),
                                                   sum_gain=("g", "sum"))
    out["share_time_long"] = pd.Series(dict(all=(B.pos > 0).mean(), fall=(B[B.wn.between(12, 16)].pos > 0).mean()))
    return out
