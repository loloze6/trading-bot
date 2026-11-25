import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            rng = (b["high"] - b["low"]) / c
            # recompute ratio from prices (long 104 mean / short 14 mean), as the component does
            ratio = rng.rolling(104, min_periods=104).mean() / rng.rolling(14).mean()
            fc = b["forecast"].astype(float)
            rec = b.get("debug_info.components.range_calm.last_history_value")
            agit = rng.rolling(30).std()  # proxy on ranges; better: daily ret std
            ret = c.pct_change()
            vol30 = ret.rolling(30).std()
            volpct = vol30.rolling(365, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            n = len(b)
            for h in (1, 3, 5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                     rising=(b["regime"].iloc[i] == "unknown"),
                                     fc=fc.iloc[i], ratio=ratio.iloc[i],
                                     rec=(rec.iloc[i] if rec is not None else np.nan),
                                     agit=volpct.iloc[i],
                                     r=c.iloc[i + h] / c.iloc[i] - 1))
    df = pd.DataFrame(rows)
    df["ex"] = df["r"] - df.groupby(["coin", "h"])["r"].transform("mean")
    out = {}

    def tb(d, col="fc"):
        d = d.dropna(subset=[col, "ex"])
        if len(d) < 30: return pd.Series(dict(n=len(d)))
        q = d[col].rank(method="first")
        k = len(d) // 3
        top = d[q > len(d) - k]["ex"]; bot = d[q <= k]["ex"]
        t = stats.ttest_ind(top, bot, equal_var=False).statistic
        sp = stats.spearmanr(d[col], d["ex"])
        return pd.Series(dict(n=len(d), top=top.mean(), bot=bot.mean(), diff=top.mean() - bot.mean(),
                              welch_t=t, spearman=sp.correlation, sp_p=sp.pvalue))

    r3 = df[(df.h == 3) & df.rising & (df.fc > 0)]
    out["main_h3_rising_fc"] = tb(r3)
    out["by_horizon_rising_ratio"] = pd.DataFrame({h: tb(df[(df.h == h) & df.rising], "ratio") for h in (1, 3, 5, 10)}).T
    out["by_horizon_notrising_ratio"] = pd.DataFrame({h: tb(df[(df.h == h) & ~df.rising], "ratio") for h in (1, 3, 5, 10)}).T
    out["by_coin_h3_rising"] = pd.DataFrame({c: tb(g) for c, g in r3.groupby("coin")}).T
    out["by_year_h3_rising"] = pd.DataFrame({y: tb(g) for y, g in r3.groupby("year")}).T
    r3["agi"] = np.where(r3.agit > 0.5, "agitated", "calm")
    out["by_agitation_h3_rising"] = pd.DataFrame({a: tb(g) for a, g in r3.dropna(subset=["agit"]).groupby("agi")}).T
    # quintile profile of ratio within rising, h=3 and h=10
    for h in (3, 10):
        d = df[(df.h == h) & df.rising].dropna(subset=["ratio"]).copy()
        d["q"] = pd.qcut(d["ratio"], 5, labels=False)
        g = d.groupby("q")["ex"]
        out[f"quintiles_ratio_rising_h{h}"] = pd.DataFrame(dict(n=g.size(), mean_ex=g.mean(),
                                                                 t=g.mean() / (g.std() / np.sqrt(g.size())),
                                                                 ratio_mid=d.groupby("q")["ratio"].median()))
    out["fc_vs_ratio_corr_rising"] = float(df[(df.h == 3) & df.rising][["fc", "ratio"]].corr().iloc[0, 1])
    return out
