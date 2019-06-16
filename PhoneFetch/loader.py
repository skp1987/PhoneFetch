import asyncio
import aiohttp
import re
from typing import List

URLs = ['https://hands.ru/company/about/',
        'https://repetitors.info/',
        'http//invalid.url']


async def fetch_async(url: str, semaphore: asyncio.locks.Semaphore):
    await semaphore.acquire()
    body = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                body = await response.text()
            await asyncio.sleep(0)
            await session.close()
    except aiohttp.InvalidURL:
        print('Invalid URL:\n' + str(url))
    except aiohttp.ClientResponseError as err:
        print('Error ' + str(err.status) + '\n' + err.message)
    except Exception as err:
        print('Unexpected error:\n\n' + str(err))
    finally:
        semaphore.release()
        return body


async def launcher(urls: List[str], num_workers: int = 5):
    phone_numbers = set()
    r_phones = re.compile(
        r'[\s>:\'"]((\+7|8)([\s\-]?|([\s\-]\()|(\)[\s\-])|(\s?-\s?))(\d([\s\-]?|([\s\-]\()|(\)[\s\-])|(\s?-\s?))){9}\d|[1-9]([\s\-]?|([\s\-]\()|(\)[\s\-])|(\s?-\s?))(\d([\s\-]?|([\s\-]\()|(\)[\s\-])|(\s?-\s?))){5}\d)[^\da-zA-Z]\D{2}')
    worker_pool = asyncio.Semaphore(num_workers)
    workers = [fetch_async(URL, worker_pool) for URL in urls]
    for i, worker in enumerate(asyncio.as_completed(workers)):
        body = await worker
        if body is not None:
            result = [re.sub(r'^(\d{7})$', r'8495\1', re.sub(r'\D', '', re.sub(r'\+7', '8', num[0])))
                      for num in r_phones.findall(body)]
            for num in result:
                phone_numbers.add(num)
    # Additional iteration needed for correct closing loop
    await asyncio.sleep(0)
    return phone_numbers


def phone_fetch(urls: List[str], num_workers: int = 5):
    loop = asyncio.new_event_loop()
    try:
        phone_numbers = loop.run_until_complete(launcher(urls))
    finally:
        loop.close()
    return phone_numbers


if __name__ == '__main__':
    print(phone_fetch(URLs))
