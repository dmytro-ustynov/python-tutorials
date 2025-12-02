"""
🎓 EDUCATIONAL RSA DEMONSTRATION
Розуміння RSA з маленькими простими числами

⚠️  WARNING: Ці маленькі прості числа використовуються ТІЛЬКИ для навчання!
    У реальному світі RSA використовує ВЕЛИЧЕЗНІ прості числа (2048+ біт)!
"""

import random
from primes import PRIMES

# ============================================================================
# RSA МАТЕМАТИКА
# ============================================================================

def gcd(a, b):
    """Найбільший спільний дільник (Greatest Common Divisor)"""
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    """
    Розширений алгоритм Евкліда
    Повертає: (gcd, x, y) де ax + by = gcd
    """
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(e, phi):
    """
    Знайти модульний обернений: d такий що (e * d) % phi = 1
    Використовує розширений алгоритм Евкліда
    """
    gcd_val, x, y = extended_gcd(e, phi)
    if gcd_val != 1:
        raise ValueError("Модульний обернений не існує")
    return x % phi

def is_prime(n):
    """Перевірка чи число просте (для маленьких чисел)"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# ============================================================================
# RSA KEY GENERATION
# ============================================================================

def generate_rsa_keys(p, q, verbose=True):
    """
    Генерувати RSA ключі з двох простих чисел p та q

    Кроки RSA:
    1. Обчислити n = p * q
    2. Обчислити φ(n) = (p-1) * (q-1)
    3. Вибрати e (публічна експонента): 1 < e < φ(n), gcd(e, φ(n)) = 1
    4. Обчислити d (приватна експонента): d * e ≡ 1 (mod φ(n))
    """

    if verbose:
        print("\n" + "="*70)
        print("🔑 RSA KEY GENERATION")
        print("="*70)

    # Перевірка чи числа прості
    if not is_prime(p):
        raise ValueError(f"❌ p = {p} не є простим числом!")
    if not is_prime(q):
        raise ValueError(f"❌ q = {q} не є простим числом!")

    if verbose:
        print(f"\n1️⃣  Вибрані прості числа:")
        print(f"   p = {p}")
        print(f"   q = {q}")

    # Крок 1: Обчислити n = p * q
    n = p * q
    if verbose:
        print(f"\n2️⃣  Обчислити n = p × q:")
        print(f"   n = {p} × {q} = {n}")
        print(f"   📝 n буде використовуватись в публічному та приватному ключі")

    # Крок 2: Обчислити φ(n) = (p-1)(q-1)
    phi = (p - 1) * (q - 1)
    if verbose:
        print(f"\n3️⃣  Обчислити φ(n) = (p-1) × (q-1):")
        print(f"   φ(n) = ({p}-1) × ({q}-1)")
        print(f"   φ(n) = {p-1} × {q-1} = {phi}")
        print(f"   📝 φ(n) - функція Ейлера (кількість чисел менших n, взаємно простих з n)")

    # Крок 3: Вибрати e (зазвичай 65537 або 3)
    # Для маленьких чисел використаємо 65537 якщо можливо, інакше 3
    common_e_values = [65537, 17, 3]
    e = None

    for candidate in common_e_values:
        if candidate < phi and gcd(candidate, phi) == 1:
            e = candidate
            break

    # Якщо жоден стандартний e не підходить, знайти найменший
    if e is None:
        e = 3
        while gcd(e, phi) != 1:
            e += 2  # Пропускаємо парні числа

    if verbose:
        print(f"\n4️⃣  Вибрати публічну експоненту e:")
        print(f"   Умови: 1 < e < φ(n) та gcd(e, φ(n)) = 1")
        print(f"   e = {e}")
        print(f"   Перевірка: gcd({e}, {phi}) = {gcd(e, phi)} ✅")
        print(f"   📝 e буде частиною публічного ключа")

    # Крок 4: Обчислити d (приватна експонента)
    d = mod_inverse(e, phi)
    if verbose:
        print(f"\n5️⃣  Обчислити приватну експоненту d:")
        print(f"   Знайти d таке що: (e × d) mod φ(n) = 1")
        print(f"   d = {d}")
        print(f"   Перевірка: ({e} × {d}) mod {phi} = {(e * d) % phi} ✅")
        print(f"   📝 d буде частиною приватного ключа")

    if verbose:
        print(f"\n" + "="*70)
        print(f"✅ RSA KEYS GENERATED!")
        print(f"="*70)
        print(f"\n📢 PUBLIC KEY (можна ділитися):")
        print(f"   e = {e}")
        print(f"   n = {n}")
        print(f"\n🔒 PRIVATE KEY (тримати в секреті!):")
        print(f"   d = {d}")
        print(f"   n = {n}")

    return {
        'public_key': (e, n),
        'private_key': (d, n),
        'p': p,
        'q': q,
        'phi': phi
    }

# ============================================================================
# RSA ENCRYPTION/DECRYPTION
# ============================================================================

def encrypt_number(message, public_key):
    """
    Зашифрувати число використовуючи публічний ключ

    Формула: ciphertext = (message^e) mod n
    """
    e, n = public_key
    if message >= n:
        raise ValueError(f"❌ Повідомлення ({message}) має бути менше n ({n})")

    ciphertext = pow(message, e, n)  # Ефективне модульне піднесення до степеня
    return ciphertext

def decrypt_number(ciphertext, private_key):
    """
    Розшифрувати число використовуючи приватний ключ

    Формула: message = (ciphertext^d) mod n
    """
    d, n = private_key
    message = pow(ciphertext, d, n)
    return message

def encrypt_text(text, public_key):
    """Зашифрувати текст (кожен символ окремо)"""
    e, n = public_key
    encrypted = []

    for char in text:
        char_code = ord(char)
        if char_code >= n:
            raise ValueError(f"❌ Символ '{char}' (код {char_code}) завеликий для n={n}")
        encrypted_num = encrypt_number(char_code, public_key)
        encrypted.append(encrypted_num)

    return encrypted

def decrypt_text(encrypted_list, private_key):
    """Розшифрувати текст"""
    decrypted_chars = []

    for encrypted_num in encrypted_list:
        char_code = decrypt_number(encrypted_num, private_key)
        decrypted_chars.append(chr(char_code))

    return ''.join(decrypted_chars)

# ============================================================================
# INTERACTIVE DEMO
# ============================================================================

def main():
    print("="*70)
    print("🎓 EDUCATIONAL RSA DEMONSTRATION")
    print("="*70)
    print("\n⚠️  Ці маленькі прості використовуються ТІЛЬКИ для навчання!")
    print("   У реальному RSA використовуються ВЕЛИЧЕЗНІ прості (2048+ біт)")

    # Показати доступні прості числа
    print("\n📋 Доступні прості числа (відповідають номерам в журналі):")
    print("-" * 70)
    for i in range(1, 41, 5):
        row = "   ".join([f"#{j}: {PRIMES[j]}" for j in range(i, min(i+5, 41))])
        print(f"   {row}")

    # Вибір простих чисел
    print("\n" + "="*70)
    print("🎲 ВИБІР ПРОСТИХ ЧИСЕЛ")
    print("="*70)

    choice = input("\nОберіть метод вибору:\n1. Ввести номер з журналу\n2. Випадковий вибір\nВаш вибір (1/2): ").strip()

    if choice == '1':
        # Вибір за номером студента
        student_num = int(input("\nВаш номер в журналі (1-40): "))
        if student_num not in PRIMES:
            print(f"❌ Невірний номер! Виберіть від 1 до 40")
            return

        p = PRIMES[student_num]

        # Для q використаємо сусідній номер або інший
        print(f"\nВаше перше просте число: p = {p}")
        q_num = int(input("Виберіть номер для другого простого (1-40, не однаковий з першим): "))
        if q_num == student_num or q_num not in PRIMES:
            print(f"❌ Невірний вибір!")
            return
        q = PRIMES[q_num]

        print(f"\n✅ Вибрано:")
        print(f"   Студент #{student_num}: p = {p}")
        print(f"   Студент #{q_num}: q = {q}")

    else:
        # Випадковий вибір
        nums = random.sample(list(PRIMES.keys()), 2)
        p = PRIMES[nums[0]]
        q = PRIMES[nums[1]]
        print(f"\n🎲 Випадково вибрано:")
        print(f"   #{nums[0]}: p = {p}")
        print(f"   #{nums[1]}: q = {q}")

    # Генерувати ключі
    keys = generate_rsa_keys(p, q, verbose=True)

    # Демонстрація шифрування числа
    print("\n" + "="*70)
    print("🔐 DEMONSTRATION: Encrypting a Number")
    print("="*70)

    message_num = 42
    print(f"\n📝 Original message (number): {message_num}")

    encrypted_num = encrypt_number(message_num, keys['public_key'])
    print(f"\n🔒 Encryption:")
    print(f"   Formula: C = M^e mod n")
    print(f"   C = {message_num}^{keys['public_key'][0]} mod {keys['public_key'][1]}")
    print(f"   C = {encrypted_num}")

    decrypted_num = decrypt_number(encrypted_num, keys['private_key'])
    print(f"\n🔓 Decryption:")
    print(f"   Formula: M = C^d mod n")
    print(f"   M = {encrypted_num}^{keys['private_key'][0]} mod {keys['private_key'][1]}")
    print(f"   M = {decrypted_num}")

    if message_num == decrypted_num:
        print(f"\n✅ Success! Original = Decrypted = {message_num}")

    # Демонстрація шифрування тексту
    print("\n" + "="*70)
    print("🔐 DEMONSTRATION: Encrypting Text")
    print("="*70)

    message_text = input("\n📝 Введіть коротке повідомлення для шифрування: ").strip()
    if not message_text:
        message_text = "HI"

    print(f"\n📝 Original message: '{message_text}'")

    # Показати коди символів
    print(f"\n🔢 Character codes:")
    for char in message_text:
        print(f"   '{char}' → {ord(char)}")

    # Зашифрувати
    encrypted_text = encrypt_text(message_text, keys['public_key'])
    print(f"\n🔒 Encrypted (list of numbers):")
    print(f"   {encrypted_text}")

    # Розшифрувати
    decrypted_text = decrypt_text(encrypted_text, keys['private_key'])
    print(f"\n🔓 Decrypted: '{decrypted_text}'")

    if message_text == decrypted_text:
        print(f"\n✅ Success! Message encrypted and decrypted correctly!")

    # Показати обмеження
    print("\n" + "="*70)
    print("⚠️  SECURITY WARNING - Why Small Primes Are INSECURE")
    print("="*70)

    n = keys['public_key'][1]
    print(f"\nВаше n = {n}")
    print(f"Це число можна швидко розкласти на множники!")
    print(f"\n🔍 Factorization attack:")
    print(f"   n = {n}")
    print(f"   Хакер перебирає дільники...")

    # Просто показати що можна швидко знайти p та q
    import time
    start = time.time()
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            found_p = i
            found_q = n // i
            break
    elapsed = time.time() - start

    print(f"   ⚡ Знайдено за {elapsed*1000:.2f} мілісекунд!")
    print(f"   p = {found_p}")
    print(f"   q = {found_q}")
    print(f"\n💡 Тепер хакер може обчислити φ(n) та знайти d!")

    print(f"\n🔒 REAL RSA uses:")
    print(f"   - Primes with 1024+ bits (309+ digits)")
    print(f"   - n with 2048+ bits (617+ digits)")
    print(f"   - Factorization would take millions of years!")

    print("\n" + "="*70)
    print("✅ COMPLETED!")
    print("="*70)

if __name__ == "__main__":
    main()