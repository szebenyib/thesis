import unittest

operator_dict = {
    "add": "+",
    "sub": "-",
    "mul": "*",
    "div": "/",
    "neg": "-",
    "sin": "sin",
    "cos": "cos",
}


class EquationParser():

    def __init__(self, variables, operators=operator_dict):
        """Creates an equation parser which will hold the variables and
        operators necessary for the parsing

        @:param variables is a tuple
        @:param operators is a dictionary of 3 char identifiers and their \
        replacement. It is important to note that only three letter operators
        are supported. Default operators are: add, sub, mul, div, neg, sin, cos.
        """
        self.variables = variables
        self.operators = operators

    def parse_equation(self, equation):
        """Parses an equation that is a gp tree from DEAP.
        :param equation = gp tree
            Example: add(x, mul(add(x, mul(add(x, mul(x, add(x, mul(x, x)))),
             add(x, mul(x, x)))), x))

        """

        j = 0
        opening_braces = 0
        closing_braces = 0
        left_side = ""
        right_side = ""
        operator = ""
        for i in range(0, len(equation)):
            #Debugging info, uncomment for inspection
            #z_current_char = equation[i]
            #z_part_till = equation[0:i]

            #Handling cases from shorter to longer
            #Only one character
            if equation in self.variables:
                return equation

            #going by three characters, standing on the opening brace
            #of the currently parsed part, it needs to be subtracted to only
            #count the ones that are inside the expression
            if j == 3:
                opening_braces -= 1
                operator = equation[i-3:i]
            j += 1

            if equation[i] == '(':
                opening_braces += 1
            if equation[i] == ')':
                closing_braces += 1
    #        if opening_braces == closing_braces and opening_braces != 0:
    #            print equation[i-1:i+1]
            if (opening_braces == closing_braces) and equation[i] == ',':
                #we are at the end of a complete part either left or right
                if left_side == "":
                    left_side = equation[4:i]
                    left_side = left_side.lstrip()
                    left_side = self.parse_equation(left_side)
                if right_side == "":
                    #i+1 -> do not include the comma
                    #len(population) - 1 -> do not include closing bracket
                    right_side = equation[i+1:len(equation)-1]
                    right_side = right_side.lstrip()
                    right_side = self.parse_equation(right_side)

            #at the last character and it is a closing bracket but
            #it has not been matched by an opening one, it means that
            #there were no other parts to check inside, only one argument
            if i == len(equation) - 1 and equation[i] == ')':
                if operator == "neg":
                    #there is a neg operator
                    return "(" + self.operators.get(operator) + \
                           self.parse_equation(equation[4:len(equation)-1]) + \
                           ")"
                elif operator == "sin" or operator == "cos":
                    #there is an operator, like sin, cos...
                    return self.operators.get(operator) + \
                        "(" + \
                        self.parse_equation(equation[4:len(equation)-1]) + \
                        ")"
                elif len(equation) == 1:
                    #there is no operator, just a variable
                    return equation[4:len(equation)-1]

        return "(" + \
               left_side + \
               self.operators.get(operator) + \
               right_side + \
               ")"


class Test(unittest.TestCase):

    def test_1_single_variable(self):
        equation_parser = EquationParser(('y',), operator_dict)
        eqn = "y"
        self.assertEqual("y", equation_parser.parse_equation(eqn))

    def test_2_single_operator_single_variable_neg(self):
        equation_parser = EquationParser(('y',), operator_dict)
        eqn = "neg(y)"
        self.assertEqual("(-y)", equation_parser.parse_equation(eqn))

    def test_3_single_operator_single_variable_trigonometric(self):
        equation_parser = EquationParser(('y',), operator_dict)
        eqn = "sin(y)"
        self.assertEqual("sin(y)", equation_parser.parse_equation(eqn))
        eqn = "cos(y)"
        self.assertEqual("cos(y)", equation_parser.parse_equation(eqn))

    def test_4_single_operator_two_variables_addmulsubdiv(self):
        equation_parser = EquationParser(('x', 'y', ), operator_dict)
        eqn = "add(x,y)"
        self.assertEqual("(x+y)", equation_parser.parse_equation(eqn))
        eqn = "sub(x,y)"
        self.assertEqual("(x-y)", equation_parser.parse_equation(eqn))
        eqn = "mul(x,y)"
        self.assertEqual("(x*y)", equation_parser.parse_equation(eqn))
        eqn = "div(x,y)"
        self.assertEqual("(x/y)", equation_parser.parse_equation(eqn))

    def test_5_complex_expression_1(self):
        equation_parser = EquationParser(('x', 'y', ), operator_dict)
        eqn = "add(mul(x,y),neg(y))"
        self.assertEqual("((x*y)+(-y))", equation_parser.parse_equation(eqn))

    def test_6_complex_expression_2(self):
        equation_parser = EquationParser(('x', 'y', ), operator_dict)
        eqn = "add(x, mul(add(x, mul(add(x, mul(x, add(x, mul(x, x))))," +\
              " add(x, mul(x, x)))), x))"
        self.assertEqual("(x+((x+((x+(x*(x+(x*x))))*(x+(x*x))))*x))",
                         equation_parser.parse_equation(eqn))

    def test_7_complex_expression_3(self):
        equation_parser = EquationParser(('x', 'y', ), operator_dict)
        eqn = "neg(sin(add(x, x)))"
        self.assertEqual("(-sin((x+x)))", equation_parser.parse_equation(eqn))

    def test_8_complex_expression_4(self):
        equation_parser = EquationParser(('x', 'y', ), operator_dict)
        eqn = "add(x, mul(add(mul(x, x), add(add(add(sin(x), x), neg(sin(" + \
              "add(x, x)))), x)), x))"
        self.assertEqual("(x+(((x*x)+(((sin(x)+x)+(-sin((x+x))))+x))*x))",
                         equation_parser.parse_equation(eqn))

    def test_9_test_long_variable_name_1(self):
        equation_parser = EquationParser(('profit',), operator_dict)
        eqn = "profit"
        self.assertEqual("profit", equation_parser.parse_equation(eqn))

    def test_10_test_long_variable_name_2(self):
        equation_parser = EquationParser(('profit',), operator_dict)
        eqn = "neg(profit)"
        self.assertEqual("(-profit)", equation_parser.parse_equation(eqn))

    def test_11_test_long_variable_name_3(self):
        equation_parser = EquationParser(('profit',), operator_dict)
        eqn = "sin(profit)"
        self.assertEqual("sin(profit)", equation_parser.parse_equation(eqn))
        eqn = "cos(profit)"
        self.assertEqual("cos(profit)", equation_parser.parse_equation(eqn))

    def test_12_test_long_variable_name_4(self):
        equation_parser = EquationParser(('profit', 'debt', ), operator_dict)
        eqn = "add(profit,debt)"
        self.assertEqual("(profit+debt)", equation_parser.parse_equation(eqn))
        eqn = "sub(profit,debt)"
        self.assertEqual("(profit-debt)", equation_parser.parse_equation(eqn))
        eqn = "mul(profit,debt)"
        self.assertEqual("(profit*debt)", equation_parser.parse_equation(eqn))
        eqn = "div(profit,debt)"
        self.assertEqual("(profit/debt)", equation_parser.parse_equation(eqn))

    def test_13_test_long_variable_name_5(self):
        equation_parser = EquationParser(('profit',), operator_dict)
        eqn = "neg(cos(neg(profit)))"
        self.assertEqual("(-cos((-profit)))",
                         equation_parser.parse_equation(eqn))

if __name__ == '__main__':
    unittest.main()