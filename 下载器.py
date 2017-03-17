# -*- coding: utf-8 -*-
"""
@author: homerX
"""

import logging
import json
import os

import asyncio
import aiohttp
from asyncio import Queue

from config import URL,data_file,downloaded_file,media_file

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s', )
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



async def downloader(q_pre):

    while True:
    
        data = await q_pre.get()
        if not data:
            await q_pre.put(None)
            break
        index,part = data[0],data[1]
        p = 0
        retry_times = 0
        while p <= part and retry_times < 10:
            url = URL.format(index,p)    
            try:
                async with aiohttp.request('GET',url=url) as rsp:
                    
                    if rsp.status == 200:
                        content = await rsp.read()
                        with open(os.path.join(media_file,'{}.ts'.format(index)),'ab') as f:
                            f.write(content)
                            logger.info('file:{0:} part:{1:} have been downloaded'.format(index,p))
                        p += 1
                        retry_times = 0
                    else:
                        logger.error('fail to get {0:}:{1:} try again! try times:{2}'.format(index,p,retry_times))
                        retry_times += 1
            except:
                logger.error('fail to get {0:}:{1:} try again! try times:{2}'.format(index,p,retry_times))
                retry_times += 1
        if p > part:
            logger.info('file {0} have been downloaded'.format(index))
            downloaded_urls.append(index)
        else:
            logger.error('error happend when downliading file{0}'.format(index))



async def link_producer(q_pre,num):
    count = 0
    for index,part in pre_urls.items():
        if index not in downloaded_urls:
            await q_pre.put([index,part])
            count += 1
        if count > num:
            break
    await q_pre.put(None)


def get_pre_from_json():
    try:
        with open(data_file,'r+') as f:
            return json.loads(f.read())
    except:
        logger.error('请用搜索器获取数据')
        return
     

def get_downloaded_from_json():
    try:
        with open(downloaded_file,'w+') as f:
            data = f.read()
            return json.loads(data) if data else []
    except:
        logger.error('error happened when get downloaded file')
        return []

def save_downloaded(data):
    try:
        with open(downloaded_file,'w+') as f:
            f.write(json.dumps(data))
    except:
        logger.error('error happened when get downloaded file')
        return

if __name__ == '__main__':

    if not os.path.exists(downloaded_file):
        os.mkdir(downloaded_file)
    pre_urls = get_pre_from_json()
    downloaded_urls = get_downloaded_from_json()
    file_num = 20
    #你需要下载的福利视频数
    task_num = 5
    #开的线程数
    q_pre = asyncio.Queue()
    loop = asyncio.get_event_loop()
    tasks = [link_producer(q_pre,file_num)]+[downloader(q_pre) for i in range(task_num)]
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    save_downloaded(downloaded_urls)