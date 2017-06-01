from A_star_TSP import search
from pylab import *

def Distance(R1, R2, Rmap_grid):
    distance_between_two = search(Rmap_grid, R1, R2)
    # print "distance_between_two, init, goal"
    # print "R1, R2 , distance_between_two----------", R1, R2, distance_between_two
    return distance_between_two


def TotalDistance(city, R, Rmap_grid):
    # print "R, city"
    # print R--- will print set of key points
    # print city [0, 1, 2, 3, 4, 5, 6]
    dist = 0
    for i in range(len(city) - 1):
        dist += Distance(R[city[i]], R[city[i + 1]], Rmap_grid)
        print "Dist:", R[city[i]], R[city[i + 1]], Distance(R[city[i]], R[city[i + 1]], Rmap_grid)
    dist += Distance(R[city[-1]], R[city[0]], Rmap_grid)
    return dist


def reverse(city, n):
    nct = len(city)
    nn = (1 + ((n[1] - n[0]) % nct)) / 2
    for j in range(nn):
        k = (n[0] + j) % nct
        l = (n[1] - j) % nct
        (city[k], city[l]) = (city[l], city[k])  # swapping

PtList = []

def Plot(city, R, dist, grid):
    Pt = [R[city[i]] for i in range(len(city))]
    Pt += [R[city[0]]]
    Pt = array(Pt)
    title('Total distance=' + str(dist))
    print "-------Pt-----"
    print Pt
    PtList = np.array(Pt).tolist()
    print "-------Pt LIST-----"
    print PtList
    plot(Pt[:, 0], Pt[:, 1], '-o')
    # show()


def Plot2(city, R, dist, grid, f_degree, b_degree, r_degree, l_degree):
    Pt = [R[city[i]] for i in range(len(city))]
    Pt += [R[city[0]]]
    Pt = array(Pt)
    title('Total distance=' + str(dist))
    print "-------Pt-----"
    print Pt
    PtList = np.array(Pt).tolist()
    plot(Pt[:, 0], Pt[:, 1], '-o')
    # show()
    print "PATH MAP__________________", PtList

    # ------------------ setting the closest entrance as start---------------------------
    cleanList = []
    [cleanList.append(x) for x in PtList if x not in cleanList]
    PtList = cleanList
    closestPoint = min(PtList)
    closestPointIndex = PtList.index(closestPoint)
    print "closestPointIndex: ", closestPointIndex
    newList = []
    for i in range(closestPointIndex):
        newList.append(PtList[i])
    for i in range(closestPointIndex):
        PtList.remove(PtList[0])
    PtList.extend(newList)

    PtList.append(PtList[0])
    print "--------------------------------new PATH MAP -------------"
    print PtList

    goal_init = PtList
    print "Initial Goal---------", goal_init[0]

    from TurtleGUI_TSP import draw as drawGui
    from TurtleGUI_TSP import search as searchGui

    drawGui(grid, goal_init, len(grid), len(grid[0]), 10)
    for i in range(len(PtList)):
        initialPoint= PtList[0]
        init = goal_init[i]
        goal = goal_init[i + 1]
        searchGui(init, goal, 10, grid,f_degree, b_degree, r_degree, l_degree, initialPoint)
        goal_init.append(init)
        goal_init.append(goal)


Rmap = []

 # edit 2
# def printRamp(Rmap_grid):
#     for kr in range(len(Rmap_grid)):
#         for kc in range(len(Rmap_grid[0])):
#             if Rmap_grid[kr][kc] == 2:
#                 # print "Two in ",kr, kc
#                 Rmap.append([kr, kc])
#                 Rmap_grid[kr][kc] = 0
#
#                 print "Rmap", Rmap

# def main(Rmap_grid,f_degree, b_degree, r_degree, l_degree):
def main(Rmap_grid,f_degree, b_degree, r_degree, l_degree, assignedArea):
    # printRamp(Rmap_grid)
    Rmap=assignedArea
    print "Rmap Grid"
    for kr in range(len(Rmap_grid)):
        print Rmap_grid[kr]
    init = Rmap[0]
    goal = Rmap[1]
    print "init, goal: ", init, goal

    # Rmap =[[1,1],[5,2],[8,9],[2,4],[3,3]]
    # Rmap = [[0, 0], [0, 4], [2, 1], [3, 5], [4, 2]]
    ncity = len(Rmap)  # Number of cities to visit
    maxTsteps = 1  # Temperature is lowered not more than maxTsteps
    Tstart = 0.2  # Starting temperature - has to be high enough
    fCool = 0.9  # Factor to multiply temperature at each cooling step
    maxSteps = 10 * ncity  # Number of steps at constant temperature
    maxAccepted = 10 * ncity  # Number of accepted steps at constant temperature

    Preverse = 0.5  # How often to choose reverse/transpose trial move

    # Choosing city coordinates
    R = []  # coordinates of cities are choosen randomly

    for i in range(ncity):
        # R.append([rand(), rand()])
        R.append(Rmap[i])
        # R.append([Rmap[i]])
        # print Rmap[i]
    R = array(R)
    city = range(ncity)
    # Distance of the travel at the beginning
    dist = TotalDistance(city, R, Rmap_grid)

    # Stores points of a move
    n = zeros(6, dtype=int)
    nct = len(R)  # number of cities

    T = Tstart  # temperature

    Plot(city, R, dist, Rmap_grid)

    for t in range(maxTsteps):  # Over temperature

        accepted = 0
        for i in range(maxSteps):  # At each temperature, many Monte Carlo steps

            while True:  # Will find two random cities sufficiently close by
                # Two cities n[0] and n[1] are choosen at random
                n[0] = int((nct) * rand())  # select one city
                n[1] = int((nct - 1) * rand())  # select another city, but not the same
                if (n[1] >= n[0]):
                    n[1] += 1
                if (n[1] < n[0]):
                    (n[0], n[1]) = (n[1], n[0])  # swap, because it must be: n[0]<n[1]
                nn = (n[0] + nct - n[1] - 1) % nct  # number of cities not on the segment n[0]..n[1]
                if nn >= 3: break

            # We want to have one index before and one after the two cities
            # The order hence is [n2,n0,n1,n3]
            n[2] = (n[0] - 1) % nct  # index before n0
            n[3] = (n[1] + 1) % nct  # index after n2

            # What would be the cost to reverse the path between city[n[0]]-city[n[1]]?
            de = Distance(R[city[n[2]]], R[city[n[1]]], Rmap_grid) + Distance(R[city[n[3]]], R[city[n[0]]],Rmap_grid) - Distance(
                R[city[n[2]]], R[city[n[0]]],Rmap_grid) - Distance(R[city[n[3]]], R[city[n[1]]],Rmap_grid)

            if de < 0 or exp(-de / T) > rand():  # Metropolis
                accepted += 1
                dist += de
                reverse(city, n)

            if accepted > maxAccepted: break
        print "T=%10.5f , distance= %10.5f " % (T, dist)
        T *= fCool  # The system is cooled down
        if accepted == 0: break  # If the path does not want to change any more, we can stop

    Plot2(city, R, dist, Rmap_grid, f_degree, b_degree, r_degree, l_degree)


if __name__ == '__main__':
    main()
