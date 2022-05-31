import argparse, itertools, os
from copy import deepcopy
from os import path

class aes_base:
    _SBox = [
        [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
        [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
        [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
        [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
        [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
        [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
        [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
        [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
        [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
        [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
        [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
        [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
        [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
        [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
        [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
        [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
    ]
    _SBoxInv = [
        [0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB],
        [0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB],
        [0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E],
        [0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25],
        [0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92],
        [0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84],
        [0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06],
        [0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B],
        [0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73],
        [0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E],
        [0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B],
        [0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4],
        [0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F],
        [0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF],
        [0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61],
        [0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D]
    ]
    ByteSize = 8
    RoundNumber = 9
    BlockSize = 128
    def encrypt(PlainTextMatrix,KeyRoundMatrix):
        Inverse = False
        ARK = aes_base._add_round_key(PlainTextMatrix,aes_base._get_round_key(KeyRoundMatrix,0))
        for i in range(aes_base.RoundNumber):
            BSB = aes_base._byte_sub(ARK,Inverse)
            SR = aes_base._shift_row(BSB,Inverse)
            MC = aes_base._mix_columns(SR,Inverse)
            ARK = aes_base._add_round_key(MC,aes_base._get_round_key(KeyRoundMatrix,i+1))
        BSB = aes_base._byte_sub(ARK,Inverse)
        SR = aes_base._shift_row(BSB,Inverse)
        ARK = aes_base._add_round_key(SR,aes_base._get_round_key(KeyRoundMatrix,aes_base.RoundNumber+1))
        return ARK
    def decrypt(CipherTextMatrix,KeyRoundMatrix):
        Inverse = True
        ARK = aes_base._add_round_key(CipherTextMatrix,aes_base._get_round_key(KeyRoundMatrix,0))
        SR = aes_base._shift_row(ARK,Inverse)
        BSB = aes_base._byte_sub(SR,Inverse)
        for i in range(aes_base.RoundNumber):
            ARK = aes_base._add_round_key(BSB,aes_base._get_round_key(KeyRoundMatrix,i+1))
            MC = aes_base._mix_columns(ARK,Inverse)
            SR = aes_base._shift_row(MC,Inverse)
            BSB = aes_base._byte_sub(SR,Inverse)
        ARK = aes_base._add_round_key(BSB,aes_base._get_round_key(KeyRoundMatrix,aes_base.RoundNumber+1))
        return ARK       
    def _byte_sub(Matrix,Inverse = False):
        if Inverse == False:
            return [[aes_base._SBox[int(bin(Value)[2:].zfill(8)[:aes_base.ByteSize//2],2)][int(bin(Value)[2:].zfill(8)[aes_base.ByteSize//2:],2)] for Value in Row] for Row in Matrix]
        else:
            return [[aes_base._SBoxInv[int(bin(Value)[2:].zfill(8)[:aes_base.ByteSize//2],2)][int(bin(Value)[2:].zfill(8)[aes_base.ByteSize//2:],2)] for Value in Row] for Row in Matrix]
    def _shift_row(Matrix,Inverse = False):
        if Inverse == False:
            return [aes_base._row_rotate(Row,Idx) for Idx,Row in enumerate(Matrix)]
        else:
            return [aes_base._row_rotate(Row,Idx,True) for Idx,Row in enumerate(Matrix)]
    def _mix_columns(Matrix,Inverse = False):
        MC = deepcopy(Matrix)
        if Inverse == False:
            for i in range(aes_base.ByteSize//2):
                MC[0][i] = aes_base._g_mul(Matrix[0][i],2)^aes_base._g_mul(Matrix[1][i],3)^aes_base._g_mul(Matrix[2][i],1)^aes_base._g_mul(Matrix[3][i],1)
                MC[1][i] = aes_base._g_mul(Matrix[0][i],1)^aes_base._g_mul(Matrix[1][i],2)^aes_base._g_mul(Matrix[2][i],3)^aes_base._g_mul(Matrix[3][i],1)
                MC[2][i] = aes_base._g_mul(Matrix[0][i],1)^aes_base._g_mul(Matrix[1][i],1)^aes_base._g_mul(Matrix[2][i],2)^aes_base._g_mul(Matrix[3][i],3)
                MC[3][i] = aes_base._g_mul(Matrix[0][i],3)^aes_base._g_mul(Matrix[1][i],1)^aes_base._g_mul(Matrix[2][i],1)^aes_base._g_mul(Matrix[3][i],2)                
        else:
            for i in range(aes_base.ByteSize//2):
                MC[0][i] = aes_base._g_mul(Matrix[0][i],14)^aes_base._g_mul(Matrix[1][i],11)^aes_base._g_mul(Matrix[2][i],13)^aes_base._g_mul(Matrix[3][i],9)
                MC[1][i] = aes_base._g_mul(Matrix[0][i],9)^aes_base._g_mul(Matrix[1][i],14)^aes_base._g_mul(Matrix[2][i],11)^aes_base._g_mul(Matrix[3][i],13)
                MC[2][i] = aes_base._g_mul(Matrix[0][i],13)^aes_base._g_mul(Matrix[1][i],9)^aes_base._g_mul(Matrix[2][i],14)^aes_base._g_mul(Matrix[3][i],11)
                MC[3][i] = aes_base._g_mul(Matrix[0][i],11)^aes_base._g_mul(Matrix[1][i],13)^aes_base._g_mul(Matrix[2][i],9)^aes_base._g_mul(Matrix[3][i],14)   
        return MC
    def _add_round_key(Matrix,KeyRoundMatrix):
        return [[Value^KeyRoundMatrix[Idx][Jdx] for Jdx,Value in enumerate(Row)] for Idx,Row in enumerate(Matrix)]
    def _row_rotate(OldRow,Rotation,Inverse = False):
        Row = deepcopy(OldRow)
        if Inverse == False: #to left
            for i in range(Rotation):
                Row.append(Row.pop(0))
        else:
            for i in range(Rotation):
                Row.insert(0,Row.pop())
        return Row
    def _g_mul(Value,Factor):
        if Factor == 1:
            return Value
        elif Factor == 2:
            if Value < 2**7:
                return 2*Value
            else:
                return (2*Value)^(0x11b)
        elif Factor == 3:
            return aes_base._g_mul(Value,2)^Value
        elif Factor == 9:
            return aes_base._g_mul(aes_base._g_mul(aes_base._g_mul(Value,2),2),2)^Value
        elif Factor == 11:
            return aes_base._g_mul(aes_base._g_mul(aes_base._g_mul(Value,2),2)^Value,2)^Value
        elif Factor == 13:
            return aes_base._g_mul(aes_base._g_mul(aes_base._g_mul(Value,2)^Value,2),2)^Value
        elif Factor == 14:
            return aes_base._g_mul(aes_base._g_mul(aes_base._g_mul(Value,2)^Value,2)^Value,2)
    def _get_round_key(KeyRoundMatrix,Round):
        return [[Col[i] for Col in KeyRoundMatrix[Round*(aes_base.ByteSize//2):(Round+1)*aes_base.ByteSize]] for i in range(aes_base.ByteSize//2)]


class aes:
    MatDim = 4
    Byte = 8
    ByteSize = 16
    BitSize = 128
    RoundConst = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]
    def __init__(self,Key,OpMode = 'ECB'):
        self._OpMode = OpMode
        self._KeyRoundMatrix = aes._key_expansion(Key)
        self._InvKeyRoundMat = aes._key_inversion(self._KeyRoundMatrix)
        self._Format = list
    def encrypt(self,TextString):
        ByteMatrix = self._format_input(TextString)
        EncryptMatrix = aes_base.encrypt(ByteMatrix,self._KeyRoundMatrix)
        Encryption = self._format_output(EncryptMatrix)
        return Encryption
    def encrypt_file(self,FileName):
        File = open(FileName,'r+b')
        Block = 'EMPTY'
        TextLeng = 0
        while len(Block) != 0:
            WritePos = File.tell()
            Block = File.read(aes.ByteSize)
            TextLeng += len(Block)
            if len(Block) != 0:
                File.seek(WritePos)
                File.write(self.encrypt(Block))
        File.write(self.encrypt(aes._size_to_bytes(TextLeng)))
        File.close()
    def encrypt_folder(self,FolderName):
        Files = []
        Folders = []
        for Item in os.listdir(FolderName):
            PathName = path.join(FolderName,Item)
            if path.isfile(PathName):
                Files.append(PathName)
            elif path.isdir(PathName):
                Folders.append(PathName)
        for File in Files:
            self.encrypt_file(File)
        File = []
        for Folder in Folders:
            self.encrypt_folder(Folder)
    def decrypt(self,TextString):
        ByteMatrix = self._format_input(TextString)
        DecryptMatrix = aes_base.decrypt(ByteMatrix,self._InvKeyRoundMat)
        Decryption = self._format_output(DecryptMatrix)
        return Decryption
    def decrypt_file(self,FileName):
        File = open(FileName,'r+b')
        Block = 'EMPTY'
        while len(Block) != 0:
            WritePos = File.tell()
            Block = File.read(aes.ByteSize)
            if len(Block) != 0:
                File.seek(WritePos)
                File.write(self.decrypt(Block))
        File.seek(WritePos-aes.ByteSize)
        TextLeng = aes._bytes_to_size(File.read(aes.ByteSize))
        if(TextLeng < (2**64-1)):
            File.seek(0)
            File.truncate(TextLeng)
        File.close()
    def decrypt_folder(self,FolderName):
        Files = []
        Folders = []
        for Item in os.listdir(FolderName):
            PathName = path.join(FolderName,Item)
            if path.isfile(PathName):
                Files.append(PathName)
            elif path.isdir(PathName):
                Folders.append(PathName)
        for File in Files:
            self.decrypt_file(File)
        File = []
        for Folder in Folders:
            self.decrypt_folder(Folder)
    def _key_expansion(Key):
        KeyMatrix = list(bytes(Key.encode()))
        LeftBitsSide = 2**aes.Byte-2**(aes.Byte//2)
        RightBitsSide = 2**aes.Byte-1
        Idx = 0
        while(len(KeyMatrix) != aes.ByteSize):
            Row = ((KeyMatrix[Idx]&LeftBitsSide) >> aes.Byte//2)%aes.ByteSize
            Col = ((KeyMatrix[Idx]&RightBitsSide))%aes.ByteSize
            KeyMatrix.append(aes_base._SBox[Row][Col])
            Idx = (Row+Col+KeyMatrix[-1])%aes.ByteSize
        KeyRoundMatrix = [KeyMatrix[i*aes.MatDim:(i+1)*aes.MatDim] for i in range(aes.MatDim)]
        for i in range(aes.MatDim*(aes_base.RoundNumber+1)):
            if i%(aes.MatDim) != 0:
                KeyRoundMatrix.append([KeyRoundMatrix[i][Idx]^Value for Idx,Value in enumerate(KeyRoundMatrix[-1])])
            else:
                KeyTrafo = aes._key_col_trafo(KeyRoundMatrix[-1],i)
                KeyRoundMatrix.append([KeyRoundMatrix[i][Idx]^Value for Idx,Value in enumerate(KeyTrafo)])
        return KeyRoundMatrix
    def _key_col_trafo(Col,Round):
        return [aes._key_sbox_trafo(Col[3]), aes._key_sbox_trafo(Col[0])^aes.RoundConst[Round//aes.MatDim], aes._key_sbox_trafo(Col[1]), aes._key_sbox_trafo(Col[2])]
    def _key_sbox_trafo(Value):
        return aes_base._SBox[((Value^(2**aes.Byte-2**(aes.Byte//2))) >> aes.Byte//2)%aes.ByteSize][((Value^(2**aes.Byte-1)))%aes.ByteSize]
    def _key_inversion(KeyMatrix):
        return list(itertools.chain.from_iterable(reversed([KeyMatrix[(i*aes.MatDim):(i+1)*aes.MatDim] for i in range(aes_base.RoundNumber+2)])))
    def _8bit_to_byte(Bits):
        Byte = 0
        for Idx,Bit in enumerate(reversed(Bits)):
            Byte |= (Bit << Idx)
        return Byte
    def _size_to_bytes(Size):
        BitList = list(map(int,list(bin(Size)[2:].zfill(aes.BitSize))))
        return bytes([ aes._8bit_to_byte(BitList[i*aes.Byte:(i+1)*aes.Byte]) for i in range(aes.ByteSize)])
    def _bytes_to_size(Bytes):
        return int(''.join([ bin(Block)[2:].zfill(aes.Byte) for Block in list(Bytes)]),2)
    def _format_input(self,TextString):
        ByteList = []
        ByteMatrix = []
        if type(TextString) is str:
            ByteList = list(TextString.encode())
            ByteList.extend([255]*(aes.ByteSize-len(ByteList)))
            self._Format = bytes
        elif type(TextString) is bytes:
            ByteList = list(TextString)
            ByteList.extend([255]*(aes.ByteSize-len(ByteList)))
            self._Format = bytes
        elif type(TextString) is list:
            ByteList = [int(Sig) for Sig in TextString]+[255]*(aes.ByteSize-len(TextString))
            self._Format = list
        else:
            raise TypeError('Input must be either String, Bytes or List')
        if len(ByteList) == aes.ByteSize:
            ByteMatrix = [ByteList[i*aes.MatDim:(i+1)*aes.MatDim] for i in range(aes.MatDim)]
        elif len(ByteList) == aes.BitSize:
            pass #TODO 128-BitList to 16Byte Matrix
        else:
            raise ValueError('Input must contain 16 Bytes or 128 Bits')
        return ByteMatrix
    def _format_output(self,ByteMatrix):
        TextString = list(itertools.chain.from_iterable(ByteMatrix))
        if self._Format is bytes:
            TextString = bytes(TextString)
        return TextString



Parser = argparse.ArgumentParser(description='En-/Decryption for Strings,Files and Folders')
Parser.add_argument('--file', metavar='<PATH_TO_FILE>', type=str, nargs=1, help='File that should be en-/decrypted.', required = False)
Parser.add_argument('--folder', metavar='<PATH>', type=str, nargs=1, help='Folder with files that should be en-/decrypted; recursive.', required = False)
Parser.add_argument('--text', metavar='<PATH_TO_FILE>', type=str, nargs=1, help='File that should be en-/decrypted.', required = False)
Parser.add_argument('--key', metavar='<KEY>', type=str, nargs=1, help='asdf', required = True)
Parser.add_argument('--decrypt', help='Enable input file decryption', action='store_true', required = False)
Args = Parser.parse_args()

KeyWord = Args.key[0]
Decryption = Args.decrypt
CryptoSystem = aes(KeyWord)
if not (Args.file or Args.folder or Args.text):
    Parser.error('one of the following arguments is requested: --file, --folder, --text')

if Decryption == False:
    if Args.file:
        CryptoSystem.encrypt_file(Args.file[0])
    elif Args.folder:
        CryptoSystem.encrypt_folder(Args.folder[0])
else:
    if Args.file:
        CryptoSystem.decrypt_file(Args.file[0])
    elif Args.folder:
        CryptoSystem.decrypt_folder(Args.folder[0])