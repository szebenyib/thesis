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


def parse_equation(equation):
    """Parses an equation that is a gp tree from DEAP. IT is important to note
    that only three letter operators are supported. To be exact, the supported
    operators are: add, sub, mul, div, neg, sin, cos.
    :param equation = gp tree
        Example: add(x, mul(add(x, mul(add(x, mul(x, add(x, mul(x, x)))), add(x, mul(x, x)))), x))

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
        if len(equation) == 1:
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
                left_side = parse_equation(left_side)
            if right_side == "":
                #i+1 -> do not include the comma
                #len(population) - 1 -> do not include closing bracket
                right_side = equation[i+1:len(equation)-1]
                right_side = right_side.lstrip()
                right_side = parse_equation(right_side)

        #at the last character and it is a closing bracket but
        #it has not been matched by an opening one, it means that
        #there were no other parts to check inside, only one argument
        if i == len(equation) - 1 and equation[i] == ')':
            if operator == "neg":
                #there is a neg operator
                return "(" + operator_dict.get(operator) + \
                       equation[4:len(equation)-1] + \
                       ")"
            elif operator == "sin" or operator == "cos":
                #there is an operator, like sin, cos...
                return operator_dict.get(operator) + \
                    "(" + \
                    equation[4:len(equation)-1] + \
                    ")"
            elif len(equation) == 1:
                #there is no operator, just a variable
                return equation[4:len(equation)-1]

    return "(" + \
           left_side + \
           operator_dict.get(operator) + \
           right_side + \
           ")"


class Test(unittest.TestCase):

    def test_1_single_variable(self):
        eqn = "y"
        self.assertEqual("y", parse_equation(eqn))

    def test_2_single_operator_single_variable_neg(self):
        eqn = "neg(y)"
        self.assertEqual("(-y)", parse_equation(eqn))

    def test_3_single_operator_single_variable_trigonometric(self):
        eqn = "sin(y)"
        self.assertEqual("sin(y)", parse_equation(eqn))
        eqn = "cos(y)"
        self.assertEqual("cos(y)", parse_equation(eqn))

    def test_4_single_operator_two_variables_addmulsubdiv(self):
        eqn = "add(x,y)"
        self.assertEqual("(x+y)", parse_equation(eqn))
        eqn = "sub(x,y)"
        self.assertEqual("(x-y)", parse_equation(eqn))
        eqn = "mul(x,y)"
        self.assertEqual("(x*y)", parse_equation(eqn))
        eqn = "div(x,y)"
        self.assertEqual("(x/y)", parse_equation(eqn))

    def test_5_complex_expression_1(self):
        eqn = "add(mul(x,y),neg(y))"
        self.assertEqual("((x*y)+(-y))", parse_equation(eqn))

    def test_6_complex_expression_2(self):
        eqn = "add(x, mul(add(x, mul(add(x, mul(x, add(x, mul(x, x)))), add(x, mul(x, x)))), x))"
        self.assertEqual("(x+((x+((x+(x*(x+(x*x))))*(x+(x*x))))*x))", parse_equation(eqn))

if __name__ == '__main__':
    unittest.main()