import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [5, 10]
    rows = []
    for coin, ws in bars.items():
        dd = {}
        for h in H:
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            dd[h] = np.mean(rs) if rs else np.nan
        for w, df in ws.items():
            c = df["close"].values
            f = df["forecast"].values
            raw = df["debug_info.components.stretch.last_history_value"].values if "debug_info.components.stretch.last_history_value" in df else np.full(len(c), np.nan)
            ts = pd.to_datetime(df["timestamp"])
            yr = ts.dt.year.values
            day = ts.dt.floor("D").astype("int64").values
            for h in H:
                for i in range(0, len(c) - h, h):
                    if f[i] == 0 or np.isnan(f[i]):
                        continue
                    r = c[i + h] / c[i] - 1 - dd[h]
                    rows.append(dict(coin=coin, w=w, h=h, f=f[i], raw=raw[i], yr=yr[i], day=day[i], r=r))
    d = pd.DataFrame(rows)

    def clslope(g, x):
        g = g.dropna(subset=[x, "r"])
        n = len(g)
        if n < 15:
            return pd.Series(dict(n=n))
        X = np.column_stack([np.ones(n), g[x].values])
        y = g["r"].values
        XtX = np.linalg.inv(X.T @ X)
        b = XtX @ X.T @ y
        e = y - X @ b
        meat = np.zeros((2, 2))
        for _, idx in g.reset_index(drop=True).groupby("day").groups.items():
            s = (X[idx] * e[idx][:, None]).sum(0)
            meat += np.outer(s, s)
        V = XtX @ meat @ XtX
        dm = np.sign(g[x]) * g["r"]
        return pd.Series(dict(n=n, days=g.day.nunique(), slope=b[1], t_cl=b[1] / np.sqrt(V[1, 1]),
                              dir_mean=dm.mean()))
    out = {}
    for h in H:
        dh = d[d.h == h]
        out[f"h{h}_all_f_vs_raw"] = pd.DataFrame({"forecast": clslope(dh, "f"), "raw": clslope(dh, "raw")})
        out[f"h{h}_by_year_f"] = dh.groupby("yr").apply(lambda g: clslope(g, "f"))
        out[f"h{h}_no2021_f"] = clslope(dh[dh.yr != 2021], "f")
        out[f"h{h}_by_window_dir_mean"] = dh.groupby("w").apply(lambda g: pd.Series(dict(n=len(g), dir_mean=(np.sign(g.f) * g.r).mean())))
    return out
