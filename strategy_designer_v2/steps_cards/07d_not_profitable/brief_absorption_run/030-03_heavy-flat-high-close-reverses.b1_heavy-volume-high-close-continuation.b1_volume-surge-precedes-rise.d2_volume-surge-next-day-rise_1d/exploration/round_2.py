def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            b["nxt"] = c.shift(-1)/c - 1
            b["dayret"] = c/c.shift(1) - 1
            rng = (b["high"]-b["low"]).replace(0, np.nan)
            b["clv"] = (c - b["low"])/rng
            b["alloc"] = b["postRebalance_current_allocation"].fillna(0)
            b["coin"] = coin; b["wn"] = int(str(w).lstrip("w")); b["i"] = np.arange(len(b))
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    drift = B.dropna(subset=["nxt"]).groupby("coin")["nxt"].mean()
    B["ex"] = B["nxt"] - B["coin"].map(drift)
    cost_side = 0.0019/2
    def book(mask, name):
        X = B.copy()
        X["a"] = np.where(mask, X["alloc"], 0.0)
        X["chg"] = X.groupby(["coin","wn"])["a"].diff().abs().fillna(X["a"].abs())
        X["r"] = X["a"]*X["nxt"].fillna(0) - X["chg"]*cost_side
        bk = X.groupby(["wn","i"])["r"].mean().sort_index()
        v = (1+bk).cumprod(); dd = (v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(bk)) - 1
        loo = []
        for w in bk.index.get_level_values(0).unique():
            s = bk.drop(w, level=0); loo.append(s.mean()/s.std()*np.sqrt(365))
        inpos = (X["a"]!=0).mean()
        return pd.Series({"sharpe": bk.mean()/bk.std()*np.sqrt(365), "yearly%": yr*100,
                          "maxdd%": dd*100, "calmar": yr/abs(dd), "loo_min_sharpe": min(loo),
                          "share_in_pos": inpos, "mean_on_pos%": bk.mean()/inpos*100 if inpos>0 else np.nan})
    sig = B["forecast"] > 0
    down = B["dayret"] < 0
    low = B["clv"] < 0.5
    out["books"] = pd.DataFrame({
        "all": book(sig, "all"),
        "down_day": book(sig & down, "down"),
        "close_lower_half": book(sig & low, "low"),
        "down_and_low": book(sig & down & low, "dl"),
        "up_day_only": book(sig & ~down, "up")}).T
    # grading within signal & down: by size of the fall
    S = B[sig & down].dropna(subset=["nxt"]).copy()
    S["fallq"] = pd.qcut(S["dayret"], 3, labels=["big_fall","mid_fall","small_fall"])
    def summ(g):
        return pd.Series({"n": len(g), "mean_nxt%": g["nxt"].mean()*100, "mean_ex%": g["ex"].mean()*100,
                          "t_ex": g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g)))})
    out["sigdown_by_fall"] = S.groupby("fallq").apply(summ)
    S["fq"] = pd.qcut(S["forecast"], 3, labels=False, duplicates="drop")
    out["sigdown_by_forecast"] = S.groupby("fq").apply(summ)
    out["sigdown_by_year"] = S.groupby("year").apply(summ)
    # no-signal big falls: condition alone
    N = B[~sig & down].dropna(subset=["nxt"]).copy()
    N["fallq"] = pd.qcut(N["dayret"], 3, labels=["big_fall","mid_fall","small_fall"])
    out["nosig_down_by_fall"] = N.groupby("fallq").apply(summ)
    # in deepest fall windows 1-3: gain by up/down signal
    W = B[(B["wn"]<=3) & sig].dropna(subset=["nxt"]).copy()
    W["g"] = W["alloc"]*W["nxt"]
    out["w1_3_gain_by_dayside"] = W.groupby(down[W.index]).agg(n=("g","size"), mean_gain=("g","mean"), sum_gain=("g","sum"))
    return out
