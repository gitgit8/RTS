from task import *


class EDF:
    @staticmethod
    def SchedulableUtilization(tasks: list):
        #Tested
        tu = PTask.totalUtilization(tasks)
        Uedf = 0
        is_p_d_rel = True
        for task in tasks:
            Uedf = Uedf + task.density
            if task.p < task.relativeDeadline:
                is_p_d_rel = False
            print(task)
        print("Uedf = {} and tasks total utilization = {} is_p_d_rel {}".format(Uedf, tu, is_p_d_rel))
        print("if p is less than or equal to d for all the tasks then Uedf should be less than or equal to 1 otherwise it can be anything but we can't assume it will fail or pass")
        if tu <= Uedf:
            print("We can scheudle these tasks using EDF")
        else:
            print("We can't schedule these tasks using EDF")

    @staticmethod
    def SchedulableUtilizationForTaskI(tasks: list):
        #Tested
        n = len(tasks)
        for i in range(n):
            print("For {}".format(tasks[i].name))
            tu = PTask.totalUtilization(tasks[:i+1])
            b_t = PTask.maxBlockingTimeI(tasks, i)
            print("\tMax blocking of tasks are {}".format(b_t))
            is_p_d_rel = True
            for task in tasks[:i]:
                Uedf = Uedf + task.density
                if task.p < task.relativeDeadline:
                    is_p_d_rel = False
                print(task)
            Uedf = Uedf + float(b_t / min(tasks[i].relativeDeadline, tasks[i].p))
            print("\tUedf = {} and tasks total utilization = {} is_p_d_rel {}".format(Uedf, tu, is_p_d_rel))
            print("\tif p is less than or equal to d for all the tasks then Uedf should be less than or equal to 1 otherwise it can be anything but we can't assume it will fail or pass")
            if tu <= Uedf:
                print("\tWe can scheudle {} task using EDF".format(tasks[i].name))
            else:
                print("\tWe can't schedule {} task using EDF".format(tasks[i].name))
            if Uedf <= 1:
                print("\t<= 1 - We can scheudle {} tasks using EDF".format(tasks[i].name))
            else:
                print("\t<= 1 - We can't schedule {} task using EDF".format(tasks[i].name))

    @staticmethod
    def SchedulableUtilizationForTaskIDS(tasks: list, Tds):
        #Tested
        for task in tasks:
            print("Schedulability for {}".format(task.name))
            index = tasks.index(task)
            tu = PTask.totalUtilization(tasks[:index+1])
            b_t = PTask.maxBlocking(tasks, index)
            print("Max blocking of tasks are {}".format(b_t))
            is_p_d_equal = True
            n = len(tasks[:index+1])
            for task in tasks[:index+1]:
                Uedf = Uedf + task.density
                if task.p != task.relativeDeadline:
                    is_p_d_equal = False
                print(task)
            Uedf = Uedf + float(b_t / min(tasks[index].relativeDeadline, tasks[index].p)) + (Tds.u * (1 + ((Tds.p - Tds.e)/tasks[index].relativeDeadline)))
            print("Uedf = {} and tasks total utilization = {} is_p_d_equal {}".format(Uedf, tu, is_p_d_equal))
            print("if p and d are same then Uedf should be less than or equal to 1 otherwise it can be anything but we can't assume it will fail or pass")
            if tu <= Uedf:
                print("We can scheudle these tasks using EDF")
            else:
               print("We can't schedule these tasks using EDF")

    @staticmethod
    def graph(tasks):
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
                edf_j = PJob.find_high_prio_job_EDF(jobs, cur_time)
                if edf_j is None:
                    break
                if cur_time + edf_j.t_rem < release_times[i+1]:
                    executed = edf_j.t_rem
                    edf_j.update_t_rem(edf_j.t_rem)
                else:
                    needed = cur_time + edf_j.t_rem
                    available = edf_j.t_rem - (needed - release_times[i+1])
                    executed = available
                    edf_j.update_t_rem(available)
                print("Selected {} for execution from {} to {}".format(edf_j.name,cur_time, cur_time + executed))
                chart.append([edf_j, cur_time, cur_time + executed])
                cur_time = cur_time + executed
        for v in chart:
            print("{} -> {} - {}".format(v[0].name, v[1], v[2]))
            if (v[0].absDeadline < v[2]):
                print("Missed deadline for {}".format(v[0]))

