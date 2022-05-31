#include <iostream>
#include <vector>
#include <string>

#include "aes.hpp"

int main(){
    std::vector<unsigned> Key = {0x1a,0x58,0x2a,0x1b,0xa1,0x0e,0xa0,0x18,0xf1,0x4a,0xc3,0x11,0xaa,0x2a,0xc1,0xff};
    aes CryptoSystem(Key);

    std::vector< std::vector<unsigned char> > AES_Key = CryptoSystem.key();
    for(auto RoundKey : AES_Key){
        for(auto Value: RoundKey){
            std::cout << (char)(Value+'A') << ' ';
        }
        std::cout << std::endl;
    }

    AES_Key = CryptoSystem.key_inverse();
    for(auto RoundKey : AES_Key){
        for(auto Value: RoundKey){
            std::cout << (char)(Value+'A') << ' ';
        }
        std::cout << std::endl;
    }
}