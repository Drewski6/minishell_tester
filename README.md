# minishell_tester
A tester for minishell made in python

This tester uses {https://docs.google.com/spreadsheets/d/1uJHQu0VPsjjBkR4hxOeCMEt3AOM1Hp_SmUzPFhAH-nA/edit#gid=0} this spreadsheet 

# USE

- This tester takes data from the above spreadsheet, parses it and runs both your ./minishell and bash and shows the difference in outputs.
	- In this case, it's recommended to redirect the output to a file to make saving and finding test results easier.
- If no positional arguments are given, the tester will test every case in the spreadsheet. 
```
python3 testing_msh.py > test.log
```
- Outputs are compared with STDOUT, STDERR, and Return Value by default but you can remove checks with the flags --no_stdout (-no), --no_stderr (-ne), and --no_return (-nr) respectively.
```
python3 testing_msh.py -no -ne > test.log		### only prints diff of Return results.
```
- If one positional argument is given (as an integer) only one test will be run
```
python3 testing_msh.py 515		### test only test 515 and output to terminal.
```
- If two positional arguments are given (as integers), the test will inclusively run the range of tests given. 
```
python3 testing_msh.py 515 517		### run tests 515, 516 and 517 and print to terminal.
```

# Installation:

1. Git clone this repo to wherever you'd like
2. Use conda (Anaconda) to install packages (Optional):
	i.	Install conda environment to use this environment using the environment.yml file:

	```
	conda env create -f environment.yml
	```
	ii.	You can activate the environment with:

	```
	conda activate msh_test
	```

3. Otherwise, you can install the required dependencies to your default python3 with:

	```
	pip install pandas
	pip install openpyxl
	```

	This should install the needed dependencies in your default python environment.
4. Edit the testing_msh.py file and set the cwd path to the absolute path of your minishell project folder.
5. Download the tester spreadsheet [HERE]{https://docs.google.com/spreadsheets/d/1uJHQu0VPsjjBkR4hxOeCMEt3AOM1Hp_SmUzPFhAH-nA/edit#gid=0} as an xlsx file and place in the same directory as testing_msh.py.
6. Reame your xlsx file to "unit_tests.xlsx"
7. Run the tester. SEE ABOVE INSTRUCTIONS ON "USE"
8. Check your output for output information
9. When you're finished if you're using conda, you can exit your conda environment with:

	```
	conda deactivate
	```

# ToDo:
	1. add a check for sections so the user can select if they want to check bonuses or not.
