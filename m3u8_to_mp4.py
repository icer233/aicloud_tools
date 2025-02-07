import subprocess
from pathlib import Path

import m3u8
import aiohttp
from tqdm.asyncio import tqdm_asyncio


async def load_m3u8(s, m3u8_url):
    async with s.get(m3u8_url) as r:
        return m3u8.loads(await r.text(), uri=m3u8_url)


async def fetch(s, index, segment):
    ts_name = f'{index}.ts'
    with open(f'ts/{ts_name}', 'wb') as f:
        async with s.get(segment.absolute_uri) as r:
            async for chunk in r.content.iter_chunked(64 * 1024):
                f.write(chunk)


async def download_ts(s, playlist):
    Path('ts').mkdir(exist_ok=True)
    tasks = (fetch(s, index, segment) for index, segment in enumerate(playlist.segments))
    await tqdm_asyncio.gather(*tasks)


def new_m3u8(playlist):
    for index, segment in enumerate(playlist.segments):
        segment.uri = f"ts/{index}.ts"
    playlist.dump('new.m3u8')


def m3u82mp4(capture_output=True, mp4_path='output.mp4'):
    subprocess.run(['./ffmpeg.exe',
                    '-allowed_extensions', 'ALL',
                    '-i', 'new.m3u8',
                    '-c', 'copy',
                    mp4_path
                    ], check=True, capture_output=capture_output)


def clean_up():
    for ts_file in Path('ts').iterdir():
        ts_file.unlink()
    Path('ts').rmdir()
    Path('new.m3u8').unlink()


async def mainfunc(m3u8_url, mp4path):
    connector = aiohttp.TCPConnector(limit=8)
    async with aiohttp.ClientSession(connector=connector) as s:
        print(f'正在读取m3u8链接：{m3u8_url}')
        playlist = await load_m3u8(s, m3u8_url)
        # logging.info('正在下载ts文件')
        await download_ts(s, playlist)
    # logging.info('正在生成新的m3u8文件')
    new_m3u8(playlist)
    # logging.info('正在转换新的m3u8文件为mp4文件')
    m3u82mp4(mp4_path=mp4path)
    # logging.info('正在清理临时文件')
    clean_up()