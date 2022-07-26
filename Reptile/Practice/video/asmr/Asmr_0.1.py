# _*_ coding: utf-8 _*_
"""
# @Time : 2022/2/18 23:06
# @Author : 陌上归云
# @Version：V 0.1
# @File : Asmr_0.1.py
# @desc :
"""
import os
import re
import requests
from Crypto.Cipher import AES


def get_m3u3(num):
    url = 'https://www.733sm.com/e/DownSys/play/?classid=5&id=' + str(num)
    headers = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'
    }

    page_video = requests.get(url=url, headers=headers).text
    url_m3u3 = re.findall('url: (.*?),', page_video, re.S)
    print(url_m3u3)
    # video_name = re.findall()
    return url_m3u3


def down_m3u3(url):
    base_url = url[:url.rfind('/') + 1]
    # print(base_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    rs = requests.get(url, headers=headers).text
    list_content = rs.split('\n')
    player_list = []
    video_path = r'../../../Data/video/'
    # 如果没有merge文件夹则新建merge文件夹，用于存放ts文件
    if not os.path.exists(video_path):
        os.makedirs(video_path)

    for index, line in enumerate(list_content):
        if '#EXTINF' in line:
            # 如果没有加密，构造出url链接
            if 'ad0.ts' not in list_content[index + 1]:
                href = base_url + list_content[index + 1]
                player_list.append(href)

    print(player_list)  # 打印ts地址列表
    print("视频文件", len(player_list))
    for i, j in enumerate(player_list):
        res = requests.get(j, headers=headers)
        with open(video_path + str(i + 1) + '.ts', 'wb') as file:
            file.write(res.content)
            print('正在写入第{}个文件'.format(i + 1))
    print('下载完成')


def merge_ts():
    path = r'../../../Data/video/'
    merge_cmd = 'copy /b ' + path + '\*.ts ' + path + '\\new.mp4'
    del_cmd = 'del ' + path + '\*.ts'
    os.system(merge_cmd)  # 执行合并命令
    os.system(del_cmd)  # 执行删除命令
    print('合并完成')


if __name__ == "__main__":
    # 指定视频编号
    # num = 607
    num = input("输入视频编号：")

    # 获取指定格式文件
    # test_m3u3_url = get_m3u3(num)
    m3u3_url = 'https://cdn3.sydwzpks.com:4433/duoda/' + str(num)+'/index.m3u8'
    # 下载
    down_m3u3(m3u3_url)
    # 合并
    merge_ts()
