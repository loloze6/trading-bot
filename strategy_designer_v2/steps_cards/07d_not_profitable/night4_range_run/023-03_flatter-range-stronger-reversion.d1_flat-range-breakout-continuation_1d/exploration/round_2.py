def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []; grid = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            pos = b["postRebalance_current_allocation"].astype(float)
            r1 = c.shift(-1) / c - 1
            v = b["postRebalance_total_value"].astype(float)
            df = pd.DataFrame({"coin": coin, "w": w, "pos": pos, "gain": pos * r1, "r1": r1,
                               "br": v / v.shift(1) - 1, "fc": b["forecast"].astype(float),
                               "ret30": c / c.shift(30) - 1, "ret60": c / c.shift(60) - 1,
                               "ret90": c / c.shift(90) - 1,
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            df["k"] = np.arange(len(df))
            rows.append(df)
            idx = np.arange(0, len(c) - 5, 5)
            g = df.iloc[idx].copy(); g["f5"] = (c.shift(-5) / c - 1).iloc[idx].values
            grid.append(g)
    A = pd.concat(rows); G = pd.concat(grid).dropna(subset=["f5"])
    drift = G.groupby("coin")["f5"].mean()
    G["u5"] = G["f5"] - G["coin"].map(drift)
    G["sgn"] = np.sign(G["fc"]); G = G[G.sgn != 0]
    G["dir_u"] = G.sgn * G.u5; G["dirmove"] = G.sgn * G.f5
    G["side"] = np.where(G.sgn > 0, "long", "short")
    tt = lambda x: x.mean() / x.std() * np.sqrt(len(x))
    for h in ["ret60", "ret90"]:
        G["tr"] = np.where(G[h] > 0, "up", "down")
        out["side_" + h] = G.dropna(subset=[h]).groupby(["side", "tr"]).agg(n=("dirmove", "size"),
                             dirmove=("dirmove", "mean"), dir_u=("dir_u", "mean"), t_move=("dirmove", tt))
    # graded: dirmove vs signed long trend
    G["agree90"] = G.sgn * G["ret90"]
    G["aq"] = pd.qcut(G["agree90"], 5)
    out["by_agree90_q"] = G.dropna(subset=["agree90"]).groupby("aq").agg(n=("dirmove", "size"),
                             dirmove=("dirmove", "mean"), t=("dirmove", tt))
    out["side_year"] = G.groupby(["year", "side"])["dirmove"].mean().unstack()
    # book gain per bar by side and 90d trend
    A["side"] = np.where(A.pos > 0, "long", np.where(A.pos < 0, "short", "flat"))
    A["tr90"] = np.where(A.ret90 > 0, "up90", "down90")
    out["bar_gain_side_tr90"] = A.dropna(subset=["ret90"]).groupby(["side", "tr90"]).agg(
        n=("gain", "size"), mean_gain=("gain", "mean"), sum_gain=("gain", "sum"))
    # drawdown episode: deepest
    D = A.groupby(["w", "k"]).agg(br=("br", "mean"), hr=("r1", "mean"), pos=("pos", "mean"),
                                  r90=("ret90", "mean")).dropna(subset=["br"])
    wo = sorted(D.index.get_level_values(0).unique(), key=lambda s: int(s[1:]))
    D = D.loc[wo].reset_index()
    eq = (1 + D.br).cumprod(); peak = eq.cummax(); dd = eq / peak - 1
    trough = dd.idxmin(); pk = eq[:trough + 1].idxmax()
    seg = D.loc[pk:trough]
    out["deepest_fall"] = pd.Series({"depth": dd.min(), "days": len(seg), "windows": ",".join(seg.w.unique()),
                                     "mean_pos": seg.pos.mean(), "share_short_days": (seg.pos < 0).mean(),
                                     "hold_chain": (1 + seg.hr).prod() - 1, "mean_ret90": seg.r90.mean()})
    return out
