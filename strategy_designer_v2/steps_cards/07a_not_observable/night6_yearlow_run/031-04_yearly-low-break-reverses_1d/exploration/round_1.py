import numpy as np
import pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp")
            n = len(df)
            reg = (df["regime"] == "mean_reversion").values
            fc = df["forecast"].fillna(0).values
            yr = pd.to_datetime(df["timestamp"]).dt.year
            # episodes = starts of runs of regime bars
            starts = reg & ~np.r_[False, reg[:-1]]
            # recomputed break from window closes only (inside window, for reference)
            c = df["close"].values
            rows.append(dict(coin=coin, window=w, year=int(yr.iloc[0]), bars=n,
                             regime_bars=int(reg.sum()), episodes=int(starts.sum()),
                             regime_bars_fc_pos=int(((fc > 0) & reg).sum()),
                             regime_bars_fc_ge2=int(((fc >= 2) & reg).sum()),
                             max_fc=float(fc[reg].max()) if reg.any() else np.nan))
    t = pd.DataFrame(rows)
    by_coin = t.groupby("coin")[["bars", "regime_bars", "episodes", "regime_bars_fc_pos", "regime_bars_fc_ge2"]].sum()
    by_year = t.groupby("year")[["bars", "regime_bars", "episodes", "regime_bars_fc_pos", "regime_bars_fc_ge2"]].sum()
    by_win = t.groupby("window")[["bars", "regime_bars", "episodes", "regime_bars_fc_ge2"]].sum()
    # forecast distribution on regime bars
    fcs = []
    comps = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            m = df["regime"] == "mean_reversion"
            fcs.append(df.loc[m, "forecast"])
            col = "debug_info.components"
            if col in df.columns:
                comps.append(df.loc[m, col].astype(str).str[:120])
    fcs = pd.concat(fcs)
    dist = fcs.describe()
    bins = pd.cut(fcs.fillna(0), [-0.01, 0, 1, 2, 5, 10, 20.01]).value_counts().sort_index()
    sample = pd.Series(comps[0].head(3).values) if comps and len(comps[0]) else "none"
    # episode lengths
    lens = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            reg = (df["regime"] == "mean_reversion").astype(int).values
            run = 0
            for v in reg:
                if v: run += 1
                elif run: lens.append(run); run = 0
            if run: lens.append(run)
    lens = pd.Series(lens)
    # window length stats
    wl = t["bars"].describe()
    # 10-day returns from regime bars (non-overlapping grid) to see variability
    out = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values; reg = (df["regime"] == "mean_reversion").values
            for i in range(0, len(df) - 10, 10):
                seg = np.where(reg[i:i+10])[0]
                if len(seg):
                    j = i + seg[0]
                    if j + 10 < len(df):
                        out.append(c[j+10]/c[j]-1)
    out = pd.Series(out)
    return {"by_coin": by_coin, "by_year": by_year, "by_window": by_win,
            "fc_on_regime_bars": dist, "fc_bins": bins, "episode_len": lens.describe(),
            "window_len": wl, "first_regime_bar_per_cell_10d_ret": out.describe(),
            "debug_sample": sample}
