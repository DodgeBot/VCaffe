## How to use the scripts
### * Create train and test sets
1. create folder for the .MOV, named after it
2. python video2imge.py -i /path/to/the.MOV -o /path/to/theDIR
3. ./genImgLabel.sh /path/to/theDIR label
### * Use trained model to predict a frame
1. alter the image path in predictImg.py
2. python predictImg.py

### Labels
0 - straight
1 - left
2 - right
