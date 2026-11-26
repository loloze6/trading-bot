import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].astype(float); h = d["high"].astype(float); l = d["low"].astype(float)
            hi = h.rolling(20).max(); lo = l.rolling(20).min()
            d["pos"] = 2*(c-lo)/(hi-lo)-1
            d["calm"] = (d["regime"] != "chop")
            d["tr60"] = c/c.shift(60)-1
            r1 = c.pct_change(); d["r1"] = r1
            d["z1"] = r1 / r1.rolling(30).std().shift(1)
            d["r5past"] = c/c.shift(5)-1
            d["fwd5"] = c.shift(-5)/c-1
            d["fwd1"] = c.shift(-1)/c-1
            d["alloc"] = d["postRebalance_current_allocation"].astype(float)
            d["gain"] = d["alloc"]*d["fwd1"]
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            d["yr"] = pd.to_datetime(d["timestamp"]).dt.year
            d["coin"] = coin; d["w"] = w; d["i"] = np.arange(len(d))
            d["day"] = pd.to_datetime(d["timestamp"]).dt.floor("D")
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["i"] % 5 == 0) & A["fwd5"].notna()].copy()
    G["ex5"] = G["fwd5"] - G.groupby("coin")["fwd5"].transform("mean")
    def summ(g, col="ex5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    G["posq"] = pd.cut(G["pos"], [-1.01,-0.6,-0.2,0.2,0.6,1.01], labels=["bot","lo","mid","hi","top"])
    out["pos_bucket_by_calm"] = G.groupby(["calm","posq"]).apply(summ).unstack(0)
    G["trend"] = pd.cut(G["tr60"], [-9,-0.10,0.10,99], labels=["falling","choppy","rising"])
    G["side"] = np.sign(G["pos"])
    G["sx"] = G["side"]*G["ex5"]
    out["signed_edge_by_trend_calm"] = G[G["pos"].abs()>0.5].groupby(["calm","trend"]).apply(lambda g: summ(g,"sx"))
    out["signed_edge_by_side_calm"] = G[G["pos"].abs()>0.5].groupby(["calm","side"]).apply(lambda g: summ(g,"sx"))
    G["zb"] = pd.cut(G["z1"], [-99,-2,-1,1,2,99])
    out["after_1d_move_z"] = G.groupby(["calm","zb"]).apply(summ).unstack(0)
    G["p5b"] = pd.qcut(G["r5past"], 5, labels=False)
    out["after_past5_quintile"] = G.groupby(["calm","p5b"]).apply(summ).unstack(0)
    # weekday on coin 1-day returns, all bars
    A["ex1"] = A["fwd1"] - A.groupby("coin")["fwd1"].transform("mean")
    out["weekday_next_day"] = A.groupby("wd").apply(lambda g: summ(g,"ex1"))
    # book by side
    A["sgn"] = np.sign(A["alloc"])
    out["book_gain_by_side_calm"] = A.groupby(["sgn","calm"])["gain"].agg(["count","mean","sum"])
    out["book_gain_by_year_side"] = A.groupby(["yr","sgn"])["gain"].sum().unstack()
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)], ignore_index=True)
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median"])
    T["absf"] = pd.qcut(T["entry_forecast"].abs(), 4, labels=False, duplicates="drop")
    out["trades_by_side_absforecast"] = T.groupby(["side","absf"])["net_profit_loss_percent"].agg(["count","mean"])
    return out
