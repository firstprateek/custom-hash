//
//  main.cpp
//  Hashing
//
//  Created by Prateek Joshi on 14/09/17.
//  Copyright © 2017 Prateek Joshi. All rights reserved.
//

#include <algorithm>
#include <cstdint>
#include <limits>
#include <climits>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <stdlib.h>
#include <sstream>
using namespace std;

uint32_t MASTER_ENCRYPTION   = 0;
uint32_t RANDOM_NUMBER_RANGE = numeric_limits<uint32_t>::max()/97387;
uint32_t SEED                = 55555555;

void encrypt(char* plain_text){
    uint32_t temp_master_encrption;
    uint32_t first = (uint32_t) plain_text[0], second = (uint32_t) plain_text[1],
             third = (uint32_t) plain_text[2], fourth = (uint32_t) plain_text[3];
    
    fourth <<= 12;
    third  <<=  8;
    second <<=  4;
    first  <<=  2;
    
    temp_master_encrption = (first * fourth + second * third) % 97387;
    
    srand(SEED);
    uint32_t multiplier = rand() % RANDOM_NUMBER_RANGE;
    
    temp_master_encrption *= multiplier;
    
    if (MASTER_ENCRYPTION != 0) MASTER_ENCRYPTION ^= temp_master_encrption;
    else MASTER_ENCRYPTION = temp_master_encrption;
    
    SEED = SEED + (rand() % SEED);
}

int handle_error(string message) {
    cout << message << endl;
    return -1;
}

// For Unix Filenames Only
struct MatchPathSeparator
{
    bool operator()( char ch ) const
    {
        return ch == '/';
    }
};

int write_output_to_file(string file_name, string input_file_path) {
    ofstream output_file (file_name, ios::app);
    
    if (!output_file.is_open()) return handle_error("Could not open output file.");
    
    stringstream stream;
    stream << hex << MASTER_ENCRYPTION;
    string output(stream.str());

    if (output.size() < 8){
        int times = 8 - output.size();

        while(times){
            output += '0';
            times--;
        }
    }
    
    // string input_file_name = string(find_if( input_file_path.rbegin(), input_file_path.rend(), MatchPathSeparator()).base(), input_file_path.end());
    string input_file_name = input_file_path;
    
    output_file << output << "  " << input_file_name << '\n';
    output_file.close();
    
    cout << output << "  " << input_file_name << endl;
    
    return 0;
}

int main(int argc, const char * argv[]){
    if      (argc < 2) return handle_error("Please give a file to encrypt.");
    else if (argc > 2) return handle_error("Incorrect number of arguments.");
    
    ifstream input_file (argv[1], input_file.binary);
    
    if (!input_file.is_open()) return handle_error("Could not open input file");
    
    char four_byte_array[4] = { '0', '0', '0', '0' };
    int  counter = 0;
    
    for (char buffer; input_file.read(&buffer, sizeof buffer);){
        four_byte_array[counter] = buffer;
        
        if (counter == 3) encrypt(four_byte_array);
        
        counter = (counter + 1) % 4;
    }
    
    if(counter != 0) encrypt(four_byte_array);
    
    input_file.close();
    
    return write_output_to_file("output.txt", argv[1]);
}

