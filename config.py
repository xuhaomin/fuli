# -*- coding: utf-8 -*-
"""
@author: homerX
"""
import os

URL = 'http://2.sewewje123.com/cheng/{0:0>6}/550kb/hls/index{1:}.ts'
#福利网的url,{0}为视频编号,{1}为视频块
data_file = 'data.json'
#data是一个以{0}视频编号为键,视频块长度为值的json字典

media_file = os.path.join(os.getcwd(),"media")
#视频的保存目录
downloaded_file = 'downloaded.json'
#已下载视频的json文件,列表