import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            fc = b["forecast"].astype(float)
            raw = b["debug_info.components.range_calm.last_history_value"].astype(float) if "debug_info.components.range_calm.last_history_value" in b else pd.Series(np.nan, index=b.index)
            ret = c.pct_change()
            vol30 = ret.rolling(30, min_periods=20).std()
            vmed = vol30.expanding(min_periods=30).median()
            r60 = c / c.shift(60) - 1
            n = len(b)
            for h in (1, 2, 3, 5, 7, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                     rising=(b["regime"].iloc[i] == "unknown"),
                                     fc=fc.iloc[i], raw=raw.iloc[i],
                                     agit=(vol30.iloc[i] > vmed.iloc[i]) if pd.notna(vmed.iloc[i]) else np.nan,
                                     r60=r60.iloc[i],
                                     r=c.iloc[i + h] / c.iloc[i] - 1))
    df = pd.DataFrame(rows)
    df["ex"] = df["r"] - df.groupby(["coin", "h"])["r"].transform("mean")
    out = {}

    def tb(d, col="fc"):
        d = d.dropna(subset=[col, "ex"])
        if len(d) < 30: return pd.Series(dict(n=len(d)))
        q = d[col].rank(method="first"); k = len(d) // 3
        top = d[q > len(d) - k]["ex"]; bot = d[q <= k]["ex"]
        t = stats.ttest_ind(top, bot, equal_var=False).statistic
        sp = stats.spearmanr(d[col], d["ex"])
        return pd.Series(dict(n=len(d), top=top.mean(), bot=bot.mean(), diff=top.mean() - bot.mean(),
                              welch_t=t, spearman=sp.correlation, sp_p=sp.pvalue))

    ris = df[df.rising & (df.fc > 0)]
    out["fc_by_horizon_rising"] = pd.DataFrame({h: tb(ris[ris.h == h]) for h in (1, 2, 3, 5, 7, 10)}).T
    out["raw_by_horizon_rising"] = pd.DataFrame({h: tb(ris[ris.h == h], "raw") for h in (1, 2, 3, 5, 7, 10)}).T
    r3 = ris[ris.h == 3].copy()
    r3["agi"] = r3["agit"].map({True: "agitated", False: "calm"})
    out["agitation_h3"] = pd.DataFrame({a: tb(g) for a, g in r3.dropna(subset=["agi"]).groupby("agi")}).T
    r3["trend"] = pd.qcut(r3["r60"], 3, labels=["weak_rise", "mid_rise", "strong_rise"])
    out["trend_strength_h3"] = pd.DataFrame({a: tb(g) for a, g in r3.dropna(subset=["trend"]).groupby("trend")}).T
    r3["fq"] = pd.qcut(r3["fc"], 5, labels=False)
    g = r3.groupby("fq")["ex"]
    out["fc_quintiles_h3"] = pd.DataFrame(dict(n=g.size(), mean_ex=g.mean(), t=g.mean() / (g.std() / np.sqrt(g.size())),
                                               fc_mid=r3.groupby("fq")["fc"].median()))
    out["by_window_h3"] = pd.DataFrame({w: tb(gg) for w, gg in r3.groupby("w")}).T
    out["mean_ex_all_rising_h3"] = pd.Series(dict(n=len(r3), mean=r3.ex.mean(), t=r3.ex.mean() / (r3.ex.std() / np.sqrt(len(r3)))))
    return out
