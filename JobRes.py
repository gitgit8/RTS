class res_needed:
    def __init__(self, res, time) -> None:
        self.res = res
        self.t = time

class neededby_job:
    def __init__(self, job, time) -> None:
        self.j = job
        self.t = time

class class_resource:
    """Takes care of res"""
    def __init__(self, name) -> None:
        self.name = name
        self.neededby = []
        self.ceil = float("inf")

class class_jobs:
    """Takes care of jobs"""
    def __init__(self, name) -> None:
        self.name = name
        self.needed = []
        self.priority = float("inf")


class blockingTime:
    @staticmethod
    def find_blocking_time(jobs, res, relations):
        """Provide jobs in the priority order"""
        j = []
        r = []
        i = 1
        for job in jobs:
            j.append(class_jobs(job))
            j[i-1].priority = i
            i = i + 1
        for rs in res:
            r.append(class_resource(rs))
        for job, rs in relations.items():
            j_j = None
            for i_j in j:
                if i_j.name == job:
                    j_j = i_j
                    break
            for r_r in rs:
                if len(r_r) == 0:
                    break
                j_r = None
                for i_r in r:
                    if r_r[0] == i_r.name:
                        j_r = i_r
                        break
                j_j.needed.append(res_needed(j_r, r_r[1]))
                j_r.neededby.append(neededby_job(j_j, r_r[1]))
        for i_r in r:
            ceil = float("inf")
            for i_j in i_r.neededby:
                if ceil > i_j.j.priority:
                    ceil = i_j.j.priority
            i_r.ceil = ceil

        print("Direct blocking")
        for i_j in j:
            i_j_index = j.index(i_j)
            for res in i_j.needed:
                n_time = res.t
                for b_j in res.res.neededby:
                    b_j_index = j.index(b_j.j)
                    if b_j_index >=  i_j_index:
                        continue
                    print("\t{} blocks {} by {} for res {}".format(i_j.name,b_j.j.name,n_time,res.res.name))
        print("Priority Inheritance Blocking")
        for i_j in j:
            for res in i_j.needed:
                n_time = res.t
                for r_j in j:
                    if r_j.priority < i_j.priority and r_j.priority > res.res.ceil and r_j != i_j:
                        print("\t{} blocks {} by {} through res {}".format(i_j.name,r_j.name,n_time,res.res.name))
        print("Avoidance blocking/Priority ceiling blocking")
        for i_r in r:
            for i_j in i_r.neededby:
                i_time = i_j.t
                for j_r in r:
                    if j_r == i_r:
                        continue
                    for j_j in j_r.neededby:
                        #print(i_r.name, i_r.ceil, i_j.j.name, i_j.j.priority, j_r.name, j_r.ceil, j_j.j.name, j_j.j.priority)
                        if j_j.j.priority < i_j.j.priority and j_j.j != i_j.j and i_r.ceil <= j_j.j.priority:
                            print("\t{} blocks {} by {} by holding res {}".format(i_j.j.name,j_j.j.name,i_time,i_r.name))
        
