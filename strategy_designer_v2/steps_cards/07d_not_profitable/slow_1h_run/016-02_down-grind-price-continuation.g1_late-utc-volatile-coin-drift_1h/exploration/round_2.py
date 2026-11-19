import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    S = []
    for coin in bars:
        for w, b in bars[coin].items():
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values; h = ts.dt.hour.values
            r1 = pd.Series(c).pct_change()
            vol = r1.rolling(168).std().values
            idx = np.where(h == 20)[0]
            for i in idx:
                if i < 168 or i + 24 >= len(b): continue
                d = dict(coin=coin, vol=vol[i], r24=c[i]/c[i-24]-1, r168=c[i]/c[i-168]-1)
                for k in [2, 4, 6, 8, 12, 24]:
                    d[f"h{k}"] = c[i+k]/c[i]-1
                S.append(d)
    S = pd.DataFrame(S)
    # path of mean return after 21:00
    path = S[[f"h{k}" for k in [2,4,6,8,12,24]]].agg(["mean","std","count"]).T
    path["t"] = path["mean"]/(path["std"]/np.sqrt(path["count"]))
    # raw vol quintile within coin
    S["vq"] = S.groupby("coin").vol.transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    S["r24q"] = S.groupby("coin").r24.transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    S["r168q"] = S.groupby("coin").r168.transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    S["h2_over_vol"] = S.h2 / S.vol
    byvq = S.groupby("vq").agg(h2=("h2","mean"), vol=("vol","mean"), h2_per_vol=("h2_over_vol","mean"), n=("h2","size"))
    byr24 = S.groupby("r24q").agg(h2=("h2","mean"), r24=("r24","mean"), n=("h2","size"))
    byr168 = S.groupby("r168q").agg(h2=("h2","mean"), r168=("r168","mean"), n=("h2","size"))
    return {"path_after_2100": path, "h2_by_raw_vol_quintile": byvq,
            "h2_by_prior_24h_quintile": byr24, "h2_by_prior_7d_quintile": byr168}
