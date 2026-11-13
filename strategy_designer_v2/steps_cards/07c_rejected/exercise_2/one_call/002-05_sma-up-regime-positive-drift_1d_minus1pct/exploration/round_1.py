def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    allin, allout = [], []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            r = b["close"].pct_change().shift(-1)
            f = b["forecast"]
            raw = b["debug_info.components.sma_cross_spread.last_history_value"]
            ins = r[f > 0].dropna(); ots = r[f == 0].dropna()
            allin.append(pd.DataFrame({"r": ins, "f": f[ins.index], "raw": raw[ins.index], "w": w,
                                       "intra": (b["close"]/b["open"]-1).shift(-1)[ins.index],
                                       "gap": (b["open"].shift(-1)/b["close"]-1)[ins.index]}))
            allout.append(pd.DataFrame({"r": ots, "raw": raw[ots.index], "w": w,
                                        "intra": (b["close"]/b["open"]-1).shift(-1)[ots.index],
                                        "gap": (b["open"].shift(-1)/b["close"]-1)[ots.index]}))
            rows.append({"w": w, "n_in": len(ins), "n_out": len(ots),
                         "mean_in": ins.mean(), "mean_out": ots.mean(),
                         "up_in": (ins > 0).mean(), "up_out": (ots > 0).mean(),
                         "med_in": ins.median(), "med_out": ots.median(),
                         "sd_in": ins.std(), "sd_out": ots.std(),
                         "win_ret": b["close"].iloc[-1]/b["close"].iloc[0]-1,
                         "share_raw_pos": (raw > 0).mean()})
    out["per_window"] = pd.DataFrame(rows)
    I = pd.concat(allin); O = pd.concat(allout)
    I["fq"] = pd.qcut(I["f"].rank(method="first"), 4, labels=False)
    out["in_by_forecast_q"] = I.groupby("fq").agg(n=("r","size"), f=("f","mean"), mean=("r","mean"), up=("r", lambda x:(x>0).mean()))
    out["out_raw_pos_vs_neg"] = O.groupby(O["raw"] > 0).agg(n=("r","size"), mean=("r","mean"), up=("r", lambda x:(x>0).mean()))
    out["gap_intra"] = pd.DataFrame({"in": [I["gap"].mean(), I["intra"].mean()], "out": [O["gap"].mean(), O["intra"].mean()]}, index=["gap","intra"])
    out["in_ret_dist"] = I["r"].describe()
    out["in_ret_hist"] = pd.cut(I["r"], [-1,-0.05,-0.02,-0.01,0,0.01,0.02,0.05,1]).value_counts().sort_index()
    out["out_ret_hist"] = pd.cut(O["r"], [-1,-0.05,-0.02,-0.01,0,0.01,0.02,0.05,1]).value_counts().sort_index()
    return out
