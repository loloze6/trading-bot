import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(df)
            ret28 = pd.Series(c).pct_change(28).values
            raw = df.get("debug_info.components.thin_volume.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            fc = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            h = 5
            for i in range(0, n - h, h):
                rows.append(dict(coin=coin, w=w, year=ts.dt.year.iloc[i], day=str(ts.iloc[i].date()),
                                 fr=c[i+h]/c[i]-1, regime=df["regime"].iloc[i],
                                 ret28=ret28[i], raw=raw[i], fc=fc[i]))
    R = pd.DataFrame(rows)
    R["ex"] = R["fr"] - R.groupby("coin")["fr"].transform("mean")
    T = R[(R.regime=="trending") & R.raw.notna()].copy()
    out = {}
    def creg(d, xs):
        d = d.dropna(subset=xs+["ex"])
        X = np.column_stack([np.ones(len(d))] + [d[x].values for x in xs]); y = d.ex.values
        b = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ b
        XtXi = np.linalg.inv(X.T @ X); meat = np.zeros((X.shape[1],)*2)
        for _, idx in d.reset_index(drop=True).groupby("day").indices.items():
            s = X[idx].T @ e[idx]; meat += np.outer(s, s)
        se = np.sqrt(np.diag(XtXi @ meat @ XtXi))
        return pd.Series(np.r_[len(d), d.day.nunique(), b[1:], b[1:]/se[1:]],
                         index=["n","days"]+[f"b_{x}" for x in xs]+[f"t_{x}" for x in xs])
    out["clustered raw slope, all decline cells"] = creg(T, ["raw"])
    out["clustered raw slope, raw<0 only"] = creg(T[T.raw<0], ["raw"])
    out["clustered raw slope, raw>=0 only"] = creg(T[T.raw>=0], ["raw"])
    out["clustered fc slope, all"] = creg(T, ["fc"])
    T["ret28c"] = T.ret28; T["inter"] = T.raw*T.ret28
    out["clustered raw+ret28+inter"] = creg(T.dropna(subset=["ret28"]), ["raw","ret28","inter"])
    out["corr raw vs fc where raw<0"] = float(T[T.raw<0][["raw","fc"]].corr().iloc[0,1])
    out["mean ex by raw sign"] = T.assign(pos=T.raw>=0).groupby("pos")["ex"].agg(["count","mean"])
    bw = []
    for k, g in T.groupby("w"):
        s = stats.linregress(g.raw, g.ex) if len(g)>10 else None
        bw.append(dict(w=k, n=len(g), slope=s.slope if s else np.nan, t=s.slope/s.stderr if s else np.nan, meanex=g.ex.mean()))
    out["by window raw slope"] = pd.DataFrame(bw)
    return out
