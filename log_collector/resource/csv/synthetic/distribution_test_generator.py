import random


with open('../distribution_test.csv', mode='w', encoding='UTF-8') as out:
    out.write('foo, bar, baz, qux\n')
    for i in range(1000):
        line = f'{random.uniform(0,3)}, '
        line += f'{random.gauss(2,2)}, '
        line += f'{random.weibullvariate(1,3)}, '
        line += f'{random.paretovariate(1.5)}'
        f.write(line + '\n')
