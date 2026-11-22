import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    H = [1, 2, 4, 8, 24]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=360).std()
            vr = v / v.rolling(720, min_periods=360).mean()
            z = r / sd
            d = pd.DataFrame({"coin": coin, "w": w, "z": z, "vr": vr, "pos": np.arange(len(b)),
                              "alloc": b["postRebalance_current_allocation"].astype(float),
                              "fc": b["forecast"].astype(float),
                              "raw": b.get("debug_info.components.vol_surge_up.last_history_value")})
            for h in H:
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # drift per coin per horizon on grids
    for h in H:
        g = D[D.pos % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean()
        D[f"x{h}"] = D[f"f{h}"] - D.coin.map(dr)
    G = D[D.pos % 4 == 0].dropna(subset=["z", "vr", "x4"])
    G = G.assign(zv=G.z * G.vr)
    def tab(df, col, q):
        df = df.copy(); df["bin"] = pd.qcut(df[col], q, duplicates="drop")
        t = df.groupby("bin", observed=True)["x4"].agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["mean_bp"] = t["mean"] * 1e4
        return t[["count", "mean_bp", "t"]]
    out["x4 by z*vr decile (all hours)"] = tab(G, "zv", 10)
    up = G[G.z > 0]
    # joint extremes: z bins x vr bins, up hours
    up = up.assign(zb=pd.cut(up.z, [0, 1, 2, 3, 5, 100]), vb=pd.cut(up.vr, [0, 1, 2, 3, 5, 1000]))
    p = up.groupby(["zb", "vb"], observed=True)["x4"].agg(["count", "mean"])
    p["mean_bp"] = p["mean"] * 1e4
    out["up hours x4 bp by z bin, vol-ratio bin"] = p[["count", "mean_bp"]]
    dn = G[G.z < 0]
    dn = dn.assign(zb=pd.cut(-dn.z, [0, 1, 2, 3, 5, 100]), vb=pd.cut(dn.vr, [0, 1, 2, 3, 5, 1000]))
    p2 = dn.groupby(["zb", "vb"], observed=True)["x4"].agg(["count", "mean"])
    p2["mean_bp"] = p2["mean"] * 1e4
    out["down hours x4 bp by |z| bin, vol-ratio bin"] = p2[["count", "mean_bp"]]
    # horizons for extreme up surges (all bars, non-overlap per h)
    res = []
    for h in H:
        g = D[(D.pos % h == 0)].dropna(subset=["z", "vr", f"x{h}"])
        for name, m in [("up z>3 vr>3", (g.z > 3) & (g.vr > 3)), ("down z<-3 vr>3", (g.z < -3) & (g.vr > 3)),
                        ("up z>2", g.z > 2), ("down z<-2", g.z < -2)]:
            x = g.loc[m, f"x{h}"]
            res.append({"h": h, "set": name, "n": len(x), "mean_bp": x.mean() * 1e4,
                        "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["extremes by horizon"] = pd.DataFrame(res)
    # book: trading and holding
    B = D.copy()
    B["absalloc"] = B.alloc.abs()
    out["share of bars in position"] = float((B.absalloc > 0.01).mean())
    out["mean abs alloc when in"] = float(B.loc[B.absalloc > 0.01, "absalloc"].mean())
    B["turn"] = B.groupby(["coin", "w"]).alloc.diff().abs()
    out["mean daily turnover (sum |dalloc| per coin-day)"] = float(B.turn.sum() / (len(B) / 24))
    # gross position gain per bar
    B["r1"] = B.groupby(["coin", "w"]).f1.transform(lambda s: s)
    B["gain"] = B.alloc * B.f1
    out["gross gain per day bp (mean coin)"] = float(B.gain.sum() / (len(B) / 24) * 1e4)
    out["fee per day bp est (turnover*0.055%)"] = float(B.turn.sum() / (len(B) / 24) * 0.00055 * 1e4)
    # forecast level vs alloc
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades: mean pl% gross, net, count, mean dur h"] = pd.Series({
        "gross": tr.profit_loss_percent.mean(), "net": tr.net_profit_loss_percent.mean(),
        "n": len(tr), "dur_h": tr.duration_minutes.mean() / 60})
    tr["fb"] = pd.qcut(tr.entry_forecast, 5, duplicates="drop")
    out["trades by entry forecast quintile"] = tr.groupby("fb", observed=True)[["profit_loss_percent", "net_profit_loss_percent"]].agg(["count", "mean"])
    return out
