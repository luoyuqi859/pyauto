import asyncio
import time


async def play_game():
    """玩游戏"""
    print('start play_game')
    await asyncio.sleep(1)
    print("play_game...")
    await asyncio.sleep(1)
    print("play_game...")
    await asyncio.sleep(1)
    print('end play_game')
    return "游戏gg了"


async def dian_wai_mai():
    """点外卖"""
    print("dian_wai_mai")
    await asyncio.sleep(1)
    print("wai_mai on the way...")
    await asyncio.sleep(1)
    print("wai_mai on the way...")
    await asyncio.sleep(1)
    print("wai_mai arrive")
    return "外卖到了"


async def main():
    print("start main")
    future1 = asyncio.create_task(play_game())
    future2 = asyncio.create_task(dian_wai_mai())
    ret1 = await future1
    ret2 = await future2
    print(ret1, ret2)
    print("end main")


async def main1():
    print("start main")
    future1 = asyncio.create_task(play_game())
    future2 = asyncio.create_task(dian_wai_mai())
    ret1, ret2 = await asyncio.gather(future1, future2)
    print(ret1, ret2)
    print("end main")


async def main2():
    print("start main")
    future1 = play_game()
    future2 = dian_wai_mai()
    ret1, ret2 = await asyncio.gather(future1, future2)
    print(ret1, ret2)
    print("end main")


if __name__ == '__main__':
    t1 = time.time()
    asyncio.run(main())
    t2 = time.time()
    print('cost:', t2 - t1)
