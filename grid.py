from tkinter import *
from queue import PriorityQueue
import sys
import time


class Problem(object):

    def __init__(self,i_to_g,blocker,n):

        self.i_to_g = i_to_g
        self.n       = n
        self.blocker   = blocker
        self.goals   = list(i_to_g.values())

    def isGoalState(self,coord):
        return coord == self.goal
        '''if(self.goal[(queen.x,queen.y)]!=''):
            if(self.goal[(queen.x,queen.y)].id == queen.id ):
                return True'''
        return False
    def getChildren(self, current_pos):
        ret_list = []
        moves = [(current_pos[0]-1,current_pos[1]),(current_pos[0]+1,current_pos[1]),(current_pos[0],current_pos[1]+1) ,
                 (current_pos[0],current_pos[1]-1),(current_pos[0]-1,current_pos[1]+1) ,(current_pos[0]-1,current_pos[1]-1),
                 (current_pos[0]+1,current_pos[1]-1),(current_pos[0]+1,current_pos[1]+1)]
        
        for move in moves :
            if(self.isValidPos(move)):
                ret_list.append((move,move,1))

        return ret_list

    def isValidPos(self,coord):
        if (coord not in self.blocker) and (coord[0]<self.n and coord[1] < self.n) and (coord[0]>=0 and coord[1]>=0):
            return True
        return False
    def getCostOfActions(self,actions):
        return len(actions)


    def solve(self,heuristic):
        solutions =[]
        for i in self.i_to_g:
            self.initial = i
            self.goal = self.i_to_g[i]
            self.test = self.goal
            solution = Search.a_star_search(self,self.initial,heuristic)
            solutions.append(solution)
        return solutions

class Search:

    def Straight_line(cord1, cord2):
            return ((cord2[0]-cord1[0])**2 + (cord2[1]-cord1[1])**2)**.5

    def Chebyshev(cord1,cord2):
        x1 =cord1[0]
        y1 =cord1[1]
        x2 =cord2[0]
        y2 =cord2[1]
        return max(abs(x2-x1), abs(y2-y1))

    def Manhattan(cord1,cord2):
        x1 =cord1[0]
        y1 =cord1[1]
        x2 =cord2[0]
        y2 =cord2[1]
        return abs(x1-y1) + abs(x2-y2)

    def a_star_search(problem, node, heuristic):
        startnode = node
        seen = []
        PQ = PriorityQueue()
        PQ.put( (heuristic(node, problem.test),(node,[])))
        while not PQ.empty():
            val,(node,actions) = PQ.get()
            if (problem.isGoalState(node)):
                seen.append(node)
                return (startnode,actions)

            seen.append(node)

            for coord,d,cost in problem.getChildren(node):
                if coord not in seen:
                    seen.append(coord)
                    if not problem.isGoalState(coord):
                        seen.append(coord)

                    new_actions = actions + [d]
                    score = problem.getCostOfActions(new_actions) + heuristic(coord,problem.test)
                    PQ.put((score,(coord, new_actions)))

        
            

class Grid:

    def __init__(self, size, rows, cols):
        self.size = size
        self.cols = cols
        self.rows = rows
        self.board_height = (self.rows * self.size)
        self.board_width = (self.cols * self.size)
        self.master = Tk()
        self.canvas = Canvas(self.master, width=self.board_width, height=self.board_height)
        self.canvas.pack()
        self.draw_grid()
        self.blocks  = []
        self.goals = []
        self.source = []
        self.enable_source = False
        self.enable_goal = False
        self.heuristic = None
        self.add_buttons()
        mainloop()

    def add_buttons(self):
        self.solve_button =  Button(self.master, text="Find Path", command=self.find_path)
        self.source_button = Button(self.master, text="Source" , command=(lambda self=self :self.set_enable_source(True)))
        self.goal_button = Button(self.master, text="Goal", command=(lambda self=self :self.set_enable_goal(True)))
        self.clear_all_button = Button(self.master, text="Clear All", command=self.clear_all)
        self.clear_path_button = Button(self.master, text="Clear Path", command=self.clear_path)
        self.source_button.pack(side=LEFT)
        self.goal_button.pack(side=LEFT)
        self.clear_all_button.pack(side=LEFT)
        self.clear_path_button.pack(side=LEFT)
        self.solve_button.pack(side=LEFT)
        self.heuristic_var = IntVar()
        Radiobutton(self.master, text="Straight line", variable=self.heuristic_var, value=1).pack(side=LEFT)
        Radiobutton(self.master, text="Chebyshev", variable=self.heuristic_var, value=2).pack(side=LEFT)
        Radiobutton(self.master, text="Manhattan", variable=self.heuristic_var, value=3).pack(side=LEFT)
        self.canvas.bind("<Button-1>", self.click)

    def clear_path(self):
        for i in self.canvas.find_all():
            if self.canvas.itemcget(i, "fill") == "green":
                self.canvas.itemconfig(i,fill="white")


    def clear_all(self):
        for i in self.canvas.find_all():
            self.canvas.itemconfig(i,fill="white")

        self.blocks  = []
        self.goals = []
        self.source = []

    def find_path(self):
        initials_to_goals =dict(zip(self.source,self.goals))
        p = Problem(initials_to_goals,self.blocks,self.rows)
        fn = Search.Straight_line
        if self.heuristic_var.get()==2:
            fn = Search.Chebyshev
        if self.heuristic_var.get()==3:
            fn=Search.Manhattan

        moves = p.solve(fn)[0][1][:-1]
        for move in moves:
            self.change_color(move[0],move[1],"green")


    def get_blocks(self):
        return self.blocks

    def set_enable_source(self,bool):
        self.enable_source=bool
        if bool:
            self.source_button['state'] = 'disabled'
        else:
            self.source_button['state'] = 'normal'

    def set_enable_goal(self,bool):
        self.enable_goal=bool
        if bool:
            self.goal_button['state'] = 'disabled'
        else:
            self.goal_button['state'] = 'normal'

    def set_goal(self,i):
        rowcol = self.i_to_rowcol(i)
        if self.goals:
            self.change_color(self.goals[0][0],self.goals[0][1  ],"white")
        self.goals = [rowcol]

    def set_source(self,i):
        rowcol = self.i_to_rowcol(i)
        if self.source:
            self.change_color(self.source[0][0],self.source[0][1  ],"white")
            self.blocks.remove(rowcol)
        self.source = [rowcol]
        self.blocks.append(rowcol)

    def draw_grid(self):

        x1 = 0
        y1 = 0
        x2 = x1+self.size
        y2 = y1+self.size

        for j in range(0,self.board_height,(self.board_height//self.rows)):
            for i in range(0,self.board_width,(self.board_width//self.cols)):
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                x1+=self.size
                y1+=0
                x2 = x1+self.size
                y2 = y1+self.size

            x1 = 0
            y1 += self.size
            x2 = x1+self.size
            y2 = y1+self.size

    def change_color(self, row,col,color="blue"):
        i = self.rowcol_to_i(row,col)
        self.canvas.itemconfig(i,fill=color)

    def click(self, event):
        cur = self.canvas.find_withtag(CURRENT)
        if cur:

            if self.canvas.itemcget(CURRENT, "fill") == "white":
                if self.enable_source:
                    self.canvas.itemconfig(CURRENT, fill="blue")
                    self.set_source(cur[0]) 
                    self.set_enable_source(False)
                elif self.enable_goal:
                    self.canvas.itemconfig(CURRENT, fill="gold")
                    self.set_goal(cur[0]) 
                    self.set_enable_goal(False)
                else:
                    self.canvas.itemconfig(CURRENT, fill="red")
                    self.blocks.append(self.i_to_rowcol(cur[0]))

            elif self.canvas.itemcget(CURRENT, "fill") == "red":
                self.canvas.itemconfig(CURRENT, fill="white")
                self.blocks.remove(self.i_to_rowcol(cur[0]))


    def rowcol_to_i(self,row,col):
        i = self.cols*row + col + 1
        return i

    def i_to_rowcol(self,i):
        row = (i//self.cols)
        col = (i%self.cols)-1

        if col == -1:
            col = self.cols-1
            row-=1
        
        return row,col


if __name__ == '__main__':
    
    if(len (sys.argv) != 3):
        print("Usage: grid.py size len")
        print("Example: grid.py 25 25")
        exit(1)
    size = int(sys.argv[1])
    length = int(sys.argv[2])
    Grid(size,length,length)

