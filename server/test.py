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

def a():
    for i in range(5):
        yield i

def b():
    return a()

for i in b():
    print(i)