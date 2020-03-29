import bitio
import huffman
import pickle



def read_tree(tree_stream):
	#Use pickle to load to the huffman tree
	unpickled = pickle.load(tree_stream)
	return unpickled
    


def decode_byte(tree, bitreader):

    #First node as root node
    currentnode = tree
    while isinstance(currentnode, huffman.TreeBranch):
    	currentbit = bitreader.readbit()

    	if currentbit == 0:
    		currentnode = currentnode.getLeft()
    	elif currentbit == 1:
    		currentnode =  currentnode.getRight()

    try:
    	alphabet = currentnode.getValue()
    except EOFError:
    	alphabet = None
    return alphabet					

def decompress(compressed, uncompressed):
    
    #defining reader and writer 
    bitreader1 = bitio.BitReader(compressed)
    bitwriter1 = bitio.BitWriter(uncompressed)

    tree = read_tree(compressed)
    alphabet = 0

    while alphabet!=None:
    	letter = decode_byte(tree, bitreader1)		
    	bitwriter1.writebits(letter, 8)	
    bitwriter1.flush()	



def write_tree(tree, tree_stream):

	#Use pickle to store tree in file
	pickle.dump(tree, tree_stream)



def compress(tree, uncompressed, compressed):

	write_tree(tree, compressed)
	encoding_table = huffman.make_encoding_table(tree)
	values_table = list(encoding_table.values())
	keys_table = list(encoding_table.keys())

	mybytereader = bitio.BitReader(uncompressed)
	endoffile = False

	list1 = []

	while not endoffile:
		try:
			mybyte = mybytereader.readbits(8)
			list1.append(mybyte)
		except EOFError:
			endoffile = True

	mybitwriter = bitio.BitWriter(compressed)		


	for i in list1:
		if i in encoding_table.keys():
			code = encoding_table[i]
			for h in code:
				mybitwriter.writebit(h)


	mybitwriter.writebit(None)
	mybitwriter.flush()					

