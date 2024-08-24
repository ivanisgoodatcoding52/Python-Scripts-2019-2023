import os

while True:
    # Get user input
    command = input("Enter Command: ")

    # Exit the shell
    if command.lower() == 'exit':
        break

    # Execute the command
    try:
        result = os.system(command)
        print("Exit code:", result)
    except Exception as e:
        print("Error:", e)
