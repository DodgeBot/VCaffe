# GLOBAL vars
SCRIPT_DIR="/home/fyp/FYP/fyp_ws/scripts"

# need $argc args
argc=1
if [ $# -ne $argc ]; then
	echo "[Err] Illegal No. of args"
	echo "1st arg - path of data"
fi

# nav to working dir
dir="$1"
cd $dir
dir="`pwd`"

var=($(ls -1 $dir | grep -E "^[0-9]+T[0-9]+" -o | uniq))

# comment lines below and unit test above code
# for printing unique prefixes in given path

for i in "${var[@]}"
do
	if [ -d $i ]; then
		echo "[Warnig] folder $i exists, skipping..."
	else
		# do the video2image here
		mkdir $i
		echo -n "$i: "
		python $SCRIPT_DIR/video2img.py -i "$dir/$i"video.mov -o $dir/$i
	fi
done
