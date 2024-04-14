import multiprocessing
import time


def factorize(number):
    factors = []
    for i in range(1, number+1):
        if number % i ==0:
            factors.append(i)
    return factors
    

def factorize_async(numbers):
    num_processes = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(factorize, numbers)
    return results


if __name__ == '__main__':
    # Synchronous execution
    print("Synchronous execution")
    start_time_s = time.time()
    a = factorize(128)
    print(a)
    b = factorize(255)
    print(b)
    c = factorize(99999)
    print(c)
    d = factorize(10651060)
    print(d)
    end_time_s = time.time()
    print(f'Done {end_time_s - start_time_s}')

    # Asynchronous execution
    print("Asynchronous execution")
    start_time_as = time.time()
    a, b, c, d = factorize_async([128, 255, 99999, 10651060])
    print(a)
    print(b)
    print(c)
    print(d)
    end_time_as = time.time()
    print(f'Done {end_time_as - start_time_as}')