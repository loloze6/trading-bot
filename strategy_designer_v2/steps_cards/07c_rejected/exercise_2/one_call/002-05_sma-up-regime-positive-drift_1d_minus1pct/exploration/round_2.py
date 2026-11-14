def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    I, O, T = [], [], []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            raw = b["debug_info.components.sma_cross_spread.last_history_value"]
            f = b["forecast"]
            gap = b["open"].shift(-1)/b["close"]-1
            intra = (b["close"]/b["open"]-1).shift(-1)
            d = pd.DataFrame({"gap": gap, "intra": intra, "f": f, "raw": raw, "w": w,
                              "hl": ((b["high"]-b["low"])/b["open"]).shift(-1)}).iloc[:-1]
            I.append(d[d.f > 0]); O.append(d[d.f == 0])
            # position within stretch
            pos = (raw > 0)
            run = (pos != pos.shift()).cumsum()
            age = pos.groupby(run).cumcount()
            d["age"] = age.iloc[:-1]
            T.append(d[d.f > 0])
    I = pd.concat(I); O = pd.concat(O); T = pd.concat(T)
    out["gap_desc"] = pd.DataFrame({"in": I["gap"].describe(), "out": O["gap"].describe()})
    out["gap_round"] = pd.DataFrame({"in_share_gap_near_-1pct": [((I.gap+0.01).abs() < 0.001).mean()],
                                     "out_share_gap_near_0": [(O.gap.abs() < 0.001).mean()],
                                     "in_share_gap_near_0": [(I.gap.abs() < 0.001).mean()]})
    out["intra_test"] = pd.DataFrame({"mean_in": [I.intra.mean()], "mean_out": [O.intra.mean()],
                                      "t": [stats.ttest_ind(I.intra, O.intra, equal_var=False).statistic],
                                      "up_in": [(I.intra > 0).mean()], "up_out": [(O.intra > 0).mean()],
                                      "hl_in": [I.hl.mean()], "hl_out": [O.hl.mean()]})
    out["gap_by_window"] = pd.concat([I.assign(s="in"), O.assign(s="out")]).groupby(["w", "s"]).agg(
        n=("gap", "size"), gap=("gap", "mean"), intra=("intra", "mean"))
    T["ageb"] = pd.cut(T["age"], [-1, 10, 30, 60, 120, 1000])
    out["in_by_age"] = T.groupby("ageb").agg(n=("gap", "size"), gap=("gap", "mean"), intra=("intra", "mean"))
    return out
