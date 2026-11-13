import re

with open('index.html', 'r') as f:
    html = f.read()

# Let's inspect CSS to add the 3D Tumbler, Trailer Reveal, and Hyperspace styles
print("Loaded index.html, length:", len(html))
