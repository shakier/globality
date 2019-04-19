from multiprocessing import Lock, Process, Manager
import argparse
import pickle

def process_input(input_file):
    purchase_list = []
    with open(input_file, "r") as f:
        for line in f:
            purchase = set(line.split())
            purchase_list.append(purchase)
    print len(purchase_list)
    return purchase_list


def firstPass(all_overlaps, purchase_list):
##This function will take the purchase items for each users as input, and output all the max overlaps (if two users overlap 4 items, it will contain the four itmes; but not any sub-combinations of the four items)
    for i in range(0, len(purchase_list) - 1):
        for j in range(i + 1, len(purchase_list)):
            set1 = frozenset(purchase_list[i])
            set2 = frozenset(purchase_list[j])
            common = frozenset(purchase_list[i].intersection(purchase_list[j]))
            if common and len(common) >= 3:
                if common in all_overlaps:
                    all_overlaps[common].add(i)
                    all_overlaps[common].add(j)
                else:
                    all_overlaps[common] = set()
                    all_overlaps[common].add(i)
                    all_overlaps[common].add(j)
    max_overlaps = all_overlaps.keys()
    return max_overlaps

def processPartOverlap(all_overlaps, tmp_dict, overlap_list):
    tmp_list = set()
    while len(overlap_list) > 1:
        for i in range(0, len(overlap_list) - 1):
            for j in range(i + 1, len(overlap_list)):
                set1 = frozenset(overlap_list[i])
                set2 = frozenset(overlap_list[j])
                common = frozenset(set1.intersection(set2))
                if common and len(common) >= 3:
                    tmp_list.add(common)
                    users1 = all_overlaps[set1]
                    users2 = all_overlaps[set2]
                    if common not in tmp_dict:
                        tmp_dict[common] = set()
                    users_with_common = tmp_dict[common]
                    users_with_common.update(users1)
                    users_with_common.update(users2)
                    tmp_dict[common] = users_with_common
        overlap_list = list(tmp_list)
        tmp_list = set()


def chunkIt(seq, avg):
    out = []
    last = 0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

def mpProcessOverlaps(all_overlaps, max_overlaps):
#This function takes the output from first pass, and then compare each of the pairs of the max output; the purpose is to find out all the sub combinations with size larger than three.
    overlap_list = max_overlaps
    while len(overlap_list) > 1:
        print ("processing overlap list of length: " + str(len(overlap_list)))
        chunks = chunkIt(overlap_list, 100)
        manager = Manager()
        tmp_dict = manager.dict()
        overlap_parts = manager.list(chunks)
        for chunk in overlap_parts:
            p = Process(target = processPartOverlap, args = (all_overlaps, tmp_dict, chunk))
            p.start()
        p.join()
        for overlaps in tmp_dict.keys():
            users = tmp_dict[overlaps]
            if overlaps not in all_overlaps:
                all_overlaps[overlaps] = users
            else:
                all_overlaps[overlaps].update(users)
        overlap_list = tmp_dict.keys()

    count_map = {}
    for common, counts in all_overlaps.iteritems():
        count_map[common] = len(all_overlaps[common])
    return count_map

def count_order(count_map, backup_file):
    count_map_reverse = {}
    for pair, count in count_map.iteritems():
        if count in count_map_reverse:
            count_map_reverse[count].append(pair)
        else:
            count_map_reverse[count] = []
            count_map_reverse[count].append(pair)
    pickle.dump(count_map_reverse, open(backup_file, "wb"))


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--input_file", default="", type = str)
    FLAGS = args.parse_args()
    input_file = FLAGS.input_file
    print("input_file " + input_file)
    backup_file = "/".join(input_file.split('/')[:-1]) + "/tmp/"+input_file.split('/')[-1]+".pkl"
    print("backup_dir " + backup_file)
    purchase_list = process_input(input_file)
    all_overlaps = {}
    max_overlaps = firstPass(all_overlaps, purchase_list)
    print "total number of pairwise max overlaps: " + str(len(max_overlaps))
    count_map = mpProcessOverlaps(all_overlaps, max_overlaps)
    count_order(count_map, backup_file)


