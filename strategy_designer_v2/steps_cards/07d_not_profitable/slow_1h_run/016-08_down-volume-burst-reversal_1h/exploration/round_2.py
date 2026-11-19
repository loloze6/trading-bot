import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    grid = []
    daily = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            s = pd.Series(cl)
            r72 = s.pct_change(72).values
            r720 = s.pct_change(720).values
            lv = np.log(s).diff()
            vol72 = lv.rolling(720).std().values * np.sqrt(72)
            z = r72 / vol72
            fwd = np.r_[cl[72:] / cl[:-72] - 1, [np.nan] * 72]
            fwd24 = np.r_[cl[24:] / cl[:-24] - 1, [np.nan] * 24]
            idx = np.arange(0, len(b), 72)
            grid.append(pd.DataFrame({"coin": c, "r72": r72[idx], "r720": r720[idx], "z": z[idx],
                                      "fwd": fwd[idx], "fc": b["forecast"].values[idx]}))
            # daily book with state at day's last bar
            ts = pd.to_datetime(b["timestamp"])
            dfb = pd.DataFrame({"day": ts.dt.floor("D"), "v": b["postRebalance_total_value"].values,
                                "cl": cl, "r720": r720, "z": z, "pos": b["postRebalance_current_allocation"].fillna(0).values})
            dd = dfb.groupby("day").last()
            dd["br"] = dd["v"].pct_change(); dd["cr"] = dd["cl"].pct_change()
            # state at prior day's close
            dd["tr_prev"] = (dd["r720"] > 0).shift(1)
            dd["z_prev"] = dd["z"].shift(1)
            dd["pos_prev"] = dd["pos"].shift(1)
            dd["coin"] = c
            daily.append(dd.dropna(subset=["br", "tr_prev"]))
    G = pd.concat(grid).dropna(subset=["fwd", "r72", "z"])
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    dn = G[G["r72"] < 0].copy()
    dn["zq"] = pd.qcut(dn["z"], 5, labels=False)
    tt = lambda x: x.mean() / x.std() * np.sqrt(len(x))
    out["down_by_z_quintile"] = dn.groupby("zq").agg(zmean=("z", "mean"), ex=("ex", "mean"), n=("ex", "size"), t=("ex", tt))
    dn = dn.dropna(subset=["r720"])
    dn["tr"] = np.where(dn["r720"] > 0, "up30", "down30")
    out["down_z_x_trend"] = dn.groupby(["tr", "zq"]).agg(ex=("ex", "mean"), n=("ex", "size"), t=("ex", tt))
    # correlation of fc with ex by trend
    out["fc_corr_by_trend"] = dn.dropna(subset=["fc"]).groupby("tr").apply(lambda x: pd.Series({"spearman": stats.spearmanr(x["fc"], x["ex"]).correlation, "n": len(x)}))
    out["fc_corr_with_z_in_down"] = dn.dropna(subset=["fc"]).groupby("zq").apply(lambda x: stats.spearmanr(x["fc"], x["ex"]).correlation)
    D = pd.concat(daily)
    inpos = D[D["pos_prev"] > 0.01]
    out["book_days_held_by_trend"] = inpos.groupby("tr_prev").agg(book=("br", "mean"), coin=("cr", "mean"), n=("br", "size"),
                                                                   sharpe=("br", lambda x: x.mean() / x.std() * np.sqrt(365)))
    inpos = inpos.dropna(subset=["z_prev"]).copy()
    inpos["zq"] = pd.qcut(inpos["z_prev"], 5, labels=False)
    out["book_days_held_by_zq"] = inpos.groupby("zq").agg(z=("z_prev", "mean"), book=("br", "mean"), coin=("cr", "mean"), n=("br", "size"))
    out["share_days_held"] = len(D[D["pos_prev"] > 0.01]) / len(D)
    return out
