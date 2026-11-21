def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    rows = []
    for coin, wins in bars.items():
        drift = {}; usual = {}
        for H in (8, 24, 72):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                rs.append(c[idx + H] / c[idx] - 1)
            rs = np.concatenate(rs); drift[H] = rs.mean(); usual[H] = rs.std()
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"]
            r1 = c.pct_change()
            vol24 = r1.rolling(24).std()
            vavg = vol24.rolling(720, min_periods=200).mean()
            ts = pd.to_datetime(d["timestamp"]) + pd.Timedelta(hours=1)
            pos = np.arange(len(d))
            f = pd.DataFrame({"coin": coin, "win": w, "year": ts.dt.year, "hour": ts.dt.hour,
                              "pos": pos, "vr": vol24 / vavg,
                              "r2": (c / c.shift(2) - 1) / vavg,
                              "r24": (c / c.shift(24) - 1) / vavg,
                              "u24": usual[24], "u8": usual[8],
                              "f8": c.shift(-8) / c - 1, "f24": c.shift(-24) / c - 1,
                              "f72": c.shift(-72) / c - 1,
                              "d8": drift[8], "d24": drift[24], "d72": drift[72], "u72": usual[72]})
            rows.append(f)
    B = pd.concat(rows, ignore_index=True)
    def tt(v):
        v = v.dropna(); return pd.Series({"n": len(v), "mean": v.mean(), "t": v.mean() / v.std() * np.sqrt(len(v))})
    # 1. 24h move, one per 24-bar grid cell (pos%24==0), next 24h unusual move, by sign and vol
    G = B[(B.pos % 24 == 0)].dropna(subset=["r24", "vr", "f24"]).copy()
    G["s24"] = (G.f24 - G.d24) / G.u24
    G["dir"] = np.where(G.r24 < 0, "fall", "rise")
    G["vq"] = pd.qcut(G.vr, 3, labels=["lowvol", "midvol", "highvol"])
    G["mq"] = G.groupby(["coin", "dir"])["r24"].transform(lambda s: pd.qcut(s.abs(), 3, labels=False))
    G["rev"] = -np.sign(G.r24) * G.s24
    G["revbps"] = -np.sign(G.r24) * (G.f24 - G.d24) * 1e4
    G["totbps"] = -np.sign(G.r24) * G.f24 * 1e4
    a = G.groupby(["dir", "vq", "mq"]).apply(lambda x: pd.concat([tt(x.rev), pd.Series({"unus_bps": x.revbps.mean(), "tot_bps": x.totbps.mean()})]))
    out["G1_24h_reversal_next24_dir_vol_size"] = a
    big = G[(G.dir == "fall") & (G.mq == 2) & (G.vq == "highvol")]
    out["G2_bigfall_highvol_by_coin"] = big.groupby("coin").apply(lambda x: pd.concat([tt(x.rev), pd.Series({"tot_bps": x.totbps.mean()})]))
    out["G3_bigfall_highvol_by_year"] = big.groupby("year").apply(lambda x: pd.concat([tt(x.rev), pd.Series({"tot_bps": x.totbps.mean()})]))
    # graded: within falls in high vol, regression of rev on |r24|
    hf = G[(G.dir == "fall") & (G.vq == "highvol")]
    out["G4_fall_highvol_corr_size_rev"] = float(np.corrcoef(hf.r24.abs(), hf.rev)[0, 1])
    hr = G[(G.dir == "rise") & (G.vq == "highvol")]
    out["G4b_rise_highvol_corr_size_rev"] = float(np.corrcoef(hr.r24.abs(), hr.rev)[0, 1])
    # 2. 2h reversal at all hours, 8-bar grid, by direction and size (high vol), total bps
    E = B[(B.pos % 8 == 0)].dropna(subset=["r2", "vr", "f8"]).copy()
    E = E[E.vr >= 1]
    E["dir"] = np.where(E.r2 < 0, "fall", "rise")
    E["qa"] = E.groupby("coin")["r2"].transform(lambda s: pd.qcut(s.abs(), 5, labels=False))
    E["rev"] = -np.sign(E.r2) * (E.f8 - E.d8) / E.u8
    E["tot"] = -np.sign(E.r2) * E.f8 * 1e4
    out["E1_2h_rev_8h_grid_highvol_dir_size"] = E.groupby(["dir", "qa"]).apply(lambda x: pd.concat([tt(x.rev), pd.Series({"tot_bps": x.tot.mean()})]))
    top = E[E.qa == 4]
    out["E2_top2h_by_year"] = top.groupby("year").apply(lambda x: pd.concat([tt(x.rev), pd.Series({"tot_bps": x.tot.mean()})]))
    out["E3_top2h_by_coin"] = top.groupby("coin").apply(lambda x: pd.concat([tt(x.rev), pd.Series({"tot_bps": x.tot.mean()})]))
    # 3. trades short vs long by year
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()], ignore_index=True)
    T["year"] = pd.to_datetime(T.entry_time).dt.year
    out["T1_trades_side_year"] = T.groupby(["year", "side"]).agg(n=("net_profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"), med=("profit_loss_percent", "median"))
    return out
