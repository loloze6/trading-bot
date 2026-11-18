import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20).std()
            z = r / vol
            vr = vol.rolling(365, min_periods=91).rank(pct=True)
            nxt = c.shift(-1) / c - 1
            n3 = c.shift(-3) / c - 1
            n5 = c.shift(-5) / c - 1
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "r": r, "z": z, "vr": vr,
                              "nxt": nxt, "n3": n3, "n5": n5, "r5": r5, "r20": r20, "vol": vol,
                              "f": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                              "wd": ts.dt.weekday, "yr": ts.dt.year})
            rows.append(d)
    D = pd.concat(rows)
    mu = D.groupby("coin")["nxt"].transform("mean")
    D["ex"] = D["nxt"] - mu
    D["gain"] = D["alloc"] * D["nxt"]
    out["n_by_coin"] = D.groupby("coin").size()
    # z quintile x vol-rank tercile next-day excess
    E = D.dropna(subset=["z", "vr", "ex"]).copy()
    E["zq"] = pd.qcut(E["z"], 5, labels=False)
    E["vt"] = pd.qcut(E["vr"], 3, labels=False)
    out["nextday_mean_bps_zq_x_vt"] = (E.pivot_table(index="zq", columns="vt", values="ex", aggfunc="mean") * 1e4).round(1)
    out["count_zq_x_vt"] = E.pivot_table(index="zq", columns="vt", values="ex", aggfunc="count")
    # slope of ex on z by coin and by vt
    res = []
    for (k, g) in list(E.groupby("coin")) + list(E.groupby("vt")) + list(E.groupby("yr")):
        s = stats.linregress(g["z"], g["ex"])
        res.append({"grp": str(k), "slope_bps": s.slope * 1e4, "t": s.slope / s.stderr, "n": len(g)})
    out["slope_ex_on_z"] = pd.DataFrame(res).round(2)
    # multi-day non-overlapping on grid
    for h, col in [(3, "n3"), (5, "n5")]:
        G = D[(D["pos"] % h == 0)].dropna(subset=[col, "z", "r5"])
        G = G.assign(ex=G[col] - G.groupby("coin")[col].transform("mean"))
        rr = []
        for x in ["z", "r5", "r20"]:
            g = G.dropna(subset=[x])
            s = stats.linregress(g[x], g["ex"])
            rr.append({"x": x, "slope": s.slope, "t": s.slope / s.stderr, "n": len(g)})
        out[f"h{h}_slopes"] = pd.DataFrame(rr).round(4)
    # weekday
    wd = D.dropna(subset=["nxt"]).groupby("wd")["nxt"].agg(["mean", "std", "count"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["nextday_by_weekday_of_signal_bar"] = wd.round(5)
    # book long vs short gain
    D["side"] = np.sign(D["alloc"])
    sg = D.dropna(subset=["gain"]).groupby(["coin", "side"])["gain"].agg(["mean", "count", "sum"])
    out["gain_by_side"] = sg.round(5)
    # book by window
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, w=w))
    DD = pd.concat(dd)
    bw = DD.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    out["by_window_mean_daily_x1e4"] = (bw * 1e4).round(1).T
    return out
