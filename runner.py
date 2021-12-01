import argparse

from runner_utils import (
    DayManager,
    TestManager,
    SolverManager,
    create_folder_structure,
    get_last_day
)


parser = argparse.ArgumentParser(description='Runner utils')
parser.add_argument(
    '-g',
    '--generate-day',
    action='store_const',
    const=True,
    help='Generates the folder needed for the next day'
)
parser.add_argument(
    '-r',
    '--run-day',
    help='Run a specific day'
)
parser.add_argument(
    '-a',
    '--run-all-solvers',
    action='store_const',
    const=True,
    help='Run all solvers for a specific day'
)
parser.add_argument(
    '-t',
    '--run-tests',
    action='store_const',
    const=True,
    help='Run tests'
)

args = parser.parse_args()

def run(day):
    day_manager = DayManager(day)
    if args.run_tests:
        runner = TestManager(day_manager)
        runner.run_all_tests()
        print("All good! :)")
    else:
        solver = SolverManager(day_manager)
        if args.run_all_solvers:
            solver.run_solvers()
        else:
            solver.run_last_solver()


if args.generate_day:
    create_folder_structure()
elif args.run_day:
    run(args.run_day)
else:
    run(get_last_day())
