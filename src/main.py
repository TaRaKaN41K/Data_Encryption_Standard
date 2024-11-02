from DES import DES

if __name__ == '__main__':

    input_string = "KFO N34481"
    key = "DESkey56"

    # Преобразуем строки в битовый массив (строку битов)
    bit_string = ''.join(format(byte, '08b') for byte in input_string.encode('utf-8'))
    key_bit_string = ''.join(format(byte, '08b') for byte in key.encode('utf-8'))

    DES = DES()

    # Шифруем сообщение
    encrypted_string = DES.encrypt_decrypt(
        bit_string=bit_string,
        key_bit_string=key_bit_string,
        is_encrypted=True
    )

    ascii_encrypted_string = ''.join(chr(int(encrypted_string[i:i + 8], 2)) for i in range(0, len(encrypted_string), 8) if int(encrypted_string[i:i + 8], 2) != 0)

    # Дешифруем сообщение
    decrypted_string = DES.encrypt_decrypt(
        bit_string=encrypted_string,
        key_bit_string=key_bit_string,
        is_decrypted=True
    )

    ascii_decrypted_string = ''.join(chr(int(decrypted_string[i:i + 8], 2)) for i in range(0, len(decrypted_string), 8) if int(decrypted_string[i:i + 8], 2) != 0)

    print(f'Входная строка ASCII:         {input_string}')
    print(f'Зашифрованная строка ASCII:   {ascii_encrypted_string}')
    print(f'Дешифрованная строка ASCII:   {ascii_decrypted_string}')
    print(f'Входная строка в битах:       {bit_string}')
    print(f'Зашифрованная строка в битах: {encrypted_string}')
    print(f'Дешифрованная строка в битах: {decrypted_string}')
