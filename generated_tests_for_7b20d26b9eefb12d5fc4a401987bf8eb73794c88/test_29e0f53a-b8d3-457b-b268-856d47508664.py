import csv


def test_modulo_equals_one():
    assert Calculator().calculate('1 % 2') == 1


def test_modulo_equals_two():
    assert Calculator().calculate('2 % 3') == 2


def test_modulo_equals_zero():
    assert Calculator().calculate('10 % 5') == 0


def test_addition_and_modulo():
    assert Calculator().calculate("1 + 10 % 3") == 2
# Generate asserts for all test cases in the table
with open('test_1.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        exec("""def test_{0}(): assert Calculator().calculate('{1}') == {2} """.format(row[3], row[0], row[1]))
