from task import *

class DMA:
    @staticmethod
    def graph(original_tasks):
        tasks = PTask.sortDMA(original_tasks)
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
                rma_j = PJob.find_high_prio_job_DMA(jobs, cur_time)
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
                

