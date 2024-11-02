from typing import List


def block_division(block: str, block_size: int):
    """Разбивает битовую строку на блоки по block_size бит."""

    # Разбиваем битовую строку на блоки по block_size бит
    blocks: List = [block[i:i + block_size] for i in range(0, len(block), block_size)]

    # Дополняем строку '0' до block_size бит
    blocksNb: List = [block.ljust(block_size, '0') for block in blocks]

    return blocksNb


def permutation(block: str, block_size: int, permutation_table: List) -> str:
    """Применяет перестановку к блоку."""

    # Проверяем, что блок имеет длину block_size бит
    if len(block) != block_size:
        raise ValueError(f"The input block must be {block_size} bits long.")

    # Применяем перестановку по permutation_table
    permuted_block = ''.join(block[i - 1] for i in permutation_table)

    return permuted_block


def lshift_28bit(block: str, shift: int) -> str:
    """Выполняем циклический сдвиг влево на shift позиций"""

    # Преобразуем блок из двоичного представления в число
    block_int = int(block, 2)

    # Выполняем циклический сдвиг влево на shift позиций
    block_int = ((block_int << shift) | (block_int >> (-shift & 27))) & ((1 << 28) - 1)

    block = format(block_int, f'0{len(block)}b')

    return block


def bitwise_xor_strings(bin_str1: str, bin_str2: str) -> str:
    # Преобразуем строки битов в целые числа
    int1 = int(bin_str1, 2)
    int2 = int(bin_str2, 2)

    # Выполняем побитовое XOR
    xor_result = int1 ^ int2

    # Преобразуем обратно в строку, используя длину исходных строк для сохранения ведущих нулей
    result_str = f"{xor_result:0{len(bin_str1)}b}"
    return result_str