import pandas as pd, numpy as np

def explore(data):
    out = {}
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            ret = b["close"].pct_change()
            sd = ret.rolling(720, min_periods=200).std()
            vr = b["volume"] / b["volume"].rolling(720, min_periods=200).mean()
            d = pd.DataFrame({"z": ret/sd, "vr": vr, "coin": c, "win": w,
                              "year": pd.to_datetime(b["timestamp"]).dt.year,
                              "alloc": b["postRebalance_current_allocation"],
                              "dalloc": (b["postRebalance_current_allocation"]-b["previous_allocation"]).abs(),
                              "fee": (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"],
                              "g": b["postRebalance_current_allocation"]*(b["close"].shift(-1)/b["close"]-1),
                              "fc": b["forecast"]})
            for h in [2, 6, 24]:
                d[f"f{h}"] = b["close"].shift(-h)/b["close"]-1
            d["pos"] = np.arange(len(b))
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # grid-based falls by depth x volume, horizon h on its own grid
    res = []
    for h in [2, 6, 24]:
        G = D[D.pos % h == 0]
        drift = G.groupby("coin")[f"f{h}"].mean()
        sdv = G[f"f{h}"].std()
        F = G[(G.z < -2)].dropna(subset=["vr", f"f{h}"]).copy()
        F["zb"] = pd.cut(-F.z, [2, 3, 4, 6, 100]).astype(str)
        F["vb"] = np.where(F.vr > 3, "v>3", "v<=3")
        F["u"] = F[f"f{h}"] - F.coin.map(drift)
        for (zb, vb), g in F.groupby(["zb", "vb"]):
            res.append({"h": h, "zb": zb, "vb": vb, "n": len(g), "u_bp": g.u.mean()*1e4,
                        "t": g.u.mean()/g.u.std()*np.sqrt(len(g)) if len(g) > 2 else np.nan,
                        "strength": g.u.mean()/sdv})
    out["grid_falls"] = pd.DataFrame(res)
    # extreme falls by year, 2h and 24h on every bar (rare events)
    E = D[(D.z < -5) & (D.vr > 3)].copy()
    dr2 = D[D.pos % 2 == 0].groupby("coin")["f2"].mean(); dr24 = D[D.pos % 24 == 0].groupby("coin")["f24"].mean()
    E["u2"] = E.f2 - E.coin.map(dr2); E["u24"] = E.f24 - E.coin.map(dr24)
    out["extreme_by_year"] = E.groupby("year").agg(n=("u2", "size"), u2_bp=("u2", lambda x: x.mean()*1e4),
                                                   u24_bp=("u24", lambda x: x.mean()*1e4))
    # book gross and fee by forecast size
    A = D[D.fc > 0].copy()
    A["fb"] = pd.cut(A.fc, [0, 0.5, 2, 5, 10, 20.01]).astype(str)
    out["book_by_forecast"] = A.groupby("fb").agg(bars=("g", "size"), gross_bp=("g", lambda x: x.mean()*1e4),
                                                   fee_bp=("fee", lambda x: x.mean()*1e4), alloc=("alloc", "mean"))
    out["flat_bars_fee_bp"] = pd.Series({"bars_fc0": int((D.fc == 0).sum()),
                                         "fee_sum_share_on_fc0": D.loc[D.fc == 0, "fee"].sum()/D.fee.sum(),
                                         "gross_sum_share_fc_gt5": D.loc[D.fc > 5, "g"].sum()/D.g.sum()})
    return out
