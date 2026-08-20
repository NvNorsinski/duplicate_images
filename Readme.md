# Duplicate Image finder

This tools can find images which are identical even if the resolution is different. This is done by creating Hash values for each image using pHash.
The the distance between the Hash values is calculated. Above an adjustable Threshold images are set as different.
Start with

`python main.py "path/to/image/direcotry"`