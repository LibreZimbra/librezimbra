# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Enrico Weigelt, metux IT consult <info@metux.net>

from metux.util.log import warn, info

class TaskFail(Exception):

    def __init__(self, tsk, msg):
        self.msg = msg
        self.tsk = tsk
        Exception.__init__(self, "[task "+tsk.get_name()+"] "+msg)

    def get_message(self):
        return self.msg

    def get_task_name(self):
        return self.tsk.get_name()

class Task(object):

    def __init__(self, param):
        self.param = param
        self.name = param['name']
        self._my_done = False

    def get_name(self):
        return self.name

    def fail(self, msg):
        raise TaskFail(self, msg)

    def check_task_list(self, tasklist):
        x = 0
        for t in tasklist:
            if not isinstance (t, Task):
                fail("subtask #"+str(x)+" is not Task")
            x = x+1
        return tasklist

    """ [override] check whether the task needs to run """
    def need_run(self):
        return True

    """ [override] do the actual task. return true if actually did something"""
    def do_run(self):
        return False

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
    """run a task and skip those which don't need to be run.
       @return true if at least one task actually ran."""
    def runTask(self, task):
        if task._my_done:
            return False

        res = False

        # need to do it that way to defeat shortcut evaluation
        for t in task.check_task_list(task.get_subtasks()):
            res |= self.runTask(t)

        if task.need_run():
            res |= task.do_run()

        task._my_done = True
        return res
