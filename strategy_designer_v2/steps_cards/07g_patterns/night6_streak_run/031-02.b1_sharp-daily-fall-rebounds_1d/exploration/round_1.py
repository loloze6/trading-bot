import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(60, min_periods=20).std()
            z = r / sd
            # streak: signed consecutive closes
            s = np.sign(r).fillna(0).values
            st = np.zeros(len(s))
            for i in range(len(s)):
                if s[i] == 0: st[i] = 0
                elif i > 0 and np.sign(st[i-1]) == s[i]: st[i] = st[i-1] + s[i]
                else: st[i] = s[i]
            ret20 = c / c.shift(20) - 1
            volq = sd
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z": z, "r": r,
                               "streak": st, "ret20": ret20, "sd": sd,
                               "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "f1": c.shift(-1)/c - 1, "f2": c.shift(-2)/c - 1, "f5": c.shift(-5)/c - 1,
                               "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    out = {}
    for h, col in [(1, "f1"), (2, "f2"), (5, "f5")]:
        d["ex%d" % h] = d[col] - d.groupby("coin")[col].transform(lambda x: x[d.loc[x.index, "pos"] % h == 0].mean())
    g2 = d[(d.pos % 2 == 0)].dropna(subset=["z", "ex2"])
    g5 = d[(d.pos % 5 == 0)].dropna(subset=["z", "ex5"])
    def summ(g, key, col):
        a = g.groupby(key)[col].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.drop(columns="std")
    g2 = g2.assign(zb=pd.cut(g2.z, [-99, -2.5, -1.5, -0.75, 0, 0.75, 1.5, 2.5, 99]))
    out["z bucket -> ex2"] = summ(g2, "zb", "ex2")
    g5 = g5.assign(zb=pd.cut(g5.z, [-99, -2.5, -1.5, -0.75, 0, 0.75, 1.5, 2.5, 99]))
    out["z bucket -> ex5"] = summ(g5, "zb", "ex5")
    g2s = g2.assign(sb=g2.streak.clip(-5, 5))
    out["streak -> ex2"] = summ(g2s, "sb", "ex2")
    g5s = g5.assign(sb=g5.streak.clip(-5, 5))
    out["streak -> ex5"] = summ(g5s, "sb", "ex5")
    # falls by vol tercile (within coin)
    g2 = g2.assign(vq=g2.groupby("coin")["sd"].transform(lambda x: pd.qcut(x, 3, labels=False)))
    falls = g2[g2.z < 0]
    out["falls: slope ex2 on -z by vol tercile"] = falls.groupby("vq").apply(
        lambda x: pd.Series({"slope": stats.linregress(-x.z, x.ex2).slope,
                             "t": stats.linregress(-x.z, x.ex2).slope / stats.linregress(-x.z, x.ex2).stderr,
                             "n": len(x), "mean": x.ex2.mean()}))
    falls = falls.assign(tr=np.where(falls.ret20 > 0, "up20", "down20"))
    out["falls: slope by 20d trend"] = falls.dropna(subset=["ret20"]).groupby("tr").apply(
        lambda x: pd.Series({"slope": stats.linregress(-x.z, x.ex2).slope,
                             "t": stats.linregress(-x.z, x.ex2).slope / stats.linregress(-x.z, x.ex2).stderr,
                             "n": len(x), "mean": x.ex2.mean()}))
    rises = g2[g2.z > 0]
    lr = stats.linregress(rises.z, rises.ex2)
    out["rises: slope ex2 on z"] = pd.Series({"slope": lr.slope, "t": lr.slope / lr.stderr, "n": len(rises)})
    out["falls slope by coin"] = falls.groupby("coin").apply(
        lambda x: pd.Series({"t": stats.linregress(-x.z, x.ex2).slope / stats.linregress(-x.z, x.ex2).stderr, "n": len(x)}))
    g1 = d.dropna(subset=["ex1"])
    out["weekday -> ex1 (all bars)"] = summ(g1, "wd", "ex1")
    # 20-day return grade -> ex5
    g5 = g5.dropna(subset=["ret20"])
    g5 = g5.assign(rb=g5.groupby("coin")["ret20"].transform(lambda x: pd.qcut(x, 5, labels=False)))
    out["ret20 quintile -> ex5"] = summ(g5, "rb", "ex5")
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, w=w))
    dd = pd.concat(dd)
    bk = dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    bk["yr"] = pd.to_datetime(bk.index.get_level_values("day")).year
    out["book by year"] = bk.groupby("yr").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    return out
