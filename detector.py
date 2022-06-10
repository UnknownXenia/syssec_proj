from base64 import decode
import os
import re
import csv
import tlsh
import time
import argparse
import FastSearch as fs

dbPath = "./db/database.csv"
threshold = 30
hashes = []
data_root = fs.Node()

def compressFileBody(fileName):
    string = ""
    with open(fileName, 'r', encoding='utf-8', errors='ignore') as lf:
        for line in lf:
            line = str(line).replace("\n", " ").replace("\t", " ").replace('\r', ' ').replace('{', ' ').replace('}',
                                                                                                                ' ')
            string += line
    lf.close()
    return string


def removeComment(string):
    c_regex = re.compile(
        r'(?P<comment>//.*?$|[{}]+)|(?P<multilinecomment>/\*.*?\*/)|(?P<noncomment>\'(\\.|[^\\\'])*\'|"(\\.|[^\\"])*"|.[^/\'"]*)',
        re.DOTALL | re.MULTILINE)
    return ''.join([c.group('noncomment') for c in c_regex.finditer(string) if c.group('noncomment')])


def computeTlsh(string):
    string = str.encode(string)
    hs = tlsh.hash(string)
    return hs

ptr = 5
def doCompare(targetPath, in_disk, build_tree, acc):
    global ptr
    ReuseCnt = 0
    print("[+] Start to do compare.")

    possible = (".c", ".cc", ".cpp")
    fileCnt = 0
    for root, dirs, files in os.walk(targetPath, topdown=False):
        for file in files:
            if file.endswith(possible):
                fileCnt += 1
                fileName = root + "/" + file
                s = compressFileBody(fileName)
                s = removeComment(s)
                if (len(s) < 50):
                    continue
                s = computeTlsh(s)
                if in_disk:

                    fp = open(dbPath, 'r')
                    csv_reader = csv.reader(fp)

                    # main loop, traverse through every row in database.csv,
                    # if the diff < threshold, break at once
                    for row in csv_reader:
                        hashval = row[0]
                        if tlsh.diff(s, hashval) < threshold:
                            ReuseCnt += 1
                            break
                    fp.close()
                elif not build_tree:
                    # min_diff = fs.INF
                    for hashval in hashes:
                        if tlsh.diff(s, hashval) < threshold:
                            ReuseCnt += 1
                            break

                elif build_tree:
                    min_diff = fs.SearchTree(data_root, s, acc)
                    if min_diff < threshold:
                        ReuseCnt += 1

    p = ReuseCnt / fileCnt * 100
    print("[+] Comparison end.")
    print("[+] A total of %d files were reused" % ReuseCnt)
    print("[+] total of files : %d" % fileCnt)
    print("[+] The project reuse rate was %.2f%%" % p)


def Read2Mem(path):
    fp = open(path, 'r')
    csv_reader = csv.reader(fp)
    i = 0
    for row in csv_reader:
        # hashval = row[0]
        hashes.append(row[0])
        i += 1
    return hashes


def main():
    global data_root
    currPath = os.getcwd()

    parser = argparse.ArgumentParser()
    parser.add_argument('--in_disk', type=int, default=1)
    parser.add_argument('--build_tree', type=int, default=0)
    parser.add_argument('--acc', type=int, default=1)
    parser.add_argument('--target', type=str)
    args = parser.parse_args()

    targetPath = os.path.join(currPath, "data/glibc", args.target)
    print(targetPath)

    # It's used for reading data from disk to memory
    Read2Mem(dbPath)
    # It's used for building a tree on hash
    data_root = fs.Node(data=hashes)
    data_root = fs.TreeBuild(data_root)

    time_start = time.time()
    doCompare(targetPath, args.in_disk, args.build_tree, args.acc)
    time_end = time.time()

    print('[!] time cost', time_end - time_start, 's')


if __name__ == '__main__':
    main()
