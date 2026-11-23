def explore(data):
    import numpy as np, pandas as pd
    out = {}
    drift = {}
    for c, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            g = b.sort_values("timestamp")["close"].values[::3]; allr += list(g[1:]/g[:-1]-1)
        drift[c] = np.mean(allr)
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            r1 = b["close"].pct_change()
            mad = r1.abs().rolling(60, min_periods=20).mean()
            fwd = b["close"].shift(-3)/b["close"]-1
            ret20 = b["close"]/b["close"].shift(20)-1
            ret60 = b["close"]/b["close"].shift(60)-1
            # path min over next 3 bars
            lowf = pd.concat([b["low"].shift(-k) for k in (1,2,3)], axis=1).min(axis=1)/b["close"]-1
            prev2 = b["close"].shift(1)/b["close"].shift(3)-1  # Fri->Sat? two bars before Sunday
            df = pd.DataFrame({"coin": c, "wn": int(w[1:]), "dow": ts.dt.dayofweek, "fc": b["forecast"],
                               "al": b["postRebalance_current_allocation"], "r1": r1, "z": r1/mad, "fwd": fwd,
                               "lowf": lowf, "ret20": ret20, "ret60": ret60, "prev2": prev2, "year": ts.dt.year})
            rows.append(df)
    A = pd.concat(rows).dropna(subset=["fwd", "z", "ret20"])
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    A["pnl"] = A["al"] * A["fwd"]
    S = A[(A.dow == 6) & (A.fc > 0)].copy()
    S["zb"] = pd.cut(-S.z, [0, 0.5, 1, 1.5, 2, 2.5, 3, 20])
    def summ(g):
        return pd.Series({"n": len(g), "fc": g.fc.mean(), "al": g.al.mean(), "ex": g.ex.mean(),
                          "t": g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "pnl_sum": g.pnl.sum(), "pnl_neg_sum": g.pnl[g.pnl < 0].sum(), "lowf": g.lowf.mean()})
    out["sun_by_zbin"] = S.groupby("zb").apply(summ).round(4)
    # condition alone: weekday falls by z bin (not Sunday)
    W = A[(A.dow != 6) & (A.dow != 5) & (A.z < 0)].copy()
    W = W[W.index % 3 == 0]  # crude thinning
    W["zb"] = pd.cut(-W.z, [0, 1, 2, 3, 20])
    out["weekday_fall_by_zbin"] = W.groupby("zb").apply(lambda g: pd.Series({"n": len(g), "ex": g.ex.mean(), "t": g.ex.mean()/(g.ex.std()/np.sqrt(len(g)))})).round(4)
    # Sunday falls in deep-loss: ret20 quartile x zbin
    S["q20"] = pd.qcut(S.ret20, 4, labels=False)
    S["zb2"] = pd.cut(-S.z, [0, 2, 20])
    out["sun_q20_x_z"] = S.groupby(["q20", "zb2"]).apply(lambda g: pd.Series({"n": len(g), "ex": g.ex.mean(), "pnl_sum": g.pnl.sum()})).round(4)
    out["ret20_quart_edges"] = pd.Series(S.ret20.quantile([0.25, .5, .75]).values).round(3)
    # pnl by window block
    S["blk"] = pd.cut(S.wn, [0, 2, 10, 17, 24])
    out["pnl_by_block"] = S.groupby("blk").apply(summ).round(4)
    out["pnl_by_block_bigz"] = S[-S.z > 2].groupby("blk").apply(summ).round(4)
    # alternative weights: cap z at 2 vs actual, case-level pseudo sharpe
    S["w_cap"] = np.minimum(-S.z, 2) * (-S.z <= 2)
    for nm, wt in [("actual_al", S.al), ("z_upto2_only", S.w_cap * S.al / S.fc.replace(0, np.nan)), ("flat_al", S.al.where(-S.z <= 2, 0))]:
        p = wt.fillna(0) * S.fwd
        out["alt_" + nm] = pd.Series({"sum": p.sum(), "mean": p.mean(), "sd": p.std(), "worst5_sum": p.nsmallest(20).sum()}).round(4)
    # worst 20 case pnls: their z, ret20, lowf
    out["worst20_cases"] = S.nsmallest(20, "pnl")[["wn", "z", "fc", "al", "fwd", "ret20", "ret60"]].round(3).reset_index(drop=True)
    # Sunday fall z>2 : prev2 (Fri-Sun prior) and ret60 means vs z<=2
    out["bigz_vs_small_context"] = S.groupby(-S.z > 2)[["ret20", "ret60", "prev2", "lowf", "al"]].mean().round(4)
    return out
