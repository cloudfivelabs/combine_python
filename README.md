## combine_python
Sample code to combine two CSV files as explained by this test:

#Test for Python developers

A CSV file contains quality metrics per module as follows:

````
module|density/KLOC,bugs,LOC,maxCCN,avgCCN
mod-a|0.0,0,778,8,1.68
mod-b|1.0,137,139048,75,2.20 
mod-c|0.4,1,2574,34,2.60
````
Notice that each module has 5 metrics associated with it. Also notice the file has a header record. Assume the unique identifier is the module name.

Write a Python script that will combine two files that conform to the above format sending the output to standard output.

Usage: combine.py <left> <right>

Where <left> and <right> are filenames.

The logic rules for combining the two files (left and right) are as follows:

1. If the module exists in both <left> and <right> files, then the combined record will look like this:
<module>|l1,l2,l3,l4,l5;r1,r2,r3,r4,r5
2. If the module only exists in the <left> file, then the combined record will look like this:
<module>|l1,l2,l3,l4,l5;,,,,
3. If the module only exists in the <right> file, then the combined record will look like this:
<module>|,,,,;r1,r2,r3,r4,r5
4. The combine.py script needs to be re-entrant - which means that the <left> file may be a previously combined file. For example, it needs to support the following scenario:

````
$ cat f1
module|density/KLOC,bugs,LOC,maxCCN,avgCCN
mod-a|0.0,0,778,8,1.68
mod-b|1.0,137,139048,75,2.20
~/t
````
````
$ cat f2
module|density/KLOC,bugs,LOC,maxCCN,avgCCN
mod-b|2.0,237,139048,75,2.20
mod-c|0.8,2,2574,34,2.60
~/t
````
````
$ combine.py f1 f2 | tee -a f1f2 module|density/KLOC,bugs,LOC,maxCCN,avgCCN;density/KLOC,bugs,LOC,maxCCN,avgCCN
￼￼￼￼￼￼￼￼mod-a|0.0,0,778,8,1.68;,,,, mod-b|1.0,137,139048,75,2.20;2.0,237,139048,75,2.20 mod-c|,,,,;0.8,2,2574,34,2.60
````
````
$ cat f3
module|density/KLOC,bugs,LOC,maxCCN,avgCCN mod-b|0.5,137,274048,75,2.20 mod-c|0.4,1,2574,34,2.60 mod-d|0.2,1,5074,34,2.60
~/t
````
````
$ combine.py f1f2 f3 module|density/KLOC,bugs,LOC,maxCCN,avgCCN;density/KLOC,bugs,LOC,maxCCN,avgCCN;density /KLOC,bugs,LOC,maxCCN,avgCCN
mod-a|0.0,0,778,8,1.68;,,,,;,,,, mod-b|1.0,137,139048,75,2.20;2.0,237,139048,75,2.20;0.5,137,274048,75,2.20 mod-c|,,,,;0.8,2,2574,34,2.60;0.4,1,2574,34,2.60
mod-d|,,,,;,,,,;0.2,1,5074,34,2.60
````