import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            n = len(df)
            r20 = np.full(n, np.nan); r20[20:] = c[20:] / c[:-20] - 1
            r60 = np.full(n, np.nan); r60[60:] = c[60:] / c[:-60] - 1
            for h in (10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, f=f[i], r20=r20[i], r60=r60[i],
                                     ret=c[i+h]/c[i]-1, year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby(["coin","h"])["ret"].transform("mean")
    out = {}
    res = []
    for h in (10, 20):
        g = d[(d.h == h)].dropna(subset=["r20"])
        for name, sub in [("all", g), ("on", g[g.f > 0]), ("off", g[g.f == 0])]:
            for var in ("r20", "r60"):
                s2 = sub.dropna(subset=[var])
                # rank-free: z-score per coin
                z = s2.groupby("coin")[var].transform(lambda x: (x - x.mean())/x.std())
                s = stats.linregress(z, s2["ex"])
                a = s2[s2[var] > 0]["ex"]; b = s2[s2[var] <= 0]["ex"]
                tt = stats.ttest_ind(a, b, equal_var=False)
                res.append(dict(h=h, set=name, var=var, n=len(s2), slope=s.slope, t=s.slope/s.stderr,
                                up_ex=a.mean(), dn_ex=b.mean(), n_up=len(a), t_updn=tt.statistic))
    out["momentum_tests"] = pd.DataFrame(res)
    g = d[(d.h == 10)].dropna(subset=["r20"])
    gon = g[g.f > 0]
    def cs(x):
        a = x[x.r20 > 0]["ex"]; b = x[x.r20 <= 0]["ex"]
        return pd.Series(dict(n_up=len(a), n_dn=len(b), up=a.mean(), dn=b.mean(),
                              t=stats.ttest_ind(a, b, equal_var=False).statistic if len(a)>2 and len(b)>2 else np.nan))
    out["on_r20split_by_coin"] = gon.groupby("coin").apply(cs)
    out["on_r20split_by_year"] = gon.groupby("year").apply(cs)
    out["all_r20split_by_coin"] = g.groupby("coin").apply(cs)
    # book decomposition
    rows = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            b = bars[coin][w]
            pos = b.set_index(pd.to_datetime(b["timestamp"]).dt.floor("D"))["postRebalance_current_allocation"]
            pos = pos.groupby(level=0).last().shift(1)
            dd2 = dd.copy(); dd2["dayk"] = pd.to_datetime(dd2["day"])
            dd2["pos"] = dd2["dayk"].map(pos)
            dd2["coin"] = coin
            rows.append(dd2)
    D = pd.concat(rows).dropna(subset=["book_return","coin_return","pos"])
    D["mu"] = D.groupby("coin")["coin_return"].transform("mean")
    daily = D.groupby("dayk").agg(book=("book_return","mean"), beta=("pos", lambda x: (x*D.loc[x.index,"mu"]).mean()))
    out["book_decomp"] = pd.Series(dict(book_mean=daily.book.mean(), market_part=daily.beta.mean(),
                                       timing=daily.book.mean()-daily.beta.mean(), mean_pos=D.pos.mean()))
    return out
