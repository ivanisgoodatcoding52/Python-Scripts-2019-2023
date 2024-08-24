def calculator():
    numbers = []
    
    while True:
        user_input = input("Enter a number (type 'stop' to calculate): ")
        
        if user_input.lower() == 'stop':
            break
        
        try:
            number = float(user_input)
            numbers.append(number)
        except ValueError:
            print("Invalid input. Please enter a valid number or 'stop' to calculate.")
    
    return numbers

def main():
    print("Welcome to the 'Taxer!")
    print("Enter numbers, and I will add them up and tax them for you.")
    numbers = calculator()
    total = sum(numbers)
    z = input("Do you want to add a discount? Press y if yes, Press x if no.")
    if z == 'x':
        pass
    elif z == 'y':
        b = float(input("Enter a WHOLE NUMBER (like 1, 2, 3. NO DECIMALS OR FRACTIONS OR NEGITIVES!): "))
        a = (b/100)
        
    x = input("Do you want to tax or not? Press y if yes, press n for no.")
    if x == 'n':
        print(f"\nResult: The sum of the prices without tax is {total}")
    if x == 'y' and z != 'y':
        y = total + (total * 0.1175)
        e = round(y, 2)
        print(f"\nResult: The sum of the prices plus tax is {e}")
    elif z == 'y' and x == 'y':
        y = total + (total * 0.1175)
        g = y - (y * a)
        e = round(y, 2)
        print(f"\nResult: The sum of the prices plus tax with a discount is {e}")
    

if __name__ == "__main__":
    main()
