def take_input_from_options(options):
    while True:
        print("Choose one of the following options:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        choice = input("Enter your choice (1-" + str(len(options)) + "): ")

        # Check if input is a valid integer
        if not choice.isdigit():
            print("Invalid input. Please enter a number.")
            continue

        choice = int(choice)

        # Check if input is within the range of options
        if choice < 1 or choice > len(options):
            print("Invalid choice. Please enter a number between 1 and", len(options))
            continue

        return options[choice - 1]

def main():
    # Example usage:
    options = ["Option 1", "Option 2", "Option 3"]
    chosen_option = take_input_from_options(options)
    print("You chose:", chosen_option)

import subprocess

def run_script(script_file, file_type='csh'):
    try:
        subprocess.run(["csh", script_file], check=True)
        print("C shell script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing C shell script: {e}")

def script_run():
    # Example usage:
    csh_script_file = "example_script.csh"
    run_script(csh_script_file)


if __name__ == '__main__':
    # main()
    # main()
    script_run()
