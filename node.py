from pyomo.environ import *

class Node:
    def __init__(self):
        self.model = ''
        self.parent = None
        self.is_solution = False
        self.must_search_child = True

    def create_model(self, model):
        self.model = model.clone()

    def new_constraint(self, variable, constraint_type, limit):
        if(constraint_type == "<="):
            self.model.constraints.add(variable <= limit)
        if(constraint_type == ">="):
            self.model.constraints.add(variable >= limit)

    def solve_node(self):        
        solver = SolverFactory("glpk", tee=True)
        results = solver.solve(self.model)