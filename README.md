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
6. Name the downloaded spreadsheet "unit_tests.xlsx"
7. Run the tester:

```
python3 testing_msh.py > test.log
```

8. check your test.log for output information
9. Some notes about the log file:
	1. The test number is the same number as the row number in the spreadsheet.
	2. Some tests are excluded and these are located in the ignore_list because they cause issues with the tester. You can add tests to this list if you like.
10. When you're finished you can exit your conda environment with:

```
conda deactivate
```

# ToDo:
	1. add a check for sections so the user can select if they want to check bonuses or not.
