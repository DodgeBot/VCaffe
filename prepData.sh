# GLOBAL vars
SCRIPT_DIR="/home/fyp/FYP/fyp_ws/scripts"

# need $argc args
argc=1
if [ $# -ne $argc ]; then
	echo "[Err] Illegal No. of args"
	echo "1st arg - path of data"
	exit
fi

# nav to working dir
datedir="$1"
cd $datedir
datedir="`pwd`"

# var=($(ls -1 $dir | grep -E "^M[0-9]+" -o | uniq))

# comment lines below and unit test above code
# for printing unique prefixes in given path

for x in {0,1,2}; do
	dir="$datedir/cam$x"
	cd $dir
	dir="`pwd`"

	var=($(ls -1 $dir | grep -E "^M[0-9]+" -o | uniq))
	for i in "${var[@]}"
	do
		# make sure at start of each loop
		# pwd is $dir
		cd $dir
		echo "$dir/$i"
		if [ -d $i ]; then
			echo "[Warnig] folder $i exists, skipping..."
		else
			# do the video2image here
			mkdir $i
			echo -n "$i: "
			python $SCRIPT_DIR/video2img.py -i "$dir/$i".MP4 -o $dir/$i

			# resize images created
			echo "Resizing images to 256x256..."
			tgt_dir="$dir/$i"
			cd $tgt_dir
			tgt_dir="`pwd`"
			images=($(ls))
			# num_images=($(ls -F |grep -v / | wc -l))
			# count=0
			for img in "${images[@]}"; do
			  convert -resize 256x256\! $img "resized_$img"
			  rm $img
			  mv "resized_$img" $img
			  # ((count++))
			  # if [ $(($count%1000)) == 0 ]; then
			  #   echo "$count out of $num_images completed ..."
			  # fi
			done
		fi
	done
done
