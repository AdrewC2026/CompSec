# Andrew Cotaj
# acotaj
# 26 February 2025
# HWK2

# DES PROBLEM DECRYPTION/GENERATOR

from generate_keys import keygen
import DESTables

def xor(bitstring1, bitstring2):
    """Perform XOR operation between two bitstrings."""
    return ''.join(str(int(a) ^ int(b)) for a, b in zip(bitstring1, bitstring2))

def f(right_half, subkey):
    """The DES function that expands, XORs with the subkey, applies S-boxes, and permutes."""
    # Expansion permutation
    expanded_right = ''.join([right_half[i - 1] for i in DESTables.e])
    
    # XOR with the subkey
    xor_result = xor(expanded_right, subkey)
    
    # Split into 8 groups of 6 bits
    groups = [xor_result[i:i+6] for i in range(0, 48, 6)]
    sbox_result = ""

    # Apply S-boxes
    for num, group in enumerate(groups):
        first_bit = group[0]
        last_bit = group[-1]
        
        row = int(first_bit + last_bit, 2)
        col = int(group[1:-1], 2)

        sbox_value = DESTables.s[num + 1][row][col]
        sbox_result += bin(sbox_value)[2:].zfill(4)

    # Permutation
    return ''.join([sbox_result[i-1] for i in DESTables.p])

def main():
    encrypted_text = "1100101011101101101000100110010101011111101101110011100001110011"
    key = "0100110001001111010101100100010101000011010100110100111001000100"

    print('Keys:')
    subkeys = keygen(key)
    
    # Apply initial permutation to the encrypted text
    permuted_text = ''.join([encrypted_text[i-1] for i in DESTables.ip])

    # Split the permuted text into left and right halves
    half_length = len(permuted_text) // 2
    left_half = permuted_text[:half_length]
    right_half = permuted_text[half_length:]

    print()
    print('N: 1...16')
    for round_number in range(16):
        subkey = subkeys.pop()
       
        new_left_half = right_half
        
        f_result = f(right_half, subkey)
        new_right_half = xor(left_half, f_result)

        print(f'L{round_number+1}: {new_left_half}')
        print(f'R{round_number+1}: {new_right_half}')
        print('')

        left_half = new_left_half
        right_half = new_right_half

    # Combine the halves and apply the final permutation
    combined_halves = right_half + left_half
    final_permutation = ''.join([combined_halves[i-1] for i in DESTables.ip_1])
   
    print('Deciphered Text in Binary:')
    print(final_permutation)
    print()
    print('Deciphered Text in ASCII:')
    deciphered_text = ''.join(chr(int(final_permutation[i:i+8], 2)) for i in range(0, len(final_permutation), 8))
    print(deciphered_text)

if __name__ == '__main__':
    main()