import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            hi20 = c.rolling(20, min_periods=20).max()
            sd20 = r.rolling(20, min_periods=15).std()
            depth = (c - hi20) / hi20 / sd20
            ret60 = c / c.shift(60) - 1
            vol_rel = b["volume"] / b["volume"].rolling(20, min_periods=10).mean()
            lvr = np.log(vol_rel)
            sd_rel = sd20 / r.rolling(60, min_periods=40).std()
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            rows.append(pd.DataFrame({"coin": coin, "w": w, "r": r, "rz": r / sd20, "nxt": nxt, "nxt2": nxt2,
                "depth": depth, "ret60": ret60, "lvr": lvr, "sd_rel": sd_rel, "clpos": clpos,
                "pos": b["postRebalance_current_allocation"].astype(float), "day": pd.to_datetime(b["timestamp"]).dt.floor("D")}))
    d = pd.concat(rows, ignore_index=True).dropna(subset=["nxt", "r", "lvr"])
    drift = d.groupby("coin")["nxt"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(drift)
    d["up"] = d["r"] > 0
    d["trend"] = np.where(d.ret60 > .1, "rising", np.where(d.ret60 < -.1, "falling", "choppy"))
    d.loc[d.ret60.isna(), "trend"] = "na"
    d["agit"] = np.where(d.sd_rel > 1, "agit", "calm")

    def summ(g):
        x = g["ex"].dropna()
        # day-clustered t
        s = g.dropna(subset=["ex"]).groupby("day")["ex"].sum()
        return pd.Series({"n": len(x), "days": len(s), "mean_ex_%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "t_day": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out = {}
    u = d[d.up].dropna(subset=["depth"]).copy()
    u["dq3"] = pd.qcut(u.depth, 3, labels=["deep", "mid", "shal"])
    u["vq3"] = pd.qcut(u.lvr, 3, labels=["lowvol", "midvol", "hivol"])
    out["up_depth_x_vol"] = u.groupby(["dq3", "vq3"]).apply(summ)
    u["wgrp"] = np.where(u.w.isin(["w7","w8","w9","w10","w11","w12"]), "B", "C")
    out["up_lowvol_by_fold"] = u.groupby(["wgrp", "vq3"]).apply(summ)
    dn = d[~d.up].copy()
    dn["vq4"] = pd.qcut(dn.lvr, 4, labels=False)
    out["down_vol_by_profile"] = dn.groupby(["trend", "agit", "vq4"]).apply(summ)
    dn["wgrp"] = np.where(dn.w.isin(["w7","w8","w9","w10","w11","w12"]), "B", "C")
    out["down_vol_by_fold"] = dn.groupby(["wgrp", "vq4"]).apply(summ)
    dn["mq3"] = pd.qcut(dn.rz, 3, labels=["bigfall", "mid", "smallfall"])
    out["down_vol_x_move"] = dn.groupby(["mq3", "vq4"]).apply(summ)
    # correlation grade
    for nm, g in [("up", u), ("down", dn)]:
        gg = g.dropna(subset=["lvr", "ex"])
        rr, p = stats.spearmanr(gg.lvr, gg.ex)
        out[f"spearman_lvr_ex_{nm}"] = f"rho {rr:.4f} p {p:.4g} n {len(gg)}"
    # book biggest days
    bd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            bd.append(x.assign(coin=coin, w=w))
    bd = pd.concat(bd).dropna(subset=["book_return"])
    dm = bd.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index()
    dm["bq"] = pd.qcut(dm.br, 10, labels=False, duplicates="drop")
    out["book_decile_vs_coin"] = dm.groupby("bq").agg(n=("br", "size"), book_bp=("br", lambda x: 1e4*x.mean()), coin_bp=("cr", lambda x: 1e4*x.mean()))
    return out
