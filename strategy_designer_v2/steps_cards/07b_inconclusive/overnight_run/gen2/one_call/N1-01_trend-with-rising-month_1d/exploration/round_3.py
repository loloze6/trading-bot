import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    def summ(x):
        x = pd.Series(x).dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), median=x.median(), hit=(x > 0).mean(),
                              t=stats.ttest_1samp(x, 0).statistic if len(x) > 2 else np.nan))
    # BTC active state by timestamp
    btc_act = {}
    for w, df in data["bars"]["BTCUSD"].items():
        for ts, fc in zip(df["timestamp"], df["forecast"].astype(float)):
            btc_act[pd.Timestamp(ts)] = fc > 0
    res = {}
    for h in (5, 10, 20):
        rows = []
        mean_h = {}
        for coin, wins in data["bars"].items():
            allf = []
            for w, df in wins.items():
                c = df["close"].astype(float).values
                n = len(c)
                if n > h:
                    allf.append(c[h:] / c[:-h] - 1)
            mean_h[coin] = np.mean(np.concatenate(allf))
            for w, df in wins.items():
                df = df.reset_index(drop=True)
                c = df["close"].astype(float).values
                n = len(c)
                fc = df["forecast"].astype(float).values
                bir = pd.to_numeric(df["debug_info.bars_in_regime"], errors="coerce").values
                for i in range(0, n - h, h):
                    ts = pd.Timestamp(df["timestamp"].iloc[i])
                    rows.append(dict(coin=coin, fc=fc[i], bir=bir[i],
                                     lr=np.log(c[i+h]/c[i]) - np.log1p(mean_h[coin]),
                                     btc=btc_act.get(ts, np.nan)))
        R = pd.DataFrame(rows)
        A = R[R["fc"] > 0]
        I = R[R["fc"] <= 0]
        res[h] = (A, I)
        out[f"h{h}_active_vs_inactive"] = pd.DataFrame({"active": summ(A["lr"]), "inactive": summ(I["lr"])}).T
    A5, I5 = res[5]
    out["h5_active_by_coin"] = A5.groupby("coin").apply(lambda g: summ(g["lr"]))
    out["h5_active_by_bir"] = A5.groupby(pd.cut(A5["bir"], [-1, 5, 20, 1e9], labels=["<=5", "6-20", ">20"])).apply(lambda g: summ(g["lr"]))
    A20, _ = res[20]
    nb = A20[A20["coin"] != "BTCUSD"]
    out["h20_alts_by_btc_active"] = nb.groupby("btc").apply(lambda g: summ(g["lr"]))
    nb5 = A5[A5["coin"] != "BTCUSD"]
    out["h5_alts_by_btc_active"] = nb5.groupby("btc").apply(lambda g: summ(g["lr"]))
    return out
