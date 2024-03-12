import random

if __name__ == '__main__':
    random.seed(b'\x01\xc6C\x95\xaaO+M\xf2dN*5D\xb5\xdc\xe3\xc5\xc6G')

    # Generate a list of 24 unique numbers from 1 to 66
    random_numbers = random.sample(range(1, 67), 24)

    random_numbers.sort()
    print(random_numbers)

