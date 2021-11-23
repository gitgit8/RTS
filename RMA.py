from task import *

class RMA:
    @staticmethod
    def SchedulableUtilization(tasks: list):
        #Tested
        tu = PTask.totalUtilization(tasks)
        is_p_d_equal = True
        v = []
        n = len(tasks)
        for task in tasks:
            print(task)
            v.append(task.v)
            if task.p != task.relativeDeadline:
                is_p_d_equal = False
        if is_p_d_equal:
            print("Periods and the relative deadliens are equal so we can use this formula Urm = n * ((2 ^ (1/n)) - 1)")
            Urm = n * ((2 ** (1/n)) - 1)
            print("Urm = {} and tasks total utilization = {}".format(Urm, tu))
            if tu <= Urm:
                print("We can scheudle these tasks using RMA")
            else:
                print("We can't schedule these tasks using RMA")
        else:
            print("Periods and relative deadlines are not equal so we need to find v -> Di = V * Pi")
            tmp = v[0]
            all_v_same = True
            for x in v:
                if tmp != x:
                    all_v_same = False
            if all_v_same is False:
                print("V should be same for everything, exiting now {}".format(v))
                exit
            if tmp <= 0.5:
                print("v of all the tasks given is {} so Urm is v".format(tmp))
                Urm = tmp
            elif tmp > 0.5 and tmp <= 1:
                print("v of all the tasks given is {} so Urm is (n*((2v ^ 1/n ) - 1)) + 1 - v".format(tmp))
                Urm = (n * ((2*tmp) ** (1/n) - 1) + 1 - tmp)
            else:
                print("v of all the tasks given is {} - is it int???(2,3,4,5 ...), then only belive me. so Urm is  (v(n-1) * ((((v+1) / (v))^((1/n)-1))-1)".format(tmp))
                Urm = (tmp *(n-1)) * ((((tmp + 1)/(tmp)) ** ((1/n)-1))-1)
            print("Urm = {} and tasks total utilization = {}".format(Urm, tu))
            if tu <= Urm:
                print("We can scheudle these tasks using RMA")
            else:
                print("We can't schedule these tasks using RMA")

    def SchedulableUtilizationForTaskI(tasks: list, i: int):
        #Not tested
        i = i - 1
        tu = PTask.totalUtilization(tasks[:i])
        b_t = PTask.maxBlocking(tasks[i:])
        print("Max blocking of tasks are {}".format(b_t))
        tu = tu + float(b_t/tasks[i].p)
        is_p_d_equal = True
        v = []
        n = len(tasks[:i])
        for task in tasks[:i]:
            print(task)
            v.append(task.v)
            if task.p != task.relativeDeadline:
                is_p_d_equal = False
        if is_p_d_equal:
            print("Periods and the relative deadliens are equal so we can use this forumla Urm = n * ((2 ^ (1/n)) - 1)")
            Urm = n * ((2 ** (1/n)) - 1)
            print("Urm = {} and tasks total utilization = {}".format(Urm, tu))
            if tu <= Urm:
                print("We can scheudle these tasks using RMA")
            else:
                print("We can't schedule these tasks using RMA")
        else:
            print("Periods and relative deadlines are not equal so we need to find v -> Di = V * Pi")
            tmp = v[0]
            all_v_same = True
            for x in v:
                if tmp != x:
                    all_v_same = False
            if all_v_same is False:
                print("V should be same for everything, exiting now {}".format(v))
                exit
            if tmp <= 0.5:
                print("v of all the tasks given is {} so Urm is v".format(tmp))
                Urm = tmp
            elif tmp > 0.5 and tmp <= 1:
                print("v of all the tasks given is {} so Urm is (n*((2v ^ 1/n ) - 1)) + 1 - v".format(tmp))
                Urm = (n * ((2*tmp) ** (1/n) - 1) + 1 - tmp)
            else:
                print("v of all the tasks given is {} - is it int???(2,3,4,5 ...), then only belive me. so Urm is  (v(n-1) * ((((v+1) / (v))^((1/n)-1))-1)".format(tmp))
                Urm = (tmp *(n-1)) * ((((tmp + 1)/(tmp)) ** (1/(n-1)))-1)
            print("Urm = {} and tasks total utilization = {}".format(Urm, tu))
            if tu <= Urm:
                print("We can scheudle these tasks using RMA")
            else:
                print("We can't schedule these tasks using RMA")
    
    def SchedulableUtilizationForTaskIDS(tasks: list, Tds):
        """Tds server period is arbitrary"""
        #Tested
        for task in tasks:
            print("Schedulabiltiy for {}".format(task.name))
            index = tasks.index(task)
            tu = PTask.totalUtilization(tasks[:index+1])
            b_t = PTask.maxBlockingTimeI(tasks, index)
            print("\tMax blocking of tasks are {}".format(b_t))
            tu_ds = 0
            n = len(tasks[:index+1])
            if task.p > Tds.p:
                print("\tTDS - calc {}".format(float(Tds.e / tasks[index].p))) 
                tu_ds = float(Tds.e / tasks[index].p) + Tds.u
                n = n + 1
            tu = tu + float(b_t/tasks[index].p) + tu_ds
            is_p_d_equal = True
            v = []
            for task in tasks[:index+1]:
                print("\t" + str(task))
                v.append(task.v)
                if task.p != task.relativeDeadline:
                    is_p_d_equal = False
            if is_p_d_equal:
                print("\tPeriods and the relative deadliens are equal so we can use this forumla Urm = n * ((2 ^ (1/n)) - 1) where n is {}".format(n))
                Urm = n * ((2 ** (1/n)) - 1)
                print("\tUrm = {} and tasks total utilization = {}".format(Urm, tu))
                if tu <= Urm:
                    print("\tWe can scheudle these tasks using RMA")
                else:
                    print("\tWe can't schedule these tasks using RMA")
            else:
                print("Periods and relative deadlines are not equal so we need to find v -> Di = V * Pi")
                tmp = v[0]
                all_v_same = True
                for x in v:
                    if tmp != x:
                        all_v_same = False
                if all_v_same is False:
                    print("V should be same for everything, exiting now {}".format(v))
                    exit
                if tmp <= 0.5:
                    print("v of all the tasks given is {} so Urm is v".format(tmp))
                    Urm = tmp
                elif tmp > 0.5 and tmp <= 1:
                    print("v of all the tasks given is {} so Urm is (n*((2v ^ 1/n ) - 1)) + 1 - v".format(tmp))
                    Urm = (n * ((2*tmp) ** (1/n) - 1) + 1 - tmp)
                else:
                    print("v of all the tasks given is {} - is it int???(2,3,4,5 ...), then only belive me. so Urm is  (v(n-1) * ((((v+1) / (v))^((1/n)-1))-1)".format(tmp))
                    Urm = (tmp *(n-1)) * ((((tmp + 1)/(tmp)) ** (1/(n-1)))-1)
                print("Urm = {} and tasks total utilization = {}".format(Urm, tu))
                if tu <= Urm:
                    print("We can scheudle these tasks using RMA")
                else:
                    print("We can't schedule these tasks using RMA")

    def SchedulableUtilizationForTaskIV2(tasks: list):
        #Tested
        n = len(tasks)
        for i in range(n):
            tu = PTask.totalUtilization(tasks[:i+1])
            b_t = PTask.maxBlockingTimeI(tasks,i)
            print("Max blocking of tasks are {}".format(b_t))
            tu = tu + float(b_t/tasks[i].p)
            is_p_d_equal = True
            v = []
            n = len(tasks[:i])
            for task in tasks[:i]:
                print(task)
                v.append(task.v)
                if task.p != task.relativeDeadline:
                    is_p_d_equal = False
            if is_p_d_equal:
                print("Periods and the relative deadliens are equal so we can use this forumla Urm = n * ((2 ^ (1/n)) - 1)")
                Urm = n * ((2 ** (1/n)) - 1)
                print("Urm = {} and tasks total utilization = {}".format(Urm, tu))
                if tu <= Urm:
                    print("We can scheudle these tasks using RMA")
                else:
                    print("We can't schedule these tasks using RMA")
            else:
                print("Periods and relative deadlines are not equal so we need to find v -> Di = V * Pi")
                tmp = v[0]
                all_v_same = True
                for x in v:
                    if tmp != x:
                        all_v_same = False
                if all_v_same is False:
                    print("V should be same for everything, exiting now {}".format(v))
                    exit
                if tmp <= 0.5:
                    print("v of all the tasks given is {} so Urm is v".format(tmp))
                    Urm = tmp
                elif tmp > 0.5 and tmp <= 1:
                    print("v of all the tasks given is {} so Urm is (n*((2v ^ 1/n ) - 1)) + 1 - v".format(tmp))
                    Urm = (n * ((2*tmp) ** (1/n) - 1) + 1 - tmp)
                else:
                    print("v of all the tasks given is {} - is it int???(2,3,4,5 ...), then only belive me. so Urm is  (v(n-1) * ((((v+1) / (v))^((1/n)-1))-1)".format(tmp))
                    Urm = (tmp *(n-1)) * ((((tmp + 1)/(tmp)) ** (1/(n-1)))-1)
                print("Urm = {} and tasks total utilization = {}".format(Urm, tu))
                if tu <= Urm:
                    print("We can scheudle these tasks using RMA")
                else:
                    print("We can't schedule these tasks using RMA")

    @staticmethod
    def graph(original_tasks):
        tasks = PTask.sortRMA(original_tasks)
        hp = PTask.calc_HyperPeriod(tasks)
        jobs = []
        release_times = []
        chart = []
        for task in tasks:
            print(task)
            r_times = task.releaseTimesInHyperPeriod(hp)
            for r in r_times:
                jobs.append(PJob(task,r))
            release_times += r_times
        release_times = list(set(release_times))
        release_times.sort()
        release_times.append(int(hp))
        l = len(release_times)
        for i in range(l):
            cur_time = release_times[i]
            if cur_time == hp:
                break
            while (cur_time < release_times[i+1] and cur_time != hp):
                rma_j = PJob.find_high_prio_job_RMA(jobs, cur_time)
                if rma_j is None:
                    break
                if cur_time + rma_j.t_rem < release_times[i+1]:
                    executed = rma_j.t_rem
                    rma_j.update_t_rem(rma_j.t_rem)
                else:
                    needed = cur_time + rma_j.t_rem
                    available = rma_j.t_rem - (needed - release_times[i+1])
                    executed = available
                    rma_j.update_t_rem(available)
                print("Selected {} for execution from {} to {}".format(rma_j.name,cur_time, cur_time + executed))
                chart.append([rma_j, cur_time, cur_time + executed])
                cur_time = cur_time + executed
        for v in chart:
            print("{} -> {} - {}".format(v[0].name, v[1], v[2]))
            if (v[0].absDeadline < v[2]):
                print("Missed deadline for {}".format(v[0]))


