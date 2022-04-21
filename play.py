import argparse

from solver.game import run_solver

def main():
    args = argparse()
    run_solver(args.word)

if __name__ == '__main__':
    pass