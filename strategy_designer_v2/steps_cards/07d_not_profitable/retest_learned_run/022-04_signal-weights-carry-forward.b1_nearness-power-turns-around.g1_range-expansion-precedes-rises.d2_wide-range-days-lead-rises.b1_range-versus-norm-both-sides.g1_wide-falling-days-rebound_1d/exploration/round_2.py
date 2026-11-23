import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    rows = []; grids = {h: [] for h in (1, 3, 5, 7, 10)}
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            b["nret"] = b["close"].shift(-1)/b["close"] - 1
            b["ret1"] = b["close"].pct_change()
            rng = (b["high"]-b["low"])/b["close"]
            b["rr"] = rng / rng.rolling(30, min_periods=20).mean()
            b["r30"] = b["close"]/b["close"].shift(30) - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["g"] = b["pos"]*b["nret"]
            b["coin"] = c; b["win"] = w
            for h in grids:
                bb = b.copy(); bb["fh"] = bb["close"].shift(-h)/bb["close"] - 1
                grids[h].append(bb.iloc[::h])
            rows.append(b)
    A = pd.concat(rows)
    out = {}
    hz = []
    for h, gl in grids.items():
        G = pd.concat(gl)
        G["ex"] = G["fh"] - G["coin"].map(G.groupby("coin")["fh"].mean())
        G["usual"] = G["coin"].map(G.groupby("coin")["fh"].std())
        F = G[(G["ret1"] < 0) & G["rr"].notna() & G["ex"].notna()]
        thr = F["rr"].quantile(0.8)
        top = F[F["rr"] >= thr]
        hz.append({"h": h, "n_top": len(top), "mean_ex": top["ex"].mean(),
                   "t": top["ex"].mean()/(top["ex"].std()/np.sqrt(len(top))),
                   "strength": (top["ex"]/top["usual"]).mean(),
                   "n_all_fall": len(F), "all_fall_ex": F["ex"].mean()})
        if h == 3:
            F = F.copy()
            F["rrd"] = pd.qcut(F["rr"], 10, labels=False)
            out["h3_fall_by_rr_decile"] = F.groupby("rrd").agg(n=("ex","size"), ex=("ex","mean"), rr=("rr","mean"))
            W = F[F["rr"] >= thr].copy()
            W["trend"] = np.where(W["r30"] > 0, "up30", "down30")
            out["h3_widefall_by_trend"] = W.groupby("trend")["ex"].agg(["count","mean"])
            G2 = G[G["ex"].notna()].copy()
            G2["trend"] = np.where(G2["r30"] > 0, "up30", "down30")
            out["h3_all_by_trend_alone"] = G2.groupby("trend")["ex"].agg(["count","mean"])
    out["horizon_top_quintile_widefall"] = pd.DataFrame(hz)
    # long-only and top-forecast-only gains, per bar in position
    A["inlong"] = A["pos"] > 0
    A["intop"] = (A["pos"] > 0) & (A["forecast"] > 2)
    out["gain_share"] = pd.Series({
        "all_mean_per_bar": A["g"].mean(),
        "long_only_mean_per_bar": A["g"].where(A["inlong"], 0).mean(),
        "long_share_bars": A["inlong"].mean(),
        "long_mean_when_in": A.loc[A["inlong"], "g"].mean(),
        "fc>2_mean_when_in": A.loc[A["intop"], "g"].mean(),
        "fc>2_share_bars": A["intop"].mean(),
        "abs_pos_long": A.loc[A["inlong"], "pos"].mean(),
        "abs_pos_short": A.loc[A["pos"] < 0, "pos"].abs().mean(),
    })
    # long-only book drawdown approx: daily mean over coins of long gains
    A["day"] = pd.to_datetime(A["timestamp"]).dt.floor("D")
    A["wn"] = A["win"].str[1:].astype(int)
    for nm, mask in (("all", A["pos"].notna()), ("long", A["inlong"]), ("fc>2", A["intop"])):
        gg = A["g"].where(mask, 0)
        bk = gg.groupby([A["wn"], A["day"]]).mean().sort_index()
        v = (1+bk).cumprod(); dd = (v/v.cummax()-1).min()
        yrs = len(bk)/365
        out["book_"+nm] = pd.Series({"mean": bk.mean(), "sharpe": bk.mean()/bk.std()*np.sqrt(365),
                                     "yearly": v.iloc[-1]**(1/yrs)-1, "maxdd": dd,
                                     "calmar": (v.iloc[-1]**(1/yrs)-1)/abs(dd)})
    return out
