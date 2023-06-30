# Create element for the Huffman tree

class HuffmanNode(object):
   def __init__(self, frequency, character, left=None, right=None):
        self.frequency = frequency
        self.character=character
        self.left = left
        self.right = right
        self.bit=''

# Encoding the given text by creating a tree and assigning a code to each character present in the text based on the frequency of the character

def HuffmanEncoding(the_data):

    frequencyDict = FrequencyDict(the_data)  
    huffmanNodeList = []  
      
    for char in frequencyDict:  
       huffmanNodeList.append(HuffmanNode(frequencyDict[char], char))  
      
    while len(huffmanNodeList) > 1:   

        huffmanNodeList = sorted(huffmanNodeList, key = lambda x: x.frequency)  

        right = huffmanNodeList[0]  
        left = huffmanNodeList[1]  
      
        left.bit = 0  
        right.bit = 1  
      
        # combining the 2 smallest nodes to create new node  
        newNode = HuffmanNode(left.frequency + right.frequency, left.bit + right.bit, left, right)  
      
        huffmanNodeList.remove(left)  
        huffmanNodeList.remove(right)  
        huffmanNodeList.append(newNode)  

    charKeydict={}

    #Assigning Codes to each Node

    def CodeAssignment(node, value):  

        newValue = value + str(node.bit)  
    
        if(node.left):  
            CodeAssignment(node.left, newValue)  
        if(node.right):  
            CodeAssignment(node.right, newValue)  
    
        if(not node.left and not node.right):  
            charKeydict[node.character] = newValue  
            
        return charKeydict
              
    huffmanEncoding = CodeAssignment(huffmanNodeList[0], '')  
    encodedDataList=[]
    for element in the_data:
        encodedDataList.append(huffmanEncoding[element])  
          
    encodedData= ''.join([str(item) for item in encodedDataList])     
        

    return encodedData, huffmanNodeList[0]

# Decodes the string based using the huffman Tree

def HuffmanDecoding(input, huffmanTree):  
    encodedData=input
    treeHead = huffmanTree  
    decodedOutput = []  
    for x in encodedData:  
        if x == '1':  
            huffmanTree = huffmanTree.right     
        elif x == '0':  
            huffmanTree = huffmanTree.left  
        try:  
            if huffmanTree.left.character == None and huffmanTree.right.character == None:  
                pass  
        except AttributeError:  
            decodedOutput.append(huffmanTree.character)  
            huffmanTree = treeHead
    string = ''.join([str(item) for item in decodedOutput]) 
    return string


# Encoding and Decoding 1 and 0 strings to a bit64 system"

charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'

def encode(bin_string):
    chunks = [bin_string[i:i+6] for i in range(0, len(bin_string), 6)]
    last_chunk_length = len(chunks[-1])
    decimals = [int(chunk, 2) for chunk in chunks]
    decimals.append(last_chunk_length)
    ascii_string = ''.join([charset[i] for i in decimals])

    return ascii_string

def decode(ascii_string):
    decimals = [charset.index(char) for char in ascii_string]
    last_chunk_length, last_decimal = decimals.pop(-1), decimals.pop(-1)
    bin_string = ''.join([bin(decimal)[2:].zfill(6) for decimal in decimals])
    bin_string += bin(last_decimal)[2:].zfill(last_chunk_length)

    return bin_string


#Calculates the frequency of each character

def FrequencyDict(the_data):  
    the_symbols = dict()  
    for item in the_data:  
        if item not in the_symbols:  
            the_symbols[item] = 1  
        else:   
            the_symbols[item] += 1       
    return the_symbols

#Main function

def main():
    #Takes in path of the target file as the input
    path=input("Enter the path of the file to be compressed:- ")

    fileInput=open(path,"r")
    the_data=fileInput.read()
    fileInput.close()
    encoding, huffmanTree = HuffmanEncoding(the_data)

    compressedPath=path+"commpressed"
    fileOutput=open(compressedPath,"w+")
    fileOutput.write(encode(encoding))
    fileOutput.close()

    print("The compressed file has is stored at:- ", compressedPath)


    response=input("Do you want to decode the file? (Type y or Y if yes) :- ")

    if response=="y" or response=="Y":

        fileInput=open(compressedPath,"r")
        the_data=fileInput.read()
        the_data=decode(the_data)
        decodedPath=path+"decoded"

        fileOutput=open(decodedPath,"w+")
        fileOutput.write(HuffmanDecoding(the_data, huffmanTree))
        fileOutput.close()

        print("The decoded file has is stored at", decodedPath)


    
main()



