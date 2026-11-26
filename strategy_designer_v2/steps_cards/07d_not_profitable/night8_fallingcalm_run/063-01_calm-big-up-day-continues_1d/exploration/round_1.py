import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            fwd = c.shift(-5) / c - 1
            r5p = c / c.shift(5) - 1
            r20p = c / c.shift(20) - 1
            pos = b["postRebalance_current_allocation"].astype(float)
            df = pd.DataFrame({"coin": coin, "w": w, "z": z, "fwd": fwd, "r5p": r5p, "r20p": r20p,
                               "calm": (b["regime"] == "unknown"), "fc": b["forecast"].astype(float),
                               "pos": pos, "i": np.arange(len(b))})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A.i % 5 == 0) & A.fwd.notna()].copy()
    drift = G.groupby("coin").fwd.mean()
    G["ex"] = G.fwd - G.coin.map(drift)
    G = G[G.z.notna()]
    G["zb"] = pd.cut(G.z, [-99, -2, -1, -0.5, 0, 0.5, 1, 2, 99])
    def summ(g):
        return pd.Series({"n": len(g), "fwd": g.fwd.mean(), "ex": g.ex.mean(),
                          "t_ex": g.ex.mean() / (g.ex.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    out["calm_by_z"] = G[G.calm].groupby("zb").apply(summ)
    out["agit_by_z"] = G[~G.calm].groupby("zb").apply(summ)
    # in calm and z>1: by prior 20d trend sign
    S = G[G.calm & (G.z > 1)].copy()
    S["tr"] = pd.cut(S.r20p, [-9, -0.1, 0, 0.1, 9])
    out["calm_z>1_by_r20"] = S.groupby("tr").apply(summ)
    C = G[G.calm & (G.z <= 1)].copy()
    C["tr"] = pd.cut(C.r20p, [-9, -0.1, 0, 0.1, 9])
    out["calm_z<=1_by_r20"] = C.groupby("tr").apply(summ)
    # book daily
    d = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; d.append(x)
    D = pd.concat(d, ignore_index=True)
    bk = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index()
    bk = bk.sort_values(["w", "day"]).dropna()
    v = (1 + bk.br).cumprod(); dd = v / v.cummax() - 1
    bk["dd"] = dd.values
    out["book_by_window"] = bk.groupby("w").agg(book=("br", "sum"), coins=("cr", "sum"), mindd=("dd", "min"))
    out["deepest_dd"] = float(dd.min())
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    T["fcb"] = pd.qcut(T.entry_forecast, 4, duplicates="drop")
    out["trades_by_entry_fc"] = T.groupby("fcb").agg(n=("net_profit_loss_percent", "size"),
        net=("net_profit_loss_percent", "mean"), gross=("profit_loss_percent", "mean"), dur=("duration_minutes", "mean"))
    out["trades_side"] = T.groupby("side").net_profit_loss_percent.describe()
    return out
