

from Program import *
       
def main():
    program = Program()
    program.Build("entrees.txt")
    program.WriteBinaryProgram("sorties.txt")
    
if __name__ == "__main__":
    main()