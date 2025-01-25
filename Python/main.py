#Allow user to show grid environment
from environment import Grid

def main():
    env = Grid(0.25, 5)
    env.DisplayGrid()

if __name__ == "__main__":
    main()