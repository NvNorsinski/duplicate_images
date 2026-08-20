# Duplicate Image finder

This tool can find images which are identical or clode to beeing identical even if the resolution is different. This is done by creating a hash value for each image using pHash.
The distance between the hash values is calculated. Under an adjustable threshold, images are set as identical.

Start with:

`python main.py "path/to/image/direcotry"`


Similiar images are then printed out in groups. A groups are images identified as identical or nearly identical