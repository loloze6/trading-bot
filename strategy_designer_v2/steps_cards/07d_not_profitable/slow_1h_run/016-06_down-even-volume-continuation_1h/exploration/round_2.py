def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    rows = []; grid = []
    for c in bars:
        allr = []
        for w in bars[c]:
            allr.append(bars[c][w]["close"].iloc[::72].pct_change().shift(-1).dropna())
        cm72 = pd.concat(allr).mean()
        hm = pd.concat([bars[c][w]["close"].pct_change() for w in bars[c]]).mean()
        for w in bars[c]:
            b = bars[c][w].copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            a = b["postRebalance_current_allocation"]
            b["g"] = a * b["ret1"]
            b["timing"] = a * (b["ret1"] - hm)
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["turn"] = (a - b["previous_allocation"]).abs()
            b["past72"] = b["close"] / b["close"].shift(72) - 1
            vol = b["ret1"].shift(1).rolling(72).std()
            b["fallz"] = b["past72"] / (vol * np.sqrt(72))
            v = b["volume"]
            b["conc"] = np.log(v.rolling(72).mean() / v.rolling(72).median())
            b["fwd72"] = b["close"].shift(-72) / b["close"] - 1
            b["coin"] = c
            rows.append(b[["g", "timing", "fee", "turn", "past72", "fallz", "conc", "postRebalance_current_allocation"]])
            gg = b.iloc[::72].copy(); gg["exc"] = gg["fwd72"] - cm72
            grid.append(gg[["past72", "fallz", "conc", "exc"]])
    B = pd.concat(rows).dropna(subset=["past72", "fallz"])
    R = pd.concat(grid).dropna()
    A = B[B["postRebalance_current_allocation"] != 0].copy()
    A["fzq"] = pd.qcut(A["fallz"], 5, labels=False)
    out["active bars by vol-scaled fall quintile (0=deepest)"] = A.groupby("fzq").agg(n=("g", "size"), gain=("g", "mean"), timing=("timing", "mean"), fee=("fee", "mean"), turn=("turn", "mean"), alloc=("postRebalance_current_allocation", "mean"), fallz=("fallz", "mean"))
    out["share of fee bars with turnover"] = (B["turn"] > 0).mean()
    out["mean turnover per bar"] = B["turn"].mean()
    F = R[R["past72"] < 0].copy()
    F["fzq"] = pd.qcut(F["fallz"], 5, labels=False)
    def summ(x):
        return pd.Series({"n": len(x), "exc": x["exc"].mean(), "t": x["exc"].mean() / (x["exc"].std() / np.sqrt(len(x)))})
    out["fallen grid by vol-scaled fall quintile"] = F.groupby("fzq").apply(summ)
    S = F[F["fzq"] >= 2].copy()
    S["cq"] = pd.qcut(S["conc"], 3, labels=False)
    out["shallow falls (fzq>=2) by conc tercile (0=even)"] = S.groupby("cq").apply(summ)
    from scipy import stats
    sl = stats.linregress(S["fallz"], S["exc"])
    out["shallow: slope exc on fallz, t"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(S)})
    sl2 = stats.linregress(S["conc"], S["exc"])
    out["shallow: slope exc on conc, t"] = pd.Series({"slope": sl2.slope, "t": sl2.slope / sl2.stderr})
    return out
