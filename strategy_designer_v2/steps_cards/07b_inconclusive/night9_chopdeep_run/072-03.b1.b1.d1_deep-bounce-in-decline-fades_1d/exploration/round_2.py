def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [3, 5, 7, 10]
    drift = {}
    for coin, wins in bars.items():
        dr = {}
        for h in H:
            r = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                r.extend(list(c[idx + h] / c[idx] - 1))
            dr[h] = np.mean(r) if r else np.nan
        drift[coin] = dr

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
    for G in [5, 10]:
        rows = []
        for coin, wins in bars.items():
            for w, df in wins.items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                f = df["forecast"].fillna(0).values
                rawc = df.get("debug_info.components.depth.last_history_value")
                raw = rawc.values if rawc is not None else np.full(len(df), np.nan)
                ts = pd.to_datetime(df["timestamp"])
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
                    cell = i // G
                    if cell in seen:
                        continue
                    seen.add(cell)
                    row = dict(coin=coin, win=w, year=ts[i].year, day=ts[i].normalize(), fc=f[i], raw=raw[i])
                    for h in H:
                        row[f"u{h}"] = -(c[i + h] / c[i] - 1 - drift[coin][h]) if i + h < len(c) else np.nan
                        row[f"t{h}"] = -(c[i + h] / c[i] - 1) if i + h < len(c) else np.nan
                    rows.append(row)
        d = pd.DataFrame(rows)
        out[f"grid{G}_by_h_unusual"] = pd.DataFrame({h: ct(d, f"u{h}") for h in H}).T
        out[f"grid{G}_by_h_total"] = pd.DataFrame({h: ct(d, f"t{h}") for h in H}).T
        med = d["fc"].abs().median()
        d["fh"] = np.where(d["fc"].abs() > med, "deep", "shallow")
        dd = d.dropna(subset=["raw"]).copy()
        rmed = dd["raw"].abs().median()
        dd["rh"] = np.where(dd["raw"].abs() > rmed, "deep", "shallow")
        for h in [5, 10]:
            a = d.groupby("fh").apply(lambda x: ct(x, f"u{h}"))
            b = dd.groupby("rh").apply(lambda x: ct(x, f"u{h}"))
            out[f"grid{G}_fc_half_u{h}"] = a
            out[f"grid{G}_raw_half_u{h}"] = b
        if G == 5:
            out["grid5_by_year_u5"] = d.groupby("year").apply(lambda x: ct(x, "u5"))
            out["grid5_by_window_u5"] = d.groupby("win").apply(lambda x: ct(x, "u5"))
            out["grid5_corr_raw_u5"] = float(dd[["raw", "u5"]].corr().iloc[0, 1])
            out["grid5_corr_fc_u5"] = float(d[["fc", "u5"]].corr().iloc[0, 1])
    return out
