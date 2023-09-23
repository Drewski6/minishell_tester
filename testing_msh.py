## IMPORTS
import pandas as pd
import subprocess as sp


## SETTINGS
testing_file = "unit_tests.xlsx"
minishell_path = "./minishell"
cwd = "/home/drew/Documents/ecole_42/minishell"
bash_path = "bash"
ignore_list = [601 - 2]
start = 700 - 2  # start = 28 - 2 # actual start
end = 709 - 2  # end = 769 - 2 # actual end
tests_conducted = 0
tests_succeeded = 0
files_to_delete = [
    "dir",
    "a",
    "b",
    "bonjour*",
    "c",
    "d",
    "e",
    "hey",
    "hola*",
    "'$HOLA'",
    "HOLA",
    "ls1",
    "pwd",
    "srcs/hello",
    "srcs/bonjour",
]


def tab_form(check):
    return str(check).replace("\n", "\n\t\t\t")


def p_form(check):
    if check:
        return ">>>>"
    else:
        return "    "


def cleanup_test_files(files_to_delete):
    if files_to_delete:
        sp.run(
            f'rm -rf {" ".join(files_to_delete)}',
            shell=True,
            cwd=cwd,
        )


def print_results(tests_conducted, tests_succeeded):
    print("\n\n*******************\n\n")
    print(f"Total tests: {tests_conducted}")
    print(f"Successes  : {tests_succeeded}")
    print(f"Percentage : {tests_succeeded / tests_conducted * 100:.2f}%")


def run_test(test):
    stdoutdiff = False
    stderrdiff = False
    returndiff = False
    result_msh = sp.run(
        f"echo '{test}' | {minishell_path}",
        shell=True,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        text=True,
        cwd=cwd,
    )
    result_bash = sp.run(
        f"echo '{test}' | {bash_path}",
        shell=True,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        text=True,
        cwd=cwd,
    )
    if result_msh.stdout != result_bash.stdout:
        stdoutdiff = True
    if result_msh.stderr != result_bash.stderr:
        stderrdiff = True
    if result_msh.returncode != result_bash.returncode:
        returndiff = True
    if not stdoutdiff and not stderrdiff and not returndiff:
        print(" OK!")
        return 0
    else:
        print("\n****RESULTS MINISHELL****")
        print(f"    test:\t{tab_form(test)}")
        print(f"{p_form(stdoutdiff)}stdout: {tab_form(result_msh.stdout)}")
        print(f"{p_form(stderrdiff)}stderr: {tab_form(result_msh.stderr[:-1])}")
        print(f"{p_form(returndiff)}return: {tab_form(result_msh.returncode)}")

        print("\n****RESULTS BASH****")
        print(f"    test:\t{tab_form(test)}")
        print(f"{p_form(stdoutdiff)}stdout: {tab_form(result_bash.stdout)}")
        print(f"{p_form(stderrdiff)}stderr: {tab_form(result_bash.stderr)}")
        print(f"{p_form(returndiff)}return: {tab_form(result_bash.returncode)}\n")
    return 1


df = pd.read_excel(testing_file)

for line in range(start, end):
    if line in ignore_list:
        continue
    print(f"TEST {line + 2}", end="")
    test_col = 1
    bash_col = 7
    tests = [
        i[3:] if i[:3] == "$> " else i for i in df.iloc[line, test_col].split("\n")
    ]
    test = "\n".join(tests)
    test += "\n"
    bash = df.iloc[line, bash_col]
    i = line
    tests_conducted = tests_conducted + 1
    if not run_test(test):
        tests_succeeded = tests_succeeded + 1

cleanup_test_files(files_to_delete)
print_results(tests_conducted, tests_succeeded)
