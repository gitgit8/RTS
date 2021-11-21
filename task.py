import math

def find_factor(num: int):
    factors = []
    for i in range(1, num + 1):
       if num % i == 0:
           factors.append(i)
    return factors


class PTask:
    def __init__(self, name, phase=0, p=0, e=0, d=0, bt=0, ss=0, pcp_b=0, nss=0, ncs= 0, tcs=0):
        self.name = name
        self.phase = float(phase)
        self.p = float(p)
        if tcs != 0 and ncs !=0:
            self.e = float(e) + 2*float(ncs)*float(tcs)
        elif tcs !=0:
            self.e = float(e) + 2*float(tcs)
        else:
            self.e = float(e)
        self.tcs = float(tcs)
        self.ncs = float(ncs)
        if d == 0:
            self.relativeDeadline = self.p
        else:
            self.relativeDeadline = float(d)
        self.u = float(self.e / self.p)
        self.density = float(self.e / min(self.p, self.relativeDeadline))
        self.v = float(self.relativeDeadline / self.p)
        self.bt = float(bt)
        self.ss = float(ss)
        self.nss = float(nss)
        self.pcp_block = float(pcp_b)
    
    def __str__(self) -> str:
        buf = "{} - Phase {} p {} e {} Di {} U {} density {} v {} bt {} ss {} nss {} pcp_clock {} cs {} ncs {}".format(self.name, self.phase, self.p, self.e, self.relativeDeadline, self.u, self.density, self.v, self.bt, self.ss, self.nss, self.pcp_block, self.tcs,self.ncs)
        return buf
    
    def NumJobsInHP(self, hp):
        return hp / self.p
    
    def utilization(self):
        return self.u

    def releaseTimesInHyperPeriod(self, hp):
        return [r for r in range(int(self.phase), int(hp), int(self.p))]

    def absDeadlinesInHyperPeriod(self, hp):
        releases = self.releaseTimesInHyperPeriod(hp)
        return [x + int(self.relativeDeadline) for x in releases]

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

    @staticmethod
    def maxBlocking(tasks: list):
        bp = 0
        for task in tasks:
            print("{} has blocking time {}".format(task.name, task.bt))
            bp = max(bp, task.bt)
        return bp
    
    @staticmethod
    def maxBlockingTimeI(tasks:list, i):
        """Eg:  a = [1,2,3,4,5,6,7] a[3] = 4 so i should start from 0 and end with n-1"""
        ss = 0
        bp = 0
        buf = ""
        total_block_time = 0
        for task in tasks[i+1:]:
            buf = buf + "\t{} has blocking time {}\n".format(task.name, task.bt)
            bp = max(bp, task.bt)
        if i != 0:
            for task in tasks[:i]:
                buf = buf + "\t{} has suspension time {}\n".format(task.name, task.ss)
                ss = ss + min(task.ss, task.e)
        buf = buf + "\tself suspend {} high prio task suspend {} low priority block time {} number of self suspends {}".format(tasks[i].ss,ss,bp,tasks[i].nss)
        total_block_time = tasks[i].ss + ss + ((tasks[i].nss + 1) * bp)
        if total_block_time:
            print(buf)
        return total_block_time

    @staticmethod
    def staticFindFrameSize(tasks: list):
        cond_1 = 0
        for task in tasks:
            cond_1 = max(cond_1, task.e)
        print("Cond 1: frame should be max of {}".format(cond_1))
        hp = PTask.calc_HyperPeriod(tasks)
        factors = find_factor(hp)
        factors = [x for x in factors if x >= cond_1]
        print("Cond 2: Factors of hp={} are {}".format(hp, factors))
        cond_3 = []
        for frame in factors:
            failed = False
            for task in tasks:
                rhs = int(2*frame - math.gcd(int(task.p), frame))
                if (rhs) <= int(task.relativeDeadline):
                    print("{} passed for frame {} - {} <= {}".format(task.name, frame, rhs, task.relativeDeadline))
                else:
                    print("{} failed for frame {} - {} <= {}".format(task.name, frame, rhs, task.relativeDeadline))
                    failed = True
                    break
            if not failed:
                cond_3.append(frame)
        print("cond 3: final possible frames are {}".format(cond_3))
        print("*****************Final Answer**********************")
        print("Cond 1: frame should be max of {}".format(cond_1))
        print("Cond 2: Factors of hp={} are {}".format(hp, factors))
        print("cond 3: final possible frames are {}".format(cond_3))
        if not cond_3:
            print("Try slicing - Divide the highest execution task into smaller tasks")
        return cond_3

    @staticmethod
    def NFGFindFrameSize(tasks: list):
        cond_1 = 0
        print("Cond 1: frame should be max of {} - NA".format(cond_1))
        hp = PTask.calc_HyperPeriod(tasks)
        factors = find_factor(hp)
        print("Cond 2: Factors of hp={} are {}".format(hp, factors))
        cond_3 = []
        for frame in factors:
            failed = False
            for task in tasks:
                rhs = int(2*frame - math.gcd(int(task.p), frame))
                if (rhs) <= int(task.relativeDeadline):
                    print("{} passed for frame {} - {} <= {}".format(task.name, frame, rhs, task.relativeDeadline))
                else:
                    print("{} failed for frame {} - {} <= {}".format(task.name, frame, rhs, task.relativeDeadline))
                    failed = True
                    break
            if not failed:
                cond_3.append(frame)
        print("cond 3: final possible frames are {}".format(cond_3))
        print("*****************Final Answer**********************")
        print("Cond 1: frame should be max of {}".format(cond_1))
        print("Cond 2: Factors of hp={} are {}".format(hp, factors))
        print("cond 3: final possible frames are {} - Take max to avoid CT".format(cond_3))
        return cond_3
    
    @staticmethod
    def sortRMA(tasks):
        new_tasks = {}
        final_tasks = []
        for task in tasks:
            new_tasks[(task.p, task.name)] = task
        new_tasks = sorted(new_tasks)
        for p, n in new_tasks:
            for task in tasks:
                if n is task.name:
                    final_tasks.append(task)
        return final_tasks

    @staticmethod
    def sortDMA(tasks):
        new_tasks = {}
        final_tasks = []
        for task in tasks:
            new_tasks[(task.relativeDeadline, task.name)] = task
        new_tasks = sorted(new_tasks)
        for p, n in new_tasks:
            for task in tasks:
                if n is task.name:
                    final_tasks.append(task)
        return final_tasks


class PJob:
    def __init__(self, task, releaseTime) -> None:
        self.name = "{}-J{}".format(task.name, int(releaseTime/task.p) + 1)
        self.rel_time = releaseTime
        self.task = task
        self.absDeadline = releaseTime + task.relativeDeadline
        self.relativeDeadline = task.relativeDeadline
        self.t_rem = task.e
        self.slack = float("inf")
        self.done = False

    def calc_slack_time(self, cur_time):
        if self.rel_time > cur_time or self.done == True:
            return
        self.slack = self.absDeadline - cur_time - self.t_rem
        print("At {} slack time for {} is {} - {} - {} = {}".format(cur_time,self.name,self.absDeadline, cur_time, self.t_rem,self.slack))
    
    def update_t_rem(self, e_time):
        self.t_rem = self.t_rem - e_time
        if self.t_rem <= 0:
            self.done = True
    
    def __str__(self) -> str:
        buf = "{} - Task {} release time {} Deadline {} time remaining {} slack {} done {}".format(self.name, self.task.name, self.rel_time, self.absDeadline, self.t_rem, self.slack, self.done)
        return buf

    @staticmethod
    def find_least_slack(jobs):
        index = 0
        least_slack = float("inf")
        l = len(jobs)
        for i in range(l):
            if jobs[i].done == False and jobs[i].slack < least_slack:
                least_slack = jobs[i].slack
                index = i
        return index

    @staticmethod
    def find_least_stack_job(jobs):
        lst_j = None
        lst_time = float("inf")
        for job in jobs:
            if job.done == False and lst_time > job.slack:
                lst_time = job.slack
                lst_j = job
        return lst_j
    
    @staticmethod
    def find_high_prio_job_RMA(jobs, cur_time):
        high_j = None
        period = float("inf")
        for job in jobs:
            if job.done == False and job.rel_time <= cur_time and period > job.task.p:
                high_j = job
                period = job.task.p
        return high_j

    @staticmethod
    def find_high_prio_job_DMA(jobs, cur_time):
        high_j = None
        deadline = float("inf")
        for job in jobs:
            if job.done == False and job.rel_time <= cur_time and deadline > job.task.relativeDeadline:
                high_j = job
                deadline = job.task.relativeDeadline
        return high_j

    @staticmethod
    def find_high_prio_job_EDF(jobs, cur_time):
        high_j = None
        deadline = float("inf")
        for job in jobs:
            if job.done == False and job.rel_time <= cur_time and deadline > job.absDeadline:
                high_j = job
                deadline = job.absDeadline
        return high_j