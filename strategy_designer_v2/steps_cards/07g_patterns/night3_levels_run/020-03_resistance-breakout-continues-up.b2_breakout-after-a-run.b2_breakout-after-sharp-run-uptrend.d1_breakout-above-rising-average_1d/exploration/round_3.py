import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    recs = []
    for coin, wins in data["bars"].items():
        g = {h: [] for h in (5, 10, 20)}
        cr = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); fc = b["forecast"].astype(float).fillna(0)
            n = len(c); pos = np.arange(n)
            ts = pd.to_datetime(b["timestamp"])
            for h in (5, 10, 20):
                f = c.shift(-h) / c - 1
                g[h].append(f[(pos % h == 0)].dropna())
            start = (fc > 0) & (fc.shift(1).fillna(0) <= 0)
            last = -10**9
            for i in np.where(start)[0]:
                d = dict(coin=coin, win=w, year=ts.iloc[i].year, sep=(i - last >= 20))
                if i - last >= 20:
                    last = i
                for h in (5, 10, 20):
                    d[f"f{h}"] = c.iloc[i + h] / c.iloc[i] - 1 if i + h < n else np.nan
                d["f5_20"] = c.iloc[i + 20] / c.iloc[i + 5] - 1 if i + 20 < n else np.nan
                d["brk"] = b["debug_info.components.break.last_history_value"].iloc[i]
                d["mad"] = b["debug_info.components.ma_dist.last_history_value"].iloc[i]
                cr.append(d)
        R = pd.DataFrame(cr)
        for h in (5, 10, 20):
            s = pd.concat(g[h]); R[f"u{h}"] = R[f"f{h}"] - s.mean(); R[f"s{h}"] = R[f"u{h}"] / s.std()
        s5 = pd.concat(g[5]).mean(); s20 = pd.concat(g[20]).mean()
        R["u5_20"] = R["f5_20"] - (s20 - s5)
        recs.append(R)
    R = pd.concat(recs)
    def st(x, col):
        x = x[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    S = R[R.sep]
    out["sep20_starts"] = pd.DataFrame({c: st(S, c) for c in ["u5", "u10", "u20", "u5_20"]}).T.round(4)
    out["all_starts_day5_to_20"] = st(R, "u5_20").round(4)
    out["sep_u20_by_coin"] = S.groupby("coin").apply(lambda x: st(x, "u20")).round(4)
    out["sep_u20_by_year"] = S.groupby("year").apply(lambda x: st(x, "u20")).round(4)
    out["sep_s20_mean"] = S.s20.mean()
    R["bq"] = pd.qcut(R.brk.rank(method="first"), 4, labels=False)
    out["u_by_break_strength"] = R.groupby("bq").agg(n=("u20", "count"), brk=("brk", "mean"), u5=("u5", "mean"), u20=("u20", "mean")).round(4)
    out["spearman_brk_u20"] = stats.spearmanr(R.brk, R.u20, nan_policy="omit").correlation
    R["mq"] = pd.qcut(R.mad.rank(method="first"), 4, labels=False)
    out["u20_t_by_mad"] = R.groupby("mq").apply(lambda x: st(x, "u20")).round(4)
    return out
