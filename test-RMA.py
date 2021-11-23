from task import *
from RMA import *

tasks = [ PTask("T1", p=3, e=0.6), PTask("T2", p=5, e=0.5), PTask("T3", p=7, e=1.4, bt=0.2)]
tds = PTask("TDS", 0, 4, 0.8, 4)
RMA.SchedulableUtilizationForTaskIDS(tasks, tds)
