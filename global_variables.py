#Exemplo 1
coef = [5, -1]
n_variables = range(2)
obj_type = "maximize"

#Exemplo 2
#coef = [15, 11.2, 17.5, 4, 3, 4.8]
#n_variables = range(6)
#obj_type = "maximize"

#Exemplo 3
#coef = [-2.5, -1.1, -0.9, -1.5]
#n_variables = range(4)
#obj_type = "minimize"

def obj_function(model):
    sum = 0
    for i in n_variables:
        sum = sum + (model.variable[i] * coef[i])
    return sum