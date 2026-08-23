# Duplicate Image finder

This tool can find images which are identical or close to beeing identical, even if the resolution is different. This is done by creating a hash value for each image using pHash.
The distance between the hash values is calculated. Distances lower than an adjustable threshold, lead to an identification of identical or close to beeing identical images.

Start with:

`python main.py "path/to/image/direcotry"`


Similiar images are then printed out in groups. A group are images identified as identical or nearly identical