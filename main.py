from tkinter import *
from agent import Agent
from world import World
from grid import Grid_Label
import time


def wumpus_world(master, world_file):
    world = World()
    world.generate_world(world_file)


    label_grid = [[Grid_Label(master, i, j) for j in range(
        world.cols)] for i in range(world.rows)]
    agent = Agent(world, label_grid)


    while agent.have_gold == False:
        agent.explore_world()
        if agent.glitter == True:
            agent.leave_cave()
        break

    
    agent.re_world()
    agent.knowledge_base[agent.world.agent_row][agent.world.agent_col].remove('A')
    time.sleep(1)
    agent.re_world()
    

master = Tk()
master.title("Wumpus World")

world = World()
world.generate_world("world.txt")
label_grid = [[Grid_Label(master, i, j)for j in range(world.cols)]
              for i in range(world.rows)]


world1 = Button(master, text="테스트 월드1",  command=lambda: wumpus_world(master, "world1.txt"), width=8,
                font="Verdana 10 bold", bg="gray80", fg="gray40", borderwidth=5, activeforeground="white", activebackground="gray40")
world2 = Button(master, text="테스트 월드2",  command=lambda: wumpus_world(master, "world2.txt"), width=8,
                font="Verdana 10 bold", bg="gray80", fg="gray40", borderwidth=5, activeforeground="white", activebackground="gray40")




world1.grid(row=4, column=1)
world2.grid(row=4, column=2)


mainloop()
