#ifndef AES_HPP_
#define AES_HPP_

#include <algorithm>
#include <iterator>
#include <vector>
#include <string>

#include "aesbase.hpp"

class aes{
	public:
        aes(std::string && KeyWord);
        aes(std::string & KeyWord);
        aes(std::vector<unsigned> && KeyWord);
        aes(std::vector<unsigned> & KeyWord);
		aes(std::vector<unsigned char> && KeyWord);
        aes(std::vector<unsigned char> & KeyWord);

        std::vector< std::vector<unsigned char> > key();
        std::vector< std::vector<unsigned char> > key_inverse();
        void set_key(std::vector<unsigned char> && KeyWord);
        void set_key(std::vector<unsigned char> & KeyWord);
        bool Init;
        unsigned value();

    private:
        void _adjust_key_length(std::vector<unsigned char> & KeyWord);

        std::vector< std::vector<unsigned char> > _KeyRoundMatrix;
        std::vector< std::vector<unsigned char> > _InvKeyRoundMat;
        const std::vector<unsigned> _RoundConst = {0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36};
        const unsigned MatDim = 4;
        const unsigned Byte = 8;
        const unsigned RoundNumber = 9;
        const unsigned ByteSize = 16;
        const unsigned BitSize = 128;
        unsigned _Value;
};

#endif