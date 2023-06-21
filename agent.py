import time


class Agent():

    def __init__(self, world, label_grid):
        self.world = world  
        self.knowledge_base = [[[] for i in range(self.world.cols)] for j in range(
            self.world.rows)]  
        self.knowledge_base[self.world.agent_row][self.world.agent_col].append('A')  
        self.stenches = 0  
        self.out_cave = [[self.world.agent_row, self.world.agent_col]]
        self.visited()
        self.world.cave_in_row = self.world.agent_row
        self.world.cave_in_col = self.world.agent_col
        self.glitter = False
        self.grab_gold = False
        self.have_gold = False
        self.label_grid = label_grid

        self.re_world()

    def re_world(self):
        for i in range(self.world.rows):
            for j in range(self.world.cols):
                updated_text = []
                if 'A' in self.knowledge_base[i][j]:
                    updated_text.append('\nAgent\n')
                if 'W' in self.knowledge_base[i][j]:
                    updated_text.append('W')
                if 'P' in self.knowledge_base[i][j]:
                    updated_text.append('P')
                if 'B' in self.knowledge_base[i][j]:
                    updated_text.append('B')
                if 'S' in self.knowledge_base[i][j]:
                    updated_text.append('S')
                if 'G' in self.knowledge_base[i][j]:
                    updated_text.append('G')

                updated_str = "" 
                self.label_grid[i][j].change_text(
                    updated_str.join(updated_text))
                if '.' in self.knowledge_base[i][j]:
                    self.label_grid[i][j].label.config(bg="green")
                    
                if 'S' in self.knowledge_base[i][j] or 'B' in self.knowledge_base[i][j] and '.' in self.knowledge_base[i][j]:
                    self.label_grid[i][j].label.config(bg="red")
                                      
                if 'G' in self.knowledge_base[i][j] and '.' in self.knowledge_base[i][j]:
                    self.label_grid[i][j].label.config(bg="yellow")

                    
                self.label_grid[i][j].label.update()

    def bump_wall(self):
        
        if self.world.agent_row-1 == self.out_cave[-1][0]:
            self.move('u')
        if self.world.agent_row+1 == self.out_cave[-1][0]:
            self.move('d')
        if self.world.agent_col+1 == self.out_cave[-1][1]:
            self.move('r')
        if self.world.agent_col-1 == self.out_cave[-1][1]:
            self.move('l')
        
        del self.out_cave[-1]

    def leave_cave(self):
        print("A safe place : "+str(self.out_cave))
        for tile in reversed(self.out_cave):
            if self.world.agent_row-1 == tile[0]:
                self.move('u')
            if self.world.agent_row+1 == tile[0]:
                self.move('d')
            if self.world.agent_col+1 == tile[1]:
                self.move('r')
            if self.world.agent_col-1 == tile[1]:
                self.move('l')


            if self.world.cave_in_row == self.world.agent_row:
                if self.world.cave_in_col == self.world.agent_col:
                    if self.glitter == True:
                        self.have_gold = True
                        break
                            
                                           
                        
    def explore_world(self):
        last_move = ''
        already_moved = False
        while self.glitter == False:
            if self.glitter == True:
                break
            try:
                if '.' not in self.knowledge_base[self.world.agent_row][self.world.agent_col+1] and self.is_safe_move(self.world.agent_row, self.world.agent_col+1):
                    if already_moved == False:
                        if self.move('r'):
                            already_moved = True
            except IndexError:
                pass
            
            try:
                if '.' not in self.knowledge_base[self.world.agent_row-1][self.world.agent_col] and self.is_safe_move(self.world.agent_row-1, self.world.agent_col):
                    if already_moved == False:
                        if self.move('u'):
                            already_moved = True
            except IndexError:
                pass


            try:
                if '.' not in self.knowledge_base[self.world.agent_row+1][self.world.agent_col] and self.is_safe_move(self.world.agent_row+1, self.world.agent_col):
                    if already_moved == False:
                        if self.move('d'):
                            already_moved = True

            except IndexError:
                pass

            try:
                if '.' not in self.knowledge_base[self.world.agent_row][self.world.agent_col-1] and self.is_safe_move(self.world.agent_row, self.world.agent_col-1):
                    if already_moved == False:
                        if self.move('l'):
                            already_moved = True

            except IndexError:
                pass                              
        
            if already_moved == False:
                self.bump_wall()

            already_moved = False

                
    def move(self, direction):

        self.re_world()

        if self.glitter == True and self.grab_gold == False:
            self.grab_gold == True
            if 'G' in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
                self.knowledge_base[self.world.agent_row][self.world.agent_col].remove('G')

        successful_move = False

        
        if direction == 'r':
            if self.is_safe_move(self.world.agent_row, self.world.agent_col+1):
                successful_move = self.move_right()
        if direction == 'u':
            if self.is_safe_move(self.world.agent_row-1, self.world.agent_col):
                successful_move = self.move_up()
        if direction == 'l':
            if self.is_safe_move(self.world.agent_row, self.world.agent_col-1):
                successful_move = self.move_left()
        if direction == 'd':
            if self.is_safe_move(self.world.agent_row+1, self.world.agent_col):
                successful_move = self.move_down()

        if successful_move:
            self.add_knowledge_base()
            self.visited()
            self.stench_wumpus()
            self.breeze_pits()
            self.clean_state()
            self.confirm_wumpus_knowledge()

            
            if 'G' in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
                self.glitter = True
                
            if self.glitter == False:
                self.out_cave.append(
                    [self.world.agent_row, self.world.agent_col])
            
            time.sleep(1)
            
        return successful_move
       
        
    def add_knowledge_base(self):
        if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'B' not in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
                self.knowledge_base[self.world.agent_row][self.world.agent_col].append('B')
        if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'S' not in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
                self.knowledge_base[self.world.agent_row][self.world.agent_col].append('S')
        if 'G' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'G' not in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
                self.knowledge_base[self.world.agent_row][self.world.agent_col].append('G')
        if 'P' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'P' not in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
                self.knowledge_base[self.world.agent_row][self.world.agent_col].append('P')
        if 'W' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'W' not in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
                self.knowledge_base[self.world.agent_row][self.world.agent_col].append('W')

    def breeze_pits(self):
        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row-1][self.world.agent_col]:
                        if 'P' not in self.knowledge_base[self.world.agent_row-1][self.world.agent_col]:
                            self.knowledge_base[self.world.agent_row -
                                                1][self.world.agent_col].append('P')
        except IndexError:
            pass

        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col+1 < self.world.cols:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col+1]:
                        if 'P' not in self.knowledge_base[self.world.agent_row][self.world.agent_col+1]:
                            self.knowledge_base[self.world.agent_row][self.world.agent_col+1].append('P')
        except IndexError:
            pass

        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row+1 < self.world.rows:
                    if '.' not in self.world.world[self.world.agent_row+1][self.world.agent_col]:
                        if 'P' not in self.knowledge_base[self.world.agent_row+1][self.world.agent_col]:
                            self.knowledge_base[self.world.agent_row +
                                                1][self.world.agent_col].append('P')
        except IndexError:
            pass

        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col-1]:
                        if 'P' not in self.knowledge_base[self.world.agent_row][self.world.agent_col-1]:
                            self.knowledge_base[self.world.agent_row][self.world.agent_col-1].append('P')
        except IndexError:
            pass

    def stench_wumpus(self):
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row-1][self.world.agent_col]:
                        if 'W' not in self.knowledge_base[self.world.agent_row-1][self.world.agent_col]:
                            self.knowledge_base[self.world.agent_row -
                                                1][self.world.agent_col].append('W')
        except IndexError:
            pass
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col+1 < self.world.cols:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col+1]:
                        if 'W' not in self.knowledge_base[self.world.agent_row][self.world.agent_col+1]:
                            self.knowledge_base[self.world.agent_row][self.world.agent_col+1].append('W')
        except IndexError:
            pass
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row+1 < self.world.rows:
                    if '.' not in self.world.world[self.world.agent_row+1][self.world.agent_col]:
                        if 'W' not in self.knowledge_base[self.world.agent_row+1][self.world.agent_col]:
                            self.knowledge_base[self.world.agent_row +
                                                1][self.world.agent_col].append('W')
        except IndexError:
            pass
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col-1]:
                        if 'W' not in self.knowledge_base[self.world.agent_row][self.world.agent_col-1]:
                            self.knowledge_base[self.world.agent_row][self.world.agent_col-1].append('W')
        except IndexError:
            pass

    def clean_state(self):
        self.stenches = 0

        for i in range(self.world.rows):
            for j in range(self.world.cols):
                if 'S' in self.knowledge_base[i][j]:
                    self.stenches += 1
                if 'W' in self.knowledge_base[i][j]:
                    try:
                        if i-1 >= 0:
                            if '.' in self.knowledge_base[i-1][j]:
                                if 'S' not in self.knowledge_base[i-1][j]:
                                    self.knowledge_base[i][j].remove('W')
                                    self.knowledge_base[i][j].append('NW')
                    except IndexError:
                        pass
                    try:
                        if j+1 < self.world.cols:
                            if '.' in self.knowledge_base[i][j+1]:
                                if 'S' not in self.knowledge_base[i][j+1]:
                                    self.knowledge_base[i][j].remove('W')
                                    self.knowledge_base[i][j].append('NW')
                    except IndexError:
                        pass
                    try:
                        if i+1 < self.world.rows:
                            if '.' in self.knowledge_base[i+1][j]:
                                if 'S' not in self.knowledge_base[i+1][j]:
                                    self.knowledge_base[i][j].remove('W')
                                    self.knowledge_base[i][j].append('NW')
                    except IndexError:
                        pass
                    try:
                        if j-1 >= 0:
                            if '.' in self.knowledge_base[i][j-1]:
                                if 'S' not in self.knowledge_base[i][j-1]:
                                    self.knowledge_base[i][j].remove('W')
                                    self.knowledge_base[i][j].append('NW')
                    except IndexError:
                        pass

                if 'P' in self.knowledge_base[i][j]:
                    try:
                        if i-1 >= 0:
                            if '.' in self.knowledge_base[i-1][j]:
                                if 'B' not in self.knowledge_base[i-1][j]:
                                    self.knowledge_base[i][j].remove('P')
                                    self.knowledge_base[i][j].append('NP')
                    except IndexError:
                        pass
                    try:
                        if j+1 < self.world.cols:
                            if '.' in self.knowledge_base[i][j+1]:
                                if 'B' not in self.knowledge_base[i][j+1]:
                                    self.knowledge_base[i][j].remove('P')
                                    self.knowledge_base[i][j].append('NP')
                    except IndexError:
                        pass
                    try:
                        if i+1 < self.world.rows:
                            if '.' in self.knowledge_base[i+1][j]:
                                if 'B' not in self.knowledge_base[i+1][j]:
                                    self.knowledge_base[i][j].remove('P')
                                    self.knowledge_base[i][j].append('NP')
                    except IndexError:
                        pass
                    try:
                        if j-1 >= 0:
                            if '.' in self.knowledge_base[i][j-1]:
                                if 'B' not in self.knowledge_base[i][j-1]:
                                    self.knowledge_base[i][j].remove('P')
                                    self.knowledge_base[i][j].append('NP')
                    except IndexError:
                        pass

    def confirm_wumpus_knowledge(self):
        for i in range(self.world.rows):
            for j in range(self.world.cols):
                if 'W' in self.knowledge_base[i][j]:
                    stenches_around = 0
                    try:
                        if i-1 >= 0:
                            if 'S' in self.knowledge_base[i-1][j]:
                                stenches_around += 1
                    except IndexError:
                        pass
                    try:
                        if j+1 < self.world.cols:
                            if 'S' in self.knowledge_base[i][j+1]:
                                stenches_around += 1
                    except IndexError:
                        pass
                    try:
                        if i+1 < self.world.rows:
                            if 'S' in self.knowledge_base[i+1][j]:
                                stenches_around += 1
                    except IndexError:
                        pass
                    try:
                        if j-1 >= 0:
                            if 'S' in self.knowledge_base[i][j-1]:
                                stenches_around += 1
                    except IndexError:
                        pass

                    if stenches_around < self.stenches:
                        self.knowledge_base[i][j].remove('W')
                        self.knowledge_base[i][j].append('NW')

    def move_up(self):
        try:
            if self.world.agent_row-1 >= 0:
                self.remove_agent()
                self.world.agent_row -= 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False

    def move_right(self):
        try:
            if self.world.agent_col+1 < self.world.cols:
                self.remove_agent()
                self.world.agent_col += 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False

    def move_down(self):
        try:
            if self.world.agent_row+1 < self.world.rows:
                self.remove_agent()
                self.world.agent_row += 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False

    def move_left(self):
        try:
            if self.world.agent_col-1 >= 0:
                self.remove_agent()
                self.world.agent_col -= 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False

    def remove_agent(self):
        self.world.world[self.world.agent_row][self.world.agent_col].remove('A')
        self.knowledge_base[self.world.agent_row][self.world.agent_col].remove('A')

    def add_agent(self):
        self.world.world[self.world.agent_row][self.world.agent_col].append('A')
        self.knowledge_base[self.world.agent_row][self.world.agent_col].append('A')

    def visited(self):
        if '.' not in self.knowledge_base[self.world.agent_row][self.world.agent_col]:
            self.world.world[self.world.agent_row][self.world.agent_col].append('.')
            self.knowledge_base[self.world.agent_row][self.world.agent_col].append('.')
             

    def is_dead(self):
        if 'W' in self.world.world[self.world.agent_row][self.world.agent_col]:
            print("Died by wumpus")
            return True
        elif 'P' in self.world.world[self.world.agent_row][self.world.agent_col]:
            print("Died by pit")
            return True
        else:
            return False

    def is_safe_move(self, row, col):
        try:
            if 'W' in self.knowledge_base[row][col]:
                return False
        except IndexError:
            pass
        try:
            if 'P' in self.knowledge_base[row][col]:
                return False
        except IndexError:
            pass
        try:
            if 'W' in self.knowledge_base[row][col]:
                return False
        except IndexError:
            pass
        try:
            if 'P' in self.knowledge_base[row][col]:
                return False
        except IndexError:
            pass

        return True
                   
