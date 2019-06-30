"""
semaphore是用于控制进入数量的锁, 内部使用了condition实现.
如文件可读, 可写. 在写入时应该为一个线程写, 但是读时可以有多个线程读.
我们希望在读取时, 仅为10个线程读.
"""
import time
import threading


class Spider(threading.Thread):

    def __init__(self, url: str, semaphore: threading.Semaphore):
        super().__init__()
        self.__url = url
        self.semaphore = semaphore

    def run(self) -> None:
        time.sleep(2)
        print("获取: {}".format(self.__url))
        self.semaphore.release()


class UrlProducer(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore):
        super().__init__()
        self.__semaphore = semaphore
        self.info = None

    def run(self) -> None:
        for i in range(100):
            self.__semaphore.acquire()
            thread = Spider(r"http://baidu.com/{}".format(i), self.__semaphore)
            thread.start()


if __name__ == '__main__':
    s = threading.Semaphore(5)
    producer = UrlProducer(s)
    producer.start()
