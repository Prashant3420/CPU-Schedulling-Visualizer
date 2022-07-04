import tkinter as tk
from tkinter import ttk
from tkinter import *
from ctypes import windll
from tkinter.messagebox import askyesno
import mysql.connector
from tkinter.font import Font
from tkinter.messagebox import showinfo
import webbrowser

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456",
    database="companyx"
)
myCursor = mydb.cursor()

windll.shcore.SetProcessDpiAwareness(1)


class RoundRobin_scheduling():
    def __init__(self,num_of_process,time):
        self.pnum=num_of_process
        self.data = []
        self.btime = []
        self.time_slice=time
        # self.process=[]

    def add_process(self,ProcessId,burst):
        # self.process.append()
        self.data.append([ProcessId,burst])
        self.btime.append([ProcessId,burst])

    def logic(self):
        counter = 0
        pdata = []
        pdata=self.data[:]
        comp=[]

        while len(pdata) != 0:
            n = len(pdata)
            print (n)
            while n != 0:
                n =  n-1
                temp = pdata[0]
                pdata.pop(0)
                counter = counter + min(temp[1],self.time_slice)
                temp[1] = temp[1] - min(temp[1],self.time_slice)

                if temp[1] != 0:
                    pdata.append(temp)
                else:
                    comp.append([temp[0],counter])

        comp = sorted(comp, key=lambda item: item[0])
        waiting = []

        for i in range(len(comp)):
            print(comp[i][0]," ",comp[i][1])

        print(len(comp), len(self.data))
        for i in range(len(comp)):
            a = comp[i][1]
            b=self.btime[i][1]
            print (a,b)
            waiting.append([i,a-b])

        print (waiting)

        return (comp,waiting)

obj = RoundRobin_scheduling(3,2)
obj.add_process(1,4)
obj.add_process(2,3)
obj.add_process(3,5)
obj.logic()














class fcfs_scheduling():
    def __init__(self,num_of_process):
        self.process=[]
        self.num = num_of_process
        self.data = dict()

    def add_process(self,ProcessId,arrival,burst):
       self.process.append(ProcessId)
       self.data[ProcessId]=[arrival,burst]

    def logic(self):
        n = self.num
        d = self.data

        d = sorted(d.items(), key=lambda item: item[1][0])

        ET = []
        for i in range(len(d)):
            # first process
            if i == 0:
                print (i,d[i],d[i][1],d[i][1][1],d[i][0],d[i][1][0])
                ET.append(d[i][1][1]+d[i][1][0])

            # get prevET + newBT
            else:
                ET.append(ET[i - 1] + d[i][1][1])

        TAT = []
        for i in range(len(d)):
            TAT.append(ET[i] - d[i][1][0])

        WT = []
        for i in range(len(d)):
            if TAT[i] - d[i][1][1] == 0:
                WT.append(0)
            else:
                WT.append(TAT[i] - d[i][1][1])

        avg_WT = 0
        for i in WT:
            avg_WT += i
        avg_WT = (avg_WT / n)

        print("Process | Arrival | Burst | Exit | Turn Around | Wait |")
        for i in range(n):
            print("   ", d[i][0], "   |   ", d[i][1][0], " |    ", d[i][1][1], " |    ", ET[i], "  |    ", TAT[i],
                  "  |   ", WT[i], "   |  ")
        print("Average Waiting Time: ", avg_WT)

        return (self.process,TAT,WT)


obj = fcfs_scheduling(5)
obj.add_process(1,2,6)
obj.add_process(2,5,2)
obj.add_process(3,1,8)
obj.add_process(4,0,3)
obj.add_process(5,4,4)
obj.logic()




class simulator(tk.Toplevel):

    def giveResult(self):
        nodes = int(self.vertices.get())
        print(type(nodes))
        r = []

        if self.selected.get() == "1" or self.selected.get() == '3':
            self.g = fcfs_scheduling(nodes)
            for i in self.edges:
                self.g.add_process(i[0], i[1], i[2])

            r1, r2, r3 = self.g.logic()
            for i in range(len(r1)):
                r.append([r1[i], r2[i], r3[i]])
        else:
            self.g = RoundRobin_scheduling(nodes,int(self.num_of_edges.get()))
            for i in self.edges:
                self.g.add_process(i[0], i[1])

            r1, r2 = self.g.logic()
            for i in range(len(r1)):
                r.append([r1[i][0],r1[i][1],r2[i][1]])

        # for i in self.edges:
        #     self.g.add_process(i[0],i[1],i[2])




        print ("r:",r)

        self.frame3 = LabelFrame(self.frame, text="EFFECTIVE CONNECTIONS", font=self.myfont,
                                 padx=20, pady=20, bg="black", fg="#1de962")
        self.frame3.grid(column=20, row=10, columnspan=5,sticky=tk.W)
        columns = ('PROCESS ID','COMPLETION','WAITING')

        self.tree = ttk.Treeview(self.frame3, columns=columns, show='headings')

        for i in columns:
            self.tree.heading(i, text=i)


        for row in r:
            self.tree.insert('', tk.END, values=row)

        # self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        self.tree.grid(row=230, column=1000, sticky='nsew', rowspan=400, columnspan=100)

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.frame3, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=230, column=2001, sticky='ns')


    def insertEdge(self):
        row = []

        if self.selected.get()=="2":
            a=int(self.text1.get())
            b=int(self.text3.get())
            row=[a,b]
        else:
            a = int(self.text1.get())
            b = int(self.text2.get())
            c=int(self.text3.get())
            row=[a,b,c]

        self.tree2.insert('', tk.END, values=row)

        self.edges.append(row)

    def generateGraph(self):

        self.frame4 = LabelFrame(self.frame, text="PROCESS INFO", font=self.myfont,
                                 padx=30, pady=10, bg="black", fg="#1de962")

        self.frame4.grid(column=20, row=0, columnspan=10,
                         rowspan=10, sticky=W)

        columns = None
        if self.selected.get() == "1":
            columns = ("PROCESS ID", "ARRIVAL TIME", "BURST TIME")
        elif self.selected.get() == "3":
            columns=('PROCESS ID','PRIORITY','BURST TIME')
        else:
            columns=('PROCESS ID', "BURST TIME")

        self.tree2 = ttk.Treeview(self.frame4, columns=columns, show='headings')

        for i in columns:
            self.tree2.heading(i, text=i)


        self.tree2.grid(row=230, column=1000, sticky='nsew', rowspan=400, columnspan=100)

        scrollbar = ttk.Scrollbar(self.frame4, orient=tk.VERTICAL, command=self.tree2.yview)
        self.tree2.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=230, column=2002, sticky='ns')

        self.frame2 = LabelFrame (self.frame, text = "PROCESS LIST", font = self.myfont,
                                  pady = 20,bg = "black", fg = "#1de962")
        self.frame2.grid (column = 0, row = 10,sticky=W)

        for i in range(int(self.vertices.get())):
            label4 = Label(self.frame2, text="PROCESS ID", bg="black", font=self.myfont,fg="#f0dc06",padx = 10, pady = 10)
            label4.grid(column=0, row=6)

            self.text1 = tk.StringVar()
            from_entry = Entry(self.frame2, textvariable=self.text1,font=self.buttonFont)
            from_entry.grid(column=1, row=6)

            if self.selected.get()=="1":
                label4 = Label(self.frame2, text="ARRIVAL", bg="black", font=self.myfont, fg="#f0dc06", padx=10, pady=10)
                label4.grid(column=0, row=7)
            elif self.selected.get()=="3":
                label4 = Label(self.frame2, text="PRIORITY", bg="black", font=self.myfont, fg="#f0dc06", padx=10, pady=10)
                label4.grid(column=0, row=7)



            if self.selected.get() != "2":
                self.text2 = tk.StringVar()
                to_entry = Entry(self.frame2, textvariable=self.text2, font=self.buttonFont)
                to_entry.grid(column=1, row=7)

            label5 = Label(self.frame2, text="BURST TIME", bg="black",font=self.myfont, fg="#f0dc06", padx=10, pady=10)
            label5.grid(column=0, row=8)

            self.text3 = tk.StringVar()
            weight_entry = Entry(self.frame2, textvariable=self.text3, font= self.buttonFont)
            weight_entry.grid(column=1, row=8)

            label3 = Label(self.frame, text="", bg="black")
            label3.grid(column=1, row=9, padx=40)

            self.button1 = Button(self.frame2, text="INSERT PROCESS", font=self.buttonFont, bg="#66FCf1",
                                  height=1,
                                  width=25)
            self.button1.config(command=self.insertEdge)
            self.button1.grid(column=1, row=10, padx=40, pady=20)






        button1 = Button(self.frame2, text="SCHEDULE PROCESSES", font=self.buttonFont, bg="red", height=1,
                         width=25, fg = "white")
        button1.config(command=self.giveResult)
        button1.grid(column=1, row=12, padx=40)


    def keyPressed(self):
        print (self.selected.get())


        logo_frame = Frame(self, width=10, height=10, borderwidth=0, bg="black")
        logo_frame.grid(column=10, row=10)
        self.frame_name = None

        self.frame = LabelFrame(self, text="SCHEDULING SIMULATOR",
                                font=self.myfont, padx=20, pady=20, bg="black",
                                fg="red")

        self.frame.place(x=30, y=360)

        self.new_frame = LabelFrame(self.frame, text="SCHEDULING REQUIREMENTS", font=self.myfont,
                                    padx=20, pady=20, bg="black", fg="#1de962")
        self.new_frame.grid(column=0, row=0)

        self.user_img = PhotoImage(file=r"C:\Users\piyush chauhan\Pictures\home.png")

        label1 = Label(self.new_frame, text="NO.OF PROCESS", bg="black", padx=10, pady=10, font=self.myfont,fg="#f0dc06")
        label1.grid(column=0, row=0,sticky=W)

        self.vertices = tk.StringVar()
        self.num_of_edges = tk.StringVar()

        vertices_entry = ttk.Entry(self.new_frame, textvariable=self.vertices, font=self.buttonFont)
        vertices_entry.focus()
        vertices_entry.grid(column=1, row=0, padx=40, pady=10)

        if self.selected.get() == "2":
            label1 = Label(self.new_frame, text="TIME SLICE", bg="black", padx=10, pady=10,font=self.myfont,fg="#f0dc06")
            label1.grid(column=0, row=1,sticky=W)
            num_of_edges_entry = ttk.Entry(self.new_frame, textvariable=self.num_of_edges, font=self.buttonFont)
            num_of_edges_entry.grid(column=1, row=1, padx=40, pady=10)

        button1 = Button(self.new_frame, text="GENERATE PROCESS LIST", font=self.buttonFont, bg="#66FCf1", height=1,
                         width=30)
        button1.config(command=self.generateGraph)
        button1.grid(column=1, row=3, padx=40, pady=20)


    def __init__(self,parent):
        super().__init__(parent)
        self.title ("Simulator")
        self.geometry ("2000x2000")
        self.config(bg="black")

        self.edges = []
        self.myfont = Font(
            family="corbel",
            size=10,
            weight="bold"
        )

        self.linkfont = Font(
            family="corbel",
            size=12,
            weight="bold"
        )

        self.buttonFont = Font(
            family="Arial",
            size=9,
            weight="bold"
        )

        label1 = Label(self,text="Hi Geek!", font=("Franklin Gothic Heavy",35),foreground="green",bg="black")
        label1.place(x=30,y=30)

        label2 = Label(self,text="Welcome to the CPU Scheduling Simulator.            \nRun Simulation and learn about algo in a better way",
                      font=("Arial",11),bg="black",fg="white",pady=20)
        label2.place(x=30,y=100)

        self.num_of_edges = None
        frame1 = LabelFrame (self, text="SCHEDULING ALGORITHM",
                             bg="black",fg="red",
                             font = self.myfont)
        frame1.place(x = 30, y= 200)

        self.selected = tk.StringVar()


        r1 = Radiobutton(frame1, text="First Come First Serve(FCFS)", variable=self.selected,
                         font=self.linkfont,foreground="white",background="black",
                         activeforeground="green",value='1',selectcolor="red")
        r2 = Radiobutton(frame1, text="Round Robin(RR)",variable=self.selected,
                         font=self.linkfont, foreground="white", background="black",
                         activeforeground="green",value='2',selectcolor="red")
        r3 = Radiobutton(frame1, text="Priority Queue Scheduling", variable=self.selected,
                         font=self.linkfont, foreground="white", background="black",
                         activeforeground="green",value='3',selectcolor="red")

        r1.grid(column=0,row=0,padx=20,pady = 10,sticky=W)
        r2.grid(column=1, row=0, padx=20,pady=10,sticky=W)
        r3.grid(column=2, row=0, padx=20,pady=10,sticky=W)

        button = Button(frame1, text="START SIMULATION", font=self.buttonFont, bg="white",
                        height=1, width=20,command=self.keyPressed)
        button.grid (column = 0, row = 3, pady=10,sticky=W,padx=45)





def callback(url):
    webbrowser.open_new(url)

class readArticle(tk.Toplevel):
    def __init__(self,parent):
        super(). __init__(parent)

        self.title ("Articles")
        self.geometry("2500x2500")
        self.config (bg ="black")

        self.myfont = Font(
            family="corbel",
            size=12,
            weight="bold"
        )

        self.bg = PhotoImage(file=r"C:\Users\piyush chauhan\Desktop\OS project images\nbg5.png")

        Label (self, image=self.bg).place(x=0,y=0)



        ''' ---------------------------FCFS-------------------------'''

        self.frame = LabelFrame(self, text='FCFS SCHEDULING',
                                font=self.myfont, padx=20, pady=20, bg="black",
                                fg="#f0dc06")

        self.frame.place(x=50, y=60)

        link1 = Label(self.frame, text="FCFS Scheduling Algorithm: What is, Example Program",
                      fg="green", cursor="hand2", font=("Arial",12),bg="black")
        link1.grid (column=0, row = 0, sticky=W,pady = 5)
        link1.bind("<Button-1>", lambda e: callback("https://www.guru99.com/fcfs-scheduling.html"))

        link1=Label (self.frame,text = "FCFS stands for First Come First Serve. A real-life example of \n"
                                       "the FCFS method is buying a movie ticket on the ticket counter.\n"
                                       "It is the simplest form of a CPU scheduling algorithm.              ",
                     fg="white",font = ("arial",10),bg="black")
        link1.grid(column=0,row=1,sticky=W,pady=10)



        link1 = Label(self.frame, text="Program fro FCFS CPU SCHEDULIING|Set 1-GeeksForGeeks",
                      fg="green", cursor="hand2", font=("Arial",12),bg="black")
        link1.grid (column=0, row = 2, sticky=W,pady =5)
        link1.bind("<Button-1>", lambda e: callback("https://www.geeksforgeeks.org/program-for-fcfs-cpu-scheduling-set-1/"))

        link1 = Label(self.frame, text="Given n processes with their burst times, the task is to find average\n"
                                       "waiting time and average turn around time using FCFS scheduling\n"
                                       "algorithm                                                                       "
                      "            ",
                      fg="white", font=("arial", 10), bg="black")
        link1.grid(column=0, row=3, sticky=W)



        '''---------------------------- SJF-----------------------'''

        self.frame = LabelFrame(self, text='SJF',
                                font=self.myfont, padx=20, pady=20, bg="black",
                                fg="#f0dc06")

        self.frame.place(x= 680, y=60)

        link1 = Label(self.frame, text="Shortest Job First(SJF) Scheduling in Operating System",
                      fg="green", cursor="hand2", font=("Arial", 12), bg="black")
        link1.grid(column=0, row=0, sticky=W, pady=5)
        link1.bind("<Button-1>", lambda e: callback(
            "https://data-flair.training/blogs/shortest-job-first-sjf-scheduling-in-operating-system/"))

        link1 = Label(self.frame, text="Characteristics of SJF Scheduling. Following are some characteristics\n"
                                       "of SJF: Associated with every job as it requires a unit of time for a\n"
                                       "job to complete. Helpful for batch-type processing.",
                      fg="white", font=("arial", 10), bg="black")
        link1.grid(column=0, row=1, sticky=W, pady=10)

        link1 = Label(self.frame, text="SJF Scheduling in OS-Tutorial and Example",
                      fg="green", cursor="hand2", font=("Arial", 12), bg="black")
        link1.grid(column=0, row=2, sticky=W, pady=5)
        link1.bind("<Button-1>", lambda e: callback("https://www.tutorialandexample.com/shortest-job-first-sjf-scheduling"))

        link1 = Label(self.frame, text="When all the processes are available at the same time, then the Shortest\n"
                                       "Job Scheduling algorithm becomes optimal. Non-Preemptive SJF: - In      \n"
                                       "Non-Preemptive Scheduling, if a CPU is located to the process.            ",
                      fg="white", font=("arial", 10), bg="black")
        link1.grid(column=0, row=3, sticky=W)

        '''--------------------------PRIORITY--------------------------'''

        self.frame = LabelFrame(self, text='PRIORITY',
                                font=self.myfont, padx=20, pady=20, bg="black",
                                fg="#f0dc06")

        self.frame.place(x=1290, y=60)

        link1 = Label(self.frame, text="Priority Scheduling Algorithm: Preemptive,Non-Preemptive",
                      fg="green", cursor="hand2", font=("Arial", 12), bg="black")
        link1.grid(column=0, row=0, sticky=W, pady=5)
        link1.bind("<Button-1>", lambda e: callback(
            "https://www.guru99.com/priority-scheduling-program.html"))

        link1 = Label(self.frame, text="Priority scheduling is a method of scheduling processes that is based \n"
                                       "on priority. In this algorithm, the scheduler selects the tasks to work\n"
                                       "as per the priority.                                                                    ",
                      fg="white", font=("arial", 10), bg="black")
        link1.grid(column=0, row=1, sticky=W, pady=10)

        link1 = Label(self.frame, text="Priority Scheduling in OS- Tutorial and Example",
                      fg="green", cursor="hand2", font=("Arial", 12), bg="black")
        link1.grid(column=0, row=2, sticky=W, pady=5)
        link1.bind("<Button-1>", lambda e: callback("https://www.tutorialandexample.com/priority-scheduling"))

        link1 = Label(self.frame, text="Priority Scheduling is a type of CPU Scheduling algorithm which is used \n"
                                       "for process scheduling based on some priorities                                \n",
                      fg="white", font=("arial", 10), bg="black")
        link1.grid(column=0, row=3, sticky=W)


        '''-------------------------- ROUND ROBIN---------------------'''

        self.frame = LabelFrame(self, text='ROUND ROBIN',
                                font=self.myfont, padx=20, pady=20, bg="black",
                                fg="#f0dc06")

        self.frame.place(x=30, y=700)

        link1 = Label(self.frame, text="Round Robin Scheduling Algorithm with Example",
                      fg="green", cursor="hand2", font=("Arial", 12), bg="black")
        link1.grid(column=0, row=0, sticky=W, pady=5)
        link1.bind("<Button-1>", lambda e: callback(
            "https://www.guru99.com/round-robin-scheduling-example.html"))

        link1 = Label(self.frame, text="Example of Round-robin Scheduling. Step 1) The execution begins with \n"
                                       "process P1, which has burst time 4. Here, every process executes for 2\n"
                                       "seconds. P2 and P3 are still in the waiting queue.                     ",
                      fg="white", font=("arial", 10), bg="black")
        link1.grid(column=0, row=1, sticky=W, pady=10)

        link1 = Label(self.frame, text="Program for Round Robin scheduling GeeksforGeeks",
                      fg="green", cursor="hand2", font=("Arial", 12), bg="black")
        link1.grid(column=0, row=2, sticky=W, pady=5)
        link1.bind("<Button-1>", lambda e: callback("https://www.geeksforgeeks.org/program-round-robin-scheduling-set-1/"))

        link1 = Label(self.frame, text="Round Robin is a CPU scheduling algorithm where each process is   \n"
                                       "assigned a fixed time slot in a cyclic way.. It is simple, easy to implement,    \n",
                                       # "and starvation-free as all processes get fair share of CPU. One of the most               \n"
                                       # "commonly used technique in CPU scheduling as a core.                                        ",
                      fg="white", font=("arial", 10), bg="black")
        link1.grid(column=0, row=3, sticky=W)

        '''-------------------------- Multi level---------------------'''

        self.frame = LabelFrame(self, text='MULTI LEVEL',
                                font=self.myfont, padx=20, pady=20, bg="black",
                                fg="#f0dc06")

        self.frame.place(x=660, y=700)

        link1 = Label(self.frame, text="Multilevel Queue Scheduling Algorithm - Studytonight",
                      fg="green", cursor="hand2", font=("Arial", 12), bg="black")
        link1.grid(column=0, row=0, sticky=W, pady=5)
        link1.bind("<Button-1>", lambda e: callback(
            "https://www.studytonight.com/operating-system/multilevel-queue-scheduling"))

        link1 = Label(self.frame, text="A multi-level queue scheduling algorithm partitions the ready queue into          \n"
                                       "several separate queues. The processes are permanently assigned to one        \n"
                                       "queue,generally based on some property of the process                                    ",
                      fg="white", font=("arial", 10), bg="black")
        link1.grid(column=0, row=1, sticky=W, pady=10)

        link1 = Label(self.frame, text="Multilevel Queue (MLQ) CPU Scheduling - GeeksforGeeks",
                      fg="green", cursor="hand2", font=("Arial", 12), bg="black")
        link1.grid(column=0, row=2, sticky=W, pady=5)
        link1.bind("<Button-1>",
                   lambda e: callback("https://www.geeksforgeeks.org/multilevel-queue-mlq-cpu-scheduling/"))

        link1 = Label(self.frame, text="Multilevel Queue (MLQ) CPU Scheduling. It may happen that processes in the\n"
                                       "ready queue can be divided into different classes where each class has its \n",
                                       # "own scheduling needs. For example, a common division is a foreground (interactive)\n"
                                       # "process and a background (batch) process.                                      ",
                      fg="white", font=("arial", 10), bg="black")
        link1.grid(column=0, row=3, sticky=W)

        '''--------------------------MULTI LEVEL FEEDBACK--------------------------'''

        self.frame = LabelFrame(self, text='MULTI LEVEL FEEDBACK',
                                font=self.myfont, padx=20, pady=20, bg="black",
                                fg="#f0dc06")

        self.frame.place(x=1320, y=700)

        link1 = Label(self.frame, text="Multilevel Feedback Queue Scheduling Algorithm",
                      fg="green", cursor="hand2", font=("Arial", 12), bg="black")
        link1.grid(column=0, row=0, sticky=W, pady=5)
        link1.bind("<Button-1>", lambda e: callback(
            "https://www.studytonight.com/operating-system/multilevel-feedback-queue-scheduling"))

        link1 = Label(self.frame, text="Although a multilevel feedback queue is the most general scheme, it is \n"
                                       "also the most complex. An example of a multilevel feedback queue can be \n"
                                       ,
                      fg="white", font=("arial", 10), bg="black")
        link1.grid(column=0, row=1, sticky=W)

        link1 = Label(self.frame, text="Multilevel Feedback Queue Scheduling \n(MLFQ)- GeeksforGeeks                   ",
                      fg="green", cursor="hand2", font=("Arial", 12), bg="black")
        link1.grid(column=0, row=2, sticky=W, pady=5)
        link1.bind("<Button-1>", lambda e: callback("https://www.geeksforgeeks.org/multilevel-feedback-queue-scheduling-mlfq-cpu-scheduling/"))

        link1 = Label(self.frame, text="Multilevel Feedback Queue Scheduling (MLFQ) keeps analyzing the \n"
                                       "behavior (time of execution) of processes and according to which it\n",                     fg="white", font=("arial", 10), bg="black")
        link1.grid(column=0, row=3, sticky=W)


class MainWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('2000x2000')
        self.title('Main Window')

        self.myfont = Font(
            family="corbel",
            size=10,
            weight="bold"
        )

        photo = tk.PhotoImage(file=r"C:\Users\piyush chauhan\Desktop\OS project images\bg3.png")

        image_label = ttk.Label(self, text="image", image=photo, padding=5)
        image_label.image = photo
        image_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame = LabelFrame(self, text = "LEARN",bg = "black", fg = "red",font=self.myfont, borderwidth=10, relief="sunken")
        self.frame.place(x=70,y=300)

        self.frame2 = LabelFrame(self, text="LEARN", bg="black", fg="red", font=self.myfont, borderwidth=10,
                                relief="sunken")
        self.frame2.place(x=750, y=300)
        self.frame3 = LabelFrame(self, text="DEVELOP", bg="black", fg="red", font=self.myfont, borderwidth=10,
                                relief="sunken")
        self.frame3.place(x=1425, y=300)

        mainWindowFont = Font(
            family="Arial",
            size=14,
            weight="bold",
        )

        self.buttonFont = Font(
            family="Arial",
            size=10,
            weight="bold"
        )

        label1 = ttk.Label(self.frame, font=mainWindowFont, foreground="#1de962",background="black",
                           text="RUN SIMULATIONS")
        label1.grid(column=0,row=0, pady = 5,sticky=W)
        label1 = ttk.Label(self.frame, foreground="white", background="black",
                           text="Learn about Gantt Charts and \nCPU scheduling Algorithms\nthrough simulations")
        label1.grid(column=0, row=1, pady=10,sticky=W)

        label2 = ttk.Label(self.frame2, font=mainWindowFont, foreground="#1de962", background="black",
                           text="READ ARTICLES")
        label2.grid(column=0, row=0, pady=5,sticky=W)
        label2 = ttk.Label(self.frame2, foreground="white", background="black",
                           text="Read indepth about CPU scheduling\nalgorithms and how they are \nimplemented at kernel level.")
        label2.grid(column=0, row=1, pady=10,sticky=W)


        label3 = ttk.Label(self.frame3, font=mainWindowFont, foreground="#1de962", background="black",
                           text="ABOUT APP")
        label3.grid(column=0, row=0, pady=5,sticky=W)
        label3 = ttk.Label(self.frame3, foreground="white", background="black",
                           text="Learn more about CPU SCHEDULING\nSUITE and contribute to the\ndevelopment of app")
        label3.grid(column=0, row=1, pady=10,sticky=W)


        button1 = Button(self.frame, text="OPEN SIMULATION", font=self.buttonFont, bg="white", height=1, width=17)
        button1.config(command=self.open_simulator_window)

        button2 = Button(self.frame2, text="READ ARTICLE", font=self.buttonFont, bg="white", height=1, width=15)
        button2.config(command=self.open_article_window)

        button3 = Button(self.frame3, text="LEARN APP", font=self.buttonFont, bg="white", height=1, width=13)
        # button3.config(command=self.open_generatePayslip_window)
        button3.bind("<Button-1>", lambda e: callback(
            "https://docs.google.com/document/d/1X9TX4e4OJ9_PBs85FkKGudmBZcx_ySfbPM-yJsTMO2Q/edit?usp=sharing"))



        button1.grid(column=1, row=1, padx=50, pady = 20)
        button2.grid(column=1, row=1, padx=50,pady =20)
        button3.grid(column=1, row=1, padx=30,pady=20)


    def open_simulator_window(self):
        window = simulator(self)
        window.grab_set()

    def open_article_window(self):
        window = readArticle(self)
        window.grab_set()







class App(tk.Tk):
    def checkDetails(self):
        print("checking details")

        sql = "select password from login_details where username = %s"
        myCursor.execute(sql, (self.username.get(),))
        myResult = myCursor.fetchall()

        for i in myResult:
            print(i)
            if (i[0] == ""):
                self.destroy()
            else:
                self.correctPass = i[0]

        print(type(self.correctPass))
        if self.password.get() != self.correctPass:
            self.destroy()
        else:
            window = MainWindow(self)
            window.grab_set()

    def returnKeyPressed(self):
        print("return key pressed")
        self.checkDetails()

    def loginWindow(self):
        self.user_img = PhotoImage(file=r"C:\Users\piyush chauhan\Pictures\username.png")
        self.pass_img = PhotoImage(file=r"C:\Users\piyush chauhan\Pictures\password.png")

        self.frame = LabelFrame(self, text='GEEK DETAILS',
                                font=self.myfont, padx=20, pady=20, bg="black",
                                fg="red")
        self.frame.place(x=1400, y=110)


        label1 = Label(self.frame, image=self.user_img, bg="black", padx=10, pady=10)
        label1.grid(column=0, row=0)
        label2 = Label(self.frame, image=self.pass_img, bg="black", padx=10, pady=10)
        label2.grid(column=0, row=1)

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        username_entry = ttk.Entry(self.frame, textvariable=self.username, font=self.buttonFont)
        username_entry.focus()
        username_entry.grid(column=1, row=0, padx=20, pady=10)

        password_entry = ttk.Entry(self.frame, textvariable=self.password, show="*", font=self.buttonFont)
        password_entry.grid(column=1, row=1, padx=30, pady=20)


        button1 = Button(self.frame, text="ENTER", font=self.buttonFont, bg="white", height=1, width=8)
        button1.config(command=self.returnKeyPressed)
        button1.grid(column=2, row=1,padx=22)

    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("2500x2500")
        self.config (bg = "black")
        # self.resizable(0, 0)

        self.myfont = Font(
            family="corbel",
            size=10,
            weight="bold"
        )


        self.buttonFont = Font(
            family="Arial",
            size=10,
            weight="bold"
        )

        self.code = "while (!login) cout << \"Can't access features!\""

        photo = tk.PhotoImage(file=r"C:\Users\piyush chauhan\Desktop\OS project images\bg7.png")
        # nphoto = tk.PhotoImage(file=r"C:\Users\piyush chauhan\Desktop\OS project images\bg8.png")

        image_label = ttk.Label(self, text="image", image=photo, background="black",padding=5)
        image_label.image = photo
        image_label.place (x=0,y=0)


        self.username = tk.StringVar()
        self.password = tk.StringVar()
        loginFont = Font(
            family="STsong",
            size=25,
            weight="bold",
            underline=1
        )



        label = Label(self, text=self.code, fg="#1de962", font=("courier new", 10), bg="black")
        label.place(x=780, y=710)

        button1 = Button(self, text="LOGIN", font=self.buttonFont, bg="white", height=2, width=8)
        button1.config(command=self.loginWindow)
        button1.place(x=1770,y=50)


if __name__ == "__main__":
    app = App()
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
finally:
    app.mainloop()

