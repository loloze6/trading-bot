def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            r = b.close.pct_change()
            mad = r.abs().rolling(720, min_periods=200).mean().shift(1)
            df = pd.DataFrame({"coin": c, "w": w})
            df["z"] = r / mad
            df["vr"] = b.volume / b.volume.rolling(720, min_periods=200).mean()
            df["r24"] = b.close / b.close.shift(24) - 1
            sd24 = (b.close / b.close.shift(24) - 1).rolling(720, min_periods=200).std()
            df["zs24"] = df.r24 / sd24
            df["f24"] = b.close.shift(-24) / b.close - 1
            df["f6"] = b.close.shift(-6) / b.close - 1
            df["idx"] = np.arange(len(b))
            df["year"] = pd.to_datetime(b.timestamp).dt.year.values
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[A.idx % 24 == 0].dropna(subset=["zs24", "f24"]).copy()
    usual = G.groupby("coin").f24.std()
    G["u24"] = G.f24 - G.coin.map(G.groupby("coin").f24.mean())
    G["s"] = -np.sign(G.zs24)  # reversal direction
    G["su"] = G.s * G.u24
    G["st"] = G.su / G.coin.map(usual)
    G["tot"] = G.s * G.f24
    def tt(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "bp": s.mean() * 1e4, "t": s.mean() / (s.std() / np.sqrt(len(s)))})
    G["zb"] = pd.cut(G.zs24.abs(), [0, 0.5, 1, 1.5, 2, np.inf])
    out["rev24_su_by_size"] = G.groupby("zb", observed=True).su.apply(tt).unstack()
    out["rev24_strength_by_size"] = G.groupby("zb", observed=True).st.mean()
    out["rev24_total_by_size_bp"] = G.groupby("zb", observed=True).tot.mean() * 1e4
    big = G[G.zs24.abs() > 1]
    out["rev24_big_by_coin"] = big.groupby("coin").su.apply(tt).unstack()
    out["rev24_big_by_year"] = big.groupby("year").su.apply(tt).unstack()
    out["rev24_big_by_side"] = big.groupby(np.where(big.zs24 > 0, "after_rise", "after_fall")).su.apply(tt).unstack()
    out["usual_24h_move"] = usual
    # quiet rises, 24h horizon, by prior-24h sign
    Q = A[(A.idx % 24 == 0) & (A.vr.between(0.5, 1.5)) & (A.z > 1.5)].dropna(subset=["f24", "r24"]).copy()
    Q["u24"] = Q.f24 - Q.coin.map(G.groupby("coin").f24.mean())
    out["quiet_rise_short_u24_by_prior_day"] = Q.groupby(np.where(Q.r24 > 0, "day_up", "day_down")).u24.apply(
        lambda s: tt(-s)).unstack()
    return out
