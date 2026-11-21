import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    drift = {}; usual = {}
    for H in (18, 36):
        for coin, wins in bars.items():
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                rs.extend(list(c[idx + H] / c[idx] - 1))
            drift[(coin, H)] = np.mean(rs); usual[(coin, H)] = np.std(rs)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            f = df["forecast"].fillna(0).values
            prior_hi = pd.Series(hi).shift(1).rolling(12).max().values
            mr = pd.Series(hi - lo).rolling(180, min_periods=45).mean().values
            raw = np.maximum(0, c - prior_hi) / mr
            n = len(c); runmin = 0.0; taken = set()
            for t in range(n):
                cell = t // 18
                if f[t] - runmin >= 2 and f[t] > 0 and cell not in taken:
                    taken.add(cell); runmin = f[t]
                    if t + 18 < n:
                        u36 = c[t + 36] / c[t] - 1 - drift[(coin, 36)] if t + 36 < n else np.nan
                        rows.append(dict(coin=coin, year=pd.to_datetime(df["timestamp"].iloc[t]).year,
                                         raw=raw[t], u18=c[t + 18] / c[t] - 1 - drift[(coin, 18)], u36=u36,
                                         s36=u36 / usual[(coin, 36)] if u36 == u36 else np.nan))
                else:
                    runmin = min(runmin, f[t])
    d = pd.DataFrame(rows)
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out = {}
    med = d.raw.median()
    top = d[d.raw > med]; bot = d[d.raw < med]
    out["raw_median_split_u18"] = pd.Series({"top": top.u18.mean(), "bot": bot.u18.mean(), "diff": top.u18.mean() - bot.u18.mean(), "welch_t": stats.ttest_ind(top.u18, bot.u18, equal_var=False).statistic, "spearman_raw_u18": stats.spearmanr(d.raw, d.u18).correlation})
    out["all_u36"] = tt(d.u36); out["strength36"] = float(d.s36.mean())
    d["rq"] = pd.qcut(d.raw.rank(method="first"), 5, labels=False)
    out["raw_q_u36"] = d.groupby("rq").u36.apply(tt).unstack()
    d["top"] = d.raw > med
    out["top_half_by_coin_u18"] = d[d.top].groupby("coin").u18.apply(tt).unstack().join(d[~d.top].groupby("coin").u18.mean().rename("bot_mean"))
    out["top_half_by_year_u18"] = d[d.top].groupby("year").u18.apply(tt).unstack().join(d[~d.top].groupby("year").u18.mean().rename("bot_mean"))
    return out
