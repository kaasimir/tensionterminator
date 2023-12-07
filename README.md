# Tension Terminator README

## 3 Installation Instructions

### 3.1 Database Installation

Before proceeding with the installation of the PostgreSQL Database, ensure that a database administration and management tool is installed. We recommend using "pgAdmin," but alternatives like DBeaver, Datagrip, or Navicat can also be used. Install pgAdmin by referring to [pgAdmin Download](https://www.pgadmin.org/download/).

1. Download the zip-file "BigBlock_01" and extract it to a chosen directory.
2. Run the "big_block_create_02.exe" on Windows or execute the Python code located in the "BigBlock_1" directory. On macOS, a compatibility tool like Wine or CrossOver is required for running the .exe.
3. During execution, provide your username and password, corresponding to the login data used to set up your database administration tool.

After these installations, you'll be able to retrieve data for the models in the subsequent steps. Refer to the Database and Data Collection Section 4.2.5 Version 4 for more details.

### 3.2 Technical Setup Installation

Follow these steps to retrieve the source code and create a working environment:

1. Ensure Python 3 or higher is installed. Install Python from [Python Downloads](https://www.python.org/downloads/).
2. Update the package installer for Python (pip) by referring to [pip Installation](https://pypi.org/project/pip/).
3. It is recommended to install the implementation in a virtual environment to avoid interference with your personal setup.

   - On Windows:
     ```bash
     cd path\to\your\project
     python -m venv venv
     venv\Scripts\activate
     ```

   - On macOS:
     ```bash
     cd path\to\your\project
     python3 -m venv venv
     source venv/bin/activate
     ```

   - For JupyterLab (using Anaconda):
     ```bash
     conda create --name myenv
     conda activate myenv
     ```

4. Clone the git repository using one of the following methods:

   - Command Line:
     ```bash
     cd path\to\your\project
     git clone https://github.com/kaasimir/tensionterminator.git
     ```

   - GitHub Desktop or IDE (e.g., PyCharm):
     Follow the steps provided in the relevant sections.

5. Navigate to the cloned repository and install dependencies:

   ```bash
   pip install -r requirements.txt  # Windows or macOS
   ```

   or

   ```bash
   conda install --file requirements.txt  # Anaconda/JupyterLab
   ```

Ensure that the requirements.txt file is present in your project folder. If not, download and place it manually.

### 3.3 Start Training Models

Once the database is installed, and the source code is retrieved, follow these steps:

1. Install all requirements.
2. To train existing models for existing classes:
   - Navigate to the "notebooks" directory.
   - Choose the specific directory (e.g., "tool_finder," "alternative_toolfinder," or "bodyside_finder").
   - Open "dataloader.ipynb" in the chosen directory and run the code.
   - After the dataloader is finished, open "datamodel.ipynb" and adjust the input dataset variable and the number of workers.
   - Refer to the provided documentation for available model setups.
   - Run the code.

### 3.4 Extend Current Setup with New Classes

Extend the current setup and train models for new classes by:

1. Navigate to the "db_builder" directory.
2. In the "db_handler," create new functions with file paths for the chosen new classes.
3. Navigate to the "notebooks" directory and define a new class directory.
4. Copy and paste "Dataloader" and "Datamodel" for the new classes, modifying parameters and variables accordingly.
5. Further details can be found in the Implementation Chapters and Sub-chapters of this paper.
