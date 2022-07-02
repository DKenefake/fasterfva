from scipy.io import loadmat
import numpy
from .fvfa import FVAProblem


def read_file_mat(directory_path: str, model_name: str, mu: float = 0.9):
    """
    Loads in a cobra formatted .mat file from a directory

    returns: FVAProblem from the given model_name
    """
    problem_mat = loadmat(f'{directory_path}\\{model_name}.mat')[model_name][0]
    S = numpy.array(problem_mat['S'][0]).astype(numpy.float64)
    lb = numpy.array(problem_mat['lb'][0]).astype(numpy.float64)
    ub = numpy.array(problem_mat['ub'][0]).astype(numpy.float64)
    c = numpy.array(problem_mat['c'][0]).astype(numpy.float64)
    return FVAProblem(S, ub, lb, c, mu)
