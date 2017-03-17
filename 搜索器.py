# -*- coding: utf-8 -*-
"""
@author: homerX
"""

import logging
import json

import asyncio
import aiohttp

from config import URL,data_file

logging.basicConfig(level=logging.DEBUG,
format='%(asctime)s %(message)s', )
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

coroutine_num = 400
#根据你机器配置决定你开的协程数量
deep = 20000//coroutine_num

#detector 搜索该url是否有效,若有效搜索视频块长度
async def detector(i):
    k = 0
    p = -1
    t = 0
    while True:
        url = URL.format(i,k)    
        try:
            async with aiohttp.request('GET',url=url,chunked=1) as rsp:
                
                if rsp.status == 200:
                    if p == -1:
                        k =  k<<1 if k else 2
                    elif p > 1:
                        p = p>>1
                        k += p
                    else:
                        logger.info('file {0:}: end with part{1:} '.format(i,k))
                        data[str(i)] = k
                        break
                else:
                    if k:
                        if p == -1:
                            k = k>>1
                            p = k>>1
                            k = k+p
                        elif p > 1:
                            p = p>>1
                            k = k-p
                        else:
                            logger.info('file {0:}: end with part{1:} '.format(i,k-1))
                            data[str(i)] = k-1
                            break
                    else:
                        break
        except:
            logger.error('error happened when get {0:}:{1:}'.format(i,k))
            t+=1
            if t>3:
                break


async def run(l):
    for i in range(deep):
        await detector(deep*l+i+190000)



if __name__ == '__main__':

  
    global data
    data= {}
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(run(i)) for i in range(coroutine_num)]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()


    with open(data_file,'w') as f:
            f.write(json.dumps(data))

