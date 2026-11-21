import pandas as pd, numpy as np

def explore(data):
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            pos = b["postRebalance_current_allocation"].astype(float)
            nxt = c.shift(-1) / c - 1
            f = pd.DataFrame({
                "g": (pos * nxt).values,
                "pos": pos.values,
                "nxt": nxt.values,
                "r720": (c / c.shift(720) - 1).values,
                "r168": (c / c.shift(168) - 1).values,
                "off": (c / c.rolling(720).max() - 1).values,
                "r72": (c / c.shift(72) - 1).values,
            })
            f["coin"] = coin
            f["wn"] = int(w[1:])
            rows.append(f)
    F = pd.concat(rows).dropna(subset=["g"])
    drift = F.groupby("coin")["nxt"].mean()
    F["timing"] = F["g"] - F["pos"] * F["coin"].map(drift)
    F["loss"] = F["g"].clip(upper=0)
    tot_loss = F["loss"].sum()
    for col in ["r720", "off", "r72"]:
        x = F.dropna(subset=[col])
        q = pd.qcut(x[col], 5, labels=False, duplicates="drop")
        g = x.groupby(q)
        out["by_" + col] = pd.DataFrame({
            "lo": g[col].min(), "hi": g[col].max(),
            "mean_pos": g["pos"].mean(),
            "gain_bps_per_bar": g["g"].mean() * 1e4,
            "timing_bps": g["timing"].mean() * 1e4,
            "share_of_total_gain": g["g"].sum() / x["g"].sum(),
            "share_of_losses": g["loss"].sum() / tot_loss,
            "sd_gain_bps": g["g"].std() * 1e4,
        }).round(3)
    x = F.dropna(subset=["r720"])
    x["state"] = np.where(x["r720"] > 0, "up30", "down30")
    g = x[x["pos"] > 0].groupby("state")
    out["long_bars_by_30d_sign"] = pd.DataFrame({
        "n": g.size(),
        "gain_bps": g["g"].mean() * 1e4,
        "t": g["g"].mean() / (g["g"].std() / np.sqrt(g.size())),
        "coin_next_bps": g["nxt"].mean() * 1e4,
    }).round(3)
    return out
