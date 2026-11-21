def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            n = len(b)
            dec = (b["regime"] == "mean_reversion").sum()
            col = "debug_info.components.combo.post_pipeline_value"
            combo = b[col].notna().sum() if col in b else 0
            yr = pd.to_datetime(b["timestamp"]).dt.year.iloc[0]
            rows.append(dict(coin=coin, window=w, year=yr, bars=n, decline_bars=dec, combo_bars=combo,
                             decline_grid5=int((b["regime"].iloc[::5] == "mean_reversion").sum())))
    df = pd.DataFrame(rows)
    per_win_len = df.groupby("window")["bars"].agg(["min", "max", "mean"])
    per_coin = df.groupby("coin")[["bars", "decline_bars", "combo_bars", "decline_grid5"]].sum()
    per_year = df.groupby("year")[["bars", "decline_bars", "decline_grid5"]].sum()
    return {
        "window length (bars) by window": per_win_len,
        "per coin totals": per_coin,
        "per year totals": per_year,
        "max window length overall": int(df["bars"].max()),
        "windows with >= 370 bars": int((df["bars"] >= 370).sum()),
        "total decline grid cases": int(df["decline_grid5"].sum()),
    }
