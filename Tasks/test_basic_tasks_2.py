"""
Тести для перевірки задач з basic_tasks_2.md

Використання:
1. Реалізуйте функції нижче
2. Запустіть файл: python test_basic_tasks_2.py
3. Якщо всі тести пройдуть - побачите "Всі тести пройдено успішно!"

Примітка: Деякі функції мають шаблонну реалізацію з pass.
Замініть pass на свій код.
"""


# ============================================================================
# TASK 1: Фільтрація парних чисел
# ============================================================================
def filter_even_numbers(numbers):
    """Повертає список тільки з парними числами"""
    pass  # TODO: Реалізуйте функцію


def test_task_1():
    assert filter_even_numbers([1, 2, 3, 4, 5, 6, 7, 8]) == [2, 4, 6, 8]
    assert filter_even_numbers([15, 22, 37, 48]) == [22, 48]
    assert filter_even_numbers([1, 3, 5, 7]) == []  # Немає парних
    assert filter_even_numbers([2, 4, 6]) == [2, 4, 6]  # Всі парні
    assert filter_even_numbers([]) == []  # Порожній список
    print("✓ Task 1 passed")


# ============================================================================
# TASK 2: Підрахунок слів
# ============================================================================
def count_words(sentence):
    """Підраховує кількість слів у реченні"""
    pass  # TODO: Реалізуйте функцію


def test_task_2():
    assert count_words("Hello world") == 2
    assert count_words("Python is awesome") == 3
    assert count_words("I love programming in Python") == 5
    assert count_words("") == 0  # Порожній рядок
    assert count_words("OneWord") == 1
    print("✓ Task 2 passed")


# ============================================================================
# TASK 3: Перевірка анаграм
# ============================================================================
def is_anagram(word1, word2):
    """Перевіряє чи є слова анаграмами"""
    pass  # TODO: Реалізуйте функцію


def test_task_3():
    assert is_anagram("listen", "silent") == True
    assert is_anagram("hello", "world") == False
    assert is_anagram("evil", "vile") == True
    assert is_anagram("a", "a") == True
    assert is_anagram("abc", "cba") == True
    print("✓ Task 3 passed")


# ============================================================================
# TASK 4: Найдовше слово
# ============================================================================
def find_longest_word(sentence):
    """Знаходить найдовше слово у реченні"""
    pass  # TODO: Реалізуйте функцію


def test_task_4():
    assert find_longest_word("Python is a powerful programming language") == "programming"
    assert find_longest_word("Hello world") == "Hello"
    assert find_longest_word("a bb ccc") == "ccc"
    assert find_longest_word("test") == "test"
    print("✓ Task 4 passed")


# ============================================================================
# TASK 5: Частота літер
# ============================================================================
def letter_frequency(text):
    """Повертає словник з частотою кожної літери"""
    pass  # TODO: Реалізуйте функцію


def test_task_5():
    assert letter_frequency("hello") == {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    result = letter_frequency("Programming")
    assert result == {'p': 1, 'r': 2, 'o': 1, 'g': 2, 'a': 1, 'm': 2, 'i': 1, 'n': 1}
    assert letter_frequency("aaa") == {'a': 3}
    assert letter_frequency("") == {}
    print("✓ Task 5 passed")


# ============================================================================
# TASK 6: Видалення дублікатів
# ============================================================================
def remove_duplicates(items):
    """Видаляє дублікати зі списку, зберігаючи порядок"""
    pass  # TODO: Реалізуйте функцію


def test_task_6():
    assert remove_duplicates([1, 2, 2, 3, 4, 4, 5]) == [1, 2, 3, 4, 5]
    assert remove_duplicates(["a", "b", "a", "c", "b"]) == ["a", "b", "c"]
    assert remove_duplicates([1, 1, 1]) == [1]
    assert remove_duplicates([1, 2, 3]) == [1, 2, 3]
    assert remove_duplicates([]) == []
    print("✓ Task 6 passed")


# ============================================================================
# TASK 7: Конвертація температури
# ============================================================================
def celsius_to_fahrenheit(celsius):
    """Конвертує Цельсій в Фаренгейт"""
    pass  # TODO: Реалізуйте функцію


def fahrenheit_to_celsius(fahrenheit):
    """Конвертує Фаренгейт в Цельсій"""
    pass  # TODO: Реалізуйте функцію


def test_task_7():
    assert celsius_to_fahrenheit(25) == 77.0
    assert celsius_to_fahrenheit(0) == 32.0
    assert celsius_to_fahrenheit(100) == 212.0
    assert abs(fahrenheit_to_celsius(100) - 37.78) < 0.01
    assert fahrenheit_to_celsius(32) == 0.0
    print("✓ Task 7 passed")


# ============================================================================
# TASK 8: Перевірка простого числа
# ============================================================================
def is_prime(n):
    """Перевіряє чи є число простим"""
    pass  # TODO: Реалізуйте функцію


def test_task_8():
    assert is_prime(7) == True
    assert is_prime(10) == False
    assert is_prime(13) == True
    assert is_prime(1) == False
    assert is_prime(2) == True
    assert is_prime(0) == False
    print("✓ Task 8 passed")


# ============================================================================
# TASK 10: Сума цифр числа
# ============================================================================
def sum_of_digits(number):
    """Повертає суму всіх цифр у числі"""
    pass  # TODO: Реалізуйте функцію


def test_task_10():
    assert sum_of_digits(123) == 6
    assert sum_of_digits(4567) == 22
    assert sum_of_digits(999) == 27
    assert sum_of_digits(0) == 0
    assert sum_of_digits(5) == 5
    print("✓ Task 10 passed")


# ============================================================================
# TASK 11: Сортування словників
# ============================================================================
def sort_students_by_grade(students):
    """Сортує список студентів за оцінкою (від найвищої)"""
    pass  # TODO: Реалізуйте функцію


def test_task_11():
    students = [
        {"name": "Alice", "grade": 85},
        {"name": "Bob", "grade": 92},
        {"name": "Charlie", "grade": 78}
    ]
    sorted_students = sort_students_by_grade(students)
    assert sorted_students[0]["name"] == "Bob"
    assert sorted_students[1]["name"] == "Alice"
    assert sorted_students[2]["name"] == "Charlie"
    assert sorted_students[0]["grade"] == 92
    print("✓ Task 11 passed")


# ============================================================================
# TASK 12: Валідація номера телефону
# ============================================================================
def is_valid_ukrainian_phone(phone):
    """Перевіряє чи є номер валідним українським номером"""
    pass  # TODO: Реалізуйте функцію


def test_task_12():
    assert is_valid_ukrainian_phone("+380501234567") == True
    assert is_valid_ukrainian_phone("0501234567") == False
    assert is_valid_ukrainian_phone("+38050123456") == False
    assert is_valid_ukrainian_phone("+380-50-123-45-67") == False
    assert is_valid_ukrainian_phone("+0100501234567") == False
    print("✓ Task 12 passed")


# ============================================================================
# TASK 13: Числа що діляться на 3 або 5
# ============================================================================
def divisible_by_3_or_5(n):
    """Повертає список чисел від 1 до n, які діляться на 3 або 5"""
    pass  # TODO: Реалізуйте функцію


def test_task_13():
    assert divisible_by_3_or_5(15) == [3, 5, 6, 9, 10, 12, 15]
    assert divisible_by_3_or_5(10) == [3, 5, 6, 9, 10]
    assert divisible_by_3_or_5(5) == [3, 5]
    assert divisible_by_3_or_5(2) == []
    print("✓ Task 13 passed")


# ============================================================================
# TASK 14: Перевертання слів
# ============================================================================
def reverse_words(sentence):
    """Перевертає кожне слово, але зберігає порядок слів"""
    pass  # TODO: Реалізуйте функцію


def test_task_14():
    assert reverse_words("Hello World") == "olleH dlroW"
    assert reverse_words("Python Programming") == "nohtyP gnimmargorP"
    assert reverse_words("a b c") == "a b c"
    assert reverse_words("test") == "tset"
    print("✓ Task 14 passed")


# ============================================================================
# TASK 15: Об'єднання відсортованих списків
# ============================================================================
def merge_sorted_lists(list1, list2):
    """Об'єднує два відсортовані списки в один відсортований"""
    pass  # TODO: Реалізуйте функцію


def test_task_15():
    assert merge_sorted_lists([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
    assert merge_sorted_lists([1, 2, 3], [4, 5, 6]) == [1, 2, 3, 4, 5, 6]
    assert merge_sorted_lists([], [1, 2, 3]) == [1, 2, 3]
    assert merge_sorted_lists([1, 2, 3], []) == [1, 2, 3]
    print("✓ Task 15 passed")


# ============================================================================
# TASK 17: Другий за величиною елемент
# ============================================================================
def second_largest(numbers):
    """Знаходить другий за величиною елемент у списку"""
    pass  # TODO: Реалізуйте функцію


def test_task_17():
    assert second_largest([1, 2, 3, 4, 5]) == 4
    assert second_largest([10, 5, 8, 12, 3]) == 10
    assert second_largest([1, 1, 2]) == 1
    assert second_largest([5, 5, 5, 3]) == 3
    print("✓ Task 17 passed")


# ============================================================================
# TASK 19: Збалансовані дужки
# ============================================================================
def are_brackets_balanced(s):
    """Перевіряє чи збалансовані дужки в рядку"""
    pass  # TODO: Реалізуйте функцію


def test_task_19():
    assert are_brackets_balanced("(())") == True
    assert are_brackets_balanced("()()") == True
    assert are_brackets_balanced("(()") == False
    assert are_brackets_balanced("())(") == False
    assert are_brackets_balanced("({[]})") == True
    assert are_brackets_balanced("") == True
    print("✓ Task 19 passed")


# ============================================================================
# TASK 20: НСД (найбільший спільний дільник)
# ============================================================================
def gcd(a, b):
    """Знаходить найбільший спільний дільник двох чисел"""
    pass  # TODO: Реалізуйте функцію


def test_task_20():
    assert gcd(48, 18) == 6
    assert gcd(100, 50) == 50
    assert gcd(17, 19) == 1
    assert gcd(12, 8) == 4
    assert gcd(1, 1) == 1
    print("✓ Task 20 passed")


# ============================================================================
# TASK 21: Високосний рік
# ============================================================================
def is_leap_year(year):
    """Визначає чи є рік високосним"""
    pass  # TODO: Реалізуйте функцію


def test_task_21():
    assert is_leap_year(2020) == True
    assert is_leap_year(2021) == False
    assert is_leap_year(2000) == True
    assert is_leap_year(1900) == False
    assert is_leap_year(2024) == True
    print("✓ Task 21 passed")


# ============================================================================
# TASK 22: Дільники числа
# ============================================================================
def get_divisors(n):
    """Повертає список всіх дільників числа"""
    pass  # TODO: Реалізуйте функцію


def test_task_22():
    assert get_divisors(12) == [1, 2, 3, 4, 6, 12]
    assert get_divisors(15) == [1, 3, 5, 15]
    assert get_divisors(7) == [1, 7]
    assert get_divisors(1) == [1]
    print("✓ Task 22 passed")


# ============================================================================
# TASK 23: Шифр Цезаря
# ============================================================================
def caesar_cipher(text, shift):
    """Шифрує текст шифром Цезаря"""
    pass  # TODO: Реалізуйте функцію


def test_task_23():
    assert caesar_cipher("hello", 3) == "khoor"
    assert caesar_cipher("abc", 1) == "bcd"
    assert caesar_cipher("xyz", 3) == "abc"
    assert caesar_cipher("ABC", 1) == "BCD"
    print("✓ Task 23 passed")


# ============================================================================
# TASK 24: Пари чисел з заданою сумою
# ============================================================================
def find_pairs_with_sum(numbers, target_sum):
    """Знаходить всі пари чисел, сума яких дорівнює target_sum"""
    pass  # TODO: Реалізуйте функцію


def test_task_24():
    result1 = find_pairs_with_sum([1, 2, 3, 4, 5], 5)
    assert sorted(result1) == [(1, 4), (2, 3)]

    result2 = find_pairs_with_sum([1, 2, 3, 4], 6)
    assert result2 == [(2, 4)]

    result3 = find_pairs_with_sum([1, 2, 3], 10)
    assert result3 == []
    print("✓ Task 24 passed")


# ============================================================================
# TASK 26: Перевірка всіх голосних
# ============================================================================
def has_all_vowels(text):
    """Перевіряє чи містить текст всі голосні літери"""
    pass  # TODO: Реалізуйте функцію


def test_task_26():
    assert has_all_vowels("education") == True
    assert has_all_vowels("hello world") == False
    assert has_all_vowels("sequoia") == True
    assert has_all_vowels("aeiou") == True
    assert has_all_vowels("bcdfg") == False
    print("✓ Task 26 passed")


# ============================================================================
# TASK 27: Факторіал
# ============================================================================
def factorial(n):
    """Обчислює факторіал числа"""
    pass  # TODO: Реалізуйте функцію


def test_task_27():
    assert factorial(5) == 120
    assert factorial(3) == 6
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(4) == 24
    print("✓ Task 27 passed")


# ============================================================================
# TASK 28: Найдовша послідовність однакових символів
# ============================================================================
def longest_sequence(text):
    """Знаходить найдовшу послідовність однакових символів"""
    pass  # TODO: Реалізуйте функцію


def test_task_28():
    assert longest_sequence("aaabbbcc") == "bbb"
    assert longest_sequence("aabbbbcccc") == "cccc"
    assert longest_sequence("abcd") == "a"
    assert longest_sequence("aaa") == "aaa"
    assert longest_sequence("a") == "a"
    print("✓ Task 28 passed")


# ============================================================================
# TASK 29: Flatten (розгортання списків)
# ============================================================================
def flatten(nested_list):
    """Розгортає вкладені списки в один плоский список"""
    pass  # TODO: Реалізуйте функцію


def test_task_29():
    assert flatten([1, [2, 3], [4, [5, 6]]]) == [1, 2, 3, 4, 5, 6]
    assert flatten([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5]
    assert flatten([1, 2, 3]) == [1, 2, 3]
    assert flatten([]) == []
    print("✓ Task 29 passed")


# ============================================================================
# TASK 32: Конвертація витрати палива
# ============================================================================
def mpg_to_liters_per_100km(mpg):
    """Конвертує милі на галон в літри на 100 км"""
    pass  # TODO: Реалізуйте функцію


def test_task_32():
    assert abs(mpg_to_liters_per_100km(13) - 18.09) < 0.01
    assert abs(mpg_to_liters_per_100km(8) - 29.4) < 0.01
    assert abs(mpg_to_liters_per_100km(34) - 6.92) < 0.01
    assert abs(mpg_to_liters_per_100km(50) - 4.70) < 0.01
    print("✓ Task 32 passed")


# ============================================================================
# ЗАПУСК ВСІХ ТЕСТІВ
# ============================================================================
def run_all_tests():
    """Запускає всі тести"""
    tests = [
        test_task_1,
        test_task_2,
        test_task_3,
        test_task_4,
        test_task_5,
        test_task_6,
        test_task_7,
        test_task_8,
        test_task_10,
        test_task_11,
        test_task_12,
        test_task_13,
        test_task_14,
        test_task_15,
        test_task_17,
        test_task_19,
        test_task_20,
        test_task_21,
        test_task_22,
        test_task_23,
        test_task_24,
        test_task_26,
        test_task_27,
        test_task_28,
        test_task_29,
        test_task_32,
    ]

    print("\n" + "="*60)
    print("ЗАПУСК ТЕСТІВ".center(60))
    print("="*60 + "\n")

    failed_tests = []

    for test in tests:
        try:
            test()
        except AssertionError as e:
            test_name = test.__name__
            failed_tests.append(test_name)
            print(f"✗ {test_name} FAILED: {e}")
        except Exception as e:
            test_name = test.__name__
            failed_tests.append(test_name)
            print(f"✗ {test_name} ERROR: {e}")

    print("\n" + "="*60)
    if failed_tests:
        print(f"ПРОВАЛЕНО ТЕСТІВ: {len(failed_tests)}/{len(tests)}".center(60))
        print("="*60)
        print("\nПровалені тести:")
        for test_name in failed_tests:
            print(f"  - {test_name}")
    else:
        print("ВСІ ТЕСТИ ПРОЙДЕНО УСПІШНО! 🎉".center(60))
        print("="*60)


if __name__ == "__main__":
    run_all_tests()