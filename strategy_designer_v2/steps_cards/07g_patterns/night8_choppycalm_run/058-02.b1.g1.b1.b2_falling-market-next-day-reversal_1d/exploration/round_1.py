import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd20 = r.rolling(20).std()
            z = r / sd20
            nxt = c.shift(-1) / c - 1
            tr60 = c / c.shift(60) - 1
            vol30 = r.rolling(30).std()
            volrel = vol30 / vol30.expanding(30).median()
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "z": z, "r": r, "nxt": nxt, "tr60": tr60,
                               "volrel": volrel, "clpos": clpos, "rng_z": rng / rng.rolling(20).mean(),
                               "wd": ts.dt.weekday, "regime": b["regime"],
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "fc": b["forecast"].astype(float), "day": ts.dt.floor("D")})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    cm = d.groupby("coin")["nxt"].transform("mean")
    d["ex"] = d["nxt"] - cm
    d = d.dropna(subset=["nxt", "z"])
    d["active"] = d["regime"] != "chop"
    def tbl(g):
        return pd.Series({"n": len(g), "mean_ex%": g["ex"].mean()*100,
                          "t": g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))) if len(g) > 2 else np.nan})
    d["zb"] = pd.cut(d["z"], [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    out = {}
    out["z_bin_active(falling)"] = d[d.active].groupby("zb", observed=True).apply(tbl)
    out["z_bin_notfalling"] = d[~d.active].groupby("zb", observed=True).apply(tbl)
    dt = d.dropna(subset=["tr60"]).copy()
    dt["prof"] = np.where(dt.tr60 > 0.1, "rising", np.where(dt.tr60 < -0.1, "falling", "choppy"))
    dt["sgn_ex"] = -np.sign(dt["z"]) * dt["ex"]  # fade payoff
    dt["big"] = dt["z"].abs() > 1
    out["fade_by_prof_big"] = dt.groupby(["prof", "big"]).apply(lambda g: tbl(g.assign(ex=g.sgn_ex)))
    dt["vq"] = pd.qcut(dt["volrel"], 3, labels=["lowvol", "mid", "highvol"])
    out["fade_by_prof_vol_big"] = dt[dt.big].groupby(["prof", "vq"], observed=True).apply(lambda g: tbl(g.assign(ex=g.sgn_ex)))
    d["cb"] = pd.cut(d["clpos"], [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
    out["closepos_all"] = d.groupby("cb", observed=True).apply(tbl)
    out["weekday_all"] = d.groupby("wd").apply(tbl)
    # book days
    bd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            bd.append(x.assign(coin=coin, w=w))
    bd = pd.concat(bd)
    bk = bd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bk.groupby("w").agg(n=("book_return", "size"), book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"))
    return out
