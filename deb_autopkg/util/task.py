from metux.log import warn, info

class TaskFail(Exception):

    def __init__(self, tsk, msg):
        Exception.__init__(self, "[task "+tsk.get_name()+"] "+msg)

class Task(object):

    def __init__(self, param):
        self.param = param
        self.name = param['name']
        self._my_done = False

    def get_name(self):
        return self.name

    def fail(self, msg):
        raise Exception(self, msg)

    def check_task_list(self, tasklist):
        x = 0
        for t in tasklist:
            if not isinstance (t, Task):
                fail("subtask #"+str(x)+" is not Task")
            x = x+1
        return tasklist

    # private !
    def run_subtasks(self):
        res = False
        for t in self.check_task_list(self.get_subtasks()):
            res |= t.auto_run()
        return res

    """ [override] check whether the task needs to run """
    def need_run(self):
        return True

    """ [override] do the actual task. return true if actually did something"""
    def do_run(self):
        return False

    """ only run if necessary. skip if need_run() tells false or already ran"""
    def auto_run(self):
        if self._my_done or (not self.need_run()):
            return False;

        # need to do it that way to defeat shortcut evaluation
        res = self.run_subtasks()
        res |= self.do_run()

        self._my_done = True
        return res

    """ [override] get a list of sub tasks"""
    def get_subtasks(self):
        return []

    def log_warn(self, text):
        warn("("+self.name+") "+text)

    def log_info(self, text):
        info("("+self.name+") "+text)

class TaskRunner(object):

    def __init__(self, name):
        self.name = name
        self.tasks = []

    # fixme: should add some queue management and dependency resolution
    def runTask(self, task):
        subs = task.auto_run()
