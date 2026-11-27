import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    sd = {}
    H = [3, 7, 14, 21]
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
            sd[(coin, h)] = np.std(rs, ddof=1) if len(rs) > 1 else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            m30 = df["debug_info.components.month_fall.last_history_value"].values if "debug_info.components.month_fall.last_history_value" in df else np.full(len(c), np.nan)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(0, len(c), 7):
                if not (f[i] < 0):
                    continue
                r = {"coin": coin, "win": w, "year": yr[i], "fc": f[i], "m30": m30[i]}
                for h in H:
                    if i + h < len(c):
                        ret = c[i + h] / c[i] - 1
                        r[f"u{h}"] = -(ret - drift[(coin, h)])
                        r[f"t{h}"] = -ret
                        r[f"s{h}"] = r[f"u{h}"] / sd[(coin, h)]
                rows.append(r)
    d = pd.DataFrame(rows)
    out = {}
    def summ(g, col="u7"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    hz = {}
    for h in H:
        x = d[f"u{h}"].dropna(); tt = d[f"t{h}"].dropna()
        y = d.loc[x.index]
        sl = stats.linregress(y["fc"], x)
        hz[h] = {"n": len(x), "unusual": x.mean(), "t_unusual": x.mean()/(x.std()/np.sqrt(len(x))), "total": tt.mean(), "strength": d[f"s{h}"].mean(), "slope_t_on_fc": sl.slope/sl.stderr}
    out["by_horizon"] = pd.DataFrame(hz).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_window"] = d.groupby("win").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["by_fc_tercile"] = d.groupby("fq").apply(summ)
    d["mq"] = pd.qcut(d["m30"].rank(method="first"), 3, labels=["m30_deep", "m30_mid", "m30_shallow"])
    out["by_m30_tercile"] = d.groupby("mq").apply(summ)
    out["by_m30_tercile_h14"] = d.groupby("mq").apply(lambda g: summ(g, "u14"))
    x = d.dropna(subset=["m30", "u7"])
    sl = stats.linregress(x["m30"], x["u7"])
    out["slope_u7_on_raw_m30_t"] = float(sl.slope / sl.stderr)
    out["corr_fc_m30"] = float(d[["fc", "m30"]].corr().iloc[0, 1])
    return out
