# while True:
#     print("1. Addition")
#     print("2. Subtraction")
#     print("3. Multiplication")
#     print("4. Division")
#     print("5. Exit")

#     choice = int(input("Enter choice: "))

#     #     if choice == 5:
#     #         print("Thank you!")
#     #         break

#     a = int(input("Enter the number: "))
#     b = int(input("Enter a number: "))

    #     if choice == 1:
    #         print("Result:", a + b)

    #     elif choice == 2:
    #         print("Result:", a - b)

    #     elif choice == 3:
    #         print("Result:", a * b)

    #     elif choice == 4:
    #         print("Result:", a / b)

    #     else:
    #         print("Invalid Choice")

    # except ValueError:
    #     print("Enter numbers only")

    # except ZeroDivisionError:
    #     print("Cannot divide by zero")
    
# try:
#     num=int(input("Enter number:"))
#     if num<0:
#         raise Exception("Negative not allowed")
# except Exception as e:
#     print("error:",e)
# finally:
#     print("completed")
        
try:
    name=input("Enter name:")
    password=input("Enter password:")
    attempt=int(input("Enter Attempts:"))

    if name=='':
        raise Exception("Not be empty")
   
    a=len(password)
    print(a)
    if a<8:
        raise ValueError("Enter max characters")
    if attempt<0:
        raise ValueError("Attempts cannot be negative")
    print("Login data successful")

except ValueError as e:
    print("ValueError:", e)

except Exception as e:
    print("Error:", e)

else:
    print("Login data accepted")

finally:
    print("Validation completed")


    
