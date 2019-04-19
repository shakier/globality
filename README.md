#  Supermarket Optimization : Code Exercise
## HOW TO RUN:
1. If this is the first time you run this program, please run this first:
```python overlaps.py --input_file "./retail_25k.dat" ```
This way, the program creates a data file under the folder of ./tmp. The data file contains the counts of all the possible combinations of products generated from the data. I ran on my local machine (Mac 2.7 GHz Intel Core i7), it took 16 mins to finish this step.
2. Then, to specify the sigma and return a file of combinations of minimal support level, run:
 ```python comb_counts.py --input_file "./retail_25k.dat" --sigma 4```
 Through this, the program will write the outputs to a file. You can also specify the name of the output file by putting the tag `--output_file "./output.dat"`. The results were written sub second in my local machine.
 
 ## HOW I DID IT:
The basic idea is to first find for each pair of the users, what the maximum overlaps of each pair. For all the overlaps, we keep a list of users that purchased those combinations of items. And then for the next step, we will repeat a similar comparison to compare all these maximum overlaps to find smaller overlaps which could involve more users. Again, for the overlaps, we will keep a list of users who have made that purchase. Through iterations, we will finally exhaust all the combinations. Then for each combination, just need to count how many users were in the list. 

The second steps took the most of the time, so I did a multiprocessing to do that step. 
