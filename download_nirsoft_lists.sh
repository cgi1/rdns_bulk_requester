

curl http://www.nirsoft.net/countryip/ > list_of_countries.html
cat list_of_countries.html | grep '<td><a href="' | awk -F 'href="' {'print $2'} | awk -F '.html' {'print $1'} > country_codes.txt

cat country_codes.txt | while read line
do
    curl http://www.nirsoft.net/countryip/$line.csv > networks_$line.csv
done



echo 'your_custom_escaped_content' > temp_file.csv
cat testfile.csv >> temp_file.csv
mv temp_file.csv testfile.csv


echo "NET_START,NET_END,TOTAL_IPS,ASSIGN_DATE,OWNER" > headerfile
for csv in *.csv; do cat headerfile $csv > tmpfile2; mv tmpfile2 $csv; done
rm headerfile