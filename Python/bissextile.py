#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

# Programme simple en python qui est capable de dire si l'année entrée par l'utilisateur est bissextile ou non.

# On demande à l'utilisateur une année
annee = input("Saisissez une année : ")

# On convertis en int
annee = int(annee)

multiple_de_4 = annee%4

if multiple_de_4 == 0:
    multiple_de_100 = annee%100

    if multiple_de_100 == 0:
        multiple_de_400 = annee%400

        if multiple_de_400 == 0:
            print("C'est une année bissextile")
        else:
            print("Ce n'est pas une année bissextile")
    else:
            print("C'est une année bissextile")
else:
    print("Ce n'est pas une année bissextile.")
