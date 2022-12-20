from Exceptions import *

class Instruction:
    
    # encodée sous la forme : (type d'opération, code de l'opération)
    OPCODE = {  "ADD" : ("UAL" , "000000"),
                "ADDI": ("UALi", "000001"),
                "SUB" : ("UAL" , "000010"),
                "SUBI": ("UALi", "000011"),
                "AND" : ("UAL" , "000100"),
                "ANDI": ("UALi", "000101"),
                "OR"  : ("UAL" , "000110"),
                "ORI" : ("UALi", "000111"),
                "XOR" : ("UAL" , "001000"),
                "XORI": ("UALi", "001001"),
                "SL"  : ("UAL" , "001010"),
                "SLI" : ("UALi", "001011"),
                "SR"  : ("UAL" , "001100"),
                "SRI" : ("UALi", "001101"),
                "MUL" : ("UAL" , "001110"),
                "MULI": ("UALi", "001111"),
                "LD"  : ("MEM" , "010000"),
                "STR" : ("MEM" , "010010"),
                "CALL": ("CTRL", "111011"),
                "RET" : ("CTRL", "111100"),
                "JMP" : ("CTRL", "111001"),
                "JEQU": ("CTRL", "110001"),
                "JNEQ": ("CTRL", "110011"),
                "JSUP": ("CTRL", "110101"),
                "JINF": ("CTRL", "110111")
                
    }
    
    def __init__(self, asm, line) -> None:
        self.asmInstruction = asm.upper()
        self.asmOperands = self.asmInstruction.split()
        self.instructionLine = line
        
        self.binaryInstrution = "0"*32
        self.operationType = ""
        self.operation = ""
        
    def ChangeBits(self,data,pos):
        """
        allows you to modify a string

        Args:
            data (list()): data that will be inserted
            pos (int): position at which the change will take place. The positions are predefined : 0, 1, 2, 3, 4
        """
        L = list(self.binaryInstrution)
        
        #operation
        if pos == 0:
            L[0:6]=data
        
        #first register
        elif pos == 1:
            L[6:9]=data
        
        #second register
        elif pos == 2:
            L[9:12]=data
            
        #third register
        elif pos == 3:
            L[12:15]=data
            
        #constant register
        elif pos == 4:
            L[16:32]=data
            
        self.binaryInstrution = "".join(L)
        
    def ConvertToBinary(self, labels):
        """
        Convert the ASM instrcution into a binary one
        """
        
        self.BuildOpCode()
        self.BuildArgs(labels)
    
    def BuildRegister(self,reg, pos):
        """
        Checks the syntax of a register and encodes it in binary

        Args:
            reg (string): raw value of the register
            pos (int): position at which the register will be encoded. The positions are predefined : 1, 2, 3

        Raises:
            InvalidInstructionRegisters: Raise an error if the syntax is not valid
        """
        if reg == "":
            raise InvalidInstructionRegisters(reg, self.instructionLine)
        if reg[0]!='R': 
            raise InvalidInstructionRegisters(reg, self.instructionLine)
        x = int(reg[1:])
        if x<0 or x>7:
            raise InvalidInstructionRegisters(reg, self.instructionLine)
        self.ChangeBits(format(x,"03b"), pos)
    
    def CheckLabel(self, label, labelList):
        """
        Check if the specified label is valid

        Args:
            label (String): label to be tested
            labelList (Dict): Dict of all labels

        Raises:
            InvalidInstructionLabel: Raised when a label doesn't exists 

        Returns:
            int: adress of this label
        """
        try:
            adr = labelList[label]
            return adr
        except:
            raise InvalidInstructionLabel(label, self.instructionLine)

    def BuildImmediate(self,imm):
        """
        Checks the syntax of a immediate value and encodes it in binary

        Args:
            imm (string): raw value of the data

        Raises:
            InvalidInstructionRegisters: Raise an error if the syntax is not valid
        """
        if imm == "":
            raise InvalidInstructionRegisters(imm, self.instructionLine)
        try:
            nb = int(imm)
            self.ChangeBits(format(nb,"016b"), 4)
        except:
            raise InvalidInstructionRegisters(imm, self.instructionLine)
        
    def CheckArgsNumber(self, nb):
        """
        Check if the instruction has the right number of arguments

        Args:
            nb (int): expected number of argument

        Raises:
            InvalidInstructionArgs: Raise an error if it has not the right number of arguments
        """
        if len(self.asmOperands)!=nb+1:
            raise InvalidInstructionArgs(self.operation,nb, len(self.asmOperands)-1, self.instructionLine)
    
    def BuildArgs(self, labels):
        """
        Encodes the arguments of the instruction
        """
        
        if self.operationType == "UALi":
            self.CheckArgsNumber(3)
            self.BuildRegister(self.asmOperands[1],1)
            self.BuildRegister(self.asmOperands[2],2)
            self.BuildImmediate(self.asmOperands[3])
            
        elif self.operationType == "UAL":
            self.CheckArgsNumber(3)
            self.BuildRegister(self.asmOperands[1],1)
            self.BuildRegister(self.asmOperands[2],2)
            self.BuildRegister(self.asmOperands[3],3)
            
        elif self.operationType == "MEM":
            self.CheckArgsNumber(2)
            self.BuildRegister(self.asmOperands[1],1)
            self.BuildRegister(self.asmOperands[2],2)
            
        elif self.operation == "JMP" or self.operation == "CALL":
            self.CheckArgsNumber(1)
            self.BuildImmediate(self.CheckLabel(self.asmOperands[1],labels))
            
        elif self.operation == "RET":
            self.CheckArgsNumber(0)
        
        elif self.operation == "JEQU" or self.operation == "JNEQ" or self.operation == "JSUP" or self.operation == "JINF":
            self.CheckArgsNumber(3)
            self.BuildRegister(self.asmOperands[1],1)
            self.BuildRegister(self.asmOperands[2],2)
            self.BuildImmediate(self.CheckLabel(self.asmOperands[3],labels))
        
    def BuildOpCode(self):
        """
        Encodes the operation of the instruction

        Raises:
            InvalidInstructionOperation: Raise an error if the operation is invalid
        """
        
        if self.asmOperands[0] not in self.OPCODE:
            raise InvalidInstructionOperation(self.asmOperands[0], self.instructionLine)
        
        opCode = self.OPCODE[self.asmOperands[0]]
        
        self.operation = self.asmOperands[0]
        self.operationType = opCode[0]
        
        self.ChangeBits(opCode[1], 0)
        
    def GetBinary(self):
        return self.binaryInstrution
    
    def GetHexa(self):
        return format(int(self.binaryInstrution,2),"08x")
    
    def __repr__(self) -> str:
        return self.asmInstruction