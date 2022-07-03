from operator import eq


def convert_to_prefix(equation):
    if '-' == equation[0]:
        equation = '0 ' + equation
    stack = []
    postfix = ''
    equation = equation.split(' ')
    for ch in equation:
        if is_operand(ch):
            postfix += ' '+ ch
        else:
            while (len(stack) != 0):
                postfix += ' ' + stack.pop()
            stack.append(ch)
    while len(stack) != 0:
        postfix += ' '+ stack.pop()
    return postfix.split(' ')[1:]

def is_operand(ch):
    return ch in ['+', '-', '/', '*', '^']
