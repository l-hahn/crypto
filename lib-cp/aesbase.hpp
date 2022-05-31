#ifndef AESBASE_CPP_
#define AESBASE_CPP_
#include <algorithm>
#include <vector>

namespace aes_base{
    std::vector<unsigned char> encrypt(std::vector<unsigned char> PlainMatrix, std::vector<unsigned char> & RoundKeyMatrix);
    std::vector<unsigned char> decrypt(std::vector<unsigned char> CipherMatrix, std::vector<unsigned char> & RoundKeyMatrix);
    void _byte_sub(std::vector<unsigned char> & Matrix, bool Inverse);
    void _shift_row(std::vector<unsigned char> & Matrix, bool Inverse);
    void _mix_columns(std::vector<unsigned char> & Matrix, bool Inverse);
    void _add_round_key(std::vector<unsigned char> & Matrix, std::vector<unsigned char>::iterator MatBegin);

    unsigned char _g_mul(unsigned char Value, unsigned char Factor);

    extern const std::vector< std::vector<unsigned> > _SBox;
    extern const std::vector< std::vector<unsigned> > _SBoxInv;
    extern const unsigned _MatDim;
    extern const unsigned _ByteSize;
    extern const unsigned _RoundNumber;
    extern const unsigned _BlockSize;
};

#endif