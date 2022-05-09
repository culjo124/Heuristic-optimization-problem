from Customer import Customer
from random import randint
from copy import deepcopy
import time

instance = "i2-d"
f = open("d_test/" + instance + ".txt")
f.read(28)
line = f.readline().split()
number, capacity = int(line[0]), int(line[1])
f.read(89)

trucks = []
customers = []

for x in f:
    line = x.split()
    new_customer = Customer(int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5]), int(line[6]))
    customers.append(new_customer)

deport = customers.pop(0)
number_of_customers = len(customers)
clusters = []
cluster = []
cluster_capacity = 0
cluster_time = 0
current_customer = deport

while len(customers) != 0:
    pick_customer = customers[0]
    min_time = cluster_time + customers[0].getDistanceCeil(current_customer)
    if min_time < pick_customer.readyTime:
        min_time = pick_customer.readyTime
    for customer in customers:
        check_time = cluster_time + customer.getDistanceCeil(current_customer)
        if check_time > customer.dueTime:
            continue
        if check_time < customer.readyTime:
            check_time = customer.readyTime
        if check_time < min_time:
            min_time = check_time
            pick_customer = customer
    if min_time <= pick_customer.dueTime and cluster_capacity + pick_customer.demand <= capacity and min_time + \
            pick_customer.serviceTime + pick_customer.getDistanceCeil(deport) <= deport.dueTime:
        current_customer = pick_customer
        cluster.append(pick_customer)
        customers.remove(pick_customer)
        cluster_capacity += pick_customer.demand
        cluster_time = min_time + pick_customer.serviceTime
    else:
        clusters.append(cluster)
        cluster = []
        cluster_capacity = 0
        cluster_time = 0
        current_customer = deport

if len(cluster) != 0:
    clusters.append(cluster)

print("trucks after greedy:", len(clusters))


def writeResults(results, instance, runTime):
    filename = "res-" + runTime + "-" + instance + ".txt"
    w = open(filename, "w")

    w.write(str(len(results)) + "\n")
    totalDistance = 0

    for i in range(len(results)):
        w.write(str(i + 1) + ": ")
        totalTime = 0
        for j in range(len(results[i])):
            if j == 0:
                totalDistance += deport.getDistance(results[i][j])
                totalTime += deport.getDistanceCeil(results[i][j])
                w.write("0(0)->")
            else:
                totalDistance += results[i][j-1].getDistance(results[i][j])
                totalTime += results[i][j-1].serviceTime + results[i][j-1].getDistanceCeil(results[i][j])

            if results[i][j].readyTime > totalTime:
                totalTime = results[i][j].readyTime
            w.write(str(results[i][j].index) + "(" + str(totalTime) + ")")
            if j != len(results[i]) - 1:
                w.write("->")
            else:
                totalDistance += deport.getDistance(results[i][j])
                totalTime += results[i][j].serviceTime + deport.getDistanceCeil(results[i][j])
                w.write("->0(" + str(totalTime) + ")")

        w.write("\n")

    w.write(str(totalDistance))
    w.close()


def checkRouteFeasible(route):
    route = [deport] + route + [deport]
    route_demand = 0
    route_time = 0
    for i in range(len(route) - 1):
        time = route_time + route[i].getDistanceCeil(route[i + 1])
        if time > route[i + 1].dueTime:
            return False
        if time < route[i + 1].readyTime:
            time = route[i + 1].readyTime

        route_demand += route[i + 1].demand
        route_time = time + route[i + 1].serviceTime

    if route_time > deport.dueTime or route_demand > capacity:
        return False
    return True


def calculateRouteTime(route):
    route = [deport] + route + [deport]
    route_time = 0
    for i in range(len(route) - 1):
        time = route_time + route[i].getDistanceCeil(route[i + 1])
        if time < route[i + 1].readyTime:
            time = route[i + 1].readyTime

        route_time = time + route[i + 1].serviceTime
    return route_time


def totals(results):
    totalDistance = 0
    totalTime = 0
    for i in range(len(results)):
        time = 0
        for j in range(len(results[i])):
            if j == 0:
                totalDistance += deport.getDistance(results[i][j])
                time += deport.getDistanceCeil(results[i][j])
            else:
                totalDistance += results[i][j - 1].getDistance(results[i][j])
                time += results[i][j - 1].serviceTime + results[i][j - 1].getDistanceCeil(results[i][j])

            if results[i][j].readyTime > totalTime:
                time = results[i][j].readyTime
            if j == len(results[i]) - 1:
                totalDistance += deport.getDistance(results[i][j])
                time += results[i][j].serviceTime + deport.getDistanceCeil(results[i][j])
        totalTime += time

    return [totalDistance, totalTime]


def compareRoutes(routes1, routes2):
    if len(routes1) > len(routes2):
        return routes2
    elif len(routes2) > len(routes1):
        return routes1
    else:
        distance1, time1 = totals(routes1)
        distance2, time2 = totals(routes2)

        if distance1 > distance2:
            print(iter, len(routes2), distance2)
            return routes2
        elif distance2 > distance1:
            return routes1
        else:
            return routes1


iter = 0
x = deepcopy(clusters)
timeout1 = time.time() + 60 * 1
print1 = True
timeout2 = time.time() + 60 * 5
print2 = True
percent = 0.01

while iter < 30000:
    if time.time() > timeout1 and print1:
        print1 = False
        writeResults(x, instance, "1m")
        print(iter, "1m", len(x))
    if time.time() > timeout2 and print2:
        print2 = False
        writeResults(x, instance, "5m")
        print(iter, "5m", len(x))
    destroyed = []
    x_t = deepcopy(x)
    while len(destroyed) < number_of_customers * percent:
        route_index = randint(0, len(x_t) - 1)
        if len(x_t[route_index]) - 1 == 0:
            index = 0
        else:
            index = randint(0, len(x_t[route_index]) - 1)
        destroyed.append(x_t[route_index].pop(index))
        for cluster in x_t:
            if len(cluster) == 0:
                x_t.remove(cluster)
    for customer in destroyed:
        possible_routes = []
        for i in range(len(x_t) - 1, 0, -1):
            route_index = 0
            min_dist = customer.getDistanceCeil(deport) + customer.getDistanceCeil(x_t[i][0])
            for j in range(len(x_t[i])):
                if j == len(x_t[i]) - 1:
                    check_dist = x_t[i][j].getDistanceCeil(customer) + customer.getDistanceCeil(deport)
                    if check_dist < min_dist:
                        min_dist = check_dist
                        route_index = j + 1
                else:
                    check_dist = x_t[i][j].getDistanceCeil(customer) + customer.getDistanceCeil(x_t[i][j+1])
                    if check_dist < min_dist:
                        min_dist = check_dist
                        route_index = j + 1
            new_route = x_t[i][:route_index] + [customer] + x_t[i][route_index:]

            if checkRouteFeasible(new_route):
                old_route_time = calculateRouteTime(x_t[i])
                new_route_time = calculateRouteTime(new_route)
                possible_routes.append([i, route_index, new_route_time-old_route_time])
        if len(possible_routes) != 0:
            possible_routes.sort(key=lambda x: x[2])
            x_t[possible_routes[0][0]].insert(possible_routes[0][1], customer)
            possible_routes = []
        else:
            x_t.append([customer])

    if compareRoutes(x, x_t) == x_t:
        x = deepcopy(x_t)
    iter += 1
    # if iter == 1000:
    #     percent = 0.05
    # if iter == 10000:
    #    percent = 0.005

writeResults(x, instance, "un")
print(iter, "kraj")

