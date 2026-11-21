def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = 96
    drift = {}; usual = {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            idx = np.arange(0, len(c) - H, H)
            rs += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(rs); usual[coin] = np.std(rs)
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).values; n = len(c)
            s = pd.Series(c)
            r24 = s / s.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=300).mean()
            z = (r24 / mabs).values
            r30 = (s / s.shift(720) - 1).values
            r7 = (s / s.shift(168) - 1).values
            for g0 in range(0, n - 192, H):
                for t in range(g0, g0 + H):
                    if np.isfinite(z[t]) and z[t] <= -1.5 and np.isfinite(r30[t]) and t + 192 < n:
                        rows.append(dict(coin=coin, win=int(w[1:]), z=z[t], r30=r30[t], r7=r7[t],
                            up24=c[t+24]/c[t]-1, up48=c[t+48]/c[t]-1, up96=c[t+96]/c[t]-1, up192=c[t+192]/c[t]-1))
                        break
    df = pd.DataFrame(rows)
    df["u96"] = df.up96 - df.coin.map(drift)
    df["str"] = df.u96 / df.coin.map(usual)
    def summ(g):
        return pd.Series({"n": len(g), "up24": g.up24.mean(), "up48": g.up48.mean(), "up96": g.up96.mean(),
            "up192": g.up192.mean(), "unus96": g.u96.mean(), "t_u96": g.u96.mean()/(g.u96.std()/np.sqrt(len(g))),
            "strength": g["str"].mean()})
    df["r30q"] = pd.qcut(df.r30, 6)
    out["plunge_long_by_r30"] = df.groupby("r30q").apply(summ)
    dn = df[df.r30 < 0].copy()
    dn["zq"] = pd.qcut(dn.z, 3)
    out["plunge_long_r30neg_by_z"] = dn.groupby("zq").apply(summ)
    deep = df[df.r30 < -0.2].copy()
    deep["half"] = np.where(deep.win <= 12, "w1-12", "w13-24")
    out["deep_by_half"] = deep.groupby("half").apply(summ)
    out["deep_by_coin"] = deep.groupby("coin").apply(summ)
    # book decomposition
    rec = []
    for coin, wins in data["bars"].items():
        allc = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allc.append(c[1:]/c[:-1]-1)
        mu = np.concatenate(allc).mean()
        for w, b in wins.items():
            c = b["close"].astype(float).values
            a = b["postRebalance_current_allocation"].fillna(0).values[:-1]
            r = c[1:]/c[:-1]-1
            rec.append(dict(coin=coin, short_share=(a < 0).mean(), mean_alloc=a.mean(),
                gross=(a*r).mean()*24, market=(a*mu).mean()*24, timing=(a*(r-mu)).mean()*24))
    R = pd.DataFrame(rec)
    out["book_decomp_daily"] = R.groupby("coin")[["short_share", "mean_alloc", "gross", "market", "timing"]].mean()
    return out
