# Vetspire ETL Technical Challenge

### Context

Data extraction and manipulation is a mainstay in the DataSync team here at Vetspire. We regularly deal with data from a host of sources, each one different and unpredictable. Clients depend on our ability to quickly identify patterns and execute on them to ensure our extractions and imports are not only correct, but constistent and reliable.

Included is a file named `client_data.bin`. It is a file containing serialized, and potentially obfuscated client data. In order for us to extract this data properly, we need to understand the method of serialization. In doing so we can then parse the necessary fields, extract the data, and store it for future use. 

### Criteria

1. **Determine Serialization Method:**
   - Analyze the `client_data.bin` file to determine the method of serialization used. Look for patterns, field structures, or any characteristics that may indicate the serialization approach.

2. **Deserialization/Extraction:**
   - Write a script that deserializes, parses, and extracts the data from `client_data.bin`. Use any language(s) and libraries you see fit!

3. **CSV:**
   - Load the data into a CSV with the following fields:
      - ID
      - Email
      - Date of Birth
      - Is Active
      - Phone Number
      - First Name
      - Last Name
      - Postal Code

Please submit a PR to this repo, building a solution that satisifies this criteria. Included should be your source code, the generated CSV, and documentation containing execution instructions, design decisions, challenges, assumptions, etc.

We don't expect you to spend more than two hours on the task.

**Don't worry about completing the task, if you run out of time. We're still interested to see what you come up with. Documentation of your thought process goes a long way.**

Good luck!
