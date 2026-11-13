def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            r = cl.pct_change()
            v = b["postRebalance_total_value"].astype(float)
            br = v.pct_change()
            a = b["postRebalance_current_allocation"].astype(float).fillna(0)
            ap = a.shift(1)
            ma50 = cl.rolling(50).mean()
            mom20 = cl.pct_change(20)
            vol = r.abs().rolling(20).mean()
            volq = vol.rank(pct=True)
            d = pd.DataFrame({"coin": c, "win": w, "year": pd.to_datetime(b["timestamp"]).dt.year,
                              "r": r, "br": br, "ap": ap, "gross": ap * r,
                              "turn": (a - ap).abs(),
                              "above": (cl.shift(1) > ma50.shift(1)),
                              "mom": np.where(mom20.shift(1) > 0, "up20", "down20"),
                              "vol": vol.shift(1)})
            rows.append(d.iloc[1:])
    D = pd.concat(rows, ignore_index=True)
    D["fee"] = D["gross"] - D["br"]
    D["volq"] = D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=["low", "mid", "high"]))
    def agg(g):
        return pd.Series({"bars": len(g), "exposure": g["ap"].mean(), "inmkt": (g["ap"].abs() > 0.01).mean(),
                          "gross_mean": g["gross"].mean(), "net_mean": g["br"].mean(),
                          "fee_mean": g["fee"].mean(), "turn_mean": g["turn"].mean(),
                          "coin_mean": g["r"].mean(),
                          "gross_per_exposed": g["gross"].sum() / max(g["ap"].sum(), 1e-9)})
    out["book_all"] = agg(D).to_frame().T
    out["book_by_year"] = D.groupby("year").apply(agg)
    out["book_by_coin"] = D.groupby("coin").apply(agg)
    out["book_by_ma50"] = D.groupby("above").apply(agg)
    out["book_by_mom"] = D.groupby("mom").apply(agg)
    out["book_by_vol"] = D.groupby("volq").apply(agg)
    D["mkt"] = np.where(D["r"] > 0, "coin_up", "coin_down")
    out["book_by_mktday"] = D.groupby("mkt").apply(agg)
    D["apb"] = pd.cut(D["ap"], [-0.01, 0.01, 0.25, 0.5, 0.75, 1.01, 10])
    out["book_by_alloc"] = D.groupby("apb").apply(agg)
    # holding days after signal: gross by days since last forecast>=10 bar not available; use alloc path
    out["alloc_desc"] = D["ap"].describe()
    return out
