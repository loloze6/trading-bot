def explore(data):
    import numpy as np, pandas as pd
    out = {}
    cases = []; barrows = []
    for c, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            cl = b["close"].values
            if len(cl) > 48: allr.append(cl[24::24] / cl[:-24:24] - 1)
        allr = np.concatenate(allr); drift = allr.mean()
        for w, b in ws.items():
            wn = int(w[1:])
            cl = b["close"].astype(float).reset_index(drop=True); n = len(cl)
            r24b = cl / cl.shift(24) - 1
            absmean = r24b.abs().rolling(720, min_periods=120).mean().shift(1)
            mult = -r24b / absmean
            vr = r24b.abs().rolling(168).mean() / absmean
            r7d = cl / cl.shift(168) - 1
            fwd1 = cl.shift(-1) / cl - 1
            pos = b["postRebalance_current_allocation"].astype(float).reset_index(drop=True)
            pv = b["postRebalance_total_value"].astype(float).reset_index(drop=True)
            tv = b["total_portfolio_value"].astype(float).reset_index(drop=True)
            fee = (tv - pv) / tv
            barrows.append(pd.DataFrame({"coin": c, "wn": wn, "pos": pos, "fwd1": fwd1, "vr": vr, "fee": fee,
                                         "r7d": r7d}))
            f24 = cl.shift(-24) / cl - 1
            fc = b["forecast"].astype(float).reset_index(drop=True)
            for s in range(0, n, 24):
                seg = fc.iloc[s:min(s + 24, n)]
                hit = seg[seg >= 2]
                if len(hit) == 0: continue
                t = hit.index[0]
                cases.append(dict(coin=c, wn=wn, mult=mult.iloc[t], vr=vr.iloc[t], r7d=r7d.iloc[t],
                                  ex24=f24.iloc[t] - drift, tot24=f24.iloc[t]))
    C = pd.DataFrame(cases).dropna()
    def summ(g):
        x = g["ex24"]
        return pd.Series({"n": len(x), "ex24": x.mean(), "t24": x.mean() / x.std() * np.sqrt(len(x)),
                          "tot24": g["tot24"].mean()})
    C["vrb"] = pd.qcut(C["vr"], 4, labels=["calm", "q2", "q3", "turb"])
    C["mb"] = pd.cut(C["mult"], [0, 1.5, 3, 100], labels=["<1.5", "1.5-3", ">3"])
    out["vr_x_mult"] = C.groupby(["vrb", "mb"], observed=True).apply(summ).round(4)
    C["fall"] = C["wn"].between(13, 16)
    out["fall_vs_rest_by_vr"] = C.groupby(["fall", "vrb"], observed=True).apply(summ).round(4)
    C["vr_x_mult"] = C["vr"] * C["mult"]
    C["vxm_b"] = pd.qcut(C["vr_x_mult"], 5)
    out["by_vr_times_mult"] = C.groupby("vxm_b", observed=True).apply(summ).round(4)
    B = pd.concat(barrows).dropna()
    B["g"] = B["pos"] * B["fwd1"]
    B["vrb"] = pd.qcut(B["vr"], 4, labels=["calm", "q2", "q3", "turb"])
    out["book_bars_by_vr"] = B.groupby("vrb", observed=True).apply(lambda g: pd.Series({
        "share_bars": len(g) / len(B), "mean_pos": g["pos"].mean(), "gain_sum": g["g"].sum(),
        "fee_sum": g["fee"].sum(), "net": g["g"].sum() - g["fee"].sum()})).round(4)
    B["fall"] = B["wn"].between(13, 16)
    out["book_bars_fall_by_vr"] = B[B["fall"]].groupby("vrb", observed=True).apply(lambda g: pd.Series({
        "share_bars": len(g) / B["fall"].sum(), "mean_pos": g["pos"].mean(), "gain_sum": g["g"].sum(),
        "fee_sum": g["fee"].sum()})).round(4)
    out["fees_total_vs_gain"] = pd.Series({"gain_sum": B["g"].sum(), "fee_sum": B["fee"].sum()})
    return out
