import importlib
import glob
import re
import os
import pathlib
import time


SOLVER_PREFIX = "solve"
FOLDER_PREFIX = "day"
DAY_RE = "day([0-9]{2})"
SOLVER_RE = "solve([0-9])"
FOLDER_STRUCTURE = [
    "__init__.py",
    "input",
    "input_test",
    "solver.py"
]


def get_all_solvers(solver_module):
    solvers = []
    for member in dir(solver_module):
        if member.startswith(SOLVER_PREFIX):
            solvers.append(member)
    return sorted(solvers)


def get_last_day():
    current_days = [0]
    for current_day in glob.glob(f"{FOLDER_PREFIX}*"):
        current_days.append(int(re.match(DAY_RE, current_day).groups()[0]))
    return max(current_days)


def get_folder_for_day(day):
    to_generate = str(day).zfill(2)
    return f"{FOLDER_PREFIX}{to_generate}"


def create_folder_structure():
    folder_name = get_folder_for_day(get_last_day() + 1)
    os.mkdir(folder_name)
    for filename in FOLDER_STRUCTURE:
        pathlib.Path(os.path.join(folder_name, filename)).touch()


def expected_test_result(result):
    def outer_decorator(fn):
        fn.expected_test_result = result
        return fn
    return outer_decorator


class File:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path) as fh:
            return fh.read()


class DayManager:
    def __init__(self, day):
        solver_pkg = get_folder_for_day(day)
        self.solver_module = importlib.import_module(f"{solver_pkg}.solver")
        self.solvers = get_all_solvers(self.solver_module)

    @property   
    def dir(self):
        return os.path.dirname(self.solver_module.__file__)

    @property
    def testing_input(self):
        test_files = {}
        for filename in os.listdir(self.dir):
            if filename.startswith("input_test"):
                file = File(os.path.join(self.dir, filename))
                if filename != "input_test":
                    solver_id = filename[-1]
                    test_files['solver{solver_id}'] = file
                else:
                    test_files['solver1'] = file
        test_files['solver2'] = test_files.get('solver2', test_files['solver1'])
        return test_files

    def get_expected_test_result(self, solver_id):
        solver = getattr(self.solver_module, f"{SOLVER_PREFIX}{solver_id}", None)
        if solver:
            return solver.expected_test_result

    @property
    def input(self):
        return File(os.path.join(self.dir, "input"))

    def run_solver(self, solver_id, input):
        solver = getattr(self.solver_module, f"{SOLVER_PREFIX}{solver_id}", None)
        if solver:
            t1 = time.time()
            result = solver(input)
            print(f"{solver.__name__} ran in: {time.time() - t1: .5f} sec")
            return result


    def run_last_solver(self, input):
        solver_id = self.solvers[-1][-1]
        return self.run_solver(solver_id, input)


class TestManager:
    def __init__(self, day_manager):
        self.day_manager = day_manager

    def run_solver1_test(self):
        input = self.day_manager.testing_input["solver1"].read()
        expected = self.day_manager.get_expected_test_result(1)
        result = self.day_manager.run_solver(1, input)
        assert result == expected, f"{result} != {expected}"

    def run_solver2_test(self):
        input = self.day_manager.testing_input["solver2"].read()
        expected = self.day_manager.get_expected_test_result(2)
        result = self.day_manager.run_solver(2, input)
        assert result == expected, f"{result} != {expected}"

    def run_all_tests(self):
        self.run_solver1_test()
        self.run_solver2_test()


class SolverManager:
    def __init__(self, day_manager):
        self.day_manager = day_manager

    def run_solver1(self):
        input = self.day_manager.input.read()
        print(self.day_manager.run_solver(1, input))

    def run_solver2(self):
        input = self.day_manager.input.read()
        print(self.day_manager.run_solver(2, input))

    def run_solvers(self):
        self.run_solver1()
        self.run_solver2()

    def run_last_solver(self):
        input = self.day_manager.input.read()
        print(self.day_manager.run_last_solver(input))
