# simulated-annealing
A Python script that performs simulated annealing on a given ordering of variables to satisfy a set of constraints. Constraints are given in the form "A B C", which means that variable C is not between A and B. Given that an optimal ordering of variables, exists for a set of constraints, the solver either returns an optimal ordering or the closest approximation found. 

##Usage
Run ``python solver.py input_file output_file`` to run the solver on a set of variables and constraints provided in an input file and output the most optimal ordering to the specified outputfile.

Run ``python run.py input_file_directory`` to run the solver on all files in a given directory and write output to "input_file.out".

## Additional Info
If a ``problematic`` folder is placed in the same directory as ``solver.py``, the script will move unsolved files to this directory, along with the best approximation in a `.out_partial' file.