class Task:
    task_list = []

    def __init__(self, t_id, t_desc, t_priority, t_status):
        self.t_id = t_id
        self.t_desc = t_desc
        self.t_priority = t_priority
        self.t_status = t_status

    def add_task(self, priority):
        if priority == 'H':
            Task.task_list.insert(0, [self.t_id, self.t_desc, self.t_priority, self.t_status])
            return
        Task.task_list.append([self.t_id, self.t_desc, self.t_priority, self.t_status])
