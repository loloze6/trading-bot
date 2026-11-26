import numpy as np, pandas as pd

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
            r1 = c.pct_change()
            sd = r1.rolling(30).std()
            d["z1"] = r1 / sd.shift(1)
            d["r5past"] = c/c.shift(5)-1
            d["z5"] = d["r5past"]/(sd*np.sqrt(5))
            d["fwd5"] = c.shift(-5)/c-1
            d["fwd3"] = c.shift(-3)/c-1
            d["coin"] = coin; d["w"] = w; d["i"] = np.arange(len(d))
            d["day"] = pd.to_datetime(d["timestamp"]).dt.floor("D")
            d["yr"] = pd.to_datetime(d["timestamp"]).dt.year
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["i"] % 5 == 0) & A["fwd5"].notna()].copy()
    G["ex5"] = G["fwd5"] - G.groupby("coin")["fwd5"].transform("mean")
    G["trend"] = pd.cut(G["tr60"], [-9,-0.10,0.10,99], labels=["falling","choppy","rising"])
    def summ(g, col="ex5"):
        x = g[col].dropna()
        if len(x) < 3: return pd.Series({"n": len(x), "mean%": np.nan, "t": np.nan})
        dd = g.loc[x.index].groupby("day")[col].sum()
        tday = x.mean()/ (np.sqrt((dd - dd.count()/len(x)*0).pow(2).sum())/len(x)) if False else np.nan
        # day-clustered t
        dev = (x - x.mean()); dsum = dev.groupby(g.loc[x.index,"day"]).sum()
        se = np.sqrt((dsum**2).sum())/len(x)
        return pd.Series({"n": len(x), "days": dsum.size, "mean%": 100*x.mean(), "t_day": x.mean()/se})
    out = {}
    Ag = G[~G["calm"]].copy()
    Ag["z5b"] = pd.cut(Ag["z5"], [-99,-1.5,-0.5,0.5,1.5,99])
    out["agit_after_z5_by_trend"] = Ag.groupby(["trend","z5b"]).apply(summ)
    Cm = G[G["calm"]].copy()
    Cm["z5b"] = pd.cut(Cm["z5"], [-99,-1.5,-0.5,0.5,1.5,99])
    out["calm_after_z5"] = Cm.groupby("z5b").apply(summ)
    Cm["posb"] = pd.cut(Cm["pos"], [-1.01,-0.5,0.5,1.01], labels=["bot","mid","top"])
    Cm["zb"] = pd.cut(Cm["z1"], [-99,-1,1,99], labels=["down","flat","up"])
    out["calm_pos_x_z1"] = Cm.groupby(["posb","zb"]).apply(summ)
    out["calm_edge_signed_by_year"] = Cm[Cm["pos"].abs()>0.5].assign(sx=lambda g: np.sign(g["pos"])*g["ex5"]).groupby("yr").apply(lambda g: summ(g,"sx"))
    out["agit_z5_signed_by_year"] = Ag[Ag["z5"].abs()>0.5].assign(sx=lambda g: -np.sign(g["z5"])*g["ex5"]).groupby("yr").apply(lambda g: summ(g,"sx"))
    out["agit_z5_signed_by_coin"] = Ag[Ag["z5"].abs()>0.5].assign(sx=lambda g: -np.sign(g["z5"])*g["ex5"]).groupby("coin").apply(lambda g: summ(g,"sx"))
    out["calm_edge_by_coin"] = Cm[Cm["pos"].abs()>0.5].assign(sx=lambda g: np.sign(g["pos"])*g["ex5"]).groupby("coin").apply(lambda g: summ(g,"sx"))
    return out
