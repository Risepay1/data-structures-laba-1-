from collections import deque

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def append(self, x, y):
        new_node = Node(x, y)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
    
    def contains(self, x, y):
        current = self.head
        while current:
            if current.x == x and current.y == y:
                return True
            current = current.next
        return False

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0]) if self.rows > 0 else 0
    
    def solve(self, starts, ends, method='array', separate_exits=True):
        """Решает лабиринт одним из трех методов:
        - 'array' - с использованием массива
        - 'linked_list' - с использованием связанного списка
        - 'std' - с использованием стандартной библиотеки (BFS)
        """
        # Проверка входов и выходов
        for x in starts:
            if self.maze[0][x] != 0:
                return False
        for y in ends:
            if self.maze[-1][y] != 0:
                return False
        
        if method == 'array':
            return self._solve_with_array(starts, ends, separate_exits)
        elif method == 'linked_list':
            return self._solve_with_linked_list(starts, ends, separate_exits)
        elif method == 'std':
            return self._solve_with_std(starts, ends, separate_exits)
        else:
            raise ValueError("Неизвестный метод. Используйте 'array', 'linked_list' или 'std'")
    
    def _solve_with_array(self, starts, ends, separate_exits):
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        
        for i in range(len(starts)):
            local_visited = [row[:] for row in visited]
            x, y = 0, starts[i]
            exit_y = ends[i] if separate_exits else ends
            
            if not self._dfs_array(local_visited, x, y, self.rows-1, exit_y, separate_exits):
                return False
        
        return True
    
    def _dfs_array(self, visited, x, y, target_x, target_y, separate_exits):
        if x == target_x and (not separate_exits or y == target_y):
            return True
        
        if (x < 0 or x >= self.rows or y < 0 or y >= self.cols or 
            self.maze[x][y] == 1 or visited[x][y]):
            return False
        
        visited[x][y] = True
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            if self._dfs_array(visited, x + dx, y + dy, target_x, target_y, separate_exits):
                return True
        
        visited[x][y] = False
        return False
    
    def _solve_with_linked_list(self, starts, ends, separate_exits):
        for i in range(len(starts)):
            visited = LinkedList()
            x, y = 0, starts[i]
            exit_y = ends[i] if separate_exits else ends
            
            if not self._dfs_linked_list(visited, x, y, self.rows-1, exit_y, separate_exits):
                return False
        
        return True
    
    def _dfs_linked_list(self, visited, x, y, target_x, target_y, separate_exits):
        if x == target_x and (not separate_exits or y == target_y):
            return True
        
        if (x < 0 or x >= self.rows or y < 0 or y >= self.cols or 
            self.maze[x][y] == 1 or visited.contains(x, y)):
            return False
        
        visited.append(x, y)
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            if self._dfs_linked_list(visited, x + dx, y + dy, target_x, target_y, separate_exits):
                return True
        
        return False
    
    def _solve_with_std(self, starts, ends, separate_exits):
        for i in range(len(starts)):
            if not self._bfs_std(0, starts[i], self.rows-1, ends[i] if separate_exits else ends):
                return False
        return True
    
    def _bfs_std(self, start_x, start_y, target_x, target_y):
        visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        queue = deque([(start_x, start_y)])
        visited[start_x][start_y] = True
        
        while queue:
            x, y = queue.popleft()
            
            if x == target_x and (isinstance(target_y, int) and y == target_y or 
                                isinstance(target_y, list) and y in target_y):
                return True
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.rows and 0 <= ny < self.cols and 
                    self.maze[nx][ny] == 0 and not visited[nx][ny]):
                    visited[nx][ny] = True
                    queue.append((nx, ny))
        
        return False

# Пример использования
if __name__ == "__main__":
    maze = [
        [0, 1, 0, 0],  # Входы в позициях 0 и 2
        [0, 1, 0, 1],
        [0, 0, 0, 1],
        [0, 1, 0, 0]   # Выходы в позициях 0 и 2
    ]
    
    solver = MazeSolver(maze)
    starts = [0, 2]
    ends = [0, 2]
    
    print("Результаты для разных методов:")
    print(f"Массив: {solver.solve(starts, ends, 'array')}")
    print(f"Связанный список: {solver.solve(starts, ends, 'linked_list')}")
    print(f"BFS (стандартная библиотека): {solver.solve(starts, ends, 'std')}")
    
    print("\nЛюбой выход (разные методы):")
    print(f"Массив: {solver.solve(starts, ends, 'array', False)}")
    print(f"BFS: {solver.solve(starts, ends, 'std', False)}")
