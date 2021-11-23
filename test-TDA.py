from TDA import *
from task import *

#tasks = [PTask(name="T1", p=3, e=1), PTask(name="T2", p=4, e=1), PTask("T3", p=5, e=1)]
tasks = [PTask(name="T1", p=5, e=1), PTask(name="T2", p=8, e=2), PTask("T3", p=14, e=4,)]
TDA.WorstCaseAnalysis(tasks)