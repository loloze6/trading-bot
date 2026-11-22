def explore(data):
    import pandas as pd, numpy as np
    bars, days = data["bars"], data["days"]
    coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c].keys()}, key=lambda s: int(s[1:]))
    out = {}
    rows = []; grid = []
    allret10 = []
    for c in coins:
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True).copy()
            cl = b["close"]; r = cl.pct_change()
            b["rnext"] = cl.shift(-1) / cl - 1
            b["alloc"] = b["postRebalance_current_allocation"]
            b["gain"] = b["alloc"] * b["rnext"]
            b["ret20"] = cl / cl.shift(20) - 1
            b["ret60"] = cl / cl.shift(60) - 1
            b["ret90"] = cl / cl.shift(90) - 1
            b["dd60"] = cl / cl.rolling(60).max() - 1
            b["vol20"] = r.rolling(20).std()
            b["volratio"] = b["vol20"] / r.rolling(90).std()
            b["dd60v"] = b["dd60"] / (b["vol20"] * np.sqrt(20))
            b["ret20v"] = b["ret20"] / (b["vol20"] * np.sqrt(20))
            b["f10"] = cl.shift(-10) / cl - 1
            b["coin"] = c; b["win"] = w
            rows.append(b[["coin", "win", "alloc", "gain", "rnext", "ret20", "ret60", "ret90", "dd60", "volratio", "dd60v", "ret20v"]])
            g = b.iloc[::10]
            allret10.append(g["f10"].dropna())
            grid.append(g[["coin", "alloc", "f10", "ret20", "ret90", "dd60", "volratio", "dd60v", "ret20v"]])
    B = pd.concat(rows, ignore_index=True)
    G = pd.concat(grid, ignore_index=True)
    drift = pd.concat(allret10).mean()
    act = B[B["alloc"] > 0].dropna(subset=["gain"])
    out["exposure"] = pd.Series({"share_bars_long": (B["alloc"] > 0).mean(), "mean_alloc_when_long": act["alloc"].mean(),
                                 "mean_gain_long": act["gain"].mean(), "drift10": drift})
    res = {}
    for f in ["ret20v", "dd60v", "ret90", "volratio", "ret60"]:
        q = pd.qcut(act[f], 5, labels=False, duplicates="drop")
        gg = act.groupby(q)["gain"]
        m = gg.mean(); s = gg.std(); n = gg.size()
        res[f] = pd.Series({**{f"q{int(i)}": m[i] for i in m.index}, "t_q0": m.iloc[0] / (s.iloc[0] / np.sqrt(n.iloc[0])),
                            "t_q4": m.iloc[-1] / (s.iloc[-1] / np.sqrt(n.iloc[-1])), "worst_q_sum_share": (gg.sum().min() / act["gain"].sum())})
    out["bar_gain_by_quintile_long"] = pd.DataFrame(res).T
    # 10-day forward unusual move on grid, active cases
    Ga = G[(G["alloc"] > 0)].dropna(subset=["f10"])
    Ga = Ga.assign(u=Ga["f10"] - drift)
    res2 = {}
    for f in ["ret20v", "dd60v", "ret90", "volratio"]:
        q = pd.qcut(Ga[f], 5, labels=False, duplicates="drop")
        gg = Ga.groupby(q)["u"]
        m = gg.mean(); s = gg.std(); n = gg.size()
        res2[f] = pd.Series({**{f"q{int(i)}": m[i] for i in m.index}, "n": n.sum(),
                             "t_q0": m.iloc[0] / (s.iloc[0] / np.sqrt(n.iloc[0])), "t_q4": m.iloc[-1] / (s.iloc[-1] / np.sqrt(n.iloc[-1]))})
    out["grid_unusual10_by_quintile_long"] = pd.DataFrame(res2).T
    # quintile edges
    out["edges"] = act[["ret20v", "dd60v", "ret90", "volratio"]].quantile([0.2, 0.4, 0.6, 0.8])
    # worst days of book: features of long bars
    worst = act.nsmallest(int(len(act) * 0.05), "gain")
    out["worst5pct_bars_medians"] = pd.DataFrame({"worst": worst[["ret20v", "dd60v", "ret90", "volratio", "alloc"]].median(),
                                                  "all": act[["ret20v", "dd60v", "ret90", "volratio", "alloc"]].median()})
    return out
