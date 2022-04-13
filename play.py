import argparse

from solver.game import play_semantle



def main():
    args = argparse()
    play_semantle(args.word)

if __name__ == '__main__':
    pass