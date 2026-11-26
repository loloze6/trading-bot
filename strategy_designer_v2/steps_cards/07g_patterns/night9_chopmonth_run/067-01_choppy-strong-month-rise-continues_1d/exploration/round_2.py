import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 7
    drift = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                allr.append(c[i+H]/c[i]-1)
        drift[coin] = np.mean(allr)
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change()
            r30 = c / c.shift(30) - 1
            vol30 = r1.rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            for off in range(H):
                for i in range(off, len(c) - H, H):
                    rows.append(dict(coin=coin, w=w, off=off, yr=ts[i].year, day=ts[i].normalize(),
                        chop=(b["regime"][i] == "unknown"), r30=r30[i], vol=vol30[i],
                        ex=c[i+H]/c[i]-1-drift[coin]))
    d = pd.DataFrame(rows).dropna(subset=["r30", "vol"])
    d["vq"] = d.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 2, labels=False, duplicates="drop"))
    d["z30"] = d["r30"] / (d["vol"] * np.sqrt(30))
    out = {}
    def sl(s, x="r30"):
        if len(s) < 10: return "n<10"
        r = stats.linregress(s[x], s["ex"])
        return f"slope {r.slope:.4f} t {r.slope/r.stderr:.2f} n {len(s)}"
    ch = d[d.chop]
    # robustness over grid offsets
    out["chop slope by grid offset"] = pd.Series({o: sl(ch[ch.off == o]) for o in range(H)})
    out["chop neg-r30 slope by offset"] = pd.Series({o: sl(ch[(ch.off == o) & (ch.r30 < 0)]) for o in range(H)})
    out["chop pos-r30 slope by offset"] = pd.Series({o: sl(ch[(ch.off == o) & (ch.r30 > 0)]) for o in range(H)})
    g0 = ch[ch.off == 0]
    out["chop off0 slope by year"] = pd.Series({y: sl(g0[g0.yr == y]) for y in sorted(g0.yr.unique())})
    out["chop off0 slope excl 2018"] = sl(g0[g0.yr != 2018])
    out["chop off0 neg r30 excl 2018"] = sl(g0[(g0.yr != 2018) & (g0.r30 < 0)])
    out["chop off0 slope by vol half"] = pd.Series({v: sl(g0[g0.vq == v]) for v in [0, 1]})
    out["chop off0 neg slope by vol half"] = pd.Series({v: sl(g0[(g0.vq == v) & (g0.r30 < 0)]) for v in [0, 1]})
    out["chop off0 slope on scaled z30"] = sl(g0, "z30")
    # day-clustered mean of ex for negative r30 in chop, signed
    neg = g0[g0.r30 < 0].copy()
    pd_ = neg.groupby("day")["ex"].sum()
    out["chop neg r30: mean ex, day-clustered t, days"] = f"mean {neg.ex.mean():.4f} t {pd_.mean()/(pd_.std()/np.sqrt(len(pd_)))*np.sqrt(len(pd_))/np.sqrt(len(pd_)):.2f} days {len(pd_)} cases {len(neg)}"
    sd = neg.groupby("day")["ex"].sum()
    out["chop neg r30 day-sum t"] = float(sd.sum()/np.sqrt((sd**2).sum()))
    pos = g0[g0.r30 > 0]; sp = pos.groupby("day")["ex"].sum()
    out["chop pos r30 mean ex / day-sum t"] = f"mean {pos.ex.mean():.4f} t {sp.sum()/np.sqrt((sp**2).sum()):.2f} n {len(pos)}"
    out["chop neg r30 mean ex by coin"] = neg.groupby("coin")["ex"].agg(["count", "mean"])
    out["chop neg r30 by year"] = neg.groupby("yr")["ex"].agg(["count", "mean"])
    # book: daily returns by regime
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            br.append(dd[["book_return", "coin_return"]].assign(coin=coin))
    B = pd.concat(br).dropna()
    out["book mean daily, coin mean daily"] = f"{B.book_return.mean():.5f} {B.coin_return.mean():.5f}"
    return out
