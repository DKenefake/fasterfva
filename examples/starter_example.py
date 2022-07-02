import sys
from src.fvfa import fva_solve_faster, fva_solve_basic, FVASolution, FVAProblem
from src.utils import read_file_mat
import time


def run_analysis(model_name: str = 'e_coli_core') -> int:
    """
    Simple script to run FVA on e_coli_core using the default algorithm and the proposed algorithm.

    Prints the time to solve, the number of LPs needed to solve the problem
    """

    def run_fva(fva_func, p: FVAProblem) -> [float, FVASolution]:
        """Helper function to solve and time FVA Analysis problems"""
        start = time.time()
        sol = fva_func(p)
        stop = time.time()
        return stop - start, sol

    problem = read_file_mat("..\\example_models", model_name)

    time_basic, sol_basic = run_fva(fva_solve_basic, problem)
    time_faster, sol_faster = run_fva(fva_solve_faster, problem)

    print(f"It took {time_basic:3.4f} sec for the standard algorithm with {sol_basic.number_LPs} LPs")
    print(f"It took {time_faster:3.4f} sec for the proposed algorithm with {sol_faster.number_LPs} LPs")
    print()
    print(f"For model {model_name} there were {sol_basic.number_LPs - sol_faster.number_LPs} less LPs solved using the proposed algorithm")

    return 1


# entry point
if __name__ == '__main__':
    # run FVA analysis on iLJ478 found in the example_models folder
    sys.exit(run_analysis('iLJ478'))
