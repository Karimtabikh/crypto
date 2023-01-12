#Importing the SymPy library
from sympy import randprime

#Importing the greatest common divisor method from math
from math import gcd

#The following two functions will return a value of d when you pass it the parameters public-key exponent and totient.

#implementation of the extended Euclidean algorithm to find the GCD
#The function takes in two arguments, aa and bb, which are the two numbers for which we want to find the GCD
def extended_gcd(aa, bb):
    # The function first assigns the absolute values of aa and bb to lastremainder and remainder
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    # a while loop, where it continuously updates the values of lastremainder, remainder, x, lastx, y, and lasty until remainder is 0.
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    #returns the GCD , 
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

#We produce the private-key exponent by finding the modular inverse of the public-key exponent, using the totient as the modulus.
#This function is used to find the modular inverse of a number
# a and m, which represent the number and the modulus
#If the GCD is equal to 1, the function returns x mod m.
def modinv(a, m):
	g, x, y = extended_gcd(a, m)
	if g != 1:
		raise ValueError
	return x % m

#Try not to go for more than a 24 bit key because Python is too slow for larger numbers
print(" Please do not go for more than a 24 bit key because Python is too slow for larger numbers. ")
key_size = int(input(" Please enter the desired key size: "))
key_size_string = str(key_size)
print(" Thank You!!! You have chosen the desired key size to be of " + key_size_string + " bits.")

#Set the two prime numbers to 0 so that they are declared before the loop
prime1 = 0 
prime2 = 0

#The Loop will keep on generating prime numbers until both the following conditions are met.
#   1. Both the prime numbers are unique.
#   2. Their product is not larger than the key size (2^key_size)
while prime1 == prime2 or (prime1 * prime2) > 2**key_size:
    prime1 = randprime(3, 2**key_size/2)
    prime2 = randprime(3, 2**key_size/2)
    
#Display the two prime numbers
print("  1st Prime Number -----> " + str(prime1))
print("  2nd Prime Number -----> " + str(prime2))

#Calculate and display the RSA modulus r
RSA_modulus = prime1 * prime2
print("  RSA Modulus r -----> " + str(RSA_modulus))

#Calculate and display the Euler’s totient.
totient = (prime1 - 1)*(prime2 -1)
print("  Euler's totient -----> " + str(totient))

#Choosing the public-key exponent
public_exponent = 0

for e in range(3, totient-1):
  if gcd(e, totient) == 1:
    public_exponent = e
    break
    #Aim for the lowest possible value, thus saving computation time

#Display the public-key exponent e
print("  Public-Key exponent, e -----> " + str(e))

#Display the public key
print("  Public Key -----> (" + str(public_exponent) + ", " + str(RSA_modulus) + ")")

#Find the modular inverse of the public-key exponent and use as the private-key exponent
private_exponent = modinv(public_exponent, totient)

#Display the private-key exponent e
print("  Private-Key exponent, d -----> " + str(private_exponent))

#Display the private key
print("  Private Key -----> (" + str(private_exponent) + ", " + str(RSA_modulus) + ")")

#ENCRYPTION
#Plain text setup
print(" For the sake of simplicity, we are going to encrypt a single character. Please enter below a single character only. ")
plain_text = str(input(" Please enter the character that you would want to encrypt: "))

#Using ord to get ASCII encoding of the character entered
#chr is used to generate a character from an ASCII encoding
cipher_text = chr((ord(plain_text)**public_exponent) % RSA_modulus)

print("  Plain Text " + plain_text + " encrypted to " + cipher_text)

#DECRYPTION
message = chr((ord(cipher_text)**private_exponent) % RSA_modulus)

print("  Cipher Text " + cipher_text + " decrypted to " + message)
