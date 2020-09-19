import base64

# Encode your gif into a string
img_encoded = base64.b64encode(open('images/loading.gif', 'rb').read()) 
# It looks like this: /9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcG ......

# Then embed this string into mygif.py, 
# and in your main script: import mygif

# Decode the image into binary content
img = base64.b64decode(img_encoded)
print(img)