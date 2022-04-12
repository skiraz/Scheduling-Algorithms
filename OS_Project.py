from time import sleep

class Process():
    def __init__(self,ID,Arrival_Time,Burst_Time):
        self.Arrival_Time = Arrival_Time
        self.Burst_Time = Burst_Time
        self.Burst_Remaining = Burst_Time
        self.ID = ID
        self.Start= None
        self.completion = None
        self.waiting = None
        self.turnaround = None

def Round_Robin(quantum,Num_Proc,Arrival_Time,Burst_Time , unit):
    processes =[]
    id = 1
    z = sorted(zip(Arrival_Time,Burst_Time))
    for A , B in z:
        processes.append(Process(id,A,B))
        id+=1
    Done = Num_Proc
    timer = 0
    i=0
    cnt=0
    while Done > 0 :
            if (processes[i].Burst_Remaining <= quantum) & (processes[i].Burst_Remaining > 0):
                if processes[i].Burst_Time == processes[i].Burst_Remaining:
                    processes[i].Start = timer
                timer = timer + processes[i].Burst_Remaining
                processes[i].Burst_Remaining = 0
                cnt = 1
            elif processes[i].Burst_Remaining > 0:
                if processes[i].Burst_Time == processes[i].Burst_Remaining:
                    processes[i].Start = timer
                processes[i].Burst_Remaining = processes[i].Burst_Remaining - quantum
                timer = timer + quantum
            if (processes[i].Burst_Remaining == 0) & (cnt == 1):
                processes[i].completion = timer
                processes[i].turnaround = processes[i].completion - processes[i].Arrival_Time
                processes[i].waiting = processes[i].turnaround - processes[i].Burst_Time
                cnt =  0
                Done-=1

            if i + 1 == Num_Proc: i = 0

            elif processes[i + 1].Arrival_Time <= timer: i += 1

            else:  i = 0
    return processes

def Pre_Emptive_SJF(Num_Proc,Arrival_Time,Burst_Time):
    Done=0
    timer =0
    processes=[]
    id = 1
    for A,B in zip(Arrival_Time,Burst_Time):
        processes.append(Process(id,A,B))
        id+=1
    processes.append(Process(id,0,1000000))
    while(Done!=Num_Proc):
        low = Num_Proc
        for i in range(Num_Proc):
            if (processes[i].Arrival_Time <=timer) & (processes[i].Burst_Remaining < processes[low].Burst_Remaining) & (processes[i].Burst_Remaining>0):
                if processes[i].Burst_Remaining==processes[i].Burst_Time: processes[i].Start=timer
                low = i
        processes[low].Burst_Remaining-=1
        if (processes[low].Burst_Remaining==0):
            Done+=1
            processes[low].completion = timer+1
            processes[low].waiting = processes[low].completion - processes[low].Arrival_Time - processes[low].Burst_Time
            processes[low].turnaround = processes[low].completion - processes[low].Arrival_Time

        timer+=1
    return timer , processes

if __name__=="__main__":
    print("Enter the Number of processes :")
    num = int(input())
    Arrival_Times=[]
    Burst_Times = []
    for i in range(num):
        Arrival_Times.append(int(input(F"enter the Arrival time for process {i+1} :")))
        Burst_Times.append(int(input(F"enter the Burst time for process {i+1} : ")))
    quantum = int(input("Enter the Quantum : "))
    tp_unit = input("enter the throughput unit : ")
    print("Enter the number of one of these options :")
    print("1 - Compute Round Robin")
    print("2 - Compute Pre-Emptive SJF")
    print("3 - compare both ")
    x = int(input())
    if x==1:
        processes = Round_Robin(quantum,num,Arrival_Times,Burst_Times,tp_unit)
        print("ID ", " AT", "  BT ", " TAT", " Wait", " Start", "   EXIT", )
        sumTA =sumWT = sumRS=0
        tp = []
        for i in processes:
            print(f"{str(i.ID).ljust(3)}  {str(i.Arrival_Time).ljust(3)}   {str(i.Burst_Time).ljust(3)}   {str(i.turnaround).ljust(3)}   {str(i.waiting).ljust(3)}   {str(i.Start).ljust(3)}   {str(i.completion).ljust(3)}  ")
            sumTA += i.turnaround
            sumWT += i.waiting
            sumRS += (i.Start - i.Arrival_Time)
            tp.append(i.completion)

        print("Average Waiting time : ", sumWT / num)
        print("Average turnaround time : ", sumTA / num)
        print("Average Response time : ", sumRS / num)
        print(f"Average Throughput time {tp_unit} PER SECOND: ", num / max(tp))
    if x==2:
        timer, processes = Pre_Emptive_SJF(num, Arrival_Times, Burst_Times)
        print("ID ", " AT", "  BT ", " TAT", " Wait", " Start", "   EXIT", )
        processes.pop(-1)
        w = t = res = []
        for i in processes:
            print(f"{str(i.ID).ljust(3)}  {str(i.Arrival_Time).ljust(3)}   {str(i.Burst_Time).ljust(3)}   {str(i.turnaround).ljust(3)}   {str(i.waiting).ljust(3)}   {str(i.Start).ljust(3)}   {str(i.completion).ljust(3)}  ")
            w.append(i.waiting)
            t.append(i.turnaround)
            res.append(i.Start - i.Arrival_Time)
        print(f"Average Waiting Time: {sum(w) / num} ")
        print(f"Average Turn Around Time : {sum(t) / num} ")
        print(f"Average response Time: {sum(res) / num} ")
        print(f"Average Throughput  {tp_unit} PER SECOND: {sum(Burst_Times) / timer} ")
    if x==3:
        timer, processesP = Pre_Emptive_SJF(num, Arrival_Times, Burst_Times)
        processesR = Round_Robin(quantum,num,Arrival_Times,Burst_Times,tp_unit)

        processesP.pop(-1)
        w = t = res = []
        for i in processesP:
            w.append(i.waiting)
            t.append(i.turnaround)
            res.append(i.Start - i.Arrival_Time)

        processesR = Round_Robin(quantum, num, Arrival_Times, Burst_Times, tp_unit)
        sumTA = sumWT = sumRS = 0
        tp = []
        for i in processesR:
            sumTA += i.turnaround
            sumWT += i.waiting
            sumRS += (i.Start - i.Arrival_Time)
            tp.append(i.completion)

        #pre emptive
        P_avg_wait = sum(w) / num
        P_avg_Tat = sum(t) / num
        P_avg_res = sum(res) / num
        P_avg_throuput = sum(Burst_Times) / timer

        #round robin
        R_avg_wait =  sumWT / num
        R_avg_Tat = sumTA / num
        R_avg_res = sumRS / num
        R_avg_throuput = num / max(tp)

        pre = "Pre Emptive Shortest job first "
        rr = "Round Robin "
        d = "Did Better Than "

        print(pre + " average Throughput :", P_avg_throuput)
        print(rr + " average Throughput :", R_avg_throuput)
        if (P_avg_throuput<R_avg_throuput):
            print(pre ,d ,rr , "in throughput" )
        else :
            print(rr ,d ,pre , "in throughput" )

        print("======================")

        print(pre + " average turn around time :", P_avg_Tat)
        print(rr + " average turn around time :", R_avg_Tat)
        if (P_avg_Tat < R_avg_Tat):
            print(pre, d, rr, "in turn around time")
        else:
            print(rr, d, pre, "in turn around time")

        print("======================")


        print(pre + " average waiting time :", P_avg_wait)
        print(rr + " average  waiting time :", R_avg_wait)
        if (P_avg_wait < R_avg_wait):
            print(pre, d, rr, "in  waiting time")
        else:
            print(rr, d, pre, "in  waiting time")

        print("======================")


        print(pre + " average Response :", P_avg_res)
        print(rr + " average Response :", R_avg_res)

        if (P_avg_res < R_avg_res):
            print(pre, d, rr, "in Response")
        else:
            print(rr, d, pre, "in Response")

        print("======================")





    sleep(100)



