from Exceptions import *
from Instruction import *

class Program:
    
    def __init__(self) -> None:
        self.instructionsList = []
        self.labels = {}
        
    def InstructionParsing(self,nb,instruction):
        """
        Extract labels from instructions

        Args:
            nb (int): line number
            instruction (String): instruction
        """
        
        operands = instruction.split()
        
        #Check for the word STOP dans transform it into STOP: JMP STOP
        if operands[0]=="STOP" and len(operands)==1:
            self.labels["STOP"] = nb
            self.instructionsList.append(Instruction("JMP STOP",nb))
        
        #lists all the labels    
        elif operands[0][-1:] == ':':
            self.instructionsList.append(Instruction(" ".join(operands[1:]),nb))
            self.labels[operands[0][0:-1]] = nb
        else:
            self.instructionsList.append(Instruction(instruction, nb))
    
    
            
    def Build(self,file="entrees.txt"):
        """
        Read the asm program from a file and convert it to binary

        Args:
            file String: Input file name. Defaults to "entrees.txt".
        """
        
        currentLine = 0
        
        with open(file,'r') as f:
            for line in f.readlines():
                
                #Extract comments
                WOcomments = line.split('#')[0]           
                if len(WOcomments.split())!=0:
                    self.InstructionParsing(currentLine,WOcomments.upper())
                    currentLine+=1

        self.ConvertToBinary()
        
    def ConvertToBinary(self):
        """
        Convert every instructions into their binary form
        """
        for inst in self.instructionsList:
            inst.ConvertToBinary(self.labels)
            
    def WriteBinaryProgram(self,output="sorties.txt",logisimReady=True):
        """
        Write the converted instruction into a file
        
        Args:
            logisimReady bool: does the output file need to be formatted for logisim 
            output String: Output file name. Defaults to "sorties.txt".
        """   
        with open(output, "w") as s:
            if logisimReady:
                s.write("v2.0 raw"+"\n")
            for inst in self.instructionsList:
                s.write(inst.GetHexa()+"\n")
                
        print("Successfully converted the program to binary !")