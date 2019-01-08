# generate-linkedin
Searches for jobs in certain locations from glassdoor, finds LinkedIn of potential connections related to the job searched for.
Writes to .csv file in the directory of download in the format jobname-location-results.csv(Example: tech support-san jose-job-results.csv)

Requires python 3.6 to be installed on system with PATH variable set.

INSTALLATION

Clone or Download the repository to a folder.
In command prompt, navigate to the folder and run the following command:
    pip install -r requires.txt
Open up "generatelinkedin.py" in a text editor and edit lines 12 and 13 to match your google API key and your custom search engine ID
(
    my_api_key = "" #Enter Your Google API Key
    my_cse_id = ""  #Enter Your Google Custom Search Engine ID
)


USAGE 

Windows: Double click "generatelinkedin.py" file to run the file.

Mac OSX: Right click and open with Python Launcher to run the file.

Linux: In command line run "python path/to/generatelinkedin.py" (Replace path/to/ with the actual path of your download file)
Enter job name and location in appropriate entry boxes and press "Find jobs" button.

