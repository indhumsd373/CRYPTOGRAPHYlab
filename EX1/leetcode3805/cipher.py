from collections import Counter
from typing import List

class Solution:
    def countPairs(self, words: List[str]) -> int:
        # Use a dictionary to store the frequency of each canonical form
        counts = Counter()
        
        for word in words:
            # Step 1: Calculate the shift needed to make the first character 0
            # We use the first character as the reference point
            base_val = ord(word[0])
            
            # Step 2: Create a tuple of relative differences
            # (char_val - base_val) % 26
            # Example: "fusion" and "layout" will result in the same tuple
            canonical_form = tuple((ord(c) - base_val) % 26 for c in word)
            
            counts[canonical_form] += 1
            
        # Step 3: For each group of size 'v', calculate pairs: v * (v - 1) // 2
        ans = 0
        for v in counts.values():
            if v > 1:
                ans += (v * (v - 1)) // 2
                
        return ans
