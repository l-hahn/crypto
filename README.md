# crypto

Implementation of different crypto systems; bases on Introduction to Cryptography with Open-Source Software by Alasdair McAndrew.

Visited successfully the cryptography lecture and now experimenting a bit with AES in C++ and python.

This short script/library is an approach to understand and implement the AES-128 en-/decryption not only to bit-lists, but also to typical files on your system.
At the moment, files can be en-/decrypted using only the 'electronic-code-book' mode (ECB), with a low security level in python.
Files of each type can be read, since files are opened binary.

Future aspects/goals:
  -more modes, like CBC etc.
  -additional to files, take whole folders/paths for en-/decryption
  -speed up the python script (xx-08-2017: ~10KB/