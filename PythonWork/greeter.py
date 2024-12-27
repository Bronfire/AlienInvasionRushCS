print("hello");

def get_user_names():
    while True:
        first_name = input("Enter your first name (or 'q' to quit): ").strip()
        if first_name.lower() == 'q':
            print("Exiting program. Goodbye!")
            break

        last_name = input("Enter your last name (or 'q' to quit): ").strip()
        if last_name.lower() == 'q':
            print("Exiting program. Goodbye!")
            break

        print(f"Hello, {first_name} {last_name}!")
        
formatted_name = get_user_names();

n = 1
while True: 

    print(n)
    n += 1
    if n == 5:
        break

    

        
print("end of program")