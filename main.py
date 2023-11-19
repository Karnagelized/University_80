
import asyncio
from classes import Program

async def main():
    await Program().run()


if __name__ == '__main__':
    asyncio.run(main())
