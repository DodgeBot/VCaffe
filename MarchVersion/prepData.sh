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
		echo "$dir/$i"
		if [ -d $i ]; then
			echo "[Warnig] folder $i exists, skipping..."
		else
			# do the video2image here
			mkdir $i
			echo -n "$i: "
			python $SCRIPT_DIR/video2img.py -i "$dir/$i".MP4 -o $dir/$i
		fi
	done
done
