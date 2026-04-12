def encrypt_text(text, shift1, shift2):
    encrypted = ""
    rules = ""  # stores which rule was used per character

    for char in text:
        if char.islower():
            if 'a' <= char <= 'm':
                shift = shift1 * shift2
                new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                rules += "1"
            else:
                shift = shift1 + shift2
                new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                rules += "2"

        elif char.isupper():
            if 'A' <= char <= 'M':
                shift = shift1
                new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                rules += "1"
            else:
                shift = shift2 ** 2
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                rules += "2"

        else:
            new_char = char
            rules += "0"

        encrypted += new_char

    return encrypted, rules


def decrypt_text(encrypted, rules, shift1, shift2):
    result = ""

    for i in range(len(encrypted)):
        char = encrypted[i]
        rule = rules[i]

        if rule == "1":
            if char.islower():
                shift = shift1 * shift2
                new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            elif char.isupper():
                shift = shift1
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                new_char = char

        elif rule == "2":
            if char.islower():
                shift = shift1 + shift2
                new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            elif char.isupper():
                shift = shift2 ** 2
                new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                new_char = char

        else:
            new_char = char

        result += new_char

    return result


def verify_files(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f1, \
         open(file2, 'r', encoding='utf-8') as f2:

        content1 = f1.read()
        content2 = f2.read()

        if content1 == content2:
            print(" Decryption successful: Files match.")
        else:
            print(" Decryption failed: Files do not match.")

            for i in range(min(len(content1), len(content2))):
                if content1[i] != content2[i]:
                    print(f"Mismatch at position {i}")
                    print(f"Raw char: {repr(content1[i])}")
                    print(f"Decrypted char: {repr(content2[i])}")
                    break


def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    with open("raw_text.txt", "r", encoding='utf-8') as file:
        raw_text = file.read()

    # Encrypt
    encrypted, rules = encrypt_text(raw_text, shift1, shift2)

    with open("encrypted_text.txt", "w", encoding='utf-8') as f:
        f.write(encrypted)

    with open("rules.txt", "w", encoding='utf-8') as f:
        f.write(rules)

    # Decrypt
    with open("encrypted_text.txt", "r", encoding='utf-8') as f:
        encrypted = f.read()

    with open("rules.txt", "r", encoding='utf-8') as f:
        rules = f.read()

    decrypted = decrypt_text(encrypted, rules, shift1, shift2)

    with open("decrypted_text.txt", "w", encoding='utf-8') as f:
        f.write(decrypted)

    # Verify
    verify_files("raw_text.txt", "decrypted_text.txt")


if __name__ == "__main__":
    main()