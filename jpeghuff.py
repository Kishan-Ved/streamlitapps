import streamlit as st
import huffman
import numpy as np

# Create a 2D array (8x8) with DCT coefficients (replace with your actual coefficients)
dct_coefficients = np.array([
    [20, 30, 10, 25, 30, 0, 0, 0],
    [0, 5, 0, 0, 0, 0, 5, 0],
    [0, 0, 15, 0, 0, 0, 20, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
], dtype=np.int32)

dct_coefficients_str = "\n\n".join(["  ".join(map(str, row)) for row in dct_coefficients])


# Function to calculate (r, s) pairs for DCT coefficients
def calculate_rs_pairs(dct_coefficients):
    rs_pairs = []
    run_length = 0

    for row in dct_coefficients:
        for element in row:
            if element == 0:
                run_length += 1
            else:
                bits_needed = len(bin(abs(element))) - 2  # Calculate the number of bits needed to represent c
                rs_pairs.append(((run_length, bits_needed), element))
                run_length = 0

    return rs_pairs

# Calculate (r, s) pairs
rs_pairs = calculate_rs_pairs(dct_coefficients)


# Calculate the frequency of (r, s) pairs
frequency_rs = {}

d = {} # maps (r,s) pair to a unique symbol (for passing in huffman library)
d2 = {} # Inverse of d
alph = "abcdefghijklmnopqrstuvwxyz"
pos=0

for (r, s), _ in rs_pairs:
  if (r,s) in list(d.keys()):
    continue
  else:
    d[(r,s)] = alph[pos]
    d2[alph[pos]] = (r,s)
    pos+=1

for (r,s),_ in rs_pairs:
    if d[(r, s)] in frequency_rs:
        frequency_rs[d[(r, s)]] += 1
    else:
        frequency_rs[d[(r, s)]] = 1

# Build Huffman codes for (r, s) pairs
huffman_rs = huffman.codebook([(x,frequency_rs[x]) for x in list(frequency_rs.keys())])

# Create a dictionary to map (r, s) pairs to their Huffman codes
rs_to_huffman = {pair: huffman_rs[pair] for pair in frequency_rs.keys()}

# Encode ((r, s), c) triples
encoded_data = ""
encoded_data_l = ""
for (r, s), c in rs_pairs:
    encoded_data_l += "(({}, {}), {}) Huffman code for ({}, {}): {}   Binary representation of c: {}".format(r, s, c, r, s, rs_to_huffman[d[(r, s)]], format(c, f'0{s}b')) + "\n"  # Encode (r, s)
    encoded_data += rs_to_huffman[d[(r, s)]] + format(c, f'0{s}b')  # Encode (r, s) and c

print(len(encoded_data))

# Decode the encoded data to recover the ((r, s), c) triples
decoded_data = []
current_bits = ""
i=0
while i<len(encoded_data):
    # print(i)
    current_bits += encoded_data[i]
    i+=1
    for ch, huffman_code in rs_to_huffman.items():
        if current_bits == huffman_code:
            current_bits = ""
            c_bits = ""
            r,s = d2[ch]
            # print(s)
            for j in range(s):
                c_bits += encoded_data[i+j]
            decoded_data.append((ch,int(c_bits, 2)))
            # print(ch,int(c_bits,2))
            i+=s
            # print(i)
            c_bits = ""
        # i+=1

# Print the encoded and decoded data



dl = []
for ch,c in decoded_data:
#   print(d2[ch],c)
  dl.append((d2[ch],c))

newl = []
for ele in dl:
  r,s = ele[0]
  c = ele[1]
  for i in range(r):
    newl.append(0)
  newl.append(c)

ll = len(newl)
for i in range(ll+1,64+1):
  newl.append(0)

import numpy as np
newl = np.array(newl)
newl = np.reshape(newl,(8,8))
# Create an empty space for displaying elements of encoded_data_l
output = st.empty()




# # Display the decoded matrix as an image (assuming it represents an image)
# if st.button("Show Decoded Matrix"):
#    st.subheader("Decoded Matrix:")
#    st.image(decoded_data, caption="Decoded Image", use_column_width=True)

if __name__ == "__main__":
    st.title("Coding in JPEG")
    st.write("This is an interactive app that helps in understaning the coding in JPEG.")
    st.write()
    st.markdown("The code of a DCT matrix consists of a string of codes of every non-zero element (c), which has 2 parts:")
    st.markdown("Procedure:")
    st.markdown("1) Huffman code of the (r,s) pair associated with c and")
    st.markdown("2) s bits (as s is the number of bits used to represent c in binary form)")
    st.markdown("The DCT Matrix to be coded is:")
    st.markdown(dct_coefficients_str)

# Display the encoded and decoded data upon button click
if st.button("Show Encoding"):
   st.subheader("Encoding of data:")
   st.text(encoded_data_l)

if st.button("Show Encoded Data"):   
   st.subheader("Encoded Data:")
   st.text(encoded_data)