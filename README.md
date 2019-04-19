#  Supermarket Optimization : Code Exercise
## HOW TO RUN:
1. If this is the first time you run this program, please run this first:
```python overlaps.py --input_file "./retail_25k.dat" ```
This way, the program creates a data file under the folder of ./tmp. The data file contains the counts of all the possible combinations of products generated from the data.
2. Then, to specify the sigma and return a file of combinations of minimal support level, run:
 ```python comb_counts.py --input_file "./retail_25k.dat" --sigma 4```
 Through this, the program will write the outputs to a file. You can also specify the name of the output file by putting the tag `--output_file "./output.dat"`. 
