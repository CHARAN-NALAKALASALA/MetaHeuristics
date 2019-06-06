
for file in ../InstancesInt/*.full; do
  extname=${file##*/}
  name=${extname%%.*}
  python3 Calculation_Inferior.py $name
done
