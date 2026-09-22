"""Reference: the client half of the Lab 1 mechanism, verified 2026-09-21.

Demonstrates the two things most likely to go wrong live:

1. MCPAdapter takes a Path for a local stdio server, never a plain string. A string
   is only accepted when it is an http(s) URL, deliberately, so that a string arriving
   from configuration or from a model cannot trigger local execution.
2. Invoking a tool returns a list of content blocks, not a bare string.

Run it:
    .venv/bin/python3 reference/agente_vuelos_client.py
"""
import asyncio
from pathlib import Path

from langchain.mcp import MCPAdapter

SERVER = Path(__file__).parent / "agente_vuelos_server.py"


async def main() -> None:
    # Path, not str. This is the trap.
    adapter = MCPAdapter(SERVER)

    tools = await adapter.list_tools()
    print("tools:", [t.name for t in tools])

    buscar = tools[0]
    resultado = await buscar.ainvoke({"origen": "Buenos Aires", "destino": "Bariloche"})

    # resultado is a list of content blocks: [{'type': 'text', 'text': ..., 'id': ...}]
    print("raw:", resultado)
    print("texto:", resultado[0]["text"])


if __name__ == "__main__":
    asyncio.run(main())
