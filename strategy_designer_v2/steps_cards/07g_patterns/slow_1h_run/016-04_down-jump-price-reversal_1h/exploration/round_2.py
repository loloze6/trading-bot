import numpy as np, pandas as pd
from scipy import stats

def mreg(X, y):
    X = np.column_stack([np.ones(len(y))] + list(X)); m = np.all(np.isfinite(X), 1) & np.isfinite(y)
    X, y = X[m], y[m]
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b; s2 = e @ e / (len(y) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    return list(np.round(b[1:], 5)) + list(np.round(b[1:] / se[1:], 2)) + [len(y)]

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []; g24 = []; hr = []
    for c in bars:
        for w, b in bars[c].items():
            wi = int(w[1:])
            cl = b["close"].values.astype(float); n = len(cl)
            lr = np.diff(np.log(cl), prepend=np.nan)
            for t in range(0, n, 72):
                if t < 72 or t + 72 >= n: continue
                h = lr[t-71:t+1]; net = np.log(cl[t]/cl[t-72])
                path = np.nansum(np.abs(h))
                rows.append(dict(coin=c, wi=wi, r72=cl[t]/cl[t-72]-1, eff=abs(net)/path if path > 0 else np.nan,
                                 vol=np.nanstd(h), fwd=cl[t+72]/cl[t]-1))
            for t in range(0, n, 24):
                if t < 168 or t + 24 >= n: continue
                s = np.nanstd(lr[t-167:t+1])
                g24.append(dict(coin=c, wi=wi, r24z=np.log(cl[t]/cl[t-24])/(s*np.sqrt(24)), last1=lr[t]/s,
                                vol=s, fwd24=cl[t+24]/cl[t]-1))
            ts = pd.to_datetime(b["timestamp"])
            hr.append(pd.DataFrame({"coin": c, "wi": wi, "hour": ts.dt.hour.values, "yr": ts.dt.year.values,
                                    "nxt": np.append(lr[1:], np.nan)}))
    d = pd.DataFrame(rows); d["ex"] = d.fwd - d.groupby("coin").fwd.transform("mean")
    d["volz"] = d.vol / d.groupby("coin").vol.transform("mean")
    out = {}
    up = d[d.r72 > 0]; dn = d[d.r72 < 0]
    R = {}
    R["up ex~r72+eff+volz"] = mreg([up.r72.values, up.eff.values, up.volz.values], up.ex.values)
    R["up ex~r72*eff"] = mreg([up.r72.values, up.eff.values, (up.r72*up.eff).values], up.ex.values)
    R["dn ex~r72+eff+volz"] = mreg([dn.r72.values, dn.eff.values, dn.volz.values], dn.ex.values)
    R["dn ex~r72*(1-eff)"] = mreg([dn.r72.values, (dn.r72*(1-dn.eff)).values, dn.volz.values], dn.ex.values)
    R["up early w1-12"] = mreg([up[up.wi<=12].eff.values], up[up.wi<=12].ex.values) + [np.nan]*4
    R["up late w13-24"] = mreg([up[up.wi>12].eff.values], up[up.wi>12].ex.values) + [np.nan]*4
    out["72h regs (coefs..., t..., n)"] = pd.DataFrame({k: pd.Series(v) for k, v in R.items()}).T
    pc = {}
    for c, g in up.groupby("coin"):
        pc[c] = mreg([g.r72.values, g.eff.values], g.ex.values)
    out["up per coin (b_r72,b_eff,t_r72,t_eff,n)"] = pd.DataFrame(pc).T
    pd_ = {}
    for c, g in dn.groupby("coin"):
        pd_[c] = mreg([g.r72.values, (g.r72*(1-g.eff)).values], g.ex.values)
    out["dn per coin (b_r72,b_r72x(1-eff),t,t,n)"] = pd.DataFrame(pd_).T
    G = pd.DataFrame(g24); G["ex"] = G.fwd24 - G.groupby("coin").fwd24.transform("mean")
    pg = {}
    for c, g in G.groupby("coin"):
        pg[c] = mreg([g.r24z.values], g.ex.values) + [np.nan]
    pg["early w1-12"] = mreg([G[G.wi<=12].r24z.values], G[G.wi<=12].ex.values) + [np.nan]
    pg["late w13-24"] = mreg([G[G.wi>12].r24z.values], G[G.wi>12].ex.values) + [np.nan]
    G["volz"] = G.vol / G.groupby("coin").vol.transform("mean")
    pg["all r24z + r24z*volz"] = mreg([G.r24z.values, (G.r24z*G.volz).values], G.ex.values)
    out["24h reversal (b,t,n)"] = pd.DataFrame({k: pd.Series(v) for k, v in pg.items()}).T
    H = pd.concat(hr); H["h2021"] = H.hour.isin([20, 21])
    # daily aggregate per coin of hours 20-21 return; t over days approx via grouping by coin
    a = H[H.h2021].groupby("coin").nxt.agg(["mean", "std", "count"]); a["t"] = a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["hours20-21 next-1h per coin"] = a[["mean", "t"]]
    y = H[H.h2021].groupby("yr").nxt.agg(["mean", "std", "count"]); y["t"] = y["mean"]/(y["std"]/np.sqrt(y["count"]))
    out["hours20-21 by year"] = y[["mean", "t", "count"]]
    # book: timing vs drift, turnover
    tot = []
    for c in bars:
        for w, b in bars[c].items():
            pos = b.postRebalance_current_allocation.values.astype(float)
            cl = b.close.values.astype(float)
            g = pos[:-1] * (cl[1:]/cl[:-1]-1)
            fee = (b.total_portfolio_value.values - b.postRebalance_total_value.values) / b.total_portfolio_value.values
            tot.append(dict(coin=c, gross=g.sum(), fee=np.nansum(fee), turn=np.nansum(np.abs(b.allocation_change.values.astype(float))), nb=len(b)))
    T = pd.DataFrame(tot).groupby("coin").sum()
    T["gross per day"] = T.gross/T.nb*24; T["fee per day"] = T.fee/T.nb*24; T["turnover per day"] = T.turn/T.nb*24
    out["book gross vs fee"] = T[["gross per day", "fee per day", "turnover per day"]]
    return out
