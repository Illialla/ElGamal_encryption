[![MyTests](https://github.com/Illialla/ElGamal_encryption/actions/workflows/test-action.yml/badge.svg)](https://github.com/Illialla/ElGamal_encryption/actions/workflows/test-action.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/Illialla/ElGamal_encryption/badge.svg?branch=main)](https://coveralls.io/github/Illialla/ElGamal_encryption?branch=main)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ElGamal_encryption&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ElGamal_encryption)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=ElGamal_encryption&metric=bugs)](https://sonarcloud.io/summary/new_code?id=ElGamal_encryption)
[![Code smells](https://sonarcloud.io/api/project_badges/measure?project=ElGamal_encryption&metric=code_smells)](https://sonarcloud.io/dashboard?id=ElGamal_encryption)

## План тестирования
### 1. Блочные тесты
1. BlockTestMathUtils.TestGeneratePrimeNumberWithBitLength16:
 - Тип теста: Позитивный
 - Краткое описание: Тест проверяет, что сгенерированное число является простым и находится в пределах 16-битного диапазона
 - Входные данные: bitLength = 16
 - Ожидаемые выходные данные: Простое число primeCandidate, которое является 16-битным (значение от 32768 до 65535)
2. BlockTestMathUtils.TestGeneratePrimeNumberWithBitLength32:
 - Тип теста: Негативный
 - Краткое описание: Тест проверяет, что время работы функции при bit_length=32 превышает 5 секунд
 - Входные данные: bitLength = 32
 - Ожидаемые выходные данные: RuntimeError
3. BlockTestMathUtils.TestGCDWithSmallIntegers:
 - Тип теста: Позитивный
 - Краткое описание: Тест проверяет, что GCD для пары малых чисел вычисляется правильно.
 - Входные данные: a = 8, b = 12
 - Ожидаемые выходные данные: 4
4. BlockTestMathUtils.TestModInverseWithNotRelativelyPrime
 - Тип теста: Негативный
 - Краткое описание: Проверка на отсутствие обратного элемента, когда a и m имеют общий делитель
 - Входные данные: a = 2, m = 4
 - Ожидаемые выходные данные: ValueError (обратный элемент не существует)
5. BlockTestMathUtils.TestModInverseReturnsOne
 - Тип теста: Негативный
 - Краткое описание: Проверка на возврат крайнего значения равного 1
 - Входные данные: a = 1, m = 7
 - Ожидаемые выходные данные: 1
6. BlockTestMathUtils.TestModInverseWithRelativelyPrime
 - Тип теста: Позитивный
 - Краткое описание: Проверка на отсутствие обратного элемента, когда a и m имеют общий делитель
 - Входные данные: a = 2, m = 5
 - Ожидаемые выходные данные: ValueError (обратный элемент не существует)
7. BlockTestMathUtils.TestModPowEdgeCases
 - Тип теста: Позитивный
 - Краткое описание: Проверка корректности работы при b = 0
 - Входные данные: a = 5, b = 0, c = 7
 - Ожидаемые выходные данные: 1 (поскольку любое число в степени 0 равно 1)
8. CertificationTestElGamalEncryption.TestGetSMesWithLetters:
- Тип теста: Негативный тест
- Краткое описание: Проверка обработки сообщения содержащего буквы
- Входные данные: mes = "абв"
- Ожидаемые выходные данные: TypeError

9. BlockTestMathUtils.TestIsPrimeNumber:
- Тип теста: Позитивный
- Краткое описание: Проверяет, что функция правильно идентифицирует известные простые числа
- Входные данные: num = 7
- Ожидаемые выходные данные: True
10. BlockTestMathUtils.TestIsNotPrimeNumber:
- Тип теста: Негативный
- Краткое описание: Проверяет, что функция правильно идентифицирует известные составные числа
- Входные данные: num = 10
- Ожидаемые выходные данные: False
11. BlockTestMathUtils.TestFindPrimitiveRoot:
- Тип теста: Позитивный
- Краткое описание: Проверяет, что возвращенное значение является примитивным корнем, исполняя все необходимые проверки.
- Входные данные: p = 7
- Ожидаемые выходные данные: Все степени до 6 (0-6) не равны 1, по исключению 6 (7-1)
12. BlockTestMathUtils.TestFindPrimitiveRoot:
- Тип теста: Негативный
- Краткое описание: Проверяет, что не был найден примитивный корень
- Входные данные: p = 1
- Ожидаемые выходные данные: -1
[//]: # (8. TestMathUtils.TestElGamalEncryptionMain:)
[//]: # (- Тип теста: Позитивный)
[//]: # (- Краткое описание: Тест проверяет, что алгоритм Эль-Гамаля работает корректно и генерирует цифровую подпись.)
[//]: # (- Входные данные: mes = "123")
[//]: # (- Ожидаемые выходные данные: полученная цифровая подпись &#40;r, s&#41; и результат проверки корректности равный True.)

### 2. Интеграционные тесты
1. IntegrationTest.TestCompareGeneratedNums:
- Тип теста: Позитивный тест
- Краткое описание: Проверка того, что при нескольких вызовах функции generate_random_big_integer будут генерироваться разные числа 
- Входные данные: несколько вызовов функции generate_random_big_integer
- Ожидаемые выходные данные: массив из нескольких разных сгенерированных чисел
2. IntegrationTest.TestGeneratePrimitiveRoot:
- Тип теста: Позитивный тест
- Краткое описание: Проверка того, что при обращении из класса ElGamalEncryption к классу MathUtils с помощью функции find_primitive_root возвращается примитивный корень g  
- Входные данные: вызов функции find_primitive_root
- Ожидаемые выходные данные: возврат значения числа g
3. IntegrationTest.TestDifferentSignaturesForSameMes:
- Тип теста: Позитивный тест
- Краткое описание: Проверка того, что при нескольких запусках программы для одинакового сообщения будут генерироваться разные цифровые подписи 
- Входные данные: mes = "123", несколько запусков программы (функции main)
- Ожидаемые выходные данные: массив из нескольких разных цифровых подписей
4. IntegrationTest.TestValidSignatureVerification
- Тип теста: Позитивный тест
- Краткое описание: Проверка корректности проверки подписи для сгенерированной подписи
- Входные данные: mes = "123"
- Ожидаемые выходные данные: is_correct = True
5. IntegrationTest.TestSignatureVerificationWithInvalidSignature
- Тип теста: Негативный тест
- Краткое описание: Проверка обработки неверной подписи (измененной)
- Входные данные: mes = "123", изменение значения s в сгенерированной подписи на другое
- Ожидаемые выходные данные: is_correct = False
### 3. Аттестационные тесты
1. CertificationTestElGamalEncryption.TestElGamalEncryptionMain:
- Тип теста: Позитивный
- Краткое описание: Тест проверяет, что алгоритм Эль-Гамаля работает корректно и генерирует открытый и закрытый ключи, а также цифровую подпись при вводе корректного сообщения.
- Входные данные: mes = "123"
- Ожидаемые выходные данные:
  - Сгенерированное простое число p
  - Сгенерированное число g
  - Сгенерированное число x
  - Полученное значение y
  - Открытый ключ (y, g, p)
  - Закрытый ключ (x)
  - Сгенерированное число k
  - Полученное значение r
  - Полученная цифровая подпись (r, s)
  - Результат проверки корректности равный True
2. CertificationTestElGamalEncryption.TestElGamalEncryptionSpeedCheck:
- Тип теста: Позитивный тест
- - Краткое описание: Оценка скорости выполнения формирования цифровой подписи
- Входные данные: mes = "12" / mes = "12345678909876543223454566545456789"
- Ожидаемые выходные данные: скорость формирования цифровой подписи не превышает 5 секунд
3. CertificationTestElGamalEncryption.TestElGamalEncryptionBlankMes:
- Тип теста: Негативный тест
- Краткое описание: Проверка обработки пустого сообщения
- Входные данные: mes = ""
- Ожидаемые выходные данные: ValueError
4. CertificationTestElGamalEncryption.TestElGamalEncryptionMesWithLetters:
- Тип теста: Негативный тест
- Краткое описание: Проверка обработки сообщения содержащего буквы
- Входные данные: mes = "абв"
- Ожидаемые выходные данные: ValueError
5. CertificationTestElGamalEncryption.TestElGamalEncryptionMesWithSpecialChars:
- Тип теста: Негативный тест
- Краткое описание: Проверка обработки сообщения содержащего специальные символы
- Входные данные: mes = "@#^?"
- Ожидаемые выходные данные: ValueError
6. CertificationTestElGamalEncryption.TestElGamalEncryptionNegativeMes:
- Тип теста: Позитивный тест
- Краткое описание: Проверка обработки сообщения с отрицательным числом
- Входные данные: mes = "-23456"
- Ожидаемые выходные данные: left_check == MathUtils.mod_pow(g, message, p) = False (Проверка корректности сформированной подписи)

