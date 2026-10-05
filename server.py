import os
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("Grok-Connector-by-Gemini")

XAI_API_KEY = os.environ.get("XAI_API_KEY")
XAI_BASE_URL = "https://api.xai.com/v1"

@mcp.tool()
async def ask_grok(prompt: str, model: str = "grok-2-latest", max_tokens: int = 500) -> str:
    """Sendet eine Anfrage an Grok mit festem Token-Schutz."""
    if not XAI_API_KEY:
        return "Fehler: XAI_API_KEY ist in den Umgebungsvariablen nicht gesetzt."
    
    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [
            {"role": "system", "content": "Du bist Grok, angebunden als MCP-Tool über Gemini."},
            {"role": "user", "content": prompt}
        ],
        "model": model,
        "max_tokens": min(max_tokens, 1000),
        "stream": False
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{XAI_BASE_URL}/chat/completions", json=payload, headers=headers, timeout=30.0)
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"xAI API Fehler ({response.status_code}): {response.text}"
        except Exception as e:
            return f"Verbindungsfehler zu Grok: {str(e)}"

if __name__ == "__main__":
    mcp.run()
