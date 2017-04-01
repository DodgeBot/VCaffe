# need for 1 args
if [ $# -ne 1 ]; then
	echo "[Err] Illegal No. of args"
	echo "1st arg - path of train data."
  #echo "2nd arg - path of test data."
	exit
fi

# nav to working dir
train_dir="$1"
# test_dir="$2"
cd $train_dir

images=($(ls))
num_images=($(ls -F |grep -v / | wc -l))
count=0
for img in "${images[@]}"; do
  convert -resize 256x256\! $img "resized_$img"
  rm $img
  mv "resized_$img" $img
  ((count++))
  if [ $(($count%1000)) == 0 ]; then
    echo "$count out of $num_images completed ..."
  fi
done
