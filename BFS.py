from collections import deque
from map_processor import *

def order_bfs(grid, start_node, stones, costs): 
    totalCost = 0
    queue = deque([(start_node, tuple(stones), [], totalCost)]) # tạo hàng đợi chứa vị trí ares, vị trí đá và đường đi
    visited = set()
    directions = [(-1, 0, 'U', 'u'), (1, 0, 'D', 'd'), (0, -1, 'L', 'l'), (0, 1, 'R', 'r')] # đi đến 4 hướng

    while queue:
        (ares_x, ares_y), stones_pos, path, totalCost = queue.popleft()

        # nếu đã đi qua trường hợp tương tự, bỏ qua và đi tiếp
        if(ares_x, ares_y, stones_pos) in visited:
            continue
        # thêm trường hợp mới vào trong danh sách đã đi qua
        visited.add((ares_x, ares_y, stones_pos))
        
        # kiểm tra nếu tất cả đá đã ở đúng vt switch, trả về path
        if all(grid[x,y] == '.' for x,y in stones_pos):
            return path, totalCost
        

        # di chuyển đi 4 hướng
        for dx, dy, push, move in directions:
            new_x, new_y = ares_x + dx, ares_y + dy

            # kiểm tra xem vị trí mới có hợp lệ không
            if not is_valid(grid, new_x, new_y):
                continue
            
            cur_cost = totalCost
            cur_cost += 1 # cộng chi phí di chuyển
            new_stones = list(stones_pos) # copy trạng thái đá
            isPush = False # kiểm tra bước đi tiếp theo có đẩy viên đá không
            
            # trường hợp viên đá bị đẩy
            if (new_x,new_y) in stones_pos:
                stone_index = stones_pos.index((new_x, new_y))

                # vị trí mới của viên đá
                new_stone_x = new_x + dx
                new_stone_y = new_y + dy

                # check vt mới của đá có hợp lệ không (loại trường hợp đá chồng đá)
                if not is_valid(grid, new_stone_x, new_stone_y) or (new_stone_x, new_stone_y) in stones_pos:
                    continue
                
                # cập nhật vị trí mới của đá
                new_stones[stone_index] = (new_stone_x, new_stone_y)
                cur_cost += costs[stone_index]
                isPush = True
            
            # thêm phần tử mới vào queue
            # đẩy viên đá thì in hoa, không thì viết thường
            if isPush:
                queue.append(((new_x, new_y), tuple(new_stones), path + [push], cur_cost))
            else:
                queue.append(((new_x, new_y), tuple(new_stones), path + [move], cur_cost))

    return None


                

