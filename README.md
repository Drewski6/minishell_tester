# minishell_tester
A tester for minishell made in python

This tester uses {https://docs.google.com/spreadsheets/d/1uJHQu0VPsjjBkR4hxOeCMEt3AOM1Hp_SmUzPFhAH-nA/edit#gid=0} this spreadsheet 

# Installation:

1. Git clone this repo to wherever you'd like
2. Install conda if you don't already have it (Optional)
3. Install conda environment to use this environment using the environment.yml file:

```
conda env create -f environment.yml
```

Otherwise, you can use:

```
pip install pandas
pip install openpyxl
```

This should install the needed dependencies in your default python environment.
You can activate the environment with:

```
conda activate msh_test
```

4. Edit the testing_msh.py file and set the cwd path to the absolute path of your minishell project folder.
5. Download the tester spreadsheet [HERE]{https://docs.google.com/spreadsheets/d/1uJHQu0VPsjjBkR4hxOeCMEt3AOM1Hp_SmUzPFhAH-nA/edit#gid=0} as an xlsx file and place in the same directory as testing_msh.py
6. Run the tester:

```
python3 testing_msh.py > test.log
```

8. check your test.log for output information
