def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    recs = []; grid = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            r1 = b["close"].shift(-1)/b["close"]-1
            a = b["postRebalance_current_allocation"]
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            rise = b["close"]/b["close"].shift(72)-1
            v = b["volume"]
            ev = v.rolling(72).median()/v.rolling(72).mean()
            evz = (ev-ev.rolling(72,min_periods=20).mean())/ev.rolling(72,min_periods=20).std()
            f72 = b["close"].shift(-72)/b["close"]-1
            chg = (a-b["previous_allocation"]).abs()
            df = pd.DataFrame({"coin": c, "w": w, "a": a, "r1": r1, "g": a*r1, "fee": fee, "chg": chg,
                               "rise": rise, "ev": ev, "evz": evz, "reg": b["regime"], "f72": f72})
            recs.append(df); grid.append(df.iloc[::72])
    R = pd.concat(recs); G = pd.concat(grid)
    cm72 = G.groupby("coin")["f72"].mean()
    G["ex"] = G["f72"]-G["coin"].map(cm72)
    def tt(x): return pd.Series({"mean_ex": x.mean(), "t": x.mean()/x.std()*np.sqrt(len(x)), "n": len(x)})
    # fees: share of total fee by rise bins (incl non-trending)
    R2 = R.dropna(subset=["rise"]).copy()
    bins = [-10,-0.02,-0.005,0,0.005,0.02,0.05,10]
    R2["rb"] = pd.cut(R2["rise"], bins)
    out["fee_by_rise_bin"] = R2.groupby("rb").agg(fee_share=("fee", lambda x: x.sum()/R2["fee"].sum()),
        gain_share=("g", lambda x: x.sum()/R2["g"].sum()), turnover=("chg","mean"), n=("fee","size"))
    # grid: all rises (trending) ex72 by raw evenness tercile and by rise tercile x evenness
    GT = G[G.reg=="trending"].dropna(subset=["ex","ev","rise"]).copy()
    GT["eq"] = pd.qcut(GT["ev"], 3, labels=False)
    GT["rq"] = pd.qcut(GT["rise"], 3, labels=False)
    out["ex72_by_raw_even_t"] = GT.groupby("eq")["ex"].apply(tt).unstack()
    out["ex72_rise_x_even"] = GT.groupby(["rq","eq"])["ex"].apply(tt).unstack()
    # rise strength graded: rise / own 72h vol
    out["corr_rise_ex"] = pd.Series({"spearman_rise": GT["rise"].corr(GT["ex"], method="spearman"),
        "spearman_ev": GT["ev"].corr(GT["ex"], method="spearman"),
        "spearman_evz": GT["evz"].corr(GT["ex"], method="spearman")})
    # down moves: non-trending grid ex72 by fall size
    GN = G[(G.reg!="trending")].dropna(subset=["ex","rise"]).copy()
    GN["rq"] = pd.qcut(GN["rise"], 3, labels=False)
    out["nontrend_ex72_by_fall"] = GN.groupby("rq")["ex"].apply(tt).unstack()
    # hypothetical: gross per bar if position only when rise top 40%
    T = R[(R.reg=="trending")].dropna(subset=["rise","g"])
    thr = T["rise"].quantile(0.6)
    out["gain_split"] = pd.Series({"gross_top40": T.loc[T.rise>thr,"g"].sum(), "fee_top40": T.loc[T.rise>thr,"fee"].sum(),
        "gross_rest": T.loc[T.rise<=thr,"g"].sum(), "fee_rest": T.loc[T.rise<=thr,"fee"].sum(),
        "fee_nontrend": R.loc[R.reg!="trending","fee"].sum()})
    return out
