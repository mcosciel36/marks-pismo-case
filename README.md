# Pisms Case
## Project Setup

- I'm using python 3.9.5 for this project. 
- To set up this project with pyenv and virtualenv, use **Method 1**
- If you want to try asdf and poetry, see **Method 2** below. 
### Note that these instructions for installing the python version and it's dependencies may not be perfect.  You may hit some bumps along the way.   Do your best to achieve the following:
- The goel for a proper setup is to:
    - Startup a virtual environment with python 3.9.5
    - Install the python dependencies
    - However you choose to do this is up to you.   
    - You can try my **Method 1** or **Method 2** or some other method you prefer. 
    - I've included both a **requirements** file and a **pyproject.toml** file. 
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
pip install -r requirements.txt
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

## If using vscode, you need to point to this virtual environment. 
- You can copy and paste the "Executable** path from the above **poetry env info** command into your command pallette virtual env path. 
- If using virtualenv, you can do the same.  Copy the path to the env into your vscode virtual env path.
- In vscode, the **__pycache__** folder gets created at this point. 

## Running the faker_script_dupes2.py:
```bash
# click on the "faker_script_dupes2.py" file and hit the play button in vs code
# or do the following:
cd src/pismo_case
python faker_script_dupes2.py       # The events.json gets created with dupes
```
# Now run the pyspark script that will read in this events.json file and then: 
- Output files in Parquet format.
- Keep only the latest version for duplicate events.
- In the output directory we use partitioning by event date (year, month, day) and
event type.
```bash
# Click on the pyspark_script.py and hit play in vscode
# or
cd src/pismo_case
python pyspark_script.py
```

# Run the pytests
- **test_partitioning.py** tests the partitioning strategy
- **test_faker_script** tests the dataset model created and the dupes are created