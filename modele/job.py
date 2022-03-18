class Job:
    def __init__(self, job_id, work_times):
        if job_id is None:
            raise Exception("id must be not empty!")
        self.id = job_id
        if work_times is None:
            raise Exception("work_times must be not empty!")
        self.work_times = work_times

    def get_work_time_by_machine_id(self, machine_id):
        if len(self.work_times) == 0:
            return 0
        if 0 <= machine_id < len(self.work_times):
            return self.work_times[machine_id]
        raise Exception("machine_id is error!", machine_id)

    def get_sum_work_times(self):
        return sum(self.work_times)
