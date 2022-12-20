class InvalidInstruction(Exception):
    def __init__(self, message, line):
        super().__init__("Error : {} (Program line : {})".format(message,line+1))

class InvalidInstructionOperation(InvalidInstruction):
    "Raised when the instruction's operation doesn't exist"
    
    def __init__(self, operation, line):
        super().__init__("The operation {} does not exist".format(operation),line)
        
class InvalidInstructionRegisters(InvalidInstruction):
    "Raised when the instruction's registers/constant are not valid"
    
    def __init__(self, reg, line):
        super().__init__("The register/constant {} is not valid and/or does not correspond with the instrcution".format(reg),line)
        
class InvalidInstructionArgs(InvalidInstruction):
    "Raised when the instruction doesn't have the right number of arguments"
    
    def __init__(self, op, expt, got,line):
        super().__init__("The operation {} hasn't the right number of arguments, expected {} got {}".format(op,expt,got),line)
        
class InvalidInstructionLabel(InvalidInstruction):
    "Raised when the label doesn't exists"
    
    def __init__(self, label,line):
        super().__init__("The label {} doesn't exists".format(label),line)