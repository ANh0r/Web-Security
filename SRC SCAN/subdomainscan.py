# -*- coding:utf-8 -*-

import asyncio
import dns.resolver
import traceback
import dns.rdatatype
from concurrent.futures import ThreadPoolExecutor
# 把同步的方法放在线程->转换成异步


def query(resolver,task):
    try:
        result = dns.resolver.resolve(task, 'A')
        # 目前是同步的 不是异步 如果要加速需要将同步转化为异步
        # await rq.put({'domain': task, 'result': result})
        # ==resolver.query
        return result
    except dns.resolver.NXDOMAIN:
        return None
    except dns.resolver.NoAnswer:
        return None
    except dns.resolver.NoNameservers:
        return None
    except dns.resolver.Timeout:
        return task
    except Exception as e:
        traceback.print_exc()


async def read_dict(file,tq,target):
    await tq.put(target)
    with open(file,'r') as fp:
        for line in fp.readlines():
            await tq.put(f'{line.strip()}.{target}')
            pass


async def scan(tq:asyncio.Queue,rq:asyncio.Queue,resolver:dns.resolver.Resolver, executor):
    loop = asyncio.get_event_loop()
    while True:
        if tq.empty():
            await tq.put('end')
            break
        task = await tq.get()
        result = await loop.run_in_executor(executor,query,resolver,task)
        if result == task:
            await tq.put(result)
        elif result:
            await rq.put({
                'domain':task,
                'result':result
            }
            )


async def parse(rq,end_count):
    end_count = 0
    while True:
        if rq.empty():
            await asyncio.sleep(2)
            continue
        result = await rq.get()
        if result == 'end':
            end_count += 1
            if end_count >= scan_count:
                break
            continue
        print('='*20,result['domain'],'='*20)
        for answer in result['result'].response.answer:
            for item in answer.items:
                print(dns.rdatatype.to_text(item.rdtype),item)


if __name__ == "__main__":
    #加速
    scan_count = 5
    dict_file = 'domain_dict.txt'
    target_domain = input('host input:\n')
    main_resolver = dns.resolver.Resolver
# 协程
    executor = ThreadPoolExecutor()
    task_q, result_q = asyncio.Queue() , asyncio.Queue()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(read_dict(dict_file,task_q,target_domain))
    calls = [scan(task_q,result_q,main_resolver,executor) for _ in range(scan_count)]
    calls.append(parse(result_q,scan_count))
    # calls = [scan(task_q,result_q,main_resolver,executor),parse(result_q)]
    # loop.run_until_complete(scan(task_q,result_q,main_resolver))
    loop.run_until_complete(asyncio.wait(calls))