from PeriodicTask import PeriodicTask

n = int(input("Enter number of tasks  -"))
tasks = []
for i in range(n):
    name = input("Enter name for task {}  -".format(i))
    phase = input("Enter phase for task {}  -".format(i))
    p = input("Enter period for task {}  -".format(i))
    e = input("Enter execution for task {}  -".format(i))
    deadline = input("Enter relative deadline for task {}  -".format(i))
    tasks.append(PeriodicTask(name, phase, p, e, deadline))

HP = PeriodicTask.calc_HyperPeriod(tasks)
print("HyperPeriod of all the tasks {} ".format(HP))
for task in tasks:
    print("Number of {} jobs in HyperPeriod {} are {}".format(task.name, HP, task.NumJobsInHP(HP)))

