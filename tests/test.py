import unittest
from main import MathUtils, ElGamalEncryption
import time
from io import StringIO
import sys

class BlockTestMathUtils(unittest.TestCase):
    def test_generate_prime_number_with_bit_length_16(self):
        bit_length = 16
        prime_candidate = MathUtils.generate_prime_number(bit_length)
        self.assertTrue(MathUtils.is_prime(prime_candidate, 100))
        self.assertGreaterEqual(prime_candidate, 32768)
        self.assertLessEqual(prime_candidate, 65535)

    def test_generate_random_big_integer_runtime(self):
        bit_length = 32

        start_time = time.time()  # Запоминаем время начала
        result = MathUtils.generate_random_big_integer(bit_length)  # Вызываем функцию
        end_time = time.time()  # Запоминаем время окончания

        elapsed_time = end_time - start_time  # Вычисляем время выполнения

        # Проверяем, что время выполнения не превышает 5 секунд
        if elapsed_time > 5:
            raise RuntimeError("Время выполнения функции превышает 5 секунд.")

        # Дополнительно, вы можете проверить, что результат находится в правильном диапазоне
        min_value = 2 ** (bit_length - 1)
        max_value = (2 ** bit_length) - 1
        self.assertGreaterEqual(result, min_value)
        self.assertLessEqual(result, max_value)

    def test_gcd_with_small_integers(self):
        a = 8
        b = 12
        self.assertEqual(MathUtils.gcd(a, b), 4)

    def test_mod_inverse_with_not_relatively_prime(self):
        a = 2
        m = 4
        with self.assertRaises(ValueError):
            MathUtils.mod_inverse(a, m)

    def test_mod_inverse_returns_one(self):
        # Проверяем случай, когда a = 1, который всегда должен возвращать 1
        a = 1
        m = 7  # 1 и 7 взаимно простые
        result = MathUtils.mod_inverse(a, m)
        self.assertEqual(result, 1)

    def test_mod_pow_edge_cases(self):
        a = 5
        b = 0
        c = 7
        self.assertEqual(MathUtils.mod_pow(a, b, c), 1)

    # def test_mod_pow_edge_cases_negative(self):
    #     a = 5
    #     b = 1
    #     c = -7
    #     self.assertEqual(MathUtils.mod_pow(a, b, c), 1)

    def test_is_prime_number(self):
        num = 7
        self.assertTrue(MathUtils.is_prime(num, 100))

    def test_is_not_prime_number(self):
        num = 10
        self.assertFalse(MathUtils.is_prime(num, 100))

    def test_find_primitive_root(self):
        p = 3
        g = MathUtils.find_primitive_root(p)
        self.assertTrue(g != -1)
        for i in range(1, p - 1):
            self.assertNotEqual(MathUtils.mod_pow(g, i, p), 1)

    def test_find_primitive_root_no_root(self):
        p = 1  # 1 не имеет первообразного корня
        result = MathUtils.find_primitive_root(p)
        self.assertEqual(result, -1)

    def test_get_s_mes_with_letters(self):
        mes = "abc"
        x = 47516
        r = 3557
        k = 37973
        p = 64950
        with self.assertRaises(TypeError):
            MathUtils.get_s(mes,x,r,k,p)



class IntegrationTest(unittest.TestCase):
    def setUp(self):
        # Сохраняем оригинальный стандартный вывод
        self.original_stdout = sys.stdout
        # Перенаправляем стандартный вывод для тестирования
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        # Возвращаем стандартный вывод
        sys.stdout = self.original_stdout

    def test_compare_generated_nums(self):
        generated_nums = [MathUtils.generate_random_big_integer(16) for _ in range(10)]
        print(generated_nums)
        self.assertEqual(len(generated_nums), len(set(generated_nums))) # множество уникально и если там есть повторы, то останется только 1 число

    def test_generate_primitive_root(self):
        p = MathUtils.generate_prime_number(16)
        g = MathUtils.find_primitive_root(p)
        self.assertGreater(g, 0)
        self.assertLess(g, p)

    def test_different_signatures_for_same_mes(self):
        # Позитивный тест
        mes = "123"
        signatures = []
        for _ in range(5):
            # Перенаправляем ввод
            sys.stdin = StringIO(mes)
            result = ElGamalEncryption.main()
            signatures.append(result['s'])

        self.assertEqual(len(signatures), len(set(signatures)))

    def test_valid_signature_verification(self):
        # Позитивный тест
        mes = "123"
        sys.stdin = StringIO(mes)
        result = ElGamalEncryption.main()
        self.assertTrue(result['is_correct'])

    def test_signature_verification_with_invalid_signature(self):
        # Негативный тест
        mes = "123"
        sys.stdin = StringIO(mes)
        result = ElGamalEncryption.main()
        original_signature = result['s']

        # Изменяем значение s в подписи
        invalid_signature = (result['r'], original_signature + 1)  # Изменение s
        left_check = (MathUtils.mod_pow(result['y'], invalid_signature[0], result['p']) * MathUtils.mod_pow(
            invalid_signature[0], invalid_signature[1], result['p'])) % result['p']
        is_correct = left_check == MathUtils.mod_pow(result['g'], int(mes), result['p'])
        self.assertFalse(is_correct)


class CertificationTestMathUtils(unittest.TestCase):
    def setUp(self):
        # Сохраняем оригинальный стандартный вывод
        self.original_stdout = sys.stdout
        # Перенаправляем стандартный вывод для тестирования
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        # Возвращаем стандартный вывод
        sys.stdout = self.original_stdout

    def test_el_gamal_encryption_main(self):
        # Позитивный тест
        input_data = "123"
        sys.stdin = StringIO(input_data)

        # Запускаем метод main и получаем результат
        result = ElGamalEncryption.main()

        # Проверяем значения в возвращаемом словаре
        self.assertEqual(result["message"], 123)
        self.assertTrue(result["p"] > 0)  # Проверка, что p сгенерировано
        self.assertTrue(result["g"] > 0)  # Проверка, что g сгенерировано
        self.assertTrue(result["x"] > 0)  # Проверка, что x сгенерировано
        self.assertTrue(result["y"] > 0)  # Проверка, что y сгенерировано
        self.assertIsInstance(result["public_key"], tuple)  # Проверка, что public_key - это кортеж
        self.assertIsInstance(result["private_key"], int)  # Проверка, что private_key - это число
        self.assertTrue(result["k"] > 0)  # Проверка, что k сгенерировано
        self.assertTrue(result["r"] > 0)  # Проверка, что r сгенерировано
        self.assertTrue(result["s"] > 0)  # Проверка, что s сгенерировано
        self.assertTrue(result["is_correct"])  # Проверка корректности подписи

    def test_el_gamal_encryption_speed_check(self):
        # Позитивный тест
        input_data = "12"
        sys.stdin = StringIO(input_data)

        start_time = time.time()
        ElGamalEncryption.main()
        end_time = time.time()
        execution_time = end_time - start_time

        self.assertLess(execution_time, 5)

    def test_el_gamal_encryption_blank_mes(self):
        input_data = "\n"
        sys.stdin = StringIO(input_data)

        with self.assertRaises(ValueError):
            ElGamalEncryption.main()

    def test_el_gamal_encryption_mes_with_letters(self):
        input_data = "абв"
        sys.stdin = StringIO(input_data)

        with self.assertRaises(ValueError):
            ElGamalEncryption.main()

    def test_get_s_mes_with_letters(self):
        input_data = "абв"
        sys.stdin = StringIO(input_data)

        with self.assertRaises(ValueError):
            ElGamalEncryption.main()

    def test_get_s_mes_with_special_chars(self):
        input_data = "@#^?"
        sys.stdin = StringIO(input_data)

        with self.assertRaises(ValueError):
            ElGamalEncryption.main()

    def test_el_gamal_encryption_negative_mes(self):
        input_data = "-23456"
        sys.stdin = StringIO(input_data)

        ElGamalEncryption.main()
        output = self.held_output.getvalue().splitlines()
        self.assertTrue(any("Проверка корректности: False" in line for line in output))

if __name__ == '__main__':
    unittest.main()