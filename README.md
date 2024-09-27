# Pismo Case


## Summary
- This code generates test data in json format.
- It creates duplicate records that need to be excluded in the output directory.  Only the latest unique records should be kept. 
- Spark reads the json data into a dataframe, pulls the latest versions of each record and writes out to a directory using hive partitioning strategy. 

# Project Setup

- I'm using python 3.9.5 for this project. 
- To set up this project with pyenv and virtualenv, use **Method 1**
- If you want to try asdf and poetry, see **Method 2** below. 
### Note that these instructions for installing the python version and its dependencies may not be perfect.  You may hit some bumps along the way.   Do your best to achieve the following:
- The goal for a proper setup is to:
    - Startup a virtual environment with python 3.9.5.
    - Install the python dependencies.
        - However you choose to do this is up to you.   
    - You can try my **Method 1** or **Method 2** or some other method you prefer. 
    - I've included both a **requirements-dev.txt** file and a **pyproject.toml** file. 
    - It is up to you to either use pip or poetry to install the dependencies. 


## Method 1: virtualenv and pip
```bash
# Install Python 3.9.5 using pyenv if you're already using pyenv
pyenv install 3.9.5
pyenv local 3.9.5

# Create the virtual environment with "virtualenv" if you're already using virtualenv
pyenv virtualenv 3.9.5 myenv
ls ~/.pyenv/versions/myenv
pyenv activate myenv
pip install -r requirements-dev.txt

# Or you can try venv as an alternative to pyenv
# Insure you're using python 3.9 before using this alternative
python -m venv test-env
source test-env/bin/activate
pip install -r requirements-dev.txt
```

## Method 2: asdf and poetry:
I prefer to use asdf and poetry.   
- You'll see there's a .tools-versions file in the root dir.   
- This file is referenced when you run **asdf install**.   
- Python 3.9.5 is defined in the .tools-versions file.   
- This is how asdf install will know to install python 3.9.5.

### Install asdf
```bash
# Clone the asdf repository
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.10.2
echo '. $HOME/.asdf/asdf.sh' >> ~/.bashrc
source ~/.bashrc

# Add the Python plugin for asdf
asdf plugin add python

# Install the required Python version
asdf install
python          # should startup a python 3.9.5 repl
ctrl-d          # exit from the repl
```

### Install Poetry
```bash
curl -sSL https://install.python-poetry.org | python3 -

# Configure Poetry to create virtual environments in the project directory
poetry config virtualenvs.in-project true

# Install project dependencies
poetry env info                         # will show "NA" for "Path" and "Executable"
poetry install --with dev --no-root
poetry env info                         # will now show the Path and Executable
# Your poetry env should now be created
poetry shell                            # to enter the poetry virtual environment
pip freeze |grep pyspark                # you should see pyspark==3.5.2
```

### If using vscode, you need to point to this virtual environment. 
- You can copy and paste the "Executable** path from the above **poetry env info** command into your command palette virtual env path. 
- If using virtualenv, you can do the same.  Copy the path to the env into your vscode virtual env path.

# Code Execution
## Running the faker_script_dupes2.py:
```bash
# click on the "faker_script_dupes2.py" file and hit the play button in vs code
# or do the following:
python ./src/pismo_case/faker_script_dupes2.py  # The /src/pismo_case/events.json gets created with dupes
```
**Note:** The faker script is configured to create 10 records with a duplication ration of 50%.  You may want to set this to something like 1000 and 0.1 to get a larger sample.   A larger sample is needed in order to see that we've properly broken out data into year, month, day and event_type.  If the sample is too small you may not see different event types getting created on the same, randomly selected day.   
You can modify this in this line of code:

```bash
# Generate the events
events = generate_events(num_events=10, duplicate_ratio=0.5)
```
**Note** The faker script uses a seed for repeatability.   But, if and when you change the above line of code, the repeatability is changed based on the new parameters.   If the code changes there's no guarantee the **test_parquet_partitioning** test will pass.  
I've verified it does pass for num_events = 10 or 1000 and duplicate_ratio = 0.5 or 0.1 correspondingly.   If you change to some other values you will need to modify the **test_parquet_partitioning** to reflect any specified year, month, day, event type that is found in the output_directory.  It's very easy to modify this test.  You'll see what i'm talking about and how to change it when you look at the test. 

## Now run the pyspark script that will read in this events.json file and then: 
- Output files in Parquet format.
- Keep only the latest version for duplicate events.
- In the output directory we use partitioning by event date (year, month, day) and
event type.
```bash
# Click on the pyspark_script.py and hit play in vscode
# or
python ./src/pismo_case/pyspark_script.py   # The output_director gets created
```

## Run the pytests
- **test_partitioning.py** tests the partitioning strategy is correct in the output_directory.
- **test_faker_script_dupes2.py** tests the dataset model created is correct.  It also tests that dupes are created.
- **test_dedupe_pyspark_script.py** tests that dupes are removed keeping only the latest.
- There's also a **pyspark_script_verify.py** that can be used to read in from the .**output_directory** to verify the output data.  I read in the parquet and write out json for readability.


# Contact Info
If you have any questions or need assistance, you can contact me through [LinkedIn Profile](https://github.com/mcosciel36/marks-pismo-case)
