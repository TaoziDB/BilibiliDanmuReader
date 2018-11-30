#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import asyncio
from crawler import Crawler
from message_handle import MessageHandler
from text2voice import Speaker


class Bilibili_Client:
    def __init__(self, crawler, message_handle):
        self._crawler = crawler
        self._message_handle = message_handle

    async def run(self):
        crawl_loop = self._crawler.crawl()
        heart_beat_loop = self._crawler.heart_beat_loop()
        reader_loop = self._message_handle.read_loop()
        tasks = [asyncio.ensure_future(crawl_loop), asyncio.ensure_future(heart_beat_loop),
                 asyncio.ensure_future(reader_loop)]
        done, pending = await asyncio.wait(tasks)
        for task in done:
            print('Task ret: ', task.result())


if __name__ == '__main__':
    spk = Speaker()
    queue = asyncio.Queue()
    uid = 687627

    reader = MessageHandler(spk, queue)
    crawler = Crawler(uid, queue)

    client = Bilibili_Client(crawler, reader)

    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(client.run())
    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt as e:
        print(asyncio.Task.all_tasks())
        print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()