def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    coins = list(data["bars"].keys())
    # daily book
    rows = []
    for c in coins:
        allb = []; allc = []
        for w, d in data["days"][c].items():
            allb.append(d["book_return"].dropna()); allc.append(d["coin_return"].dropna())
        b = pd.concat(allb); cr = pd.concat(allc)
        rows.append({"coin": c, "book_mean": b.mean(), "book_sharpe": b.mean()/b.std()*np.sqrt(365),
                     "coin_mean": cr.mean(), "coin_sharpe": cr.mean()/cr.std()*np.sqrt(365)})
    out["per_coin_daily"] = pd.DataFrame(rows).set_index("coin")
    # per-bar gain decomposition, gross
    recs = []
    grid = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            r1 = b["close"].shift(-1)/b["close"]-1
            a = b["postRebalance_current_allocation"]
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            rise = b["close"]/b["close"].shift(72)-1
            f72 = b["close"].shift(-72)/b["close"]-1
            df = pd.DataFrame({"coin": c, "w": w, "a": a, "r1": r1, "g": a*r1, "fee": fee,
                               "rise": rise, "fc": b["forecast"], "reg": b["regime"], "f72": f72})
            recs.append(df)
            grid.append(df.iloc[::72])
    R = pd.concat(recs); G = pd.concat(grid)
    cm = R.groupby("coin")["r1"].mean()
    R["mkt"] = R["a"]*R["coin"].map(cm)
    out["decomp_per_bar"] = pd.Series({"gross_mean": R["g"].mean(), "fee_mean": R["fee"].mean(),
        "mkt_part": R["mkt"].mean(), "timing": R["g"].mean()-R["mkt"].mean(),
        "share_bars_long": (R["a"]>0).mean(), "mean_alloc_when_long": R.loc[R.a>0,"a"].mean()})
    # by rise size quintile among trending
    T = R[R.reg=="trending"].dropna(subset=["rise","g"])
    T["rq"] = pd.qcut(T["rise"], 5, labels=False)
    out["trend_bar_by_rise_q"] = T.groupby("rq").agg(rise=("rise","mean"), gain=("g","mean"),
        r1=("r1","mean"), fee=("fee","mean"), n=("g","size"))
    # grid forward 72 by rise quintile, excess over coin mean
    cm72 = G.groupby("coin")["f72"].mean()
    G["ex"] = G["f72"]-G["coin"].map(cm72)
    GT = G[(G.reg=="trending")].dropna(subset=["ex","rise"])
    GT["rq"] = pd.qcut(GT["rise"], 5, labels=False)
    def tt(x): return pd.Series({"mean_ex": x.mean(), "t": x.mean()/x.std()*np.sqrt(len(x)), "n": len(x)})
    out["grid_trend_ex72_by_rise_q"] = GT.groupby("rq")["ex"].apply(tt).unstack()
    GN = G[(G.reg!="trending")].dropna(subset=["ex"])
    out["grid_nontrend_ex72"] = tt(GN["ex"])
    out["grid_trend_ex72"] = tt(GT["ex"])
    # gross gain by forecast tercile
    T2 = R[(R.reg=="trending")&(R.fc>0)].dropna(subset=["g"])
    T2["fq"] = pd.qcut(T2["fc"], 3, labels=False)
    out["gain_by_fc_tercile"] = T2.groupby("fq").agg(fc=("fc","mean"), gain=("g","mean"), r1=("r1","mean"), a=("a","mean"), fee=("fee","mean"))
    # by year
    R2 = []
    for c in coins:
        for w, b in data["bars"][c].items():
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            R2.append(pd.DataFrame({"yr": yr}))
    R["yr"] = pd.concat(R2)["yr"].values
    out["by_year"] = R.groupby("yr").agg(gain=("g","mean"), fee=("fee","mean"), mkt=("mkt","mean"), r1=("r1","mean"))
    tr = pd.concat([t for c in coins for t in data["trades"][c].values()])
    out["trades"] = pd.Series({"n": len(tr), "mean_pl": tr["profit_loss_percent"].mean(),
        "mean_net": tr["net_profit_loss_percent"].mean(), "mean_dur_h": tr["duration_minutes"].mean()/60,
        "win": (tr["net_profit_loss_percent"]>0).mean()})
    return out
