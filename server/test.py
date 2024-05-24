
# import time
# n = 10**8
# # Przypadek 1: Pętla z try wewnątrz
# start = time.time()
# for i in range(n):
#     try:
#         if i % n == 0:
#             raise ValueError
#     except ValueError:
#         pass
# end = time.time()
# print(f'Pętla z try wewnątrz: {end - start} s')

# start = time.time()
# try:
#     for i in range(n):
#         if i % n == 0:
#             raise ValueError
# except ValueError:
#     pass
# end = time.time()
# print(f'Try z pętlą wewnątrz: {end - start} s')
################
# def generator():
#     yield 1
#     yield 2
#     yield 3

# gen = generator()
# print(next(gen))
# for i in gen:
#     print(' ', i)

##################

import pandas as pd

data = pd.DataFrame({'a' : [ 1, 2, 3], 'b' : ['c', 1, 2]})
for column in data:
    print(data[column])