import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    recs = []
    gridrecs = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            c = b["close"].reset_index(drop=True)
            n = len(c)
            for k in range(0, n-10, 10):
                gridrecs.append(dict(coin=coin, f10=c.iloc[k+10]/c.iloc[k]-1))
            prior_min = c.shift(1).rolling(30, min_periods=30).min()
            newlow = c < prior_min
            r30 = c/c.shift(30)-1
            r14 = c/c.shift(14)-1
            fwd = {h: c.shift(-h)/c-1 for h in [1,2,3,5,10,20]}
            fc = b["forecast"].reset_index(drop=True)
            al = b["postRebalance_current_allocation"].reset_index(drop=True)
            last = -999
            for i in range(n):
                if newlow.iloc[i] and not np.isnan(fwd[10].iloc[i]) and i-last > 10:
                    d = dict(coin=coin, w=w, fc=fc.iloc[i], al=al.iloc[i], r30=r30.iloc[i], r14=r14.iloc[i])
                    for h in fwd: d["f%d"%h] = fwd[h].iloc[i]
                    # how many bars position stays on after signal
                    j = i
                    while j < n and abs(al.iloc[j]) > 1e-6: j += 1
                    d["held_bars"] = j - i
                    recs.append(d); last = i
    G = pd.DataFrame(gridrecs)
    cm = G.groupby("coin").f10.mean()
    out["coin_mean_10"] = cm
    R = pd.DataFrame(recs)
    R["div"] = R.fc > 0
    R["ex10"] = R.f10 - R.coin.map(cm)
    def t(x): 
        x = x.dropna(); return stats.ttest_1samp(x,0).statistic if len(x)>2 else np.nan
    rows = []
    for dv, g in R.groupby("div"):
        for h in [1,2,3,5,10,20]:
            rows.append(dict(div=dv, h_days=h, n=g["f%d"%h].notna().sum(), mean=g["f%d"%h].mean(), t=t(g["f%d"%h])))
    out["fwd_by_horizon"] = pd.DataFrame(rows)
    Dv = R[R["div"]]
    out["div_held_bars"] = Dv.held_bars.describe()
    out["div_fc_vs_f10"] = pd.DataFrame({"spearman":[stats.spearmanr(Dv.fc, Dv.ex10).correlation],
                                          "pearson":[stats.pearsonr(Dv.fc, Dv.ex10)[0]], "n":[len(Dv)]})
    # grading by r30 within divergence cases
    out["div_r30_corr"] = pd.DataFrame({"spearman_r30_f10":[stats.spearmanr(Dv.r30, Dv.f10).correlation],
                                         "spearman_r14_f10":[stats.spearmanr(Dv.r14, Dv.f10).correlation]})
    Dv2 = Dv.assign(q=pd.qcut(Dv.r30, 3, labels=["deep","mid","shallow"]))
    out["div_by_r30_tercile"] = Dv2.groupby("q").agg(n=("f10","size"), r30=("r30","mean"), f10=("f10","mean"),
        ex10=("ex10","mean"), t_ex10=("ex10", t), f1=("f1","mean"))
    # all new lows: graded by r30
    R2 = R.assign(q=pd.qcut(R.r30, 3, labels=["deep","mid","shallow"]))
    out["all_newlow_by_r30"] = R2.groupby("q").agg(n=("f10","size"), r30=("r30","mean"), ex10=("ex10","mean"), t=("ex10", t))
    out["all_spearman_r30_ex10"] = stats.spearmanr(R.r30, R.ex10).correlation
    out["div_by_coin"] = Dv.groupby("coin").agg(n=("f10","size"), ex10=("ex10","mean"), t=("ex10", t), f1=("f1","mean"))
    return out
