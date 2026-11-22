import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20).std()
            z = r1 / vol
            r90 = c / c.shift(90) - 1
            r30 = c / c.shift(30) - 1
            al = b["postRebalance_current_allocation"].astype(float)
            fc = b["forecast"].astype(float)
            pos_gain = al * (c.shift(-1) / c - 1)
            # days since short opened
            age = np.zeros(len(b)); a = 0
            for i in range(len(b)):
                if al.iloc[i] < 0:
                    a = a + 1 if (i > 0 and al.iloc[i-1] < 0) else 1
                else:
                    a = 0
                age[i] = a
            # consecutive up-days count at signal
            up = (r1 > 0).astype(int)
            run = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            for i in range(len(b)):
                if al.iloc[i] < 0 and not np.isnan(pos_gain.iloc[i]):
                    rows.append(dict(coin=coin, age=age[i], gain=pos_gain.iloc[i], fc=fc.iloc[i],
                                     zero_fc=(fc.iloc[i] == 0), r90=r90.iloc[i], r30=r30.iloc[i],
                                     run=run.iloc[i], coin_next=c.shift(-1).iloc[i] / c.iloc[i] - 1))
    d = pd.DataFrame(rows)
    def agg(g):
        x = g["gain"]
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              coin_next=g["coin_next"].mean(), fc0_share=g["zero_fc"].mean()))
    out = {}
    out["by_age"] = d.groupby(pd.cut(d["age"], [0, 1, 2, 3, 5, 10, 1000])).apply(agg)
    out["by_fc_zero"] = d.groupby("zero_fc").apply(agg)
    out["by_r90q"] = d.dropna(subset=["r90"]).groupby(pd.qcut(d["r90"].dropna(), 4)).apply(agg)
    out["by_r30q"] = d.dropna(subset=["r30"]).groupby(pd.qcut(d["r30"].dropna(), 4)).apply(agg)
    out["by_uprun"] = d.groupby(pd.cut(d["run"], [-1, 0, 1, 2, 100])).apply(agg)
    return out
