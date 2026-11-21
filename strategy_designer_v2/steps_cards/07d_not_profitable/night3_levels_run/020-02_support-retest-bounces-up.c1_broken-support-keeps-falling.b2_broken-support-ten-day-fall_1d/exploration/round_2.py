import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        g_all = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(b)
            s = pd.Series(c)
            r30 = s.pct_change(30).values
            hi60 = s.rolling(60, min_periods=20).max().values
            lo60 = s.rolling(60, min_periods=20).min().values
            raw = b["debug_info.components.support_above.last_history_value"] if "debug_info.components.support_above.last_history_value" in b else pd.Series([np.nan]*n)
            for i in range(0, n - H, H):
                g_all.append(dict(coin=coin, w=w, f=b["forecast"].iloc[i], raw=raw.iloc[i],
                                  r=c[i+H]/c[i]-1, r30=r30[i],
                                  pos=(c[i]-lo60[i])/(hi60[i]-lo60[i]) if hi60[i]>lo60[i] else np.nan,
                                  alloc=b["postRebalance_current_allocation"].iloc[i]))
        g = pd.DataFrame(g_all); g["drift"] = g["r"].mean(); rows.append(g)
    G = pd.concat(rows)
    G["adj_short"] = -(G["r"] - G["drift"]); G["short_r"] = -G["r"]
    def tt(x): return x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
    S = G[G["f"] < 0].copy()
    out["overall short: adj mean, t, raw short mean, t, n"] = pd.DataFrame({"adj":[S.adj_short.mean()],"t_adj":[tt(S.adj_short)],"raw":[S.short_r.mean()],"t_raw":[tt(S.short_r)],"n":[len(S)]})
    S["fq"] = pd.qcut(S["f"].abs().rank(method="first"), 4, labels=["q1","q2","q3","q4"])
    out["by |f| quartile: raw short, t"] = S.groupby("fq")["short_r"].agg(["mean", tt, "count"])
    G["pq"] = pd.qcut(G["pos"].rank(method="first"), 5, labels=["p1low","p2","p3","p4","p5high"])
    out["all grid: position in 60d range -> 10d r"] = G.groupby("pq").agg(r=("r","mean"), t=("r", tt), share_active=("f", lambda x:(x<0).mean()), n=("r","count"))
    S["pq"] = pd.qcut(S["pos"].rank(method="first"), 3, labels=["low","mid","high"])
    out["active: |f| half x range position: raw short"] = S.assign(big=S["fq"].isin(["q3","q4"])).groupby(["big","pq"])["short_r"].agg(["mean","count"])
    S["t30"] = pd.qcut(S["r30"].rank(method="first"), 3, labels=["down","mid","up"])
    out["active: |f| half x 30d trend: raw short"] = S.assign(big=S["fq"].isin(["q3","q4"])).groupby(["big","t30"])["short_r"].agg(["mean","count"])
    F = G[G["f"] >= 0]
    out["flat bars (no low above close): 10d r, t"] = pd.DataFrame({"r":[F.r.mean()],"t":[tt(F.r)],"adj":[(F.r-F.drift).mean()],"t_adj":[tt(F.r-F.drift)],"n":[len(F)]})
    out["mean |alloc| when active"] = S["alloc"].abs().mean()
    return out
