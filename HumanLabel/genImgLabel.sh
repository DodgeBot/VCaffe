# need for 2 args
if [ $# -ne 2 ]; then
	echo "[Err] Illegal No. of args"
	echo "1st arg - path of frames"
	echo "2nd arg - label"
fi

# label for frames
label="$2"

# nav to working dir
dir="$1"
cd $dir
dir="`pwd`"

# if prev .txt exists, rm
if [ -f $dir/train.txt ]; then
	rm $dir/train.txt
fi

if [ -f $dir/test.txt ]; then
	rm $dir/test.txt
fi

# get frame names
var=($(ls))

# generate train and test img-label
for i in "${var[@]}"
do
	rand=$(($RANDOM%10))
	if [ $rand -ge 3 ]; then
		echo "$dir/$i $label" >> $dir/train.txt
	else
		echo "$dir/$i $label" >> $dir/test.txt
	fi
done

echo "test, train [image label] pair wrote to: $dir"
