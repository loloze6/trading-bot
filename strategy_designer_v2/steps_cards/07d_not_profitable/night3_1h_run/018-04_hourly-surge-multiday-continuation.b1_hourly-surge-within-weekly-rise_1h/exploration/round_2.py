import pandas as pd, numpy as np

def explore(data):
    out = {}
    try:
        rows = []
        for coin, ws in data["days"].items():
            for w, d in ws.items():
                dd = d[["day", "book_return", "coin_return"]].copy()
                dd["coin"] = coin; dd["w"] = w
                rows.append(dd)
        D = pd.concat(rows)
        D["wn"] = D["w"].str[1:].astype(int)
        B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
        B = B.dropna(subset=["book_return"]).reset_index(drop=True)
        eq = (1 + B["book_return"]).cumprod().values
        peak = np.maximum.accumulate(eq)
        dd = eq / peak - 1
        i_tr = int(np.argmin(dd)); i_pk = int(np.argmax(eq[:i_tr+1]))
        out["deepest_fall"] = pd.Series({"depth": dd[i_tr], "days": i_tr - i_pk,
            "w_start": B["wn"].iloc[i_pk], "w_end": B["wn"].iloc[i_tr],
            "coin_chain_in_fall": np.prod(1 + B["coin_return"].iloc[i_pk+1:i_tr+1].fillna(0)) - 1,
            "yearly": eq[-1] ** (365 / len(eq)) - 1, "ndays": len(eq)})
        # worst 5 drawdown episodes (distinct)
        B["dd"] = dd
        B["ep"] = (B["dd"] == 0).cumsum()
        ep = B.groupby("ep").agg(depth=("dd", "min"), days=("dd", "size"), wn=("wn", "first"),
                                 coin_chain=("coin_return", lambda s: np.prod(1 + s.fillna(0)) - 1))
        out["worst_episodes"] = ep.sort_values("depth").head(8).round(3)
        pw = []
        for wn, g in B.groupby("wn"):
            e = (1 + g["book_return"]).cumprod()
            c = (1 + g["coin_return"].fillna(0)).cumprod()
            pw.append({"w": wn, "book": e.iloc[-1] - 1, "coins": c.iloc[-1] - 1,
                       "book_mdd": (e / e.cummax() - 1).min(), "coin_mdd": (c / c.cummax() - 1).min()})
        out["per_window"] = pd.DataFrame(pw).set_index("w").round(3)
    except Exception as ex:
        out["book_err"] = str(ex)
    try:
        T = []
        for coin, ws in data["bars"].items():
            for w, b in ws.items():
                t = data["trades"][coin][w]
                if len(t) == 0: continue
                b = b.reset_index(drop=True)
                c = b["close"].astype(float)
                f = pd.DataFrame({"ts": pd.to_datetime(b["timestamp"], utc=True).dt.tz_localize(None)})
                f["idx"] = np.arange(len(b))
                f["r24"] = (c / c.shift(24) - 1).values
                f["r168"] = (c / c.shift(168) - 1).values
                f["r720"] = (c / c.shift(720) - 1).values
                hr = c.pct_change()
                f["vol_ratio"] = (hr.rolling(168).std() / hr.rolling(720).std()).values
                f["off_high720"] = (c / c.rolling(720).max() - 1).values
                f["surge_x"] = ((c / c.shift(24) - 1) / (c / c.shift(24) - 1).abs().rolling(720, min_periods=120).mean()).values
                t = t.copy()
                t["et"] = pd.to_datetime(t["entry_time"], utc=True).dt.tz_localize(None)
                t["xt"] = pd.to_datetime(t["exit_time"], utc=True).dt.tz_localize(None)
                m = pd.merge_asof(t.sort_values("et"), f.sort_values("ts"), left_on="et", right_on="ts", direction="backward")
                xi = pd.merge_asof(m[["xt"]].reset_index().sort_values("xt"), f[["ts", "idx"]], left_on="xt", right_on="ts", direction="backward").sort_values("index")["idx"].values
                cv = c.values
                ei = m["idx"].values
                p24 = []; rest24 = []
                for a, z in zip(ei, xi):
                    if np.isnan(a) or np.isnan(z): p24.append(np.nan); rest24.append(np.nan); continue
                    a = int(a); z = int(z)
                    k = min(a + 24, z)
                    p24.append(cv[k] / cv[a] - 1)
                    rest24.append(cv[z] / cv[k] - 1 if z > a + 24 else np.nan)
                m["p24"] = p24; m["rest_after24"] = rest24
                m["coin"] = coin; m["wn"] = int(w[1:])
                T.append(m)
        T = pd.concat(T)
        T = T[T["side"] == "LONG"]
        out["trades_summary"] = pd.Series({"n": len(T), "mean_net": T["net_profit_loss_percent"].mean(),
            "median_net": T["net_profit_loss_percent"].median(), "win": (T["net_profit_loss_percent"] > 0).mean(),
            "mean_dur_h": T["duration_minutes"].mean() / 60, "p10": T["net_profit_loss_percent"].quantile(.1),
            "share_below_-10": (T["net_profit_loss_percent"] < -10).mean(),
            "sum_net_of_worst10pct_over_total": T["net_profit_loss_percent"][T["net_profit_loss_percent"] <= T["net_profit_loss_percent"].quantile(.1)].sum() / T["net_profit_loss_percent"].sum()})
        for col in ["r24", "surge_x", "r168", "r720", "vol_ratio", "off_high720", "p24"]:
            x = T.dropna(subset=[col])
            q = pd.qcut(x[col], 5, labels=False, duplicates="drop")
            g = x.groupby(q)
            out["q_" + col] = pd.DataFrame({"lo": g[col].min(), "hi": g[col].max(), "n": g.size(),
                "mean_net": g["net_profit_loss_percent"].mean(),
                "sd_net": g["net_profit_loss_percent"].std(),
                "p10_net": g["net_profit_loss_percent"].quantile(.1),
                "rest_after24_pct": g["rest_after24"].mean() * 100}).round(4)
        out["by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median", "min"]).round(3)
        # concurrency: number of coins entering in the same 24h
        T["eday"] = T["et"].dt.floor("D")
        cnt = T.groupby("eday")["coin"].transform("nunique")
        T["same_day_entries"] = cnt
        g = T.groupby(pd.cut(cnt, [0, 1, 2, 3, 6]))
        out["by_same_day_entries"] = pd.DataFrame({"n": g.size(), "mean_net": g["net_profit_loss_percent"].mean(),
            "p10": g["net_profit_loss_percent"].quantile(.1)}).round(3)
    except Exception as ex:
        out["trades_err"] = str(ex)
    return out
