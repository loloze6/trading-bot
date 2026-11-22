import numpy as np, pandas as pd
from scipy import stats

def tstat(x):
    x = pd.Series(x).dropna()
    return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); n = len(c)
            if n < 30: continue
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            z1 = r1 / vol20
            hi20 = c.shift(1).rolling(20).max()
            brk = (c > hi20)
            fail = np.zeros(n); fdepth = np.full(n, np.nan)
            for t in range(n):
                for k in (1, 2, 3):
                    e = t - k
                    if e >= 0 and brk.iloc[e] and not np.isnan(hi20.iloc[e]):
                        if c.iloc[t] < hi20.iloc[e]:
                            fail[t] = 1; fdepth[t] = hi20.iloc[e] / c.iloc[t] - 1
                        break
            vchg = b["volume"].astype(float) / b["volume"].astype(float).rolling(20).mean()
            alloc = b["postRebalance_current_allocation"].astype(float)
            for H in (1, 3, 8):
                fwd = c.shift(-H) / c - 1
                fwd2 = c.shift(-H - 2) / c.shift(-2) - 1
                for t in range(0, n, H):
                    if t + H >= n: continue
                    rows.append(dict(H=H, coin=coin, w=w, wi=int(w[1:]), fwd=fwd.iloc[t],
                                     fwd2=fwd2.iloc[t] if t + H + 2 < n else np.nan,
                                     r1=r1.iloc[t], z1=z1.iloc[t], fail=fail[t], fdepth=fdepth[t],
                                     vchg=vchg.iloc[t], alloc=alloc.iloc[t]))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby(["H", "coin"])["fwd"].transform("mean")
    df["unu"] = df["fwd"] - df["drift"]
    df["unu2"] = df["fwd2"] - df["drift"]
    out = {}
    def summ(g, col="unu"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": tstat(x)})
    d = df.dropna(subset=["z1"]).copy()
    d["q"] = d.groupby(["H", "coin"])["z1"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["z1_q5_by_H"] = d.groupby(["H", "q"]).apply(summ).unstack("q")["t"]
    out["z1_q5_by_H_mean"] = d.groupby(["H", "q"]).apply(summ).unstack("q")["mean"]
    d8 = d[d.H == 8].copy()
    sp = []
    for (coin), g in d8.groupby("coin"):
        sp.append(dict(coin=coin, rho=stats.spearmanr(g["z1"], g["unu"])[0], n=len(g),
                       top_minus_bot=g[g.q == 4]["unu"].mean() - g[g.q == 0]["unu"].mean()))
    out["z1_by_coin_H8"] = pd.DataFrame(sp).set_index("coin")
    d8["half"] = np.where(d8.wi <= 12, "w1-12", "w13-24")
    out["z1_by_half_H8"] = d8.groupby(["half", "q"]).apply(summ).unstack("q")["t"]
    # regression unu ~ z1 per H
    reg = []
    for H, g in d.groupby("H"):
        s = stats.linregress(g["z1"], g["unu"])
        reg.append(dict(H=H, slope=s.slope, t=s.slope / s.stderr, n=len(g)))
    out["reg_unu_on_z1"] = pd.DataFrame(reg).set_index("H")
    # failure vs r1 control (H=8)
    f8 = d8.copy()
    out["fail_within_z1q"] = f8.groupby(["q", "fail"]).apply(summ).unstack("fail")
    ff = f8[f8.fail == 1].copy()
    out["fail_lag0_vs_lag2"] = pd.DataFrame({"lag0": summ(ff, "unu"), "lag2": summ(ff, "unu2")})
    ff["dq"] = pd.qcut(ff["fdepth"].rank(method="first"), 2, labels=False)
    out["fail_by_depth_half"] = ff.groupby("dq").apply(summ)
    # volume spike x sign of r1
    v = d8.dropna(subset=["vchg"]).copy()
    v["vq"] = v.groupby("coin")["vchg"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    v["up"] = (v["r1"] > 0).astype(int)
    out["vol_terc_x_up"] = v.groupby(["vq", "up"]).apply(summ)
    # book position vs z1
    out["short_share_by_z1q"] = d8.groupby("q")["alloc"].apply(lambda s: (s < 0).mean())
    return out
