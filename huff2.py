import streamlit as st
import heapq
import graphviz
import time
import os
import tempfile 

# Define the Node class and other necessary functions as shown in your previous code
# import heapq
import graphviz

# Set the Graphviz executable path within your Streamlit app (replace with your actual path)
# graphviz_path = "C:/Program Files/Graphviz/bin/"  # Example path, adjust as needed
# os.environ["PATH"] += os.pathsep + graphviz_path

class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''

    def __lt__(self, nxt):
        return self.freq < nxt.freq

def generate_heap_graph(nodes, step):
    dot = graphviz.Digraph(format='png')
    dot.attr(dpi='300', bgcolor='white')  # Set background color
    dot.attr(label=f"Step {step} Heap")  # Set label for the graph

    for node in nodes:
        dot.node(str(id(node)), f"{node.symbol}:{node.freq}", style="filled", fillcolor="lightblue")  # Node color

    return dot

def generate_tree_graph(root, step):
    dot = graphviz.Digraph(format='png')
    dot.attr(dpi='300', bgcolor='white')  # Set background color
    dot.attr(label=f"Step {step} Huffman Tree")  # Set label for the graph

    def add_nodes_edges(node):
        if node:
            dot.node(str(id(node)), f"{node.symbol}:{node.freq}", style="filled", fillcolor="lightblue")
            if node.left:
                dot.edge(str(id(node)), str(id(node.left)), label="0", color="blue")
                add_nodes_edges(node.left)
            if node.right:
                dot.edge(str(id(node)), str(id(node.right)), label="1", color="red")
                add_nodes_edges(node.right)

    add_nodes_edges(root)
    return dot

def print_huffman_codes(node, val=''):
    newVal = val + str(node.huff)
    if not node.left and not node.right:
        print(f"{node.symbol} -> {newVal}")
    else:
        print_huffman_codes(node.left, newVal)
        print_huffman_codes(node.right, newVal)

codes = {}

def huffman_codes(node, val=''):
    newVal = val + str(node.huff)
    if not node.left and not node.right:
        codes[node.symbol] = newVal
    else:
        huffman_codes(node.left, newVal)
        huffman_codes(node.right, newVal)

# Your character frequency data (d) here
d = {'A': 5, 'B': 9, 'C': 12, 'D': 13, 'E': 16, 'F': 20}

chars = list(d.keys())
freq = list(d.values())

nodes = []
heap_graphs = []  # List to store heap graphs at each step
tree_graphs = []  # List to store Huffman tree graphs at each step

# Initialize the heap with individual characters as nodes
for x in range(len(chars)):
    heapq.heappush(nodes, Node(freq[x], chars[x]))

heap_graphs.append(generate_heap_graph(nodes, 0))  # Add the initial heap graph

step = 1

while len(nodes) > 1:
    left = heapq.heappop(nodes)
    right = heapq.heappop(nodes)
    left.huff = '0'
    right.huff = '1'
    new_symbol = left.symbol + right.symbol
    new_freq = left.freq + right.freq
    new_node = Node(new_freq, new_symbol, left, right)
    heapq.heappush(nodes, new_node)

    heap_graph = generate_heap_graph(nodes, step)
    heap_graphs.append(heap_graph)

    tree_graph = generate_tree_graph(new_node, step)
    tree_graphs.append(tree_graph)

    step += 1

# Render all heap and tree graphs
for i, (heap_graph, tree_graph) in enumerate(zip(heap_graphs, tree_graphs)):
    heap_graph.render(f"heap_step_{i}", cleanup=True)
    tree_graph.render(f"tree_step_{i}", cleanup=True)

# Huffman coding
huffman_tree_root = nodes[0]

# Your code for displaying Huffman tree and codes here

# Define a function to generate heap and tree graphs for each step
def generate_step_graphs(d):
    chars = list(d.keys())
    freq = list(d.values())

    nodes = []
    heap_graphs = []  # List to store heap graphs at each step
    tree_graphs = []  # List to store Huffman tree graphs at each step

    # Initialize the heap with individual characters as nodes
    for x in range(len(chars)):
        heapq.heappush(nodes, Node(freq[x], chars[x]))

    heap_graphs.append(generate_heap_graph(nodes, 0))  # Add the initial heap graph

    step = 1

    while len(nodes) > 1:
        left = heapq.heappop(nodes)
        right = heapq.heappop(nodes)
        left.huff = '0'
        right.huff = '1'
        new_symbol = left.symbol + right.symbol
        new_freq = left.freq + right.freq
        new_node = Node(new_freq, new_symbol, left, right)
        heapq.heappush(nodes, new_node)

        heap_graph = generate_heap_graph(nodes, step)
        heap_graphs.append(heap_graph)

        tree_graph = generate_tree_graph(new_node, step)
        tree_graphs.append(tree_graph)

        step += 1

    return heap_graphs, tree_graphs



# Create a temporary directory to store the images
with tempfile.TemporaryDirectory() as temp_dir:
    # Set the Graphviz executable path within your Streamlit app (replace with your actual path)
    graphviz_path = "C:/Program Files/Graphviz/bin/"  # Example path, adjust as needed
    os.environ["PATH"] += os.pathsep + graphviz_path

    # Rest of your Streamlit app code...
    # Define the Streamlit app
def main():
    st.title("Huffman Encoding Visualization")
    st.write("This is an interactive app that helps in visualising the steps of building the Huffman Tree.")
    st.write()
    st.markdown("Procedure:")
    st.markdown("1. Remove the 2 elements with minimum frequencies from the min heap and combine them to give a new node.")
    st.markdown("2. Add this new node to the heap.")
    st.markdown("3. Continue till only one element is left in the heap.")
    st.write("On clicking on encode, you can visualise the elements in the heap and the new node combination for every step.")
    st.write("First try running for the text provided, next, try running by adding more characters. Please do not reduce the number of characters, it may lead to unexpected errors.")
    # Input text to be encoded
    input_text = st.text_area("Enter the text to be encoded","aaaaaaaaaaaabbbbbbbbbcccccccccdddddeeeeff")

    if st.button("Encode"):
        # Calculate character frequencies
        char_freq = {}
        for char in input_text:
            if char in char_freq:
                char_freq[char] += 1
            else:
                char_freq[char] = 1

        # Generate heap and tree graphs for each step
        heap_graphs, tree_graphs = generate_step_graphs(char_freq)
        
        # Display graphs with a time interval
        for i in range(min(len(heap_graphs), len(tree_graphs))):
            st.image(heap_graphs[i].pipe(format="png"), caption=f"Heap Step {i+1}", width=400)
            st.image(tree_graphs[i].pipe(format="png"), caption=f"Huffman Tree Step {i+1}",width=400)
            time.sleep(1)  # Add a delay of 1 second between steps
        
        # # Display Huffman Codes
        # st.subheader("Huffman Codes:")
        # huffman_codes(huffman_tree_root)
        # print_huffman_codes(huffman_tree_root)

if __name__ == "__main__":
    main()

