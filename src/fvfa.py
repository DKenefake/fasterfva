from enum import Enum

import numpy
from dataclasses import dataclass
from typing import Optional

import gurobipy as gp
from gurobipy import GRB


@dataclass
class FVAProblem:
    r"""
    This is the class object that defines FVA problems in this package

    .. math::
        \min c^Tv
    .. math::
        \begin{align}
        \text{s.t. } Sv &= 0\\
        v_l \leq v &\leq v_u\\
        v &\in R^n\\
        \end{align}

    """
    S: numpy.array
    v_u: numpy.array
    v_l: numpy.array
    c: numpy.array
    mu: float

    def __post_init__(self):
        """Some clean-up, and error checking is done here"""

        # assure that v_u and v_l are flattened arrays
        self.v_l = self.v_l.flatten()
        self.v_u = self.v_u.flatten()

        if not self.is_valid_dims():
            RuntimeError('Dimensions of vertices not correct! Please check the dims of the problems!')
        if not self.is_valid_param():
            RuntimeError('The mu parameter must be between [0,1]')

    def is_valid_dims(self) -> bool:
        """
        Checks the dimensions of the FVA problem matrices.

        :return: False if not consistent dimensions, otherwise true
        """

        num_lb = numpy.size(self.v_l)
        num_ub = numpy.size(self.v_u)
        num_c = numpy.size(self.c)

        # check upper bounds and lower bounds
        if num_lb != num_ub:
            return False

        # check the objective dims
        if (num_lb != num_c) or (num_ub != num_c):
            return False

        # check the dims of the metabolic network matrix
        if self.S.shape[1] != num_lb:
            return False

        return True

    def is_valid_param(self) -> bool:
        return 0 <= self.mu <= 1

    def num_v(self) -> int:
        return numpy.size(self.c)


@dataclass
class FVASolution:
    """
    The solution to FVAProblem instance. Contains the bounds of the fluxs, the best objective value, the number of
    LPs needed to solve and the FVAProblem instance.
    """
    lower_bound: numpy.array
    upper_bound: numpy.array
    Z: float
    number_LPs: int
    problem: FVAProblem


def build_fva_lp(problem: FVAProblem) -> [gp.Model, gp.MVar]:
    """
    Builds the initial FVA LP model

    :param problem: Problem definition (FVAProblem)
    :return: the LP model and the flux variables
    """
    # instantiate the model
    model = gp.Model()

    # quite optimizer output
    model.setParam('OutputFlag', 0)

    # quite optimizer output
    model.setParam('Method', 0)

    # set up the flux variable, v
    v = model.addMVar(problem.num_v(), vtype=GRB.CONTINUOUS, lb=problem.v_l, ub=problem.v_u)

    # add flux network constraints
    model.addConstr(problem.S @ v == 0, name='flux network')

    # set the objective to maximize the biological imperative
    model.setObjective(problem.c.flatten() @ v, sense=GRB.MAXIMIZE)

    # return the model and the flux variable
    return model, v


def setup_initial_fva_problem_solve(problem: FVAProblem) -> [gp.Model, gp.MVar, float]:
    """
    Sets up the initial LP model, solves for Z and adds the constraints

    :returns: The LP model, the LP model variables, and Z
    """
    # build the gurobi model relating to the FVA problem

    fva_model, flux_vars = build_fva_lp(problem)

    # solve initial FVA problem
    fva_model.optimize()

    # get the initial solution objective value, Z
    Z = fva_model.getObjective().getValue()

    # Add the optimization factor FVA constraint to the model
    fva_model.addConstr(problem.c.flatten() @ flux_vars >= problem.mu * Z, name='Percent Optimality')

    return fva_model, flux_vars, Z


def find_variable_range(model: gp.Model, flux_vars: gp.MVar, var_index: int, sense) -> float:
    """

    :param model: the mathematical model
    :param flux_vars: the set of flux variables
    :param var_index: the index of the variable being checked
    :param sense: the type of the optimization, e.g. minimization or maximization
    :return: the objective value, e.g. the range of the variable in the sense direction
    """
    model.setObjective(flux_vars[var_index], sense=sense)

    model.optimize()
    # model.update()

    return model.getObjective().getValue()


def fva_solve_basic(problem: FVAProblem) -> Optional[FVASolution]:
    """
    Solve the FVA problem with the standard algorithm

    :param problem: A FVAProblem type
    :return: Optionally None if the problem is not feasible, otherwise a FVASolution object
    """

    # build to solve the first step of the FVA problem
    fva_model, flux_vars, Z = setup_initial_fva_problem_solve(problem)

    # instantiate the flux bounds and the LP counting
    lower_bound = numpy.zeros(problem.num_v())
    upper_bound = numpy.zeros(problem.num_v())
    number_lps = 1 + 2 * problem.num_v()

    # solve the FVA sub problems
    for index in range(problem.num_v()):
        upper_bound[index] = find_variable_range(fva_model, flux_vars, index, GRB.MAXIMIZE)
        lower_bound[index] = find_variable_range(fva_model, flux_vars, index, GRB.MINIMIZE)

    return FVASolution(lower_bound, upper_bound, Z, number_lps, problem)

def fva_solve_basic_parallel(problem: FVAProblem) -> Optional[FVASolution]:
    """
    Solve the FVA problem with the standard algorithm

    :param problem: A FVAProblem type
    :return: Optionally None if the problem is not feasible, otherwise a FVASolution object
    """

    # build to solve the first step of the FVA problem
    fva_model, flux_vars, Z = setup_initial_fva_problem_solve(problem)

    # instantiate the flux bounds and the LP counting
    lower_bound = numpy.zeros(problem.num_v())
    upper_bound = numpy.zeros(problem.num_v())
    number_lps = 1 + 2 * problem.num_v()

    # solve the FVA sub problems
    for index in range(problem.num_v()):
        upper_bound[index] = find_variable_range(fva_model, flux_vars, index, GRB.MAXIMIZE)
        lower_bound[index] = find_variable_range(fva_model, flux_vars, index, GRB.MINIMIZE)

    return FVASolution(lower_bound, upper_bound, Z, number_lps, problem)



def fva_solve_faster(problem: FVAProblem) -> Optional[FVASolution]:
    """
    Solve the FVA problem with the proposed algorithm, note that the number of deterministic Linear programs will be smaller.

    :param problem:
    :return:
    """

    # build the sovle the first step of the FVA problem
    fva_model, flux_vars, Z = setup_initial_fva_problem_solve(problem)

    # set up problems to be solved
    upper_bound_problems = set(range(problem.num_v()))
    lower_bound_problems = set(range(problem.num_v()))

    # instantiate the flux bounds and the LP counting
    lower_bound = numpy.empty(problem.num_v())
    lower_bound.fill(numpy.nan)

    upper_bound = numpy.empty(problem.num_v())
    upper_bound.fill(numpy.nan)

    number_lps = 1

    # TODO: Clean this duplication up

    def remove_bound_problems(v_val):
        """Helper function to remove problems to solve from the lower bound"""
        problem_to_remove = numpy.where(v_val == problem.v_l)[0]
        lower_bound_problems.difference_update(set(problem_to_remove))

        problem_to_remove = numpy.where(v_val == problem.v_u)[0]
        upper_bound_problems.difference_update(set(problem_to_remove))

    # solve the upper bound problems
    while len(upper_bound_problems) != 0:
        # grab a problem of the top
        ub_problem = upper_bound_problems.pop()

        # solve the LP
        upper_bound[ub_problem] = find_variable_range(fva_model, flux_vars, ub_problem, GRB.MAXIMIZE)
        number_lps += 1

        remove_bound_problems(flux_vars.X)

    # solve the lower bound problems
    while len(lower_bound_problems) != 0:
        # grab a problem of the top
        lb_problem = lower_bound_problems.pop()

        # solve the LP
        lower_bound[lb_problem] = find_variable_range(fva_model, flux_vars, lb_problem, GRB.MINIMIZE)
        number_lps += 1

        remove_bound_problems(flux_vars.X)

    # clean up where we reset all the bounds of the problem we pruned
    for index in range(problem.num_v()):
        if numpy.isnan(upper_bound[index]):
            upper_bound[index] = problem.v_u[index]
        if numpy.isnan(lower_bound[index]):
            lower_bound[index] = problem.v_l[index]

    return FVASolution(lower_bound, upper_bound, Z, number_lps, problem)
