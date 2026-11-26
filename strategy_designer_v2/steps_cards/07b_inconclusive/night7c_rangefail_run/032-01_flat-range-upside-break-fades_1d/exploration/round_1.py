import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 10
    rows = []
    allb = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        grid = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                grid.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(grid); usual[coin] = np.std(grid, ddof=1)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values
            n = len(df)
            f = df["forecast"].fillna(0).values
            fd = np.r_[0, np.diff(f)]
            os_ = df.get("debug_info.components.overshoot.last_history_value")
            seen = set()
            for i in range(n):
                if f[i] <= -1e-9 and fd[i] <= -2:
                    cell = i // H
                    if cell in seen: continue
                    seen.add(cell)
                    if i + H >= n: continue
                    r = {}
                    for h in (3, 5, 10, 20):
                        r[f"r{h}"] = -(c[i+h]/c[i]-1 - drift[coin]*h/10) if i+h < n else np.nan
                    rows.append(dict(coin=coin, w=w, ts=df["timestamp"].iloc[i], year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                     os=os_.iloc[i] if os_ is not None else np.nan, fc=f[i], **r))
            # all breakouts, recomputed, any ER
            s = pd.Series(c)
            ph = pd.Series(hi).shift(1).rolling(60).max()
            ch = s.diff().abs().rolling(60).sum()
            er = ((s - s.shift(60)).abs() / ch).rolling(5).mean()
            prev60 = s / s.shift(60) - 1
            for i in range(n - H):
                if not np.isnan(ph[i]) and c[i] > ph[i] and i % H == 0 or (not np.isnan(ph[i]) and c[i] > ph[i] and (i==0 or c[i-1] <= ph[i-1])):
                    pass
            for i in range(n - H):
                if np.isnan(ph[i]) or np.isnan(er[i]): continue
                if c[i] > ph[i] and (c[i-1] <= ph[i-1] if not np.isnan(ph[i-1]) else True):
                    allb.append(dict(coin=coin, w=w, er=er[i], os=c[i]/ph[i]-1,
                                     up10=(c[i+H]/c[i]-1-drift[coin])))
    cs = pd.DataFrame(rows)
    out = {}
    def tday(sub, col):
        x = sub.dropna(subset=[col])
        d = x.groupby(x["ts"].astype(str).str[:10])[col].sum()
        return pd.Series(dict(n=len(x), days=len(d), mean=x[col].mean(), t=d.mean()/(d.std(ddof=1)/np.sqrt(len(d))) if len(d)>2 else np.nan))
    out["overall by horizon (short side)"] = pd.DataFrame({h: tday(cs, h) for h in ["r3","r5","r10","r20"]}).T
    out["by coin r10"] = cs.groupby("coin").apply(lambda g: tday(g, "r10"))
    out["by window r10"] = cs.groupby("w").apply(lambda g: tday(g, "r10"))
    cs["osq"] = pd.qcut(cs["os"].rank(method="first"), 3, labels=["small","mid","large"])
    out["by overshoot tercile"] = cs.groupby("osq").apply(lambda g: pd.concat([tday(g,"r10"), pd.Series({"os_mean": g["os"].mean()})]))
    ab = pd.DataFrame(allb)
    ab["erq"] = pd.cut(ab["er"], [0, 0.15, 0.3, 0.5, 1.01])
    out["fresh 60d breakouts, 10d up-move minus drift by ER"] = ab.groupby("erq")["up10"].agg(["count","mean","median", lambda x: x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))])
    ab["osq"] = pd.qcut(ab["os"].rank(method="first"), 3, labels=["small","mid","large"])
    out["fresh breakouts by overshoot tercile"] = ab.groupby("osq")["up10"].agg(["count","mean", lambda x: x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))])
    out["share of cases rising over 10d"] = float((cs["r10"] < 0).mean())
    return out
