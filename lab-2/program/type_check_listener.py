from SimpleLangListener import SimpleLangListener
from SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckListener(SimpleLangListener):

  def __init__(self):
    self.errors = []
    self.types = {}

  def exitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left = self.types[ctx.expr(0)]
    right = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left, right):
        self.errors.append(f"Unsupported operand types for * or /: {left} and {right}")
    self.types[ctx] = FloatType() if isinstance(left, FloatType) or isinstance(right, FloatType) else IntType()

  def exitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for * or /: {left_type} and {right_type}")
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left = self.types[ctx.expr(0)]
    right = self.types[ctx.expr(1)]
    # Validate boolean addition
    if isinstance(left, BoolType) or isinstance(right, BoolType):
        self.errors.append(f"Cannot use '+' or '-' with Bool: {left}, {right}")
    elif isinstance(left, StringType) or isinstance(right, StringType):
        if ctx.op.text == '+':
            self.types[ctx] = StringType()
            return
        else:
            self.errors.append(f"Unsupported operand types for -: {left} and {right}")
    elif not self.is_valid_arithmetic_operation(left, right):
        self.errors.append(f"Unsupported operand types for + or -: {left} and {right}")
    self.types[ctx] = FloatType() if isinstance(left, FloatType) or isinstance(right, FloatType) else IntType()

  def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for + or -: {left_type} and {right_type}")
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def exitPowMod(self, ctx: SimpleLangParser.PowModContext):
    left = self.types[ctx.expr(0)]
    right = self.types[ctx.expr(1)]
    if ctx.op.text == '^':
        if not self.is_valid_arithmetic_operation(left, right):
            self.errors.append(f"Unsupported operand types for ^: {left} and {right}")
        self.types[ctx] = FloatType() if isinstance(left, FloatType) or isinstance(right, FloatType) else IntType()
    elif ctx.op.text == '%':
        if not isinstance(left, IntType) or not isinstance(right, IntType):
            self.errors.append(f"Unsupported operand types for %: {left} and {right}")
        self.types[ctx] = IntType()
  
  def enterInt(self, ctx: SimpleLangParser.IntContext):
    self.types[ctx] = IntType()

  def enterFloat(self, ctx: SimpleLangParser.FloatContext):
    self.types[ctx] = FloatType()

  def enterString(self, ctx: SimpleLangParser.StringContext):
    self.types[ctx] = StringType()

  def enterBool(self, ctx: SimpleLangParser.BoolContext):
    self.types[ctx] = BoolType()

  def enterParens(self, ctx: SimpleLangParser.ParensContext):
    pass

  def exitParens(self, ctx: SimpleLangParser.ParensContext):
    self.types[ctx] = self.types[ctx.expr()]

  def is_valid_arithmetic_operation(self, left_type, right_type):
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
      return True
    return False
