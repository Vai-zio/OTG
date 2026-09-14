import math
# Functions with one argument (binary_sequence)
def bin2dec(binary_sequence):
    d = 0
    i = 0
    
    for bit in binary_sequence[::-1]:
        b = int(bit) # "1" but need 1
        a = 2**i
        c = b * a
        i += 1
        d += c
    return d


def dec2bin(decimal_sequence):
    d = 0
    i = 0
    a = 2**i
    nbit = math.log2(int(decimal_sequence))
    for i in range(nbit):
        a
    d = bin(decimal_sequence)
    return d

def dec2bin2(decimal_sequence):
    nbit = math.log2(int(decimal_sequence))
    if decimal_sequence <= a:
        decimal_sequence -= a
        d += a
    else:
        i += 1 

def bin_add(bs1,bs2):
    #Error if len(bs1) != len(bs2)
    nbits = len(str(bs1))+1
    res = [0]*nbits
    for i in range(nbits):
        bit1 = bs1[i]
        bit2 = bs2[i]
        mender = 0
        if bit1 == 1 and bit2 == 1:
            if mender == 1:
                res[i] = 1
                mender = 1
            elif mender == 0:
                res[i] = 0
                mender = 1
            print(f"State 1, bit1{bit1[i]} bit2{bit2[i]} {res[i]}")

        elif bit1 == 0 and bit2 == 1:
            if mender == 1:
                res[i] = 0
                mender = 1
            elif mender == 0:
                res[i] = 1
            print(f"State 2, bit1{bit1[i]} bit2{bit2[i]} {res[i]}")

        elif bit1 == 1 and bit2 == 0:
            if mender == 1:
                res[i] = 0
                mender = 1
            elif mender == 0:
                res[i] = 1
            print(f"State 3, bit1{bit1[i]} bit2{bit2[i]} {res[i]}")

        elif bit1 == 0 and bit2 == 0:
            if mender == 1:
                res[i] = 1
                mender = 0
            elif mender == 0:
                res[i] = 0
            print(f"State 4, bit1{bit1[i]} bit2{bit2[i]} {res[i]}")

        return res

def bin_sub(bs1,bs2):
    pass

def bin_add2(bs1: str, bs2: str) -> str:
    """
    Adds two binary numbers represented as strings and returns their sum as a string.
    
    :param bs1: Binary number as a string (e.g., "1011").
    :param bs2: Binary number as a string (e.g., "1101").
    :return: The sum of the binary numbers as a string.
    """
    # Ensure both strings are of equal length by padding with zeros
    max_len = max(len(str(bs1)), len(str(bs2)))
    bs1 = bs1.zfill(max_len)
    bs2 = bs2.zfill(max_len)
    
    carry = 0
    result = []
    
    # Perform bit-by-bit addition from the least significant bit
    for i in range(max_len - 1, -1, -1):
        bit1 = int(bs1[i])
        bit2 = int(bs2[i])
        
        # Binary addition logic
        total = bit1 + bit2 + carry
        result_bit = total % 2
        carry = total // 2
        
        # Prepend the result bit to the result list
        result.insert(0, str(result_bit))
    
    # If there is a carry left, prepend it to the result
    if carry:
        result.insert(0, str(carry))
    
    # Join the result list into a single string and return
    return ''.join(result)

# Example usage
bs1 = "1011"
bs2 = "1101"
print(bin_add(bs1, bs2))  # Output: "11000"
