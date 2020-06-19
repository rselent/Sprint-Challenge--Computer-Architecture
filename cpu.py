import \
	sys

#FILENAME = "./sctest.ls8"
FILENAME = sys.argv[1]

# ALU OPS
ADD = 0xA0  # Addition
SUB = 0xA1  # Subtraction
MUL = 0xA2  # Multiplication
DIV = 0xA3  # Division
MOD = 0xA4  # Modular Division

INC = 0x65  # Increment 1 to given register
DEC = 0x66  # Decrement 1 from given register

CMP = 0xA7  # Compare values in 2 registers

AND = 0xA8  # Bitwise-AND
NOT = 0x69  # Bitwise-NOT
OR = 0xAA  # Bitwise-OR
XOR = 0xAB  # Bitwise-XOR

SHL = 0xAC  # Shift Left
SHR = 0xAD  # Shift Right

# PC MUTATORS
CALL = 0x50  # Call subroutine at address in register
RET = 0x11  # Return from subroutine, pops value from top of stack

INT = 0x52  # Issue Interrupt stored in register
IRET = 0x13  # Return from Interrupt, pops value from top of stack

JMP = 0x54  # Jump to address in register
JEQ = 0x55  # Jump if Equal is set
JNE = 0x56  # Jump if Not Equal (clear)
JGT = 0x57  # Jump if Greater-Than
JLT = 0x58  # Jump if Less-Than
JLE = 0x59  # Jump if Less-than or Equal is set
JGE = 0x5A  # Jump if Greater-than or Equal is set

# MISC CODES
NOP = 0x00  # No Operation -- do nothing
HLT = 0x01  # Halt and exit

LDI = 0x82  # Load Integer value into register
LD = 0x83  # Load register with value from another register (reads from RAM)
ST = 0x84  # Store value from register in another register (writes to RAM)

PUSH = 0x45  # Push value from register to stack
POP = 0x46  # Pop value from stack to register

PRN = 0x47  # Print numeric value in register
PRA = 0x48  # Print ASCII char from value in register

# FLAG INDICES
LE = 0x5
GR = 0x6
EQ = 0x7


class CPU:
	"""Main CPU class."""
	
	def __init__( self, filename= FILENAME):
		"""Construct a new CPU."""
		self.ram = [0] *256
		self.reg = [0] *8
		self.flag = [0] *8
		self.pc = 0
		
		self.filename = filename
		self.running = 0
		
		self.switchTable = {        # branch table masquerading as a switch
			LDI: self.LDI,
			PRN: self.PRN,
			HLT: self.HLT,
			CMP: self.CMP,
			JEQ: self.JEQ,
			JNE: self.JNE,
			JMP: self.JMP
		}
	
	def HLT( self):
		print("HALT INITIATED")
		self.running = 0
		self.pc += 1
	
	def ram_read(self, address):
		return self.ram[ address]
	
	def ram_write( self, value, address):
		self.ram[ address] = value
	
	def LDI( self):
		reg = self.ram[ self.pc + 1]
		val = self.ram[ self.pc + 2]
		self.reg[ reg] = val
#		self.pc += 3
	
	def PRN( self):
		reg = self.ram[ self.pc + 1]
		print( self.reg[ reg])
#		print( self.reg)
#		self.pc += 2
	
	def CMP( self):
		self.flag[LE] = 0x0
		self.flag[GR] = 0x0
		self.flag[EQ] = 0x0
		regA = self.ram_read( self.pc + 1)
		regB = self.ram_read( self.pc + 2)
		
		if regA == regB:
			self.flag[EQ] = 0x1
		elif regA < regB:
			self.flag[LE] = 0x1
		elif regA > regB:
			self.flag[GR] = 0x1
	
	def JEQ( self):
		reg = self.ram_read( self.pc + 1)
		
		if self.flag[EQ] == 0x1:
			self.pc = self.reg[ reg]
		else:
			self.pc += 2
	
	def JNE( self):
		reg = self.ram_read( self.pc + 1)
		
		if self.flag[EQ] == 0x0:
			self.pc = self.reg[ reg]
		else:
			self.pc += 2
	
	def JMP( self):
		reg = self.ram_read( self.pc + 1)
		
		self.pc = self.reg[ reg]
	
	
	def load( self):
		"""Load a program into memory."""
		address = 0
		
#		for instruction in program:
#			print( "instruction", instruction)
#			self.ram[ address] = instruction
#			print( "instruction in ram", self.ram[ address])
#			address += 1
	
	
	def alu( self, op, reg_a, reg_b):
		"""ALU operations."""
		if op == "ADD":
			self.reg[ reg_a] += self.reg[ reg_b]
		# elif op == "SUB": etc
		else:
			raise Exception( "Unsupported ALU operation")
	
	
	def trace( self):
		"""
		Handy function to print out the CPU state. You might want to call this
		from run() if you need help debugging.
		"""
		print( f"TRACE: %02X | %02X %02X %02X |" % (
				self.pc,
				self.ram_read( self.pc),
				self.ram_read( self.pc + 1),
				self.ram_read( self.pc + 2)
			), end= '')

		for i in range( 8):
			print( " %02X" % self.reg[i], end= '')
		print()
	
	
	def run( self):
		"""Run the CPU."""
		
		with open( self.filename) as f:
			address = 0
			print( "OPENING FILE")

			for line in f:
				lineSplit = line.split("#")
				try:
					v = int( lineSplit[0], 2)
				except ValueError:
					continue
				self.ram[ address] = v
				address += 1
			print( "OPENING COMPLETE")

		print( "FILE CONTENTS:\n", self.ram)
		self.running = 1

		while self.running:
			ir = self.ram_read( self.pc)
			flag = (ir & 0x10) >> 4
			op_a = self.ram_read( self.pc + 1)
			op_b = self.ram_read( self.pc + 2)
			
#			print( "IR", ir)
			if ir in self.switchTable:
				self.switchTable[ir]()
			
			if flag == 0:
				move = int( (ir & 0xc0) >> 6)
				self.pc += move + 1



if __name__ == "__main__":
	CPU().run()

