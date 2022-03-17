class Machine:
    def __init__(self, machine_id, constraint):
        """
        :param machine_id: 机器ID start = 0
        :param constraint: 机器约束 start = 0
                           0 WB 没有约束
                           1 RCB 工件在下一台机器上离开时释放当前机器
                           2 RSB 工件在下一台机器上开始加工时释放当前机器
                           3 RCBn 工件在下一台机器上完成加工时释放当前机器
        """
        if machine_id is None:
            raise Exception("id must be not empty!")
        self.id = machine_id
        if constraint is None:
            raise Exception("constraint must be not empty!")
        self.constraint = constraint
        self.workflow = []

    def get_last_workflow_time(self):
        """
        :return: 最后一个事件的结束时间
        """
        return 0 if len(self.workflow) == 0 else self.workflow[-1][2]

    def get_last_job_start_time(self):
        """
        :return: 最后一个工件的开始加工时间
        """
        for item in self.workflow[::-1]:
            if item[0] == 0:
                return item[1]
        return 0
