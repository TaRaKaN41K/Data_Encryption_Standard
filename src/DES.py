from constants.tables import *
from constants.sizes import *
from helpers import *


class DES:
    def encrypt_decrypt(self, bit_string: str, key_bit_string: str, is_encrypted: bool = False, is_decrypted: bool = False) -> str:

        if (is_encrypted and is_decrypted) or (not is_encrypted and not is_decrypted):
            raise ValueError("One of the parameters is_encrypted and is_decrypted must be True and the other False.")

        keys48b = self.key_expansion_to_48bits(key_bit_string=key_bit_string)

        # Разбиваем битовую строку на блоки по 64 бита и дополняем '0'
        blocks64b: List = block_division(bit_string, BLOCK_SIZE_64)
        blocks64b_encrypt: List = []

        for block in blocks64b:
            # Начальная перестановка. Применяем перестановку IP к блоку.
            block64b = permutation(block=block, block_size=BLOCK_SIZE_64, permutation_table=IP)

            # Разделяем строку на блоки по 32 бита.
            blocks32b = block_division(block=block64b, block_size=BLOCK_SIZE_32)

            left_block32b, right_block32b = self.feistel_cipher(
                left_block=blocks32b[0],
                right_block=blocks32b[1],
                keys48b=keys48b,
                is_encrypted=is_encrypted,
                is_decrypted=is_decrypted
            )

            block64b = left_block32b + right_block32b

            blocks64b_encrypt.append(permutation(block=block64b, block_size=BLOCK_SIZE_64, permutation_table=IP_INV))

        result_string = ''.join(blocks64b_encrypt)

        return result_string

    @staticmethod
    def key_expansion_to_48bits(key_bit_string: str) -> List[str]:
        """Расширение ключа до 48 бит."""

        # Разбиваем ключ на 28 битовые блоки
        left_key_block28b: str = permutation(block=key_bit_string, block_size=BLOCK_SIZE_64, permutation_table=PC_1_L)
        right_key_block28b: str = permutation(block=key_bit_string, block_size=BLOCK_SIZE_64, permutation_table=PC_1_R)

        key_blocks48b: List[str] = []

        # Шаги расширения
        for i in range(16):
            # Вычисляем сдвиг
            n = 1 if i in {0, 1, 8, 15} else 2

            # Производим циклический сдвиг на n бит.
            left_key_block28b = lshift_28bit(block=left_key_block28b, shift=n)
            right_key_block28b = lshift_28bit(block=right_key_block28b, shift=n)

            key_block56b = left_key_block28b + right_key_block28b

            # Получаем 48 битовую ключевую последовательность
            key_blocks48b.append(permutation(block=key_block56b, block_size=BLOCK_SIZE_56, permutation_table=PC_2))

        return key_blocks48b

    def feistel_cipher(
            self,
            left_block: str,
            right_block: str,
            keys48b: List,
            is_encrypted: bool,
            is_decrypted: bool,
    ) -> [str, str]:

        if is_encrypted:
            for round in range(16):
                left_block, right_block = self.round_feistel_cipher(left_block=left_block, right_block=right_block,
                                                               key48b=keys48b[round])

            left_block, right_block = right_block, left_block

        elif is_decrypted:
            for round in range(15, -1, -1):
                left_block, right_block = self. round_feistel_cipher(left_block=left_block, right_block=right_block,
                                                               key48b=keys48b[round])
            left_block, right_block = right_block, left_block

        return left_block, right_block

    def round_feistel_cipher(self, left_block: str, right_block: str, key48b: str) -> [str, str]:
        """Один раунд"""

        # Правый блок становится левым
        new_left_block = right_block

        # Левый блок XOR с f() от правого блока и ключа 48 бит и становится правым блоком
        new_right_block = bitwise_xor_strings(self.f(block=right_block, key48b=key48b), left_block)

        return new_left_block, new_right_block

    def f(self, block: str, key48b: str) -> str:
        """Применяет F-функцию к блоку."""

        # Дополняем блок до 48 бит нулями ('0').
        block48b = block.ljust(BLOCK_SIZE_48, '0')

        # Увеличиваем 32-битный блок до 48 битов при помощи E.
        block48b = permutation(block=block48b, block_size=BLOCK_SIZE_48, permutation_table=E)

        # XOR block48b и key48b
        block48b = bitwise_xor_strings(block48b, key48b)

        # Получаем 8 блоков по 6 бит
        blocks4b = self.substitutions(block48b)

        # Соединяем blocks4b в block32b
        united_blocks4b = ''.join(blocks4b)

        block32b = permutation(block=united_blocks4b, block_size=BLOCK_SIZE_32, permutation_table=P)

        return block32b

    def substitutions(self, block48b: str) -> List[str]:
        """Применяет S-блоки к блоку."""

        # Делим block48b на 8 blocks6b
        blocks6b = block_division(block=block48b, block_size=BLOCK_SIZE_6)

        blocks4b: List[str] = []

        # Применяем S-блоки к каждому из 8 blocks6b
        for block_index in range(len(blocks6b)):
            block = blocks6b[block_index]  # Для удобства

            # 2 крайних
            block2b = block[0] + block[5]

            # 4 средних
            block4b = block[1] + block[2] + block[3] + block[4]

            # Берём двоичное представление числа из SBOX
            blocks4b.append(f"{SBOX[block_index][int(block2b, 2)][int(block4b, 2)]:04b}")

        return blocks4b
