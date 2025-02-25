import heapq

class ShortestPathAgent:
    def __init__(self, env):
        self.env = env

    def heuristic(self, start, goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])
    
    def get_neighbors(self,node):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if 0 <= neighbor[0] < self.env.size_x and 0 <= neighbor[1] < self.env.size_y:
                neighbors.append(neighbor)
        
        return neighbors
    
    def shortest_path(self, start, goal):
        open_list = []
        heapq.heappush(open_list,(0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_list:
            current = heapq.heappop(open_list)[1]

            if current == goal:
                return self.reconstruct_path(came_from, current)
            
            #Check each neighbor to the current node
            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                
                #If the node is new or we found a new path with a lower cost
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
        return []
    
    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def get_action_from_position(self, start, end):
        if end[0] == start[0] - 1: #left
            return 0
        if end[0] == start[0] + 1: #right
            return 1
        if end[1] == start[1] - 1: #down
            return 2
        if end[1] == start[1] + 1: #up
            return 3
    
    def choose_action(self):
        start = self.env.agent_pos
        
        self.min_path = []
        min_path_len = float('inf')

        #Get shortest path
        for exit in self.env.exit_list:
            path = self.shortest_path(start, exit)
            if len(path) < min_path_len:
                min_path_len = len(path)
                self.min_path = path
            
        #Find action based on direction of shortest path from current position (start)
        if len(self.min_path) > 1:
            next_step = path[1]
            return self.get_action_from_position(start, next_step)
    


        