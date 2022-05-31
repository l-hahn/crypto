#include "aes.hpp"
#include <iostream>

aes::aes(std::string && KeyWord){
    set_key(std::vector<unsigned char>(KeyWord.begin(),KeyWord.end()));
}
aes::aes(std::string & KeyWord){
    set_key(std::vector<unsigned char>(KeyWord.begin(),KeyWord.end()));
}
aes::aes(std::vector<unsigned> && KeyWord){
    set_key(std::vector<unsigned char>(KeyWord.begin(),KeyWord.end()));
}
aes::aes(std::vector<unsigned> & KeyWord){
    set_key(std::vector<unsigned char>(KeyWord.begin(),KeyWord.end()));
}
aes::aes(std::vector<unsigned char> && KeyWord){
    set_key(KeyWord);
}
aes::aes(std::vector<unsigned char> & KeyWord){
    set_key(KeyWord);
}

void aes::set_key(std::vector<unsigned char> && KeyWord){
    set_key(KeyWord);
}

void aes::set_key(std::vector<unsigned char> & KeyWord){
    _adjust_key_length(KeyWord);
    std::vector< std::vector<unsigned char> > KeyMatrix;
    for(unsigned i = 0; i < MatDim; i++){
        std::vector<unsigned char> NewCol;
        for(unsigned j = 0; j < MatDim; j++){
            NewCol.push_back(KeyWord[j*4+i]);
        }
        KeyMatrix.push_back(NewCol);
    }
    for(unsigned i = 0; i < ((RoundNumber+1)*MatDim); i++){
        if(i%MatDim != 0){
            std::vector<unsigned char> NewCol;
            std::vector<unsigned char>::iterator Prev = KeyMatrix[KeyMatrix.size()-1].begin();
            std::transform(KeyMatrix[i].begin(),KeyMatrix[i].end(),std::back_inserter(NewCol),[&Prev](const unsigned char Value){
                return Value^*(Prev++);
            });
            KeyMatrix.push_back(NewCol);
        }
        else{
            std::vector<unsigned char> NewCol;
            std::vector< std::vector<unsigned> > _SBox = aes_base::_SBox;
            std::transform(KeyMatrix[KeyMatrix.size()-1].begin(),KeyMatrix[KeyMatrix.size()-1].end(),std::back_inserter(NewCol),[_SBox](unsigned char & Value){
                return aes_base::_SBox[((Value&240) >> 4)][(Value&15)];
            });
            std::rotate(NewCol.begin(),NewCol.end()-1,NewCol.end());
            NewCol[1] ^= _RoundConst[(int)i/MatDim];

            std::vector<unsigned char>::iterator Prev = KeyMatrix[i].begin();
            std::transform(NewCol.begin(),NewCol.end(),NewCol.begin(),[&Prev](unsigned char & Value){
                return Value^*(Prev++);
            });
            KeyMatrix.push_back(NewCol);
        }
    }
    std::vector< std::vector<unsigned char> > KeyRoundMatrix;
    for(unsigned i = 0; i < (RoundNumber+2); i++){
        std::vector<unsigned char> RoundKey;
        for(unsigned j = 0; j < MatDim; j++){
            RoundKey.push_back(KeyMatrix[(i*MatDim)][j]);
            RoundKey.push_back(KeyMatrix[(i*MatDim+1)][j]);
            RoundKey.push_back(KeyMatrix[(i*MatDim+2)][j]);
            RoundKey.push_back(KeyMatrix[(i*MatDim+3)][j]);
        }
        KeyRoundMatrix.push_back(RoundKey);
    }
    _KeyRoundMatrix = KeyRoundMatrix;
    _InvKeyRoundMat = KeyRoundMatrix;
    std::reverse(_InvKeyRoundMat.begin(),_InvKeyRoundMat.end());
}
std::vector< std::vector<unsigned char> > aes::key(){
    return _KeyRoundMatrix;
}
std::vector< std::vector<unsigned char> > aes::key_inverse(){
    return _InvKeyRoundMat;
}

unsigned aes::value(){
    return _Value;
}

void aes::_adjust_key_length(std::vector<unsigned char> & KeyWord){
    if(KeyWord.size() > ByteSize){
        KeyWord = std::vector<unsigned char>(KeyWord.begin(),KeyWord.begin()+ByteSize);
    }
    else{
        unsigned LeftBitsSide = 240, RightBitsSide = 15, Idx = 0, Row, Col;
        while(KeyWord.size() < ByteSize){
            Row = ((KeyWord[Idx]^LeftBitsSide) >> MatDim)%ByteSize;
            Col = (KeyWord[Idx]^RightBitsSide)%ByteSize;
            KeyWord.push_back(aes_base::_SBox[Row][Col]);
            Idx = (Row+Col+KeyWord[KeyWord.size()-1])%ByteSize;
        }
    }
}