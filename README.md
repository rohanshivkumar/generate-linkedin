# generate-linkedin
* Updated to work with glassdoor's login *

Searches for jobs in certain locations from glassdoor, finds LinkedIn of potential connections related to the job searched for.
Writes to .csv file in the directory of download in the format jobname-location-results.csv(Example: tech support-san jose-job-results.csv)

Requires python 3.6 to be installed on system with PATH variable set.

INSTALLATION

* Clone or Download the repository to a folder.

* In command prompt, navigate to the folder and run the following command:
    pip install -r requires.txt
    
* Open up "generatelinkedin.py" in a text editor and edit lines 12,13,14,15 to match your google API key, custom search engine ID, your glassdoor email login and password respectively
(
    my_api_key = "" #Enter Your Google API Key
    my_cse_id = ""  #Enter Your Google Custom Search Engine ID
    my_glassdoor_email = "" #Enter your glassdoor email ID
    my_glassdoor_pass = "" #Enter your glassdoor password
    
)


USAGE 

Windows: Double click "generatelinkedin.py" file to run the file.
            OR
        In command line run "python path/to/generatelinkedin.py" (Replace path/to/ with the actual path of your download file)

Mac OSX: Right click and open with Python Launcher to run the file.
           OR
        In command line run "python path/to/generatelinkedin.py" (Replace path/to/ with the actual path of your download file)

Linux: In command line run "python path/to/generatelinkedin.py" (Replace path/to/ with the actual path of your download file)

Enter job name and location in appropriate entry boxes and press "Find jobs" button.

