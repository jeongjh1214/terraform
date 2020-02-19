#!/bin/python3
import asyncio

async def whoami_after_sleep(name, t):
  print(f'I am {name} and gonna sleep for {t} seconds.')
  await asyncio.sleep(t)
  print(f'I am {name}. I slept for {t} seconds.')
  return ('result', name, t)

async def main():
  await asyncio.gather(
    whoami_after_sleep('A', 1),
    whoami_after_sleep('B', 2),
    whoami_after_sleep('C', 3),
  )


asyncio.run(main())