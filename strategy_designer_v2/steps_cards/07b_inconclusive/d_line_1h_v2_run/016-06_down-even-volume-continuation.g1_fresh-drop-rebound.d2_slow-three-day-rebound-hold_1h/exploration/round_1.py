import numpy as np, pandas as pd
from scipy import stats

def _slope_t(x, y):
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if len(x) < 10: return (np.nan, np.nan, len(x))
    r = stats.linregress(x, y)
    return (r.slope, r.slope / r.stderr if r.stderr > 0 else np.nan, len(x))

def explore(data):
    bars = data["bars"]
    rows_grid = []   # 72-bar grid
    rows_g24 = []    # 24-bar grid
    for coin, wins in bars.items():
        # coin means over all windows on the grid
        tmp72 = []; tmp24 = []
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].values; n = len(c)
            for i in range(0, n, 72):
                r72 = c[i+72]/c[i]-1 if i+72 < n else np.nan
                r24 = c[i+24]/c[i]-1 if i+24 < n else np.nan
                r2472 = c[i+72]/c[i+24]-1 if i+72 < n else np.nan
                r6 = c[i+6]/c[i]-1 if i+6 < n else np.nan
                tmp72.append(dict(coin=coin, w=w, wn=int(w[1:]), f=f[i], r72=r72, r24=r24, r2472=r2472, r6=r6))
            for i in range(0, n, 24):
                r24 = c[i+24]/c[i]-1 if i+24 < n else np.nan
                r6 = c[i+6]/c[i]-1 if i+6 < n else np.nan
                r12 = c[i+12]/c[i]-1 if i+12 < n else np.nan
                tmp24.append(dict(coin=coin, w=w, wn=int(w[1:]), f=f[i], r24=r24, r6=r6, r12=r12))
        a = pd.DataFrame(tmp72); b = pd.DataFrame(tmp24)
        for col in ["r72","r24","r2472","r6"]:
            a["x"+col] = a[col] - a[col].mean()
        for col in ["r24","r6","r12"]:
            b["x"+col] = b[col] - b[col].mean()
        rows_grid.append(a); rows_g24.append(b)
    G = pd.concat(rows_grid); B = pd.concat(rows_g24)
    A = G[G.f > 0]; A24 = B[B.f > 0]
    out = {}
    res = {}
    for col in ["xr6","xr24","xr2472","xr72"]:
        s, t, n = _slope_t(A.f.values, A[col].values)
        wm = np.nansum(A[col]*A.f)/A.f[A[col].notna()].sum()
        res[col] = dict(slope=s, t=t, n=n, fw_mean=wm, mean=A[col].mean())
    out["grid72 slopes by leg"] = pd.DataFrame(res).T
    res = {}
    for col in ["xr6","xr12","xr24"]:
        s, t, n = _slope_t(A24.f.values, A24[col].values)
        wm = np.nansum(A24[col]*A24.f)/A24.f[A24[col].notna()].sum()
        res[col] = dict(slope=s, t=t, n=n, fw_mean=wm)
    out["grid24 slopes"] = pd.DataFrame(res).T
    res = {}
    for coin, g in A.groupby("coin"):
        s1,t1,n1 = _slope_t(g.f.values, g.xr72.values)
        s2,t2,_ = _slope_t(g.f.values, g.xr24.values)
        s3,t3,_ = _slope_t(g.f.values, g.xr2472.values)
        res[coin] = dict(n=n1, t72=t1, t24=t2, t2472=t3, fw2472=np.nansum(g.xr2472*g.f)/g.f[g.xr2472.notna()].sum())
    out["by coin grid72"] = pd.DataFrame(res).T
    A = A.copy(); A["third"] = pd.cut(A.wn, [0,8,16,24], labels=["w1-8","w9-16","w17-24"])
    res = {}
    for k, g in A.groupby("third"):
        s1,t1,n1 = _slope_t(g.f.values, g.xr72.values)
        s2,t2,_ = _slope_t(g.f.values, g.xr24.values)
        s3,t3,_ = _slope_t(g.f.values, g.xr2472.values)
        res[k] = dict(n=n1, t72=t1, t24=t2, t2472=t3)
    out["by window third grid72"] = pd.DataFrame(res).T
    A["fq"] = pd.qcut(A.f, 4, labels=False, duplicates="drop")
    out["by forecast quartile"] = A.groupby("fq")[["f","xr6","xr24","xr2472","xr72"]].mean().assign(n=A.groupby("fq").size())
    return out
