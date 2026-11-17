import numpy as np, pandas as pd
from scipy import stats

def rsi(c, n=14):
    d = c.diff()
    up = d.clip(lower=0).ewm(alpha=1/n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
    return 100 - 100/(1 + up/dn)

def explore(data):
    out = {}
    recs = {h: [] for h in [1, 3, 7]}
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = rsi(c)
            share = b["debug_info.components.rsi_share.last_history_value"]
            r1 = c.pct_change(); vol20 = r1.rolling(20).std()
            z = r1 / vol20
            z3 = (c/c.shift(3)-1) / (vol20*np.sqrt(3))
            pos = b["postRebalance_current_allocation"]
            n = len(b)
            for h in recs:
                for i in range(0, n - h, h):
                    recs[h].append(dict(coin=coin, win=w, share=share.iloc[i], rsi=r.iloc[i],
                                        z=z.iloc[i], z3=z3.iloc[i], vol=vol20.iloc[i], pos=pos.iloc[i],
                                        fwd=c.iloc[i+h]/c.iloc[i]-1))
    for h, L in recs.items():
        g = pd.DataFrame(L)
        g["d"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
        res = {}
        for col in ["share", "rsi", "z", "z3", "pos"]:
            d = g.dropna(subset=[col, "d"])
            s = stats.linregress(d[col], d["d"])
            res[col] = s.slope / s.stderr
        res["n"] = len(g)
        out[f"t_h{h}"] = pd.Series(res)
        if h == 1:
            d = g.dropna(subset=["z", "vol", "d"]).copy()
            d["vq"] = pd.qcut(d["vol"], 3, labels=False)
            tt = {}
            for v, dd in d.groupby("vq"):
                s = stats.linregress(dd["z"], dd["d"]); tt[v] = s.slope/s.stderr
            out["h1_z_t_by_volterc"] = pd.Series(tt)
            # sides of position: welch
            a = g.loc[g.pos < 0, "fwd"].dropna(); bb = g.loc[g.pos > 0, "fwd"].dropna()
            out["h1_fwd_short_minus_long"] = f"diff {a.mean()-bb.mean():.5f} welch t {stats.ttest_ind(a, bb, equal_var=False).statistic:.2f} n {len(a)}/{len(bb)}"
            d["zq"] = pd.qcut(d["z"], 5, labels=False)
            t = d.groupby("zq").agg(n=("d","size"), z=("z","mean"), m=("d","mean"), sd=("d","std"))
            t["t"] = t.m/(t.sd/np.sqrt(t.n)); out["h1_by_z_quintile"] = t.drop(columns="sd")
        if h == 7:
            d = g.dropna(subset=["rsi", "d"]).copy()
            d["q"] = pd.qcut(d["rsi"], 5, labels=False)
            t = d.groupby("q").agg(n=("d","size"), rsi=("rsi","mean"), m=("d","mean"), sd=("d","std"))
            t["t"] = t.m/(t.sd/np.sqrt(t.n)); out["h7_by_rsi_quintile"] = t.drop(columns="sd")
    return out
