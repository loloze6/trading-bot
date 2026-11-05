"""The one model call of v2. Closed book, like v1: no tools, no settings files, a neutral cwd.
With the SDK installed (the PC): one call, the answer text returned, cost recorded.
Without it (this container): the prompt is written to <out>.prompt.md and the runner stops;
whoever answers writes <out>; the runner resumes on the next call because <out> exists."""
import asyncio, pathlib, tempfile, datetime as dt, yaml

try:
    from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock  # type: ignore
    HAVE_SDK = True
except Exception:  # noqa: BLE001
    HAVE_SDK = False


def _strip_fences(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
        t = t.rsplit("```", 1)[0]
    return t.strip() + "\n"


async def _call(prompt: str, model: str):
    opts = ClaudeAgentOptions(model=model, tools=[], setting_sources=[], cwd=tempfile.mkdtemp(prefix="sdv2_"))
    text, cost = "", None
    async for m in query(prompt=prompt, options=opts):
        if isinstance(m, AssistantMessage):
            for b in m.content:
                if isinstance(b, TextBlock):
                    text += b.text
        if hasattr(m, "total_cost_usd"):
            cost = getattr(m, "total_cost_usd", None)
    return text, cost


def ask(prompt: str, out: pathlib.Path, model: str, log: pathlib.Path) -> bool:
    """Write the model's answer to `out`. Returns True when `out` exists after the call."""
    out = pathlib.Path(out)
    if out.exists():
        return True
    if not HAVE_SDK:
        out.with_suffix(out.suffix + ".prompt.md").write_text(prompt, encoding="utf-8")
        print(f"ANSWER NEEDED: model not reachable here; prompt at {out}.prompt.md; write the answer to {out}")
        return False
    text, cost = asyncio.run(_call(prompt, model))
    out.write_text(_strip_fences(text), encoding="utf-8")
    rows = yaml.safe_load(log.read_text()) if log.exists() else []
    rows.append({"at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "model": model, "out": str(out), "cost_usd": cost})
    log.write_text(yaml.safe_dump(rows, sort_keys=False), encoding="utf-8")
    return True
