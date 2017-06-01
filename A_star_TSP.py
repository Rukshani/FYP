from heuristicCalculation import heuristic_cal

delta = [[-1, 0],  # up
         [0, -1],  # left
         [1, 0],  # down
         [0, 1]]  # right

delta_name = ['^', '<', 'v', '>']
cost = 1
def search(grid, init, goal):
        heuristic = heuristic_cal(grid)

        # print  len(grid),(len(grid[0]))
        # open list elements are of the type :[g,x,y]
        closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
        closed[init[0]][init[1]] = 1
        expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
        action = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
        policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

        # print closed

        x = init[0]
        y = init[1]
        g = 0
        h = heuristic[x][y]
        f = g + h

        open = [[f, g, h, x, y]]

        found = False  # flag that is set when search complete
        resign = False  # flag set if we can't find expand
        count = 0

        # print 'initial open list:'
        # for i in range(len(open)):
        #     print '     ',open[i]
        # print '-----------------'

        while found is False and resign is False:
            # check if we still have elements on the open list
            if len(open) == 0:  # if open list is empty, nothing to expand
                resign = True
                print 'fail'
            else:  # if there are still elements
                # remove node form list
                open.sort()  # sort elements in increasing order
                # print 'open' +str(open)
                open.reverse()
                # print 'open' +str(open)
                next = open.pop()  # pop the elements with smallest g value
                # print 'open' +str(open)
                # print 'take list item'
                # print next
                x = next[3]
                y = next[4]
                g = next[1]
                # print 'x '+str(next[1]) +',y '+str(next[2])+',g '+str(next[0])
                expand[x][y] = count
                count += 1

                # check the goal
                if x == goal[0] and y == goal[1]:
                    found = True
                    # print next
                else:
                    # expand winning elements and add to new open list
                    for i in range(len(delta)):
                        x2 = x + delta[i][0]
                        y2 = y + delta[i][1]
                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
                            if closed[x2][y2] == 0 and grid[x2][y2] == 0:  # closed[][] x2 and y2 is not yet checked/// grid[][] if no obstacle in here
                                g2 = g + cost
                                h2 = heuristic[x2][y2]
                                f2 = g2 + h2
                                open.append([f2, g2, h2, x2, y2])
                                # print 'append list item'
                                # print [g2, x2, y2]
                                closed[x2][y2] = 1
                                action[x2][y2] = i

        # for i in range(len(expand)):
        #     print expand[i]

        # policy = [[' ' for row in range(len(grid))] for col in range(len(grid[0]))]
        x = goal[0]
        y = goal[1]
        # print x, y

        policy[x][y] = '*'  # 4,5
        list = []
        while x != init[0] or y != init[1]:
            # print "x, y: "+str(x)+" "+str(y)
            # print delta[action[x][y]]
            x2 = x - delta[action[x][y]][0]
            y2 = y - delta[action[x][y]][1]
            policy[x2][y2] = delta_name[action[x][y]]
            list.append(policy[x2][y2])
            x = x2
            y = y2

        # for i in range(len(policy)):
        #     print policy[i]

        list.reverse()
        list.append(list[-1])
        # print list
        return len(list)-1 # edit 1

# search()