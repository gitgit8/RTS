from  task import *

class LST:
    def __init__(self, tasks) -> None:
        self.tasks = tasks

    def LST_analysis(jobs, cur_time):
        """Main guy who does LST"""
        for job in jobs:
            job.calc_slack_time(cur_time)
        lst_j = PJob.find_least_stack_job(jobs)
        return lst_j

    def LST_scheduling(self):
        """Provide the tasks and we will calcualte the LST analysis"""
        tasks = self.tasks
        hp = PTask.calc_HyperPeriod(tasks)
        jobs = []
        release_times = []
        chart = []
        for task in tasks:
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
                lst_j = LST.LST_analysis(jobs, cur_time)
                if (lst_j == None):
                    break
                if cur_time + lst_j.t_rem < release_times[i+1]:
                    executed = lst_j.t_rem
                    lst_j.update_t_rem(lst_j.t_rem)
                else:
                    needed = cur_time + lst_j.t_rem
                    available = lst_j.t_rem - (needed - release_times[i+1])
                    executed = available
                    lst_j.update_t_rem(available)
                print("Selected {} for execution from {} to {}".format(lst_j.name,cur_time, cur_time + executed))
                chart.append([lst_j, cur_time, cur_time + executed])
                cur_time = cur_time + executed
        for v in chart:
            print("{} -> {} - {}".format(v[0].name, v[1], v[2]))
            if (v[0].absDeadline < v[2]):
                print("Missed deadline for {}".format(v[0]))