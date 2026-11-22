import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    # drift per coin per horizon (non-overlapping grid)
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            r1 = pd.Series(cl).pct_change()
            vol = r1.rolling(20, min_periods=10).std()
            z = (r1 / vol).values
            fc = df["forecast"].values
            reg = df["regime"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(cl)
            # plan-like cases: first bar with forecast>=2 in each 10-bar cell
            for s in range(0, n, 10):
                for i in range(s, min(s + 10, n)):
                    if fc[i] >= 2:
                        rec = dict(coin=c, win=w, year=yr[i], fc=fc[i], z=z[i], trend=1, kind="plan")
                        for h in H:
                            rec[f"u{h}"] = (cl[i + h] / cl[i] - 1 - drift[(c, h)]) if i + h < n else np.nan
                        rows.append(rec); break
            # own cases in both regimes: first bar with z>=1.5 per 10-bar cell
            for s in range(0, n, 10):
                for i in range(s, min(s + 10, n)):
                    if np.isfinite(z[i]) and z[i] >= 1.5:
                        rec = dict(coin=c, win=w, year=yr[i], fc=fc[i], z=z[i],
                                   trend=int(reg[i] == "trending"), kind="z")
                        for h in H:
                            rec[f"u{h}"] = (cl[i + h] / cl[i] - 1 - drift[(c, h)]) if i + h < n else np.nan
                        rows.append(rec); break
    d = pd.DataFrame(rows)
    def summ(g):
        out = {}
        for h in H:
            x = g[f"u{h}"].dropna()
            out[f"m{h}"] = x.mean(); out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        out["n"] = len(g)
        return pd.Series(out)
    p = d[d.kind == "plan"].copy()
    p["fcq"] = pd.qcut(p["fc"], 4, labels=False, duplicates="drop")
    zz = d[d.kind == "z"].copy()
    zz["zq"] = pd.qcut(zz["z"], 3, labels=False, duplicates="drop")
    res = {
        "plan_all": summ(p).to_frame().T,
        "plan_by_coin": p.groupby("coin").apply(summ),
        "plan_by_year": p.groupby("year").apply(summ),
        "plan_by_fc_quartile": p.groupby("fcq").apply(summ),
        "z_by_regime": zz.groupby("trend").apply(summ),
        "z_by_regime_zq": zz.groupby(["trend", "zq"]).apply(summ),
        "usual10": pd.Series({c: usual[(c, 10)] for c in bars}),
        "drift10": pd.Series({c: drift[(c, 10)] for c in bars}),
    }
    return res
