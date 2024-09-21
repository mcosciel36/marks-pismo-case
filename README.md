# Project Title
## Project Setup

To set up this project, follow these steps:

### 1. Install `asdf`

[`asdf`](https://asdf-vm.com/) is a version manager for managing multiple runtime versions.

```bash
# Clone the asdf repository
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.10.2
echo '. $HOME/.asdf/asdf.sh' >> ~/.bashrc
source ~/.bashrc

# Add the Python plugin for asdf
asdf plugin add python

# Install the required Python version
asdf install


# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Configure Poetry to create virtual environments in the project directory
poetry config virtualenvs.in-project true

# Install project dependencies
poetry install
