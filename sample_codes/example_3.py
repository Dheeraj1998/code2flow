def main():
    print("Hello world!")
    variableValue = 10

    if(variableValue < 5):
        print("Level 1.0 of loop.")
        if(variableValue > 10):
            print("Level 1.0-1 of loop.")
            print("Level 1.0-2 of loop.")
            print("Level 1.0-3 of loop.")
        print("Level 1.1 of loop.")
        print("Level 1.2 of loop.")
    elif(variableValue < 10):
        print("Level 2.0 of loop.")
    else:
        print("Level 3.0 of loop.")
        print("Level 3.1 of loop.")
        print("Level 3.2 of loop.")
    print("Goodbye.")
main()
