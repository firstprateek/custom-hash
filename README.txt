INTRODUCTION
------------
 hashing.cpp:

 It contains the C++ code for the encrpytion algorithm. It takes a file path as a command line argument
 and outputs a hexadecimal digest, followed by two spaces, followed by the file path. It aslo writes to
 a file called "output.txt".

 analyser.py:

 It contains python code for analysing a stream of digests created by the previous script.


REQUIREMENTS
------------
 * matplotlib


INSTRUCTIONS
------------
 * Clone the repo https://github.umn.edu/pahp/hashme.git
 * Compile hashing.cpp with the following command: g++ --std=c++11 -o myhash hashing.cpp
 * Run this script to generate orig file: for I in $(seq 1 1000); do ./myhash ./hashme/orig/$I >> hashes.orig; done
 * Run this script to generate the alt file: rm hashes.alt; for I in $(seq 1 1000); do ./myhash ./hashme/orig/$I >> hashes.alt; ./myhash ./hashme/mod/$I >> hashes.alt; done
 * Run the python code via the following cmd to analyse hashes.orig and hashes.alt: python analyser.py ./hashes.orig ./hashes.alt
 
TROUBLESHOOTING
---------------
 * If the shell script throws errors please recheck if the hashme directory is cloned in the same directory as your hashing and analyser file.
