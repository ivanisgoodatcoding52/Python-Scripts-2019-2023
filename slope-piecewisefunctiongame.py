import matplotlib.pyplot as plt
import numpy as np
import random

def generate_random_piecewise_function():
    x1_start, x1_end = random.uniform(-10, 0), random.uniform(0, 10)
    x2_start, x2_end = random.uniform(-10, 0), random.uniform(0, 10)
    
    return lambda x: x + 10 if x1_start <= x <= x1_end else abs(x) if x2_start <= x <= x2_end else -x + 10

def plot_piecewise_function(piecewise_function):
    x = np.linspace(-10, 10, 100)
    y = [piecewise_function(xi) for xi in x]
    plt.plot(x, y, label='Random Piecewise Function')

def main():
    print("Welcome to the Guess the Piecewise Function Game!")
    print("You will see a graph of a random piecewise function. Try to guess the function based on the graph.")
    print("The possible functions are 'x + 10' or '|x|'. Enter your guess in the console.")

    # Generate a random piecewise function
    random_piecewise_function = generate_random_piecewise_function()
    
    # Plot the random piecewise function
    plot_piecewise_function(random_piecewise_function)
    
    # Customize the plot
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    
    plt.legend()
    plt.title('Guess the Piecewise Function')
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')

    # Show the plot
    plt.show()

    # Ask the user to guess the piecewise function
    user_guess = input("Try to guess the piecewise function (e.g., 'x + 10' or '|x|'): ")

    # Check the user's guess
    correct = user_guess.strip().lower() == 'x + 10' or user_guess.strip().lower() == '|x|'

    if correct:
        print("Congratulations! Your guess is correct.")
    else:
        print(f"Sorry, your guess is incorrect. The correct function is: {random_piecewise_function.__name__}")

if __name__ == "__main__":
    main()
