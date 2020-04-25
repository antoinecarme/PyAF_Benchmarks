for f in `echo ../pyaf/logs/YAH*`
do
g=`basename $f`
echo $f $g
mkdir $g
cp $f/*.log INTERNAL/YAHOO_STOCKS/$g/
done


