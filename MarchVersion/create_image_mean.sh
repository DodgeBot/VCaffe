#!/usr/bin/env sh
# Compute the mean image from the imagenet training lmdb
# N.B. this is available in data/ilsvrc12


# need for 1 args
if [ $# -ne 2 ]; then
	echo "[Err] Illegal No. of args"
	echo "1st arg - path of lmdb data."
  echo "2nd arg - path of target image mean binary."
	exit
fi

# nav to working dir
lmdb="$1"
target_path="$2"

TOOLS=/home/fyp/FYP/caffe-master/build/tools

$TOOLS/compute_image_mean $lmdb \
  $target_path/image_mean.binaryproto

echo "Done."
