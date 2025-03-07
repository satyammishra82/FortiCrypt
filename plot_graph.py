import matplotlib.pyplot as plt
import numpy as np
import sympy

def plot_aes_new_relationships():
    key_lengths = np.arange(128, 513, 64)  # Key lengths from 128 to 512 bits
    block_sizes = np.arange(128, 513, 64)  # Block sizes from 128 to 512 bits
    
    # Adjusting iteration counts to match key lengths
    iteration_counts = np.linspace(5, 20, len(key_lengths)).astype(int) # Now matches the key lengths

    # Safely generate prime sizes
    prime_sizes = []
    for k in key_lengths:
        try:
            lower_bound = max(2**(k//2 - 10), 2)  # Ensure a valid range
            upper_bound = 2**(k//2)
            
            # Make sure the range is valid for finding primes
            if lower_bound >= upper_bound:
                prime_sizes.append(0)  # Fallback value when range is invalid
                print(f"Skipping key length {k}: invalid prime range.")
                continue
            
            prime_number = sympy.randprime(lower_bound, upper_bound)
            if prime_number:
                prime_sizes.append(prime_number.bit_length())
            else:
                prime_sizes.append(0)  # Fallback when no prime is found
                print(f"No prime found for key length {k}.")

        except ValueError as e:
            # Handle error, log details, and append a default prime size
            prime_sizes.append(0)
            print(f"Error for key length {k}: {str(e)}")

    # Plotting the relationships
    fig, ax = plt.subplots(2, 2, figsize=(10, 10))

    ax[0, 0].plot(key_lengths, block_sizes, marker='o', color='blue')
    ax[0, 0].set_title('Key Length vs Block Size')
    ax[0, 0].set_xlabel('Key Length (bits)')
    ax[0, 0].set_ylabel('Block Size (bits)')

    ax[0, 1].plot(key_lengths, iteration_counts, marker='s', color='green')
    ax[0, 1].set_title('Key Length vs Iteration Count')
    ax[0, 1].set_xlabel('Key Length (bits)')
    ax[0, 1].set_ylabel('Iteration Count')

    ax[1, 0].plot(key_lengths, prime_sizes, marker='^', color='red')
    ax[1, 0].set_title('Key Length vs Prime Number Size')
    ax[1, 0].set_xlabel('Key Length (bits)')
    ax[1, 0].set_ylabel('Prime Number Size (bits)')

    ax[1, 1].plot(block_sizes, iteration_counts, marker='d', color='purple')
    ax[1, 1].set_title('Block Size vs Iteration Count')
    ax[1, 1].set_xlabel('Block Size (bits)')
    ax[1, 1].set_ylabel('Iteration Count')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_aes_new_relationships()
