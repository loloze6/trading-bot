def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            n = len(cl)
            prior_low = cl.shift(1).rolling(30, min_periods=30).min()
            newlow = cl < prior_low
            # Wilder RSI
            d = cl.diff()
            up = d.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
            dn = (-d.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
            rsi = 100 - 100/(1+up/dn)
            ret30 = cl/cl.shift(30)-1
            fwd = {h: cl.shift(-h)/cl-1 for h in [1,3,5,10,20]}
            for kind in ["div","nodiv"]:
                last = -999
                for i in range(34, n):
                    if not newlow.iloc[i]:
                        continue
                    seg = cl.iloc[i-30:i-3]
                    j = seg.idxmin()
                    isdiv = rsi.iloc[i] > rsi.iloc[j]
                    if (kind == "div") != bool(isdiv):
                        continue
                    if i - last >= 20:
                        last = i
                        rows.append(dict(coin=c, kind=kind, ret30=ret30.iloc[i], fc=b["forecast"].iloc[i],
                                         pos=b["postRebalance_current_allocation"].iloc[i],
                                         **{f"f{h}": fwd[h].iloc[i] for h in fwd}))
    E = pd.DataFrame(rows)
    out["fwd_by_kind"] = E.groupby("kind")[["f1","f3","f5","f10","f20"]].agg(["mean","count"]).round(4)
    tt = {}
    for h in ["f1","f3","f5","f10","f20"]:
        a = E.loc[E.kind=="div", h].dropna(); bb = E.loc[E.kind=="nodiv", h].dropna()
        tt[h] = (stats.ttest_1samp(a,0).statistic, stats.ttest_ind(a,bb,equal_var=False).statistic)
    out["t_div_mean_and_div_minus_nodiv"] = pd.DataFrame(tt, index=["t_div","t_diff"]).T.round(2)
    E["q30"] = E.groupby("kind")["ret30"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["fwd_by_kind_depth"] = E.groupby(["kind","q30"])[["ret30","f3","f5","f10","f20"]].mean().round(4)
    out["n_kind_depth"] = E.groupby(["kind","q30"]).size()
    out["corr_ret30_f5_div"] = E.loc[E.kind=="div",["ret30","f5","f10"]].corr().iloc[0]
    # short-bar gains: run length and fees
    runs = []; fees = []; gains=[]
    for c in bars:
        for w, b in bars[c].items():
            p = b["postRebalance_current_allocation"].values
            s = (p < 0).astype(int)
            k=0
            for v in s:
                if v: k+=1
                elif k: runs.append(k); k=0
            if k: runs.append(k)
            fees.append((b["total_portfolio_value"]-b["postRebalance_total_value"]).sum()/b["total_portfolio_value"].iloc[0])
            cl=b["close"]; gains.append((p*(cl.shift(-1)/cl-1)).sum())
    out["short_runs"] = pd.Series(runs).describe()
    out["fee_vs_gain_total"] = pd.Series({"sum_fee_frac": np.sum(fees), "sum_gross_gain": np.nansum(gains)})
    return out
