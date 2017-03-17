# need for 1 args
if [ $# -ne 1 ]; then
	echo "[Err] Illegal No. of args"
	echo "1st arg - path of frames"
	# echo "2nd arg - label"
	exit
fi

# label for frames
# label="$2"

# nav to working dir
datedir="$1"
cd $datedir
datedir="`pwd`"

if [ -f $datedir/train.txt ]; then
	rm $datedir/train.txt
fi

if [ -f $datedir/test.txt ]; then
	rm $datedir/test.txt
fi

for label in {0,1,2}; do
	camdir="$datedir/cam$label"
	cd $camdir
	camdir="`pwd`"

	folders=($(ls))
	for d in "${folders[@]}"; do
		if [ ! -d $d ]; then
			# echo $d
			# skip if is not folder
			continue
		fi

		dir="$camdir/$d"
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

		# pipe video data to total data
		cat $dir/train.txt >> $datedir/train.txt
		cat $dir/test.txt >> $datedir/test.txt

		cd $camdir
	done
done
echo "test, train [image label] pair wrote to: $datedir"
