# Andrew Cotaj
# acotaj
# 26 February 2025
# HWK2

import DESTables

def left_shift(amount, key):
    # Perform a left circular shift by 'amount' positions on 'key'
    return key[amount:] + key[:amount]

def permute(key_combined):
    # Permute 'key_combined' using the permutation table 'pc2' from DESTables
    return ''.join([key_combined[i-1] for i in DESTables.pc2])

def keygen(key):
    # Apply the initial permutation 'pc1' from DESTables to the key
    permuted_key = ''.join([key[i-1] for i in DESTables.pc1])

    # Split the permuted key into left and right halves, C0 and D0
    half_length = len(permuted_key) // 2
    left_half = permuted_key[:half_length]
    right_half = permuted_key[half_length:]

    # Initialize the list of iterations with the initial halves
    iterations = [[left_half, right_half]]
    subkeys = []

    # Generate 16 subkeys
    for round_number in range(16):
        # Get the shift amount for the current round from DESTables
        shift_amount = DESTables.shift[round_number]
        previous_left, previous_right = iterations[-1]
        
        # Perform left circular shifts on both halves
        shifted_left = left_shift(shift_amount, previous_left)
        shifted_right = left_shift(shift_amount, previous_right)
        
        # Append the shifted halves to the iterations list
        iterations.append([shifted_left, shifted_right])
        
        # Combine the shifted halves and permute them to generate the subkey
        combined_key = permute(shifted_left + shifted_right)
        subkeys.append(combined_key)
        
        # Print the subkey for the current round
        print(f'K{round_number + 1:<2}: {combined_key}')

    # Return the list of generated subkeys
    return subkeys