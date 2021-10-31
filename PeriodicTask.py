import math

class PeriodicTask:
    def __init__(self, name, phase, period, exectuion, deadline):
        self.name = name
        self.phase = float(phase)
        self.p = float(period)
        self.e = float(exectuion)
        self.relativeDeadline = float(deadline)
        self.u = float(self.e / self.p)
    
    def NumJobsInHP(self, hp):
        return hp / self.p
    
    @property
    def utilization(self):
        return self.u

    def releaseTimesInHyperPeriod(self, hp):
        return [r for r in range(self.p + self.phase, hp, self.p)]

    @staticmethod
    def calc_HyperPeriod(tasks: list):
        lcm = 1
        for task in tasks:
            lcm = math.lcm(lcm, int(task.p))
        return lcm

    @staticmethod
    def totalUtilization(tasks: list):
        tu = 0
        for task in tasks:
            tu = tu + task.u
        return tu