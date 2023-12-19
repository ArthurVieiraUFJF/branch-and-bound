import math
from pyomo.environ import *
from node import Node
from global_variables import (
    coef,
    n_variables,
    obj_type,
    obj_function
)

bound = 0
if(obj_type == "minimize"):
    bound = 9999999999999
solution = Node()

def check_solution(node):
    global bound

    if(not(node.parent == None)):
        doomed_node = True

        for i in n_variables:
            if(not(value(node.model.variable[i]) == value(node.parent.model.variable[i]))):
                doomed_node = False

        if(doomed_node):
            node.must_search_child = False

    if(obj_type == "maximize"):
        if(value(node.model.obj) <= bound):
            node.must_search_child = False

        node.is_solution = True

        for i in n_variables:
            if(not(float(value(node.model.variable[i])).is_integer())):
                node.is_solution = False

        if(node.is_solution):
            node.must_search_child = False

            if(value(node.model.obj) > bound):
                bound = value(node.model.obj)
                solution.create_model(node.model)
    
    if(obj_type == "minimize"):
        if(value(node.model.obj) >= bound):
            node.must_search_child = False

        node.is_solution = True

        for i in n_variables:
            if(not(float(value(node.model.variable[i])).is_integer())):
                node.is_solution = False

        if(node.is_solution):
            node.must_search_child = False

            if(value(node.model.obj) < bound):
                bound = value(node.model.obj)
                solution.create_model(node.model)
                
def branch_and_bound(actual_node):
    pivot = 0
    roundDown = 0
    roundUp = 0
    pivot_found = False
    
    i = 0        
    while (i < n_variables.__len__() and not(pivot_found)): 
        if(not(float(value(actual_node.model.variable[i])).is_integer())):
            pivot = i
            roundUp = math.ceil(value(actual_node.model.variable[i]))
            roundDown = math.floor(value(actual_node.model.variable[i]))
            pivot_found = True

            if(actual_node.must_search_child):
                left_node = Node()

                left_node.create_model(actual_node.model)
                left_node.new_constraint(left_node.model.variable[pivot], "<=", roundDown)

                right_node = Node()

                right_node.create_model(actual_node.model)
                right_node.new_constraint(right_node.model.variable[pivot], ">=", roundUp)

                left_node.parent = actual_node
                right_node.parent = actual_node

                left_node.solve_node()
                check_solution(left_node)

                branch_and_bound(left_node)

                right_node.solve_node()
                check_solution(right_node)

                branch_and_bound(right_node)
            else:
                return
        i = i + 1

root = Node()

model = ConcreteModel()

#Exemplo 1
model.variable = Var(list(n_variables), domain=NonNegativeReals)
model.obj = Objective(rule=obj_function, sense=maximize)

#Exemplo 2
#model.variable = Var(list(n_variables), domain=NonNegativeReals, bounds=(0, 1))
#model.obj = Objective(rule=obj_function, sense=maximize)

#Exemplo 3
#model.variable = Var(list(n_variables), domain=NonNegativeReals, bounds=(0, 1))
#model.obj = Objective(rule=obj_function, sense=minimize)

model.constraints = ConstraintList()

root.create_model(model)

#Exemplo 1
root.new_constraint(((7 * root.model.variable[0]) - (5 * root.model.variable[1])), "<=", 13)
root.new_constraint(((3 * root.model.variable[0]) + (2 * root.model.variable[1])), "<=", 17)

#Exemplo 2
#root.new_constraint(((5 * root.model.variable[0]) + (4 * root.model.variable[1]) + (7 * root.model.variable[2]) + (2 * root.model.variable[3]) + (3 * root.model.variable[4]) + (6 * root.model.variable[5])), "<=", 15)

#Exemplo 3
#root.new_constraint(((4 * root.model.variable[0]) + (2 * root.model.variable[1]) + (1.9 * root.model.variable[2]) + (3 * root.model.variable[3])), "<=", 9)

root.solve_node()
check_solution(root)

branch_and_bound(root)

print("Relaxed solution:")
print("z =", value(root.model.obj))
for i in n_variables:
    print("x", i + 1, "=", value(root.model.variable[i]))

print("Integer solution:")
print("z =", value(solution.model.obj))
for i in n_variables:
    print("x", i + 1, "=", value(solution.model.variable[i]))