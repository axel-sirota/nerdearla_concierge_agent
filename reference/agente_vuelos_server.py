"""Reference: the Lab 1 mechanism, verified working on 2026-09-21.

This is the shape the notebook writes to disk with %%writefile and then reaches
through MCPAdapter. Kept here so the working pattern survives even if a research
cycle later rewrites the notebook cells.

Run the round trip with:
    .venv/bin/python3 reference/agente_vuelos_client.py
"""
from mcp.server.mcpserver import MCPServer

# NOT FastMCP. mcp 2.x renamed it to MCPServer and removed mcp.server.fastmcp.
mcp = MCPServer("agente-vuelos")


@mcp.tool()
def buscar_vuelos(origen: str, destino: str) -> str:
    """Busca vuelos entre dos ciudades."""
    # Datos fijos a proposito: en un taller en vivo no dependemos de una API externa
    # que puede caerse o tener rate limit justo cuando hay 200 personas mirando.
    return f"Vuelo {origen} a {destino}: AR1234, 08:15, ARS 145000"


if __name__ == "__main__":
    mcp.run()
