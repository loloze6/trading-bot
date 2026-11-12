def explore(data):
    import numpy as np, pandas as pd
    out = {}
    b = data["bars"]["BTCUSD"]["w1"].reset_index(drop=True)
    raw = b["debug_info.components.rsi_high.last_history_value"]
    rsi = 50 - raw
    f = b["forecast"]
    ts = pd.to_datetime(b["timestamp"])
    out["span_days"] = float((ts.iloc[-1]-ts.iloc[0]).total_seconds()/86400)
    out["years"] = ts.dt.year.value_counts().sort_index()
    out["implied_rsi_quantiles"] = rsi.quantile([0, .05, .25, .5, .75, .95, 1.0])
    out["implied_rsi_share_above"] = pd.Series({k: float((rsi > k).mean()) for k in [50, 55, 60, 65, 70]})
    out["implied_rsi_when_fc<=-10"] = rsi[f <= -10].describe()
    out["implied_rsi_when_fc_0"] = rsi[f == 0].describe()
    m = (f <= -10).astype(int)
    grp = (m.diff().fillna(m.iloc[0]) != 0).cumsum()
    lens = m.groupby(grp).agg(["first", "size"])
    out["episode_lengths_fc<=-10"] = lens[lens["first"] == 1]["size"].reset_index(drop=True)
    fwd = b["close"].shift(-5)/b["close"]-1
    ex = fwd - fwd.mean()
    out["fwd5_sd_all_bars"] = float(fwd.std())
    out["fwd5_mean_all_bars"] = float(fwd.mean())
    sd = float(ex[f <= -10].std())
    out["sd_excess_extreme_bars"] = sd
    eff = 0.0234
    out["cases_needed_t2_at_effect_0.023"] = float((2*sd/eff)**2) if sd > 0 else np.nan
    out["cases_needed_t2_at_effect_0.0675"] = float((2*sd/0.0675)**2) if sd > 0 else np.nan
    out["warmup_bars_before_standardise_ready"] = int(b["debug_info.components.rsi_high.post_pipeline_value"].isna().sum())
    return out
