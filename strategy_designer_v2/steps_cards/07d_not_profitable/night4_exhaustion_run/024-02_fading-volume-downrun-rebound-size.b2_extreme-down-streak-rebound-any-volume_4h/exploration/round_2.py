import pandas as pd, numpy as np

def explore(data):
    H = 18
    out = {}
    bars = data["bars"]
    rows = []; brs = []
    for c in bars:
        dl = []
        for w, b in bars[c].items():
            cl = b["close"].values; idx = np.arange(0, len(cl) - H, H)
            dl += list(cl[idx + H] / cl[idx] - 1)
        drift = np.mean(dl)
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r = cl.pct_change()
            f = b["forecast"].fillna(0)
            alloc = b["postRebalance_current_allocation"].fillna(0)
            gain = alloc * (cl.shift(-1) / cl - 1)
            vr = r.rolling(30).std() / r.rolling(180).std()
            ret3 = cl / cl.shift(18) - 1
            ret30 = cl / cl.shift(180) - 1
            fwd = cl.shift(-H) / cl - 1
            # streak length of down closes
            down = (r < 0).astype(int)
            streak = down.groupby((down == 0).cumsum()).cumsum()
            rise = (f - f.shift(1)) >= 2
            cell = np.arange(len(b)) // H
            d = pd.DataFrame({"rise": rise, "cell": cell, "fwd": fwd, "f": f, "vr": vr, "ret3": ret3,
                              "ret30": ret30, "streak": streak})
            cs = d[d.rise].groupby("cell").head(1).dropna(subset=["fwd", "vr", "ret3"])
            cs = cs.assign(coin=c, unusual=cs.fwd - drift)
            rows.append(cs)
            brs.append(pd.DataFrame({"f": f, "alloc": alloc, "gain": gain, "vr": vr, "ret30": ret30,
                                     "fpos": (f > 0)}))
    cs = pd.concat(rows); br = pd.concat(brs)
    tt = lambda s: s.mean() / s.std() * np.sqrt(len(s))
    out["bars forecast>0 share"] = br.fpos.mean()
    out["bars long while forecast==0 share"] = ((br.alloc > 0) & (~br.fpos)).mean()
    out["long-bar gain by forecast>0"] = br[br.alloc > 0].groupby("fpos").agg(n=("gain", "size"),
        mean=("gain", "mean"), alloc=("alloc", "mean"))
    cs["vrq"] = pd.qcut(cs.vr, 3, labels=["low", "mid", "high"])
    cs["r3q"] = pd.qcut(cs.ret3, 3, labels=["fall", "flat", "rise"])
    out["cases vr x ret3"] = cs.groupby(["vrq", "r3q"]).agg(n=("unusual", "size"),
        total=("fwd", "mean"), unusual=("unusual", "mean"), t=("unusual", tt))
    out["cases by streak length"] = cs.assign(sl=cs.streak.clip(upper=6)).groupby("sl").agg(
        n=("unusual", "size"), unusual=("unusual", "mean"), t=("unusual", tt))
    bl = br[br.alloc > 0].dropna(subset=["vr"]).copy()
    bl["vrq"] = pd.qcut(bl.vr, 5, labels=False)
    out["long bars gain by vol ratio"] = bl.groupby("vrq").agg(n=("gain", "size"), mean=("gain", "mean"),
        sd=("gain", "std"), alloc=("alloc", "mean"), lo=("vr", "min"), hi=("vr", "max"))
    return out
