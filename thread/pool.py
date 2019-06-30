"""
python 使用concurrent.future.ThreadPoolExecutor实现了线程池.
同时concurrent.future也实现了进程池, 统一了接口.

1. submit 提交要执行的函数到线程池中, 同时立即返回(非阻塞)
2. done 查看函数是否执行完了
3. result 查看函数的执行结果(阻塞方法)
4. cancel 取消函数的执行(只能在函数未执行时, 结束线程的执行)
5. as_completed 获取已经成功的函数的返回.
6. map, 返回值是函数执行的结果
7. wait 等待传入的线程执行结束后才执行主线程
"""
from concurrent.futures import (ThreadPoolExecutor,
                                as_completed,
                                wait,
                                FIRST_COMPLETED)
import time


def get_url(url: str, time_: int = 2) -> str:
    time.sleep(time_)
    print("成功获取网页: ", url, time_)
    return "success"


if __name__ == '__main__':
    exe = ThreadPoolExecutor(max_workers=5)
    url_template = r"http://www.baidu.com/{}"

    # 1. submit 提交要执行的函数到线程池中, 同时立即返回(非阻塞)
    e1 = exe.submit(get_url, url_template.format(1), 2)
    e2 = exe.submit(get_url, url_template.format(2), 3)

    # 如果在这里调用result会阻塞线程, e1.done = True
    # print(e1.result())

    # 2. done 查看函数是否执行完了, 这里因为很快的返回应该为False
    print("\n2. done")
    print("e1: ", e1.done())
    print("e2: ", e2.done())
    time.sleep(3 + 1e-10)
    print("e1: ", e1.done())
    print("e2: ", e2.done())

    # 3. result 查看函数的执行结果(阻塞方法)
    print("\n3. result")
    print(e1.result())

    # 4. cancel 取消函数的执行(只能在函数未执行时, 结束线程的执行)
    # 成功取消: True
    # 未取消: False
    print("\n4. cancel")
    exe2 = ThreadPoolExecutor(max_workers=1)
    ee1 = exe2.submit(get_url, url_template.format(1), 2)
    ee2 = exe2.submit(get_url, url_template.format(5), 3)
    print("是否成功取消网页5?", ee2.cancel())

    # 5. as_completed 获取已经成功的函数的返回.
    print("\n5. as_completed")
    all_exes = [exe.submit(get_url, url_template.format(i)) for i in range(7)]
    for e in as_completed(all_exes):
        print("{} 成功执行".format(e.result()))

    # 6. map, 返回值是函数执行的结果
    print("\n6. map")
    for result in exe.map(get_url, (url_template.format(i) for i in range(7))):
        print("{} 成功执行".format(result))

    # 7. wait 等待传入的线程执行结束后才执行主线程, return_when参数有:
    # FIRST_COMPLETED 第一个执行结束后
    # FIRST_EXCEPTION 当有线程抛出异常后, 如果没有异常, 全部执行完成后执行主线程
    # ALL_COMPLETED 全部执行结束后(默认)
    print("\n7.1. wait")
    exe3 = ThreadPoolExecutor(max_workers=2)
    all_exes = [exe3.submit(get_url, url_template.format(i), i)
                for i in range(5)]
    wait([all_exes[0], all_exes[3]])
    print("="*30 + "\nmain\n" + "="*30)

    time.sleep(2)
    print("\n7.2. wait")
    exe4 = ThreadPoolExecutor(max_workers=2)
    all_exes = [exe4.submit(get_url, url_template.format(i), i)
                for i in range(5)]
    wait([all_exes[0], all_exes[3]], return_when=FIRST_COMPLETED)
    print("=" * 30 + "\nmain\n" + "=" * 30)




