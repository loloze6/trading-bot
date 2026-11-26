import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [3, 5, 10, 20]
    rows = []
    stats = {}
    # coin drift / usual move per horizon
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            rs = np.array(rs)
            stats[(coin, h)] = (rs.mean() if len(rs) else np.nan, rs.std(ddof=1) if len(rs) > 1 else np.nan)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            c = df["close"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            level = 0.0
            bet = np.zeros(n, bool)
            for i in range(n):
                if f[i] <= 0:
                    level = 0.0
                    continue
                if f[i] - level >= 2:
                    bet[i] = True
                    level = f[i]
                else:
                    level = min(level, f[i]) if level > 0 else level
            # streak length from closes
            up = np.r_[False, c[1:] > c[:-1]]
            st = np.zeros(n, int)
            for i in range(1, n):
                st[i] = st[i - 1] + 1 if up[i] else 0
            seen = set()
            for i in np.where(bet)[0]:
                cell = i // 10
                if cell in seen or i + 10 >= n:
                    continue
                seen.add(cell)
                r = {"coin": coin, "win": w, "day": ts[i].normalize(), "year": ts[i].year,
                     "fc": f[i], "streak": st[i],
                     "ret30": c[i] / c[i - 30] - 1 if i >= 30 else np.nan}
                for h in H:
                    if i + h < n:
                        m, s = stats[(coin, h)]
                        r[f"u{h}"] = c[i + h] / c[i] - 1 - m
                        r[f"s{h}"] = (c[i + h] / c[i] - 1 - m) / s
                rows.append(r)
    cs = pd.DataFrame(rows)

    def ct(d, col):
        d = d.dropna(subset=[col])
        if len(d) < 5:
            return pd.Series({"n": len(d), "days": d["day"].nunique(), "mean": d[col].mean() if len(d) else np.nan, "t": np.nan})
        m = d[col].mean()
        g = (d[col] - m).groupby(d["day"]).sum()
        D = len(g)
        se = np.sqrt((g ** 2).sum() * D / (D - 1)) / len(d)
        return pd.Series({"n": len(d), "days": D, "mean": m, "t": m / se})

    out = {}
    out["overall_by_horizon"] = pd.DataFrame({h: ct(cs, f"u{h}") for h in H}).T
    out["strength_by_horizon"] = pd.DataFrame({h: ct(cs, f"s{h}") for h in H}).T
    out["by_coin_10"] = cs.groupby("coin").apply(lambda d: ct(d, "u10"))
    out["by_year_10"] = cs.groupby("year").apply(lambda d: ct(d, "u10"))
    cs["fc_t"] = pd.qcut(cs["fc"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["by_fc_tercile"] = pd.concat({h: cs.groupby("fc_t").apply(lambda d: ct(d, f"u{h}")) for h in H})
    cs["r30_t"] = pd.qcut(cs["ret30"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["by_ret30_tercile"] = pd.concat({h: cs.dropna(subset=["ret30"]).groupby("r30_t").apply(lambda d: ct(d, f"u{h}")) for h in H})
    cs["stk"] = cs["streak"].clip(upper=6)
    out["by_streak_len"] = pd.concat({h: cs.groupby("stk").apply(lambda d: ct(d, f"u{h}")) for h in [5, 10]})
    big = cs["coin"].isin(["BTCUSD", "ETHUSD", "LTCUSD", "XMRUSD", "XRPUSD", "ZECUSD"])
    out["default6_vs_others_10"] = pd.DataFrame({"default6": ct(cs[big], "u10"), "others": ct(cs[~big], "u10")}).T
    out["median_u10"] = float(cs["u10"].median())
    out["share_pos_u10"] = float((cs["u10"] > 0).mean())
    return out
