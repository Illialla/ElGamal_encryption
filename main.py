import random

class ElGamalEncryption:

    @staticmethod
    def main():
        mes = input("Введите ваше сообщение: ")
        # Проверка на пустую строку
        if not mes.strip():
            raise ValueError("Сообщение не может быть пустым.")
        message = int(mes)

        bit_length = 16  # Длина в битах желаемого простого числа
        p = MathUtils.generate_prime_number(bit_length)
        g = MathUtils.find_primitive_root(p)
        x = MathUtils.generate_random_big_integer(bit_length)
        while x > p - 1:
            x = MathUtils.generate_random_big_integer(bit_length)

        y = MathUtils.mod_pow(g, x, p)
        print(f"Сгенерированное простое число p: {p}")
        print(f"Сгенерированное число g: {g}")
        print(f"Сгенерированное число x: {x}")
        print(f"Полученное y: {y}")

        public_key = (y, g, p)
        print(f"Полученный открытый ключ: {public_key}")
        private_key = (x)
        print(f"Полученный закрытый ключ: {private_key}")

        k = MathUtils.generate_random_big_integer(bit_length)
        while MathUtils.gcd(k, p - 1) != 1 or k > p:
            k = MathUtils.generate_random_big_integer(bit_length)

        print(f"Сгенерированное число k: {k}")
        r = MathUtils.mod_pow(g, k, p)
        print(f"Полученное r: {r}")
        s = MathUtils.get_s(message, x, r, k, p - 1)
        print(f"Сгенерированная цифровая подпись: {(r, s)}")

        print(f"Проверка: \n r>0 = {r > 0}, r<p = {r < p}, s>0 = {s > 0}, s<p-1 = {s < p - 1}")

        left_check = (MathUtils.mod_pow(y, r, p) * MathUtils.mod_pow(r, s, p)) % p
        is_correct = left_check == MathUtils.mod_pow(g, message, p)
        print(f"Проверка корректности: {is_correct}")
        return {
                "message": message,
                "p": p,
                "g": g,
                "x": x,
                "y": y,
                "public_key": public_key,
                "private_key": private_key,
                "k": k,
                "r": r,
                "s": s,
                "is_correct": is_correct,
            }

class MathUtils:

    @staticmethod
    def generate_prime_number(bit_length):
        prime_candidate = MathUtils.generate_random_big_integer(bit_length)
        while not MathUtils.is_prime(prime_candidate, 100):
            prime_candidate = MathUtils.generate_random_big_integer(bit_length)
        return prime_candidate

    @staticmethod
    def get_s(message, x, r, k, p1):
        message %= p1
        x %= p1
        r %= p1
        value = (x * r) % p1
        if value < p1:
            value = -value + p1
        value %= p1
        value += message
        k = MathUtils.mod_inverse(k, p1)
        k %= p1
        s = (value * k) % p1
        return s

    @staticmethod
    def gcd(a, b):
        while a != 0 and b != 0:
            if a > b:
                a %= b
            else:
                b %= a
        return a + b

    @staticmethod
    def find_primitive_root(p):
        for g in range(2, p):
            is_primitive_root = True
            for i in range(1, p - 1):
                if MathUtils.mod_pow(g, i, p) == 1:
                    is_primitive_root = False
                    break
            if is_primitive_root:
                return g
        return -1  # Если не найдено первообразное корень

    @staticmethod
    def mod_inverse(a, m):
        if MathUtils.gcd(a, m) != 1:
            raise ValueError("Обратный элемент не существует, так как a и m не взаимно простые.")
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return 1

    @staticmethod
    def is_prime(num, iterations):
        if num <= 1 or num % 2 == 0:
            return False
        if num == 2 or num == 3:
            return True

        d = num - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        for _ in range(iterations):
            a = random.randint(2, num - 2)  # Генерация случайного числа a в диапазоне [2, num-2]
            x = MathUtils.mod_pow(a, d, num)

            if x == 1 or x == num - 1:
                continue

            for r in range(s - 1):  # Изменено на s - 1, чтобы проверить r от 0 до s-2
                x = MathUtils.mod_pow(x, 2, num)
                if x == 1:
                    return False
                if x == num - 1:
                    break
            else:
                if x != num - 1:
                    return False
        return True

    @staticmethod
    def mod_pow(a, b, c):
        result = 1
        while b > 0:
            if b % 2 == 1:
                result = (result * a) % c
            b //= 2
            a = (a * a) % c
        return result

    @staticmethod
    def generate_random_big_integer(bit_length):
        min_value = 2 ** (bit_length - 1)  # Минимальное значение для заданного количества бит
        max_value = (2 ** bit_length) - 1  # Максимальное значение для заданного количества бит
        return random.randint(min_value, max_value)


if __name__ == "__main__":
    ElGamalEncryption.main()
