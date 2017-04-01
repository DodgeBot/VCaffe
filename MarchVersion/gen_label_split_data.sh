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

#generate train and test data folder
if [ -d $datedir/train ]; then
	rm -rf $datedir/train
fi

if [ -d $datedir/test ]; then
	rm -rf $datedir/test
fi

mkdir train
mkdir test

#create a new name for each image
img_index=0

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

		#check if it is a "flipped" folder
		if [ "${d:(-7)}" == "Flipped" ]; then
			flipped=true
		else
			flipped=false
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
				if [ $flipped == false ]; then
					#echo "$datedir/train/$img_index.jpg $label" >> $dir/train.txt
					echo "$img_index.jpg $label" >> $dir/train.txt
				else
					#echo "$datedir/train/$img_index.jpg $((2 - $label))" >> $dir/train.txt
					echo "$img_index.jpg $((2 - $label))" >> $dir/train.txt
				fi
				# cp "$dir/$i" $datedir/train
				# mv "$datedir/train/$i" "$datedir/train/$img_index.jpg"
				# ((img_index++))
				mv "$dir/$i" "$datedir/train/$img_index.jpg"
				((img_index++))
			else
				if [ $flipped == false ]; then
					#echo "$datedir/test/$img_index.jpg $label" >> $dir/test.txt
					echo "$img_index.jpg $label" >> $dir/test.txt
				else
					#echo "$datedir/test/$img_index.jpg $((2 - $label))" >> $dir/test.txt
					echo "$img_index.jpg $((2 - $label))" >> $dir/test.txt
				fi
				# cp "$dir/$i" $datedir/test
				# mv "$datedir/test/$i" "$datedir/test/$img_index.jpg"
				# ((img_index++))
				mv "$dir/$i" "$datedir/test/$img_index.jpg"
				((img_index++))
			fi
		done

		# pipe video data to total data
		cat $dir/train.txt >> $datedir/train.txt
		cat $dir/test.txt >> $datedir/test.txt

		# each time creating new files anyways, no need to keep
		rm $dir/train.txt
		rm $dir/test.txt

		cd $camdir
	done
done
echo "test, train [image label] pair wrote to: $datedir"
