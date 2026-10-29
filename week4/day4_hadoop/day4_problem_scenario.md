## Problem Scenario:
```
There is a parent organization called “Acmeshell Group”, which has two child companies named QuickTechie and BlueWorld . Both the company’s employee information is given in two separate text file as below.
Quicktechie.txt
1, Michael, California
2, Kris, London
3, Martin, Hong Kong
4, Carol, Canada
5, Sita, India

Blueworld.txt
6, John, New York
7, Ben, London
8, Carl, Tokyo
9, Smith, Singapore
10, Will, Jordon
```
## Questions
### Ques 1 : Which command will you use to check all available command line options on HDFS
```linux
hdfs --help
```
## Ques 2: Get help on individual commands.
```linux
hdfs dfs -help
hdfs dfs -help put
hdfs dfs -help get
hdfs dfs -help ls
```
## Ques 3: Create a new empty directory named Employee using command line on hdfs.
```linux
hdfs dfs -mkdir -p /Employee
hdfs dfs -mkdir /Employee
```
- with p - creates Employee if needed; succeeds if it already exists.
- without p - creates Employee; returns an error if it already exists.

## Ques 4 and 5: Create a files named quicktechie.txt and Blueworld.txt with the data on local system.
```linux
cd /home/training

cat > quicktechie.txt <<EOF
1, Michael, California
2, Kris, London
3, Martin, Hong Kong
4, Carol, Canada
5, Sita, India
EOF

cat > Blueworld.txt <<EOF
6, John, New York
7, Ben, London
8, Carl, Tokyo
9, Smith, Singapore
10, Will, Jordon
EOF
```
Check that both local files exist:
```linux
ls -l /home/training
```
## Ques 6: Put both the files using command line in hdfs.
```
- Open Hue and select File Browser.
- Navigate to /Employee.
- Look for Upload, New, a + icon, or an Actions menu.
- Select quicktechie.txt and Blueworld.txt from /home/training if the upload dialog can access that directory.
- Confirm the upload.
```
## Ques 7: Merge all the files in Employee directory and name it as MergedEmployee.txt
```linux
hdfs dfs -getmerge /Employee /home/training/MergedEmployee.txt

hdfs dfs -put /home/training/MergedEmployee.txt /Employee/
```
## Ques 8: Read the content of the file.
```linux
hdfs dfs -cat /Employee/MergedEmployee.txt
```
## Ques 9: Copy the file using command line and make a new file named Copied.txt in local.
```linux
hdfs dfs -cp /Employee/MergedEmployee.txt /Employee/Copied.txt

hdfs dfs -get /Employee/Copied.txt /home/training/Copied.txt

cat /home/training/Copied.txt
```
## Ques 10: Add content in the new file created using Hue.
```
In Hue:
1. Open File Browser and navigate to /Employee.
2. Use the available create/edit option.
3. Add the following record:
- 11, Alex, Germany
4. Save the updated file in HDFS.
```
## Ques 11. Get the file back from HDFS to local file system.
Using the Hue interface:
1. Navigate to /Employee.
2. Select MergedEmployee.txt.
3. Look for Download in the file actions or menu.
4. Download it and save it under /home/training if your browser and environment permit saving to that directory.

or

```linux
hdfs dfs -get /Employee/MergedEmployee.txt /home/training/MergedEmployee.txt
```
## Useful Info:
```
Operation	            Command

Local → HDFS	        hdfs dfs -put localfile /Employee/
HDFS → Local	        hdfs dfs -get /Employee/file /home/training/
View HDFS file	        hdfs dfs -cat /Employee/file
Merge HDFS files	    hdfs dfs -getmerge /Employee /home/training/MergedEmployee.txt
Copy within HDFS	    hdfs dfs -cp source destination
```


