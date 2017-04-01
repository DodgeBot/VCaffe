# FYP Version Caffe
Use data collected from the IMUxVideo app, process it as image-label, and randomly split as training and test

### Naming convention
Refer to the IMUxVideo app for naming convention. E.g. 
* 170118T210516video.mov
* 170118T210516X170118T210525data.csv
* 170118T210516X170118T210525info.txt

### prepData.sh
```
chmod 755 prepData.sh
vi prepData.sh
```
change the script path
`path/to/prepData.sh path/to/data/`

### video2img.py
`python video2img.py -i /path/to/video -o /path/to/framesOutPutFolder`
