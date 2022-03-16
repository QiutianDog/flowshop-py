import numpy as np
from modele.job import Job
from modele.machine import Machine


class Factory:
    def __init__(self):
        self.jobs = None
        self.machines = None

    def generate_data(self, job_num, machine_num):
        self.jobs = []
        self.machines = []

        # 随机生成工件
        for i in range(job_num):
            times = np.random.randint(1, 100, size=(1, machine_num))[0]
            job = Job(i, times)
            self.jobs.append(job)

        # 随机生成机器约束
        constraints = np.random.randint(1, 4, size=(1, machine_num))[0]
        constraints[-1] = 0
        while constraints[-2] == 2:
            constraints[-2] = np.random.randint(1, 4)
        for i, value in enumerate(constraints):
            machine = Machine(i, value)
            self.machines.append(machine)

    def complete(self, order):
        # 根据 order 依次取出工件
        for job_id in order:
            job = self.jobs[job_id]
            # 获取第一台机器的最终完成时间, 也是当前工件进入机器的时间
            last_workflow_time = self.machines[0].get_last_workflow_time()

            # 依次放入机器中加工
            for machine in self.machines:
                work_time = job.work_times[machine.id]
                constraint = machine.constraint

                # 依据不同的约束 决定不同的加工行为
                if constraint == 0:
                    # WB 无约束，上一个结束了就可以直接加工
                    # 判断机器有没有加工过
                    if len(machine.workflow) != 0:
                        # 有加工记录，读取上次的加工记录，在此基础上进行加工
                        last_time = machine.get_last_workflow_time()

                        # 上个工件的完工时间 < 当前工件进入的时间，添加空闲时间
                        if last_time < last_workflow_time:
                            machine.workflow.append([-1, last_time, last_workflow_time])

                        # 上个工件的完工时间 > 当前工件进入的时间, 进入工件的时间推迟到上个完工
                        if last_time > last_workflow_time:
                            last_workflow_time = last_time

                    # 进行加工
                    machine.workflow.append([0, last_workflow_time, last_workflow_time + work_time])
                    last_workflow_time += work_time
                    continue

                if constraint == 1:
                    # RCB 当工件在下一台机器上离开时释放当前机器
                    # 判断机器有没有加工过
                    if len(machine.workflow) != 0:
                        # 获取上一个工件在下下一台机器上的开始加工时间
                        # 如果下一台是最后一台，那么在最后一台的结束加工时间就是离开时间
                        if machine.id == len(self.machines) - 2:
                            next_start_time = self.machines[machine.id + 1].get_last_workflow_time()
                        else:
                            next_start_time = self.machines[machine.id + 2].get_last_job_start_time()

                        # 添加一定存在的阻塞时间
                        current_last_workflow_time = machine.get_last_workflow_time()
                        machine.workflow.append([1, current_last_workflow_time, next_start_time])

                        # 添加可能的空闲时间
                        if next_start_time < last_workflow_time:
                            machine.workflow.append([-1, next_start_time, last_workflow_time])

                        # 如果阻塞时间超过了当前工件进入机器的时间，以阻塞时间为准
                        if next_start_time > last_workflow_time:
                            last_workflow_time = next_start_time

                    machine.workflow.append([0, last_workflow_time, last_workflow_time + work_time])
                    last_workflow_time += work_time
                    continue

                if constraint == 2:
                    # RSB 在上一个工件在下一台机子上开机加工时释放当前机器
                    # 判断机器有无加工数据
                    if len(machine.workflow) != 0:
                        # 获取下一台机器的最后一个工件的开始加工时间
                        next_start_time = self.machines[machine.id + 1].get_last_job_start_time()

                        # 添加可能的阻塞时间
                        current_last_workflow_time = machine.get_last_workflow_time()
                        if current_last_workflow_time < next_start_time:
                            machine.workflow.append([1, current_last_workflow_time, next_start_time])

                        # 添加可能的空闲时间
                        current_last_workflow_time = machine.get_last_workflow_time()
                        if current_last_workflow_time < last_workflow_time:
                            machine.workflow.append([-1, current_last_workflow_time, last_workflow_time])

                        # 如果阻塞时间超过了当前工件进入机器的时间，以阻塞时间为准
                        if current_last_workflow_time > last_workflow_time:
                            last_workflow_time = current_last_workflow_time

                    machine.workflow.append([0, last_workflow_time, last_workflow_time + work_time])
                    last_workflow_time += work_time
                    continue

                if constraint == 3:
                    # RCBn约束 上一个工件在下一台机器上完工时释放当前机器
                    # 判断机器有没有加工过
                    if len(machine.workflow) != 0:
                        # 获取上一个工件在下一台机器上完工时间
                        next_over_time = self.machines[machine.id + 1].get_last_workflow_time()

                        # 添加阻塞时间
                        current_last_workflow_time = machine.get_last_workflow_time()
                        machine.workflow.append([1, current_last_workflow_time, next_over_time])

                        # 添加可能的空闲时间
                        if next_over_time < last_workflow_time:
                            machine.workflow.append([-1, next_over_time, last_workflow_time])

                        # 如果阻塞时间超过当前工件进入当前机器的时间，以阻塞时间为准
                        if next_over_time > last_workflow_time:
                            last_workflow_time = next_over_time

                    machine.workflow.append([0, last_workflow_time, last_workflow_time + work_time])
                    last_workflow_time += work_time
                    continue

        # 最后再遍历一遍机器，加上RCB和RCBn的阻塞时间
        for machine in self.machines:
            if machine.constraint == "RCB" or machine.constraint == "RCBn":
                last_workflow_time = machine.get_last_workflow_time()

                # 获取下一台的完工时间
                next_last_workflow_time = self.machines[machine.id + 1].get_last_workflow_time()

                # 添加阻塞时间
                machine.workflow.append([1, last_workflow_time, next_last_workflow_time])

    def load_data(self, filename):
        self.jobs = []
        self.machines = []
        with open(filename, "r", encoding="utf-8") as f:
            # 读取第一行
            constraints = f.readline().strip().split(",")

            # 根据约束生成机器
            for i, value in enumerate(constraints):
                machine = Machine(i, value)
                self.machines.append(machine)

            # 读取剩下的所有行
            lines = f.readlines()
            for i, line in enumerate(lines):
                work_times = [eval(item) for item in line.strip().split(",")]
                job = Job(i, work_times)
                self.jobs.append(job)

    def save_data(self, filename):
        factory_data = []

        # 第一行写入约束
        constraints = []
        for machine in self.machines:
            constraints.append(machine.constraint)
        factory_data.append(constraints)

        # 其他行写入工件在不同机器上的加工时间
        for job in self.jobs:
            factory_data.append(job.work_times)

        np.savetxt(filename, factory_data, fmt='%d', delimiter=',')

