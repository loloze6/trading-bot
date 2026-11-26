def explore(data):
    import pandas as pd, numpy as np
    out = {}
    out["top_keys"] = pd.Series({k: type(v).__name__ for k, v in data.items()}) if isinstance(data, dict) else str(type(data))
    info = []
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict):
                for coin, ws in v.items():
                    if isinstance(ws, dict):
                        for w, df in ws.items():
                            n = len(df) if hasattr(df, "__len__") else -1
                            ncol = df.shape[1] if hasattr(df, "shape") and len(getattr(df, "shape", ())) > 1 else -1
                            info.append((k, str(coin), str(w), type(df).__name__, n, ncol))
                    else:
                        n = len(ws) if hasattr(ws, "__len__") else -1
                        info.append((k, str(coin), "-", type(ws).__name__, n, -1))
            else:
                n = len(v) if hasattr(v, "__len__") else -1
                info.append((k, "-", "-", type(v).__name__, n, -1))
    out["structure"] = pd.DataFrame(info, columns=["table", "coin", "w", "type", "rows", "cols"]) if info else "no entries"
    out["n_entries"] = len(info)
    return out
