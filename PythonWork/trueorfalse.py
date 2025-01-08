def truthy():
    print("it's true!")
    return True

def falsey():
    print("it's false!")
    return False

print ("true or false result: ")
truthy() or falsey()

print("\nfalse or true result: ")
falsey() or truthy()

print ("\ntrue and false result: ")
truthy() and falsey()

print("\nfalse and true result: ")
falsey() and truthy()

