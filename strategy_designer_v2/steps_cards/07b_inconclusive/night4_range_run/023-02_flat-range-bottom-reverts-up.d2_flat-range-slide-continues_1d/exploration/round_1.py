import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"]; l = df["low"]
            hh = h.rolling(30).max(); ll = l.rolling(30).min()
            net = (df["close"] - df["close"].shift(29)).abs()
            ratio = net / (hh - ll)
            mid = (hh + ll) / 2
            ret10 = df["close"].pct_change(10)
            year = pd.to_datetime(df["timestamp"]).dt.year
            n = len(df)
            for H in (5, 10, 20):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, win=w, H=H, i=i, year=year.iloc[i],
                                     regime=df["regime"].iloc[i], fc=df["forecast"].iloc[i],
                                     ratio=ratio.iloc[i], below=c[i] < mid.iloc[i] if pd.notna(mid.iloc[i]) else np.nan,
                                     ret10=ret10.iloc[i], fwd=c[i+H]/c[i]-1))
    g = pd.DataFrame(rows)
    drift = g.groupby(["coin","H"])["fwd"].mean().rename("drift")
    g = g.join(drift, on=["coin","H"]); g["ex"] = g["fwd"] - g["drift"]
    out = {}
    def slope(d, x="fc"):
        d = d.dropna(subset=[x,"ex"])
        if len(d) < 10 or d[x].std()==0: return (np.nan, np.nan, len(d))
        r = stats.linregress(d[x], d["ex"]); return (r.slope, r.slope/r.stderr, len(d))
    # by horizon, regime bars
    res = []
    for H in (5,10,20):
        d = g[(g.H==H)&(g.regime=="mean_reversion")]
        s = slope(d); neg = d[d.fc<0]; zero = d[d.fc==0]
        s2 = slope(neg)
        res.append(dict(H=H, slope_t=s[1], n=s[2], slope_t_neg_only=s2[1], n_neg=s2[2],
                        ex_neg=neg.ex.mean(), ex_zero=zero.ex.mean(), n_zero=len(zero),
                        t_neg_vs_zero=stats.ttest_ind(neg.ex.dropna(), zero.ex.dropna(), equal_var=False).statistic))
    out["by_horizon_regime"] = pd.DataFrame(res)
    d5 = g[(g.H==5)&(g.regime=="mean_reversion")].copy()
    d5["bucket"] = pd.cut(d5.fc, [-21,-8,-5,-3,-2,-1,-1e-9,0.5])
    out["fc_buckets_5d"] = d5.groupby("bucket").ex.agg(["mean","count","std"]).assign(t=lambda x: x["mean"]/(x["std"]/np.sqrt(x["count"])))
    for H in (10,20):
        dh = g[(g.H==H)&(g.regime=="mean_reversion")].copy()
        dh["bucket"] = pd.cut(dh.fc, [-21,-5,-2,-1e-9,0.5])
        out[f"fc_buckets_{H}d"] = dh.groupby("bucket").ex.agg(["mean","count"])
    out["by_coin_5d"] = d5.groupby("coin").apply(lambda x: pd.Series(dict(zip(["slope","t","n"], slope(x))) | {"ex_neg": x[x.fc<0].ex.mean(), "ex_zero": x[x.fc==0].ex.mean()}))
    out["by_year_5d"] = d5.groupby("year").apply(lambda x: pd.Series(dict(zip(["slope","t","n"], slope(x))) | {"ex_neg": x[x.fc<0].ex.mean()}))
    # raw 10d return as driver, all situations
    a5 = g[g.H==5].dropna(subset=["ratio","below","ret10"]).copy()
    a5["flat"] = a5.ratio <= 0.5
    res=[]
    for (fl, bl), x in a5.groupby(["flat","below"]):
        s = slope(x, "ret10"); res.append(dict(flat=fl, below=bl, slope=s[0], t=s[1], n=s[2], ex=x.ex.mean()))
    out["ret10_slope_by_situation_5d"] = pd.DataFrame(res)
    return out
