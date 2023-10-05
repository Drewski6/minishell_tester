## IMPORTS ##
import pandas as pd
import subprocess as sp
import argparse
import pdb
import re

## SETTINGS ##
testing_file = "unit_tests.xlsx"
minishell_path = "./minishell"
cwd = "/mnt/nfs/homes/dpentlan/Documents/ecole_42/minishell"
bash_path = "bash"
offset = 2  # offset is used so that the pandas row number
# and the actual row number are the same.
# This makes looking up tests easier.
start = 28 - offset  # start = 28 - 2 # actual start is row 26
end = 770 - offset  # end = 770 - 2 # actual end is row 769
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
    "ls",
    "hey",
    "hola*",
    "'$HOLA'",
    "HOLA",
    "ls1",
    "pwd",
    "srcs/hello",
    "srcs/bonjour",
]
ignore_list = [i - offset for i in 
[
224,231,232,236,244,245,246,247,263,266,267,268,271,272,273,274,275,276,277,278,283,286,287,292,298,316,318,319,331,332,384, #env to the ignore list, only this one cd test is failing with -ne
 459, #does chmod 000 on minishell rendering all tests failure afterwards
 28, #tests :
 29,364, #tests !
 282, #tests job control (&)
 47,48,49,347,704, #tests escaped character (\)
 61,62,63,284,348, #tests semicolon (;)
 64,65,66,280,281,601,602,603,604,613,614,615,616,617,618,628, #tests bonus feature (parens)
 72,73,149, #tests wildcards not in cwd (*/*)
 74,681, #tests . (source)
 76,367,444,445,446,472, #tests ~ (expands to value of HOME)
 77,78, # tests local vars (FOO=BAR)
 94,118,128,249,255,256,279, # tests escaped character (\n \$ \\ ...)
 124, # tests shell args ($9)
 150,153,154,155,165,166,167,170,171,730,305,306, # tests the gettext feature ($"SOMETHING")
 211,212,213,214,215,216,217,218,219,220,221,222,223, #tests with signals, need to be done manually (^C/^D)
 387,735, # requires manual testing
 225,226,227,228,229,230,471, # tests env with argument(s)
 470,469,           # env with options
 233,234,235,237, # tests UB (Yes really ! check the man !)
 386, # tests history
 392,393,394,395,# tests pwd with options
 455,456,457,458, # idk spreadhseet says these are unhandled
 58,59,60,558,575,576,577,578,579,580,581,582,583,584,585,586,585,586,587,588,589,590,591,592,593,594,594,595,596,597,598,599,600,605,606,607,608,609,610,611,612,619,620,621,622,623,624,625,626,627,629,630,631,632,633,634,635,636,637,638,639, #tests bonus feature (&&/||)
250, 251,   # export with options.
355,        # unset with options
761,        # super heredoc
726,        # race condition
641,        # too hard to test lol
463,        # $SHLVL 
423,424,    # //
146,126,122        # special variables in bash
]]

valgrind_ignore_list = [i - offset for i in 
[
459,
537, 538 # contain the command ifconfig which apparently leaks
]]
#still included
# 71,129,140,141,142,143,144,145,146,147,148,149,447,448,449,764,765,766,767,768,769, #tests bonus feature (wildcard)
# 

def tab_form(check: str):
    return str(check).replace("\n", "\n            ")


def line_form(check: bool):
    if check:
        return ">>>>"
    else:
        return "    "


def cleanup_test_files(files_to_delete: list[str]):
    if files_to_delete:
        sp.run(
            f'rm -rf {" ".join(files_to_delete)}',
            shell=True,
            cwd=cwd,
        )


def print_results(tests_conducted: int, tests_succeeded: int):
    print("\n*******************\n")
    print(f"Total tests: {tests_conducted}")
    print(f"Successes  : {tests_succeeded}")
    print(f"Percentage : {tests_succeeded / tests_conducted * 100:.2f}%")




def single_test(test, command):
    result = sp.run(
        f"echo '{test}' | {command}",
        shell=True,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        text=True,
        cwd=cwd,
    )
    result.stderr = re.sub(r"bash: line \d*:", "shell:", result.stderr)
    result.stderr = re.sub(r"^minishell:", "shell:", result.stderr)
    return result


def run_test(test: str):
    result_msh = single_test(test, minishell_path)
    result_bash = single_test(test, bash_path)
    stdoutdiff = args.no_stdout and (result_msh.stdout != result_bash.stdout)
    stderrdiff = args.no_stderr and (result_msh.stderr != result_bash.stderr)
    returndiff = args.no_return and (result_msh.returncode != result_bash.returncode)
    print(f"TEST {line + offset}", end="")
    if not stdoutdiff and not stderrdiff and not returndiff:
        print(" OK!")
        return True
    else:
        print(f" Error!\n\n{test}")
        print("    RESULTS MINISHELL")
        print(f"{line_form(stdoutdiff)}stdout: {tab_form(result_msh.stdout)}")
        print(f"{line_form(stderrdiff)}stderr: {tab_form(result_msh.stderr[:-1])}")
        print(f"{line_form(returndiff)}return: {tab_form(str(result_msh.returncode))}")

        print("\n    RESULTS BASH")
        print(f"{line_form(stdoutdiff)}stdout: {tab_form(result_bash.stdout)}")
        print(f"{line_form(stderrdiff)}stderr: {tab_form(result_bash.stderr)}")
        print(
            f"{line_form(returndiff)}return: {tab_form(str(result_bash.returncode))}\n"
        )
    return False


def run_test_valgrind(test: str, line: int):
    result_msh = single_test(test, f"valgrind --leak-check=full --track-origins=yes --track-fds=yes --trace-children=yes --show-leak-kinds=all --suppressions=/mnt/nfs/homes/dpentlan/Documents/ecole_42/minishell/supp.supp {minishell_path}")
    print(f"\nTEST {line + offset}", end="")
    print(f"\n\n{test}")
    print(result_msh.stderr)
    for line in result_msh.stderr.split("\n"):
        if ("definitely lost" in line or "indirectly lost" in line or "possibly lost" in line or "still reachable" in line or "Open file descriptor " in line) and " 0 " not in line:
            if args.valgrind_stderr:
                return False
    print(f"RETURN: {result_msh.returncode}")
    print("*", end="", flush=True)
    return True


def get_test_input(line: int):
    tests = [
        i[3:] if i[:3] == "$> " else i for i in df.iloc[line, test_col].split("\n")
    ]
    test = "\n".join(tests)
    test += "\n"
    return test


def test_select(line):
    test = get_test_input(line)
    if args.valgrind or args.valgrind_stderr:
        if run_test_valgrind(test, line):
            cleanup_test_files(files_to_delete)
            return True
        else:
            print(f"test {line + 2} Failed valgrind")
            cleanup_test_files(files_to_delete)
            return False
    elif run_test(test):
        cleanup_test_files(files_to_delete)
        return True
    cleanup_test_files(files_to_delete)
    return False


parser = argparse.ArgumentParser(description="A tester for minishell.")
parser.add_argument(
    "arg1",
    type=int,
    nargs="?",
    default=-1,
    help="An integer value of the specific test you'd like to perform, or starting test if another integer is given.",
)
parser.add_argument(
    "arg2",
    type=int,
    nargs="?",
    default=-1,
    help="If a first integer is given, second integer indicates last test to exec.",
)
parser.add_argument(
    "--no_stdout",
    "-no",
    action="store_false",
    help="test will skip comparisons to stdout."
)
parser.add_argument(
    "--no_stderr",
    "-ne",
    action="store_false",
    help="test will skip comparisons to stderr."
)
parser.add_argument(
    "--no_return",
    "-nr",
    action="store_false",
    help="test will skip comparisons to return."
)
parser.add_argument(
    "--valgrind",
    "-vg",
    action="store_true",
    help="test will run in valgrind."
)
parser.add_argument(
    "--valgrind_stderr",
    "-vge",
    action="store_true",
    help="test will run in valgrind and print valgrinds error info."
)
args = parser.parse_args()
df = pd.read_excel(testing_file)
test_col = 1
bash_col = 7
if args.arg1 >= 26 and args.arg1 <= 769 and args.arg2 >= 26 and args.arg2 <= 769:
    start = args.arg1 - offset
    end = args.arg2 - offset + 1
if args.arg1 != -1 and args.arg2 == -1:
    line = args.arg1 - offset
    tests_conducted += 1
    tests_succeeded += test_select(line)
else:
    for line in range(start, end):
        if args.valgrind or args.valgrind_stderr:
            if line in valgrind_ignore_list:
                continue
        else:
            if line in ignore_list:
                continue
        tests_conducted += 1
        tests_succeeded += test_select(line)


print_results(tests_conducted, tests_succeeded)
