from task import *
import math

class TDA:
    @staticmethod
    def WorstCaseAnalysis(tasks: list):
        """Assumes the list is sorted as per the ALG"""
        """T is the multiples of period less than longest deadline"""
        n = len(tasks)
        longest_deadline = tasks[n-1].relativeDeadline
        print("Longest deadline is {}".format(longest_deadline))
        wt = []
        for task in tasks:
            xyz =task.releaseTimesInHyperPeriod(longest_deadline)[1:]
            for x in xyz:
                wt.append(x)
        #append the longest time deadline too
        wt.append(int(longest_deadline))
        wt.sort()
        print("T is the multiples of period less than longest deadline - {}".format(wt))
        tda = {}
        for t in wt:
            for i in range(n):
                t_i = i + 1
                e_others = 0
                print("At {} - Worst Case Analysis for {}".format(t, tasks[i]))
                for j in range(i):
                    e_i = float(math.ceil(t/tasks[j].p) * tasks[j].e)
                    e_others = e_others + e_i
                    print("\tFor W{}({}) -> {} - execution {}".format(t_i,t,tasks[j].name, e_i))
                low_Prio_blocking_time = PTask.maxBlockingTimeI(tasks,i)
                if low_Prio_blocking_time:
                    print("\tMax blocking time due to low priority jobs/tasks are {}".format(low_Prio_blocking_time))
                e_others = e_others + tasks[i].e + low_Prio_blocking_time + tasks[i].pcp_block
                key = "W{}({})".format(t_i,t)
                tda[key] = [t, i, e_others, tasks[i]]
                print("\tW{}({}) = {} ".format(t_i,t,str(e_others)))
        for x,y in tda.items():
            """W(t) <= t and W(t) <= Relative Deadline"""
            if y[2] <= y[0] and y[2] <= tasks[y[1]].relativeDeadline:
                print("{} - {} can be scheduled -> t {} < Di {} and worst case time is {} < t {}".format(y[3].name, x,y[0],y[3].relativeDeadline,y[2],y[0]))
            else:
                print("{} - {} can't be scheduled -> t {} - Di {} and worst case time is {} - t {}".format(y[3].name, x,y[0],y[3].relativeDeadline,y[2],y[0]))

    @staticmethod
    def WorstCaseAnalysisDS(tasks: list):
        """Assumes the list is sorted as per the ALG"""
        """T is the multiples of period less than longest deadline"""
        #Add deferrable server stuff
        n = len(tasks)
        longest_deadline = tasks[n-1].relativeDeadline
        print("Longest deadline is {}".format(longest_deadline))
        wt = []
        for task in tasks:
            xyz =task.releaseTimesInHyperPeriod(longest_deadline)[1:]
            for x in xyz:
                wt.append(x)
        #append the longest time deadline too
        wt.append(int(longest_deadline))
        wt.sort()
        print("T is the multiples of period less than longest deadline - {}".format(wt))
        tda = {}
        for t in wt:
            for i in range(n):
                t_i = i + 1
                e_others = 0
                for j in range(i):
                    e_i = float(math.ceil(t/tasks[j].p) * tasks[j].e)
                    e_others = e_others + e_i
                    print("For W{}({}) -> {} - execution {}".format(t_i,t,tasks[j].name, e_i))
                low_Prio_blocking_time = PTask.maxBlocking(tasks[t_i:])
                if low_Prio_blocking_time:
                    print("Max blocking time due to low priority jobs/tasks are {}".format(low_Prio_blocking_time))
                e_others = e_others + tasks[i].e + low_Prio_blocking_time + tasks[i].pcp_block
                key = "W{}({})".format(t_i,t)
                tda[key] = [t, i, e_others, tasks[i]]
                print("W{}({}) = {} ".format(t_i,t,str(e_others)))
        for x,y in tda.items():
            """W(t) <= t and W(t) <= Relative Deadline"""
            if y[2] <= y[0] and y[2] <= tasks[y[1]].relativeDeadline:
                print("{} - {} can be scheduled -> [Time, Tasks, Worst case] - Di => {} - {}".format(y[3].name, x,y.name,tasks[y[1]].relativeDeadline))
            else:
                print("{} - {} can't be scheduled -> [Time, Tasks, Worst case] - Di => {} - {}".format(y[3].name, x,y.name,tasks[y[1]].relativeDeadline))

class IterativeTDA:
    @staticmethod
    def WorstCaseAnalysis(tasks: list):
        """Assumes the list is sorted as per the ALG"""
        n = len(tasks)
        iTDA = {}
        for i in range(n):
            t = w_e = tasks[i].e
            i_t = i + 1
            iter = e_others = pre_w_e = 0
            print("W{}^{} = {} bcz Initially it is execution only".format(i_t, iter, w_e))
            while w_e != pre_w_e:
                iter = iter + 1
                e_others = 0
                for j in range(i):
                    e_i = float(math.ceil(t/tasks[j].p) * tasks[j].e)
                    e_others = e_others + e_i
                    print("For W{}^{}({}) -> {} - execution {}".format(i_t,iter,t,tasks[j].name, e_i))
                pre_w_e = w_e
                w_e = e_others + tasks[i].e
                print("W{}^{}({}) = {}".format(i_t,iter,t,w_e))
                t = w_e
            key = "W{}^{}({})".format(i_t,iter,t)
            iTDA[key] = [t, i, tasks[i]]
            print("For {} Worst Case Time is {}\n\n".format(tasks[i].name,w_e))
        for x,y in iTDA.items():
            if y[0] <= tasks[y[1]].relativeDeadline:
                print("{} - {} is schedulable".format(y[2].name, x))
            else:
                print("{} - {} is not schedulable".format(y[2].name, x))
