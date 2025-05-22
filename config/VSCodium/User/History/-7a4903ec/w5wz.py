import asyncio
from endpoints.create_er_diagram import generate_er_diagram_endpoint

async def main():
    await generate_er_diagram_endpoint("p38yma98zod5uc1")

if __name__ == "__main__":
    asyncio.run(main())
