# import asyncio

# async def fetch_data():
#     print("Rozpoczynam pobieranie danych...")
#     await asyncio.sleep(3)  # symulacja długotrwałej operacji
#     print("Dane zostały pobrane.")
#     return "Dane"

# async def process_data():
#     print("Rozpoczynam przetwarzanie danych...")
#     await asyncio.sleep(2)  # symulacja długotrwałej operacji
#     print("Przetwarzanie zakończone.")
#     return "Wynik"

# async def main():
#     data_task = asyncio.create_task(fetch_data())
#     process_task = asyncio.create_task(process_data())
#     print("oczekiwanie")
#     data = await data_task
    
#     result = await process_task
    
#     print(f"{data}, {result}")

# # Uruchomienie funkcji głównej
# asyncio.run(main())

import time
n = 10**8
# Przypadek 1: Pętla z try wewnątrz
start = time.time()
for i in range(n):
    try:
        if i % n == 0:
            raise ValueError
    except ValueError:
        pass
end = time.time()
print(f'Pętla z try wewnątrz: {end - start} s')

# Przypadek 2: Try z pętlą wewnątrz
start = time.time()
try:
    for i in range(n):
        if i % n == 0:
            raise ValueError
except ValueError:
    pass
end = time.time()
print(f'Try z pętlą wewnątrz: {end - start} s')