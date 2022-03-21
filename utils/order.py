import random


class Order:
    def __init__(self, jobs_num):
        count = 1
        for i in range(1, jobs_num + 1):
            count *= i
        self.max_count = count
        self.jobs_num = jobs_num

    def get_order(self, count):
        temp = [i for i in range(self.jobs_num)]

        # 利用树的特性解决全排列问题
        global_count = self.max_count
        local_count = count

        order = []
        i = 0
        while i < self.jobs_num - 2:
            global_count //= self.jobs_num - i

            # 判断local_count所处第几个位置
            index = local_count // global_count

            order.append(temp.pop(index))

            # 缩小 local_count 的范围
            local_count %= global_count
            i = i + 1

        # 最后一次决定两个
        if local_count == 0:
            order.append(temp.pop(0))
            order.append(temp.pop(0))
        else:
            order.append(temp.pop(1))
            order.append(temp.pop(0))

        return order


def random_order(jobs_nums):
    order = [i for i in range(jobs_nums)]
    random.shuffle(order)
    return order
