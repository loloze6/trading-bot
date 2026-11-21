import numpy as np, pandas as pd
from scipy import stats

def ichi(b):
    h, l, c = b["high"], b["low"], b["close"]
    ten = (h.rolling(9).max() + l.rolling(9).min()) / 2
    kij = (h.rolling(26).max() + l.rolling(26).min()) / 2
    sa = ((ten + kij) / 2).shift(26)
    sb = ((h.rolling(52).max() + l.rolling(52).min()) / 2).shift(26)
    top = np.maximum(sa, sb); bot = np.minimum(sa, sb)
    return top, bot

def tstat(x):
    x = pd.Series(x).dropna()
    return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan

def explore(data):
    bars = data["bars"]
    H = 26
    rows = []
    for coin, wins in bars.items():
        mus = {}
        for h in (5, 10, 26, 52):
            allret = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c) - h, h):
                    allret.append(c[i + h] / c[i] - 1)
            mus[h] = np.mean(allret)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].values
            top, bot = ichi(b)
            for i in range(0, len(c), H):
                if not (f[i] < 0):
                    continue
                d = dict(coin=coin, w=int(str(w).lstrip("w")), f=f[i])
                for h in (5, 10, 26, 52):
                    d[f"ex{h}"] = (-(c[i + h] / c[i] - 1) + mus[h]) if i + h < len(c) else np.nan
                d["past90"] = c[i] / c[i - 90] - 1 if i >= 90 else np.nan
                d["dist"] = c[i] / bot.iloc[i] - 1 if not np.isnan(bot.iloc[i]) else np.nan
                d["thick"] = (top.iloc[i] - bot.iloc[i]) / c[i] if not np.isnan(bot.iloc[i]) else np.nan
                d["slope_raw"] = b["debug_info.components.cloud_slope.last_history_value"].iloc[i] if "debug_info.components.cloud_slope.last_history_value" in b else np.nan
                rows.append(d)
    d = pd.DataFrame(rows)
    out = {}
    hz = {}
    for h in (5, 10, 26, 52):
        x = d[f"ex{h}"].dropna()
        hz[h] = dict(n=len(x), ex_mean=x.mean(), t=tstat(x),
                     slope_on_absf=stats.linregress(d.loc[x.index, "f"].abs(), x).slope)
    out["excess_by_horizon"] = pd.DataFrame(hz).T
    def summ(g):
        x = g["ex26"].dropna()
        return pd.Series(dict(n=len(x), ex_mean=x.mean(), t=tstat(x), hit=(x > 0).mean()))
    for col in ("past90", "dist", "thick", "slope_raw"):
        q = pd.qcut(d[col], 4, labels=False, duplicates="drop")
        out[f"by_{col}_q"] = d.groupby(q).apply(summ)
        out[f"{col}_q_edges"] = d[col].quantile([0, .25, .5, .75, 1])
    out["corr_ex26"] = d[["ex26", "past90", "dist", "thick", "slope_raw", "f"]].corr(method="spearman")["ex26"]
    return out
