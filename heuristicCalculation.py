def heuristic_cal(grid):
    rows = len(grid)
    columns = len(grid[0])
    # print "rows, columns"
    # print rows, columns
    row_columns = rows + columns

    list = []
    for i in range(row_columns):
        list.append(i)
    # list.pop()
    list.pop()
    list.reverse()
    # print list
    heuristic=[]
    for k in range(rows):
        # print list[k:k+columns]
        heuristic.append(list[k:k+columns])

    # print "-------heuristic-----"
    # # print heuristic
    # for kr in range(len(heuristic)):
    #     print heuristic[kr]
    return heuristic