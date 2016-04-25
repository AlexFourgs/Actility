#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

# Simple program for test class.

class Book:
    title=''
    pages=0

    # Initialisation function = Constructor in java.
    def __init__(self, title='', pages=0):
        self.title=title
        self.pages=pages

    # Like a toString in Java.
    def __str__(self):
        return self.title

    # Methods for addition operation between same type of object (Book)
    def __radd__(self, other):
        return self.pages + other

    def __add__(self, other):
        return self.pages + other


    # Overwrite comparative operations.

    def __lt__(self, other):
        return self.pages < other

    def __eq__(self, other):
        return self.pages == other

    def __ne__(self, other):
        return self.pages != other

    def __gt__(self, other):
        return self.pages > other

    # Overwrite comparative or equal operations.

    def __ge__(self, other):
        if isinstance(other, Book): # Verifying that "other" is an object of type "Book"
            return self.pages >= other.pages
        elif isinstance(other, (int, float)): # Verifying that "other" is an int or a float
            return self.pages >= other
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, Book):
            return self.pages <= other.pages
        elif isinstance(other, (int, float)):
            return self.pages <= other
        else:
            return NotImplemented


# Tests

book1 = Book("Harry Potter", 589)
book2 = Book("Game Of Thrones", 697)
book3 = Book("Learn Python", 724)

addition = book1 + book2

print(addition) # Work !

comparaison1 = book1 < book2

if comparaison1 == True:
    print("\"%s\" has less pages than \"%s" %(book1.title, book2.title))
else:
    print("\"%s\" has more pages than \"%s\"" %(book1.title, book2.title))


comparaison2 = book2 != book3

if comparaison2 == True:
    print("\"%s\" doesn't have the same number of pages than \"%s\"" %(book2.title, book3.title))
else:
    print("\"%s\" has the same number of pages than \"%s\"" %(book2.title, book3.title))
