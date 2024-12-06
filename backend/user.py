import random

LARGEINT = 2**16

class User:
    idList = []
    rating = 0
    def __init__(self, firstName, lastName, email):
        r = random.randint(0, LARGEINT)
        while (r in User.idList):
            r = random.randint(0, LARGEINT)
        self.id = r
        User.idList.append(self.id)
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

    def rateUser(self, rating):
        self.rating += rating

    def setGroup(self, groupID):
        self.groupID
    


# #Tests
# u1 = User("John", "Doe", "mail@mail.com")

# print(u1.id)
# print(u1.firstName)
# print(u1.lastName)
# print(u1.email)
# print(u1.idList)
# u1.rateUser(1)
# print(u1.rating)

# u2 = User("Jane", "Smith", "mail@mail.com")

# print(u2.id)
# print(u2.firstName)
# print(u2.lastName)
# print(u2.email)
# print(u2.idList)
# print(u2.rating)