import pandas as pd, numpy as np
from scipy import stats

def tstat(x):
    x = pd.Series(x).dropna()
    return x.mean()/x.std()*np.sqrt(len(x)) if len(x) > 2 else np.nan

def explore(data):
    bars, trades, days = data["bars"], data["trades"], data["days"]
    out = {}
    cs = []
    for c in bars:
        allr = []
        for w, b in bars[c].items():
            cl = b["close"].values
            for i in range(0, len(b)-5, 5):
                allr.append(cl[i+5]/cl[i]-1)
        drift = np.mean(allr)
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; hi = b["high"]; lo = b["low"]
            f = b["forecast"].values
            r30 = cl/cl.shift(30)-1
            r60 = cl/cl.shift(60)-1
            r5 = cl/cl.shift(5)-1
            lr = np.log(cl).diff()
            vol30 = lr.rolling(30).std()
            vol90r = vol30 / lr.rolling(60).std()
            pos = (cl - lo.rolling(30).min())/(hi.rolling(30).max()-lo.rolling(30).min())
            for i in range(0, len(b)-5, 5):
                if f[i] < 0:
                    fwd = cl[i+5]/cl[i]-1
                    cs.append((c, f[i], -fwd, -(fwd-drift), r30[i], r60[i], r5[i], vol30[i], vol90r[i], pos[i], drift))
    C = pd.DataFrame(cs, columns=["coin","f","tot","unus","r30","r60","r5","vol30","volratio","pos","drift"])
    def grp(col, q=4):
        g = pd.qcut(C[col], q, duplicates="drop")
        return C.groupby(g, observed=True).agg(n=("tot","size"), total=("tot","mean"), unusual=("unus","mean"),
                                               t_total=("tot", tstat), t_unus=("unus", tstat))
    for col in ["r60","r5","vol30","volratio","pos"]:
        out["grid_by_"+col] = grp(col)
    C["r30_t"] = pd.qcut(C.r30, 3, labels=["deep","mid","shallow"])
    C["f_h"] = np.where(C.f <= C.f.median(), "strong", "weak")
    out["r30_x_force"] = C.groupby(["r30_t","f_h"], observed=True).agg(n=("tot","size"), total=("tot","mean"), t_total=("tot", tstat))
    out["by_coin"] = C.groupby("coin").agg(n=("tot","size"), drift=("drift","first"), total=("tot","mean"), unusual=("unus","mean"))
    # trades distribution
    T = pd.concat([t for c in trades for t in trades[c].values() if len(t)])
    p = T.profit_loss_percent
    out["trade_pnl_dist"] = pd.Series({"mean": p.mean(), "median": p.median(), "p05": p.quantile(.05), "p95": p.quantile(.95),
        "share_loss_gt10": (p < -10).mean(), "share_gain_gt10": (p > 10).mean(),
        "mean_wo_worst5pct": p[p > p.quantile(.05)].mean(), "mean_commission": T.total_commission.mean()})
    # book daily returns: worst days contribution
    D = pd.concat([d.assign(coin=c) for c in days for d in days[c].values()]).dropna(subset=["book_return"])
    br = D.book_return
    out["book_tail"] = pd.Series({"mean": br.mean(), "sum_worst1pct_share_of_total": br[br < br.quantile(.01)].sum()/br.sum(),
        "mean_coinret_on_worst1pct_bookdays": D.coin_return[br < br.quantile(.01)].mean(),
        "corr_book_coin": D[["book_return","coin_return"]].corr().iloc[0,1]})
    return out
