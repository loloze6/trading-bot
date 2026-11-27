def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        rets = {h: [] for h in H}
        for w, df in wins.items():
            c = df["close"].values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                rets[h].extend(list(c[idx + h] / c[idx] - 1))
        drift[coin] = {h: np.mean(rets[h]) if rets[h] else np.nan for h in H}
        usual[coin] = np.std(rets[10]) if rets[10] else np.nan
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            raw = df.get("debug_info.components.depth.last_history_value")
            raw = raw.values if raw is not None else np.full(len(df), np.nan)
            ts = pd.to_datetime(df["timestamp"])
            # bets: fall of forecast >=2 from shallowest short level since last bet
            ref = 0.0
            bets = []
            for i in range(len(f)):
                if f[i] >= 0:
                    ref = 0.0
                    continue
                if f[i] <= ref - 2:
                    bets.append(i)
                    ref = f[i]
                else:
                    ref = max(ref, f[i])
            seen = set()
            for i in bets:
                cell = i // 10
                if cell in seen:
                    continue
                seen.add(cell)
                r20 = c[i] / c[i - 20] - 1 if i >= 20 else np.nan
                r60 = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                dr = np.diff(np.log(c[max(0, i - 30):i + 1]))
                vol30 = dr.std() if len(dr) > 10 else np.nan
                dr_all = np.diff(np.log(c[:i + 1]))
                row = dict(coin=coin, win=w, year=ts[i].year, day=ts[i].normalize(),
                           fc=f[i], raw=raw[i], r20=r20, r60=r60, vol30=vol30,
                           dayret=c[i] / c[i - 1] - 1 if i > 0 else np.nan)
                for h in H:
                    if i + h < len(c):
                        row[f"u{h}"] = -(c[i + h] / c[i] - 1 - drift[coin][h])
                        row[f"t{h}"] = -(c[i + h] / c[i] - 1)
                    else:
                        row[f"u{h}"] = np.nan
                        row[f"t{h}"] = np.nan
                rows.append(row)
    d = pd.DataFrame(rows)

    def ct(x, col):
        x = x.dropna(subset=[col])
        n = len(x)
        if n < 5:
            return pd.Series({"n": n, "mean": np.nan, "t": np.nan, "days": 0})
        m = x[col].mean()
        s = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / n
        return pd.Series({"n": n, "mean": m, "t": m / se if se > 0 else np.nan, "days": s.size})

    out = {}
    out["by_horizon_unusual"] = pd.DataFrame({h: ct(d, f"u{h}") for h in H}).T
    out["by_horizon_total"] = pd.DataFrame({h: ct(d, f"t{h}") for h in H}).T
    out["by_coin_u10"] = d.groupby("coin").apply(lambda x: ct(x, "u10"))
    out["by_window_u10"] = d.groupby("win").apply(lambda x: ct(x, "u10"))
    out["by_year_u10"] = d.groupby("year").apply(lambda x: ct(x, "u10"))
    d["fcq"] = pd.qcut(d["fc"].rank(method="first"), 4, labels=["deepest", "q2", "q3", "shallow"])
    out["by_fc_quart_u10"] = d.groupby("fcq").apply(lambda x: ct(x, "u10"))
    dd = d.dropna(subset=["raw"])
    dd["rq"] = pd.qcut(dd["raw"].rank(method="first"), 4, labels=["deepest", "q2", "q3", "shallow"])
    out["by_raw_quart_u10"] = dd.groupby("rq").apply(lambda x: ct(x, "u10"))
    out["by_raw_quart_u5"] = dd.groupby("rq").apply(lambda x: ct(x, "u5"))
    d["r60s"] = np.where(d["r60"].isna(), "na", np.where(d["r60"] < 0, "r60neg", "r60pos"))
    out["by_r60sign_u10"] = d.groupby("r60s").apply(lambda x: ct(x, "u10"))
    d["vq"] = pd.qcut(d["vol30"].rank(method="first"), 2, labels=["lowvol", "highvol"])
    out["by_vol_u10"] = d.groupby("vq").apply(lambda x: ct(x, "u10"))
    d["r20q"] = pd.qcut(d["r20"].rank(method="first"), 3, labels=["r20_deep", "r20_mid", "r20_small"])
    out["by_r20_u10"] = d.groupby("r20q").apply(lambda x: ct(x, "u10"))
    d["drq"] = pd.qcut(d["dayret"].rank(method="first"), 2, labels=["smallup", "bigup"])
    out["by_dayret_u10"] = d.groupby("drq").apply(lambda x: ct(x, "u10"))
    out["corr_raw_u10"] = float(dd[["raw", "u10"]].corr().iloc[0, 1])
    out["drift10_mean"] = float(np.nanmean([drift[k][10] for k in drift]))
    return out
