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
		if [ -d "$dir/$i" ]; then
			echo "Flipping frames in folder $dir/$i"
			outdir="$dir/$i"_Flipped
			if [ -d $outdir ]; then
				echo "[Warning] output folder $dir/$i exists, skipping..."
			else
				mkdir $outdir
				python $SCRIPT_DIR/flipFrames.py -i "$dir/$i" -o $outdir
			fi
		else
			echo -n "[Warning] folder $i does not exists, "
			echo "use prepData.sh script to create relevant frames first!"
		fi
	done
done
