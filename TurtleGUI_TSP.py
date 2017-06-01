import turtle

from TSP import Distance as DistanceOfTwoPoints
from heuristicCalculation import heuristic_cal

# init = [0, 0]
# goal = [len(grid) - 1, len(grid[0]) - 1]
# goal = [4, 1]

delta = [[-1, 0],  # up
         [0, -1],  # left
         [1, 0],  # down
         [0, 1]]  # right

delta_name = ['^', '<', 'v', '>']
# goal_init=[[0,0],[0,5],[4,3]]
# goal_init=[]
cost = 1
counter = 0
# screen1=turtle.Screen()

t = turtle.Pen()
dot_d = 20

new_list = []
RadiusOfWheel= 3.5

def draw(grid, goal_init, rows, columns, speed):
    turtle.clear()
    turtle.reset()
    my_start = (goal_init[0][1] * dot_d, -goal_init[0][0] * dot_d)
    turtle.penup()
    turtle.setx(my_start[0])
    turtle.sety(my_start[1])
    turtle.pendown()

    t.clear()
    t.reset()
    t.penup()
    t.speed(speed)
    print "dot " + str(turtle.position())
    for i in range(rows):
        for j in range(columns):
            # for i in range(len(grid)):
            #     for j in range(len(grid[0])):
            if grid[i][j] == 1:
                t.dot(10, "blue")
                t.forward(dot_d)
            else:
                t.dot(10, "black")
                t.forward(dot_d)

        t.back(dot_d * (j + 1))
        t.right(90)
        t.forward(dot_d)
        t.left(90)


def set_initial(goal_init, turtle):
    my_start = (goal_init[0][1] * dot_d, -goal_init[0][0] * dot_d)
    turtle.penup()
    turtle.setx(my_start[0])
    turtle.sety(my_start[1])
    turtle.pendown()


def search(init, goal, speed, grid, f_degree, b_degree, r_degree, l_degree, initialPoint):
    global speedGlobal, gridGlobal, f_degreeGlobal, b_degreeGlobal, r_degreeGlobal, l_degreeGlobal, initalLocation
    speedGlobal=speed
    gridGlobal=grid
    f_degreeGlobal=f_degree
    b_degreeGlobal=b_degree
    r_degreeGlobal=r_degree
    l_degreeGlobal=l_degree
    initalLocation=initialPoint

    heuristic = heuristic_cal(grid)
    turtle.speed(speed)
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1
    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    action = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

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
    print "Goal", x, y
    print "Init", init[0], init[1]

    policy[x][y] = '*'  # 4,5
    list = []

    currentLocationList = []
    while x != init[0] or y != init[1]:
        # print "Currrent x, y: "+str(x)+" "+str(y)
        global currentLocation
        currentLocation = [x, y] # edit 3
        currentLocationList.append(currentLocation) # edit 3

        # print delta[action[x][y]]
        x2 = x - delta[action[x][y]][0]
        y2 = y - delta[action[x][y]][1]
        policy[x2][y2] = delta_name[action[x][y]]
        list.append(policy[x2][y2])
        x = x2
        y = y2

    for i in range(len(policy)):
        print policy[i]

    currentLocationList.append(init)# edit 3
    currentLocationList.reverse()# edit 3
    # print "currentLocation", currentLocationList  # edit 3


    list.reverse()
    # print "Path List from", init, "to", goal, list
    print list
    new_list.append(list)
    # print "-----------alllist---------"
    # print new_list
    # print new_list[0]

    # ----------------------encoder tick-----------------------------
    # -----------handle this---------------------
    try:
        if DistanceOfTwoPoints(init, goal) != [] or x != init[0] or y != init[1]:
            print "Distance from", init, "to", goal, DistanceOfTwoPoints(init, goal)

            from CompassControl import key_input
            key_input(list, f_degree, b_degree, r_degree, l_degree, initialPoint, currentLocationList)  # edit 4
    except:
        print ""

    # for items, previous_item in zip(list, list[1:]):
    for items in list:

        turtle.setheading(90)
        if items == "^":
            turtle.setheading(90)
            turtle.forward(20)
            # print turtle.position()
        elif items == ">":
            turtle.setheading(90)
            turtle.right(90)
            turtle.forward(20)
            # turtle.forward(20)
            # print turtle.position()
        elif items == "<":
            turtle.setheading(90)
            turtle.left(90)
            turtle.forward(20)
            # print turtle.position()
        elif items == "v":
            turtle.setheading(90)
            turtle.left(90)
            turtle.left(90)
            turtle.forward(20)
            # print turtle.position()

    # print "-----------alllist---------"
    # print new_list
    # turtle.mainloop()

def stopAgent():
    try:
        print "currentLocationinTutleGUI_TSP:", currentLocation
        print "FirstLocationinTutleGUI_TSP",initalLocation
        from CompassControl import stop as stop
        stop(currentLocation, speedGlobal, gridGlobal, f_degreeGlobal, b_degreeGlobal, r_degreeGlobal, l_degreeGlobal,initalLocation)
    except:
        print "Found Earlier..............."
