# explanations for member functions are provided in requirements.py
# each file that uses a skip list should import it from this file.

from typing import List
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_string =False

class Trie:
     
    # Trie data structure class
    def __init__(self, is_compressed: bool):
        self.root = TrieNode()
        self.is_compressed = is_compressed
        
    def path_compression(self, node, parent, char_in_parent):
        # Compress the children first
        for char, child in list(node.children.items()):
            self.path_compression(child, node, char)

        # If this node has a single child and is not an end-of-a-string node,
        # merge it with its child
        if parent and len(node.children) == 1 and not node.is_end_of_string:
            (child_char, child_node) = next(iter(node.children.items()))
            # Update the parent node to bypass the current node
            new_char = char_in_parent + child_char
            parent.children[new_char] = child_node
            del parent.children[char_in_parent]


    def construct_trie_from_text(self, keys: List[str]) -> None:
        # uncompressed trie implementation
        for word in keys:
            curr = self.root
            for char in word:
                if char not in curr.children:
                    curr.children[char] = TrieNode()
                curr = curr.children[char]
            curr.is_end_of_string = True

        if self.is_compressed:
            self.path_compression(self.root, None, None)
        
    def print_trie(self, node=None, level=0):
        if node is None:
            node = self.root

        for key, child in node.children.items():
            print(' ' * level + key, 'End' if child.is_end_of_string else '')
            self.print_trie(child, level + 1)

    def construct_suffix_tree_from_text(self, keys: List[str]) -> None:
        substrings = []
        for key in keys:
            for i in range(len(key)):
                substrings.append(key[i:])
        self.construct_trie_from_text(substrings)
        if self.is_compressed:
            self.path_compression(self.root, None, None)
            
    # def search_and_get_depth(self, key: str) -> int:
    #     node = self.root
    #     depth = 0  # Starting depth

    #     idx = 0  # Index to track the position in the key
    #     while idx < len(key):
    #         # If the trie is compressed or uncompressed, this will work for both.
    #         # Find the child node that matches the beginning of the remaining key.
    #         matched = False  # Flag to check if we find a matching child
    #         for child_key, child_node in node.children.items():
    #             if key[idx:].startswith(child_key):
    #                 idx += len(child_key)  # Move the index forward by the length of the matched child key
    #                 depth += 1  # Increment depth for each matched path (not individual characters)
    #                 node = child_node
    #                 matched = True
    #                 break  # Break after finding the matching child

    #         if not matched:
    #             # No matching child node was found.
    #             return -1

    #     if node.is_end_of_string:
    #         return depth
    #     else:
    #         return -1  # Key not found as a complete string in the trie.
    
    def search_and_get_depth(self, key: str) -> int:
        node = self.root
        depth, idx = 0, 0  # Initialize depth and index

        # Iterate over the key using index
        while idx < len(key):
            # Attempt to find a matching child for the current key segment
            for child_key, child_node in node.children.items():
                # Check if the current segment of the key matches the child key
                if key.startswith(child_key, idx):
                    # Update index and depth, then proceed with the matched child node
                    idx += len(child_key)
                    depth += 1
                    node = child_node
                    break
            else:
                # Execution reaches here if no 'break' occurs, meaning no match was found
                return -1

        # Check if the final node corresponds to the end of a valid string
        return depth if node.is_end_of_string else -1
    
