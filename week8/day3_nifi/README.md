# Apache NiFi Lab --- CSV to JSON Conversion

## Lab Overview

**Objective:** Build and run an Apache NiFi flow that reads a CSV file,
converts its records to JSON, and saves the result.

**Flow:**

``` text
GetFile → ConvertRecord → PutFile
```

------------------------------------------------------------------------

## Task 1. Prepare the input CSV file

**What was required:** Prepare a CSV file to use as input for the NiFi
flow.

**What I did:**

Created `people.csv` with the following data:

``` csv
name,age,city
Asha,29,Mumbai
Rahul,34,Pune
```

The file was stored on the host machine in:

``` text
./nifi-input/people.csv
```

## Task 2. Configure the GetFile processor

**What was required:** Configure NiFi to read the input file from the
input directory.

**What I did:**

Added and configured the `GetFile` processor.

  Property           Value
  ------------------ -------------------
  Input Directory    `/tmp/nifi-input`
  Keep Source File   `false`
  Run Schedule       `0 sec`

**What this processor does:** `GetFile` monitors the specified
directory, retrieves files, and creates FlowFiles for the next
processor. With `Keep Source File = false`, the original file is removed
from the input directory after it is picked up successfully.

## Task 3. Configure the ConvertRecord processor

**What was required:** Convert the input records from CSV format to JSON
format.

**What I did:**

Added the `ConvertRecord` processor and configured its Controller
Services.

### CSVReader --- Record Reader

  Setting                      Value
  ---------------------------- --------------------------
  Schema Access Strategy       `Infer Schema`
  Treat First Line as Header   `true` (where available)

**Purpose:** `CSVReader` reads the incoming CSV data and interprets its
rows as records. The first row contains the field names: `name`, `age`,
and `city`.

### JsonRecordSetWriter --- Record Writer

Selected `JsonRecordSetWriter` as the Record Writer.

**Purpose:** `JsonRecordSetWriter` writes the records in JSON format.

### ConvertRecord properties

  Property                        Value
  ------------------------------- ------------------------
  Record Reader                   Configured `CSVReader`
  Record Writer                   `JsonRecordSetWriter`
  Include Zero Record FlowFiles   `true`

Both Controller Services were enabled.

**What this processor does:** `ConvertRecord` uses the reader to
interpret the CSV input and the writer to produce JSON output.

## Task 4. Configure the PutFile processor

**What was required:** Save the converted data to the output directory.

**What I did:**

Added and configured the `PutFile` processor.

  Property                       Value
  ------------------------------ --------------------
  Directory                      `/tmp/nifi-output`
  Conflict Resolution Strategy   `replace`

**What this processor does:** `PutFile` writes the FlowFile content to
the specified directory. The `replace` strategy allows an existing file
with the same name to be overwritten.

**Note:** `ConvertRecord` changes the file content, but does not
automatically change its filename. Therefore, the output file was named
`people.csv`, although its content was JSON.

## Task 5. Connect and run the processors

**What was required:** Connect the processors and run the data flow.

**What I did:**

Connected the processors in this order:

``` text
GetFile → ConvertRecord → PutFile
```

Started all three processors:

-   `GetFile`
-   `ConvertRecord`
-   `PutFile`

All three processors showed the **Running** status.

## Task 6. Copy the input file into the NiFi Docker container

**What was required:** Make the input CSV file available inside the NiFi
container.

**What I did:**

The input directory was inside the Docker container and was not
bind-mounted from the host. I copied the file into the container using:

``` bash
docker cp ./nifi-input/people.csv nifi:/tmp/nifi-input/people.csv
```

The terminal confirmed that 42 bytes were copied successfully.

## Task 7. Check the output

**What was required:** Verify that NiFi created the output file and
converted the CSV data into JSON.

**What I did:**

First, listed the contents of the output directory:

``` bash
docker exec nifi ls -lh /tmp/nifi-output
```

The output directory contained `people.csv`. Its size was 86 bytes.

Then, checked the file content:

``` bash
docker exec nifi cat /tmp/nifi-output/people.csv
```

**Actual output:**

``` json
[
  {"name":"Asha","age":"29","city":"Mumbai"},
  {"name":"Rahul","age":"34","city":"Pune"}
]
```

**Verification:** The output is valid JSON containing the two records
from the original CSV file. This confirms that the conversion worked.

## Final Result and Conclusion

The NiFi flow successfully converted the input data from CSV to JSON.

  Processor / Service   Role in the lab
  --------------------- -----------------------------------------------------
  GetFile               Reads the input CSV file
  CSVReader             Reads and interprets CSV records
  ConvertRecord         Converts records from CSV format to JSON format
  JsonRecordSetWriter   Writes records in JSON format
  PutFile               Saves the converted content to the output directory

**Conclusion:** The lab was completed successfully. The input file
`people.csv` was read by GetFile, converted to JSON by ConvertRecord,
and saved by PutFile in `/tmp/nifi-output`.

**Important observation:** The output file kept the `.csv` filename
extension, but its content was JSON. If the assignment requires a
`.json` filename, the filename must be changed separately.
