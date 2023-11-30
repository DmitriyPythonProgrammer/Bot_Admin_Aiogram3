import asyncio
import main

if __name__ == "__main__":
    try:
        asyncio.run(main.main())
    except KeyboardInterrupt:
        pass
