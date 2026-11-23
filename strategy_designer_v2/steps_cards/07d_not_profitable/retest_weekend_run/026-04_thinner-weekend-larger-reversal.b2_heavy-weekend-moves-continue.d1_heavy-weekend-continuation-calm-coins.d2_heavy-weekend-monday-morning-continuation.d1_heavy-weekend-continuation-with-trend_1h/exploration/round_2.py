def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    # position gain per bar by hours since the Monday signal, by side
    rec = []
    dayrows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values
            a = b["postRebalance_current_allocation"].fillna(0).values
            f = b["forecast"].fillna(0).values
            ret = np.r_[c[1:]/c[:-1]-1, np.nan]
            gain = a*ret
            # last signal index and side
            last = -10**9; side = 0
            hs = np.full(len(c), np.nan); sd = np.zeros(len(c))
            for i in range(len(c)):
                if f[i] != 0 and (i-last) > 24:
                    last = i; side = np.sign(f[i])
                if last >= 0: hs[i] = i-last; sd[i] = side
            df = pd.DataFrame({"hs": hs, "side": sd, "a": a, "gain": gain, "held": (a != 0).astype(int),
                               "alongside": np.sign(a)})
            df["hsb"] = pd.cut(df["hs"], [-1, 11, 23, 47, 95, 167, 10**6], labels=["0-11","12-23","24-47","48-95","96-167","168+"])
            df["coin"] = coin; df["w"] = w
            rec.append(df)
            # daily book gain split by held side (before fees approx)
            df["day"] = ts.dt.floor("D")
            df["gl"] = np.where(a > 0, gain, 0.0); df["gs"] = np.where(a < 0, gain, 0.0)
            df["g12"] = np.where(df["hs"] <= 11, gain, 0.0)
            g = df.groupby("day").agg(gl=("gl","sum"), gs=("gs","sum"), g12=("g12","sum"), gall=("gain","sum")).reset_index()
            g["w"] = int(w[1:]); g["coin"] = coin
            dayrows.append(g)
    R = pd.concat(rec)
    R = R[R["held"] == 1]
    out["held_by_hours_since_signal"] = R.groupby(["hsb","alongside"]).agg(nbars=("gain","size"), mean_gain=("gain","mean"), sum_gain=("gain","sum"), mean_abs_a=("a", lambda x: x.abs().mean())).dropna()
    D = pd.concat(dayrows)
    B = D.groupby(["w","day"])[["gl","gs","g12","gall"]].mean().reset_index().sort_values(["w","day"])
    def stats(x):
        x = x.fillna(0).values
        v = np.cumprod(1+x); dd = (v/np.maximum.accumulate(v)-1).min()
        yr = v[-1]**(365/len(x))-1
        return pd.Series({"mean": x.mean(), "sharpe": x.mean()/x.std()*np.sqrt(365), "yearly": yr, "maxdd": dd, "calmar": yr/abs(dd)})
    out["book_gross_by_part"] = pd.DataFrame({k: stats(B[k]) for k in ["gall","gl","gs","g12"]})
    # short-only gross by year
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["by_year_long_short_gross"] = B.groupby("year")[["gl","gs","g12","gall"]].sum()
    return out
