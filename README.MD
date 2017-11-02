## Example usage

- Requet rdns for network submitted as arguments. The following command queries o2 UK network which is mainly used for mobile customers
```
-ns=82.132.128.0 -ne=82.132.255.255
```

- Requet rdns for a file of newline separated list of IPs
```
-if=input_data/zeus_ipblocklist_2017-11-02.txt
```

- Requet rdns for a directory full of nirsoft csvs (see [Nirsoft Website](http://www.nirsoft.net/countryip/) and `download_nirsoft_lists.sh`)
```
-id=input_data/
```
