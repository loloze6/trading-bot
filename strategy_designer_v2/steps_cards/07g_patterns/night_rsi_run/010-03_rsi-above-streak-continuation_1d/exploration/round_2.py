import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    res = {}
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(30).std()
            rng = (b["high"] - b["low"]) / c
            rng_rel = rng / rng.rolling(30).mean()
            for k in [1, 3, 7]:
                pk = c / c.shift(k) - 1
                for H in [3, 7, 14]:
                    fwd = c.shift(-H) / c - 1
                    for i in range(0, len(b), H):
                        if pd.isna(fwd.iloc[i]) or pd.isna(pk.iloc[i]):
                            continue
                        recs.append(dict(coin=coin, w=w, k=k, H=H, fwd=fwd.iloc[i], past=pk.iloc[i],
                                         pz=pk.iloc[i] / (vol.iloc[i] * np.sqrt(k)) if vol.iloc[i] > 0 else np.nan,
                                         rng=rng.iloc[i], rr=rng_rel.iloc[i], wi=int(w[1:])))
    R = pd.DataFrame(recs)
    R["ex"] = R["fwd"] - R.groupby(["coin", "k", "H"])["fwd"].transform("mean")
    out = []
    for (k, H), x in R.groupby(["k", "H"]):
        x = x.dropna(subset=["pz"])
        s = stats.linregress(x["pz"], x["ex"])
        sr = stats.linregress(x.dropna(subset=["rr"])["rr"], x.dropna(subset=["rr"])["ex"])
        out.append(dict(k=k, H=H, n=len(x), t_pastz=s.slope / s.stderr, t_rangerel=sr.slope / sr.stderr))
    res["slopes_past_and_range"] = pd.DataFrame(out).round(3)
    # past3 -> 14 by coin and by window half
    x = R[(R.k == 3) & (R.H == 14)].dropna(subset=["pz"]).copy()
    x["half"] = np.where(x["wi"] <= 12, "w1-12", "w13-24")
    o = []
    for key, y in x.groupby(["coin", "half"]):
        s = stats.linregress(y["pz"], y["ex"])
        o.append(dict(grp=str(key), n=len(y), slope=s.slope, t=s.slope / s.stderr))
    res["past3z_to_14_by_coin_half"] = pd.DataFrame(o).round(4)
    x = R[(R.k == 3) & (R.H == 3)].dropna(subset=["pz"]).copy()
    x["q"] = x.groupby("coin")["pz"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    q = x.groupby("q")["ex"].agg(["size", "mean", "std"]); q["t"] = q["mean"] / (q["std"] / np.sqrt(q["size"]))
    res["past3z_quintile_fwd3"] = q.round(4)
    # book around its biggest days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.reset_index(drop=True).copy()
            d["next_coin5"] = sum(d["coin_return"].shift(-j) for j in range(1, 6))
            d["prev_coin5"] = sum(d["coin_return"].shift(j) for j in range(1, 6))
            d["coin"] = coin; dd.append(d)
    D = pd.concat(dd).dropna(subset=["book_return"])
    lo, hi = D["book_return"].quantile([0.05, 0.95])
    D["grp"] = np.where(D.book_return <= lo, "worst5%", np.where(D.book_return >= hi, "best5%", "mid"))
    res["book_extremes"] = D.groupby("grp")[["book_return", "coin_return", "prev_coin5", "next_coin5"]].agg(["mean", "count"]).round(4)
    return res
