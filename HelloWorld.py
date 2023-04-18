# HelloWorldPygame.py

# def PrintHelloWorldTenTimes():
#    for num in range(1, 11):
#        print(f'Hello World #{num}')
    
# PrintHelloWorldTenTimes()
# for number in range(5):
#     print ('Hello World')

# for number in range(5):
#     numberToPrint = number + 1
#     if (numberToPrint) % 2 == 0:
#        print (f'Even Hello World #{numberToPrint}')
#     else:
#        print (f'Odd Hello World #{numberToPrint}')

# while True:
#   print('Hello World')
#   break

# number = 1
# while number <= 5:
#     print (f'Hello World #{number}')
#     number = number + 1

# numbers = [1, 2, 3, 4, 5]
# for number in numbers:
#     print (f'Hello World #{number}')

# class Person:
#   def __init__(self, name, age, gender):
#     self.name = name
#     self.age = age
#     self.gender = gender

#   def introduce(self):
#     print("Hello, my name is " + self.name)

# tim = Person("Tim", 28, "Male")
# tim.introduce() 

# mary = Person("Mary", 30, "Female")
# mary.introduce() 

# for number in range(5):
#     numberToPrint = number + 1
#     if numberToPrint % 3 == 0:
#        print (f'{numberToPrint} is divisible by 3')
#     elif numberToPrint % 2 == 0:
#        print (f'{numberToPrint} is even')
#     else:
#        print (f'{numberToPrint} Not even and not divisible by 3')


# letters = ['a', 'b', 'e']
# print('starting letters: ',letters)  
# letters.append('c')   
# print('append c: ',letters) 
# letters.insert(2, 'd')  
# print('insert d at position 2: ', letters) 
# letters.remove('a')  
# print('remove a: ',letters) 

# my_list = [[1,2,3,4], [5,6,7,8], [9,10,11,12]]

# value = my_list[2][3]
# print(value)

my_dict = {
    'key1': 'value1',
    'key2': 'value2',
    'key3': 'value3'
}

# value = my_dict.get('key4', 'default_value')
# print(value)

# for key in my_dict:
#     print(key)

# for value in my_dict.values():
#     print(value)

for key, value in my_dict.items():
    print(key, value)