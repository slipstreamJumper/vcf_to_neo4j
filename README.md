# vcf_to_neo4j
Take a physical folder full of .vcf contact cards and outputs a script that for a fresh neo4J graph database.


Execution is simple. 

Step 1. Export all VCF (windows contacts) into a folder.
Step 2. Copy converter script into the same folder.
Step 3. Run script (command line prefered)
  3a. Script takes not arguments or flags
Step 4. Script will output "contacts_output.csv" which is a series of neo4J commands
Step 5. Run script in a fresh neo4J database
Step 6. ???
Step 7. PROFIT!
