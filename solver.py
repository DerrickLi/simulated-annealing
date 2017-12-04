import random
import math
import argparse
import os

# @return (Boolean): True if solution satisfies constraint, false otherwise
def satisfies_constraint_helper(solution, constraint):
    w1 = solution.index(constraint[0])
    w2 = solution.index(constraint[1])
    w3 = solution.index(constraint[2])
    if ((w3 > w2 and w3 < w1) or (w3 < w2 and w3 > w1)):
        return False
    return True


def solve(num_variables, num_constraints, solution, constraints, output_file):
    """
    Input:
        num_variables: Number of variables
        num_constraints: The number of constraints on variables
        solution: A proposed optimal ordering of variables
        constraints: A 2D-array of constraints, 
                     where constraints[0] may take the form ['A', 'B', 'C'] and means C is not between A and B
    Output:
        An ordering of variables satisfying the most constraints as found by our algorithm
    """
    solution, unsatisfied = anneal(solution, num_constraints, constraints, output_file)
    repeat_count = 0
    max_repeats = 1

    # If our algorithm did not find the optimal solution, repeat a specified amount of times starting with our best solution so far

    while unsatisfied > 0 and repeat_count < max__repeats:
        solution, unsatisfied = anneal(solution, num_constraints, constraints, output_file)
        repeat_count += 1
    return solution, unsatisfied

def neighbor(solution):
    """
    Input:
        solution: A proposed ordering of variables
    Output:
        A random "neighbor" of our solution given by popping a variable and re-inserting at a random position in the list
    """
    solution_copy = list(solution)
    solution_len = len(solution_copy)

    random_num_list = random.sample(range(0, solution_len), 2)
    wizard = solution_copy.pop(random_num_list[0])
    solution_copy.insert(random_num_list[1], wizard)
    return solution_copy

def cost(solution, num_constraints, constraints):
    num_satisfied_constraints = 0
    for constraint in constraints:
        if satisfies_constraint_helper(solution, constraint):
            num_satisfied_constraints = num_satisfied_constraints + 1

    # cost = number of unsatisfied constraints
    return num_constraints - num_satisfied_constraints 

def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    else:
        return math.exp((old_cost - new_cost) / temperature)

def anneal(solution, num_constraints, constraints, output_file):
    """
    Input:
        solution: A proposed ordering of variables
        num_constraints: The number of constraints on variables
        constraints: A 2D-array of constraints
        output_file: A file we can write to and update with a partial solution

    """
    old_cost = cost(solution, num_constraints, constraints)
    T = 1.0
    alpha = 0.9999
    T_min = 0.00001
    while T > T_min and old_cost > 0:
        i = 1
        while i <= 100:
            new_solution = neighbor(solution)
            new_cost = cost(new_solution, num_constraints, constraints)
            ap = acceptance_probability(old_cost, new_cost, T)
            if ap > random.random():
                #update our partial solution file if we've found a better solution
                if new_cost < old_cost:
                    write_partial(output_file, new_solution, new_cost)
                solution = new_solution
                old_cost = new_cost
            if old_cost == 0:
                break
            i += 1
        T = T *alpha
        print("Currently Unsatisfied: " +  str(old_cost))
    return solution, old_cost

def read_input(filename):
    with open(filename) as f:
        num_variables = int(f.readline())
        num_constraints = int(f.readline())
        constraints = []
        variables = set()
        for _ in range(num_constraints):
            c = f.readline().split()
            constraints.append(c)
            for w in c:
                variables.add(w)
                
    variables = list(variables)
    return num_variables, num_constraints, variables, constraints

def write_output(filename, solution):
    with open(filename, "w") as f:
        for variable in solution:
            f.write("{0} ".format(variable))

def write_partial(filename, partial, new_cost):
    filename = filename + "_partial"
    with open(filename, "w") as f:
        f.write("Currently Unsatisfied: " + str(new_cost) + "\n")
        for variable in partial:
            f.write("{0} ".format(variable))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Constraint Solver.")
    parser.add_argument("input_file", type=str, help = "___.in")
    parser.add_argument("output_file", type=str, help = "___.out")
    args = parser.parse_args()

    num_variables, num_constraints, solution, constraints = read_input(args.input_file)

    if os.path.exists(args.output_file + "_partial"):
        with open(args.output_file + "_partial") as f:
            dummy = f.readline()
            variables = f.readline().split()
            if variables:
                solution = variables
        print("Found partial starting solution:" + str(solution))

    # pass in args.output_file so we can update our partial solution as we go
    solution, unsatisfied = solve(num_variables, num_constraints, solution, constraints, args.output_file)

    if unsatisfied == 0:
        print("Found working solution for " + args.input_file + " : " + str(solution))
        write_output(args.output_file, solution)

    #if we cannot find the optimal solution, move it to the problematic folder if it exists   
    else:
        head, tail = os.path.split(args.input_file)
        outhead, outtail = os.path.split(args.output_file)
        path = os.path.join(head, "problematic", tail)
        outpath = os.path.join(outhead, "problematic", outtail)

        os.rename(args.input_file, path)
        write_partial(outpath, solution, unsatisfied)
        print("Moved problematic input to: " + str(path))

    #cleanup after we no longer need partial solution
    os.remove(args.output_file + "_partial")
    
