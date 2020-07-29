def main():
    print("Hello world!")
    variableValue = 10
    print("Starting the loop.")
    if(variableValue < 5):
        print("Level 1.0 of loop.")
        print("Level 1.1 of loop.")
        print("Level 1.2 of loop.")
        print("Level 1.3 of loop.")
        if(variableValue > 10):
            print("Level 1.3-1 of loop.")
            print("Level 1.3-2 of loop.")
            print("Level 1.3-3 of loop.")
        print("Level 1.4 of loop.")
        print("Level 1.5 of loop.")
        print("Level 1.6 of loop.")
    elif(variableValue < 10):
        print("Level 2.0 of loop.")
        print("Level 2.1 of loop.")
    print("Goodbye.")
main()
