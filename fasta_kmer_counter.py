#!/usr/bin/env python3

from collections import Counter
from typing import Dict, Iterator, Tuple
import argparse
import sys

"""
fasta_kmer_counter.py

Create a k-mer table (default k=3) from a DNA FASTA file.

Uses Biopython's SeqIO if available (install via bioconda: biopython).
Falls back to a minimal FASTA parser if Biopython is not installed.

Script overview:
main script runs the build_kmer_table function to create kmer table, using the parse_fasta function defined here using biopython's SeqIO function to read the FASTA file.
Then the write_kmer_table function loops through the table and prints the kmer counts.
"""

# Prefer SeqIO from Biopython (available in Bioconda). Fall back to a simple parser.
try:
    #import SeqIO from biopython to read in the fasta file
    from Bio import SeqIO  # type: ignore

    #parse_fasta will read through the fasta record by record.
   

    def parse_fasta(path: str) -> Iterator[Tuple[str, str]]:  #path: str is the file path to the input fasta, and the Iterator statement just says to generate an "iterator" that will always be a Tuple of [header, sequence].         
                                                                #The reason to use an iterator is that it doesn't load the whole file into memory at once and static types to a Tuple to use less memory. 
                                                                #I could have also used a list. 
        """
        FASTA parser using Biopython SeqIO. Header is the full description (no leading '>').
        Yields (header, sequence) pairs.
        """
        #for rec in reading through the fasta file using SeqIO. Yield specificaly produces a stream of Tuples to pass back one at a time so its not reading the whole fasta file into memory.
        #What's passed back is a "generator," at type of Iterator, rather than a list.
        for rec in SeqIO.parse(path, "fasta"):
            yield rec.description, str(rec.seq)
            # NOTE: "return" would return once and exit the function, yield produces a series of values over time.

#except Exception here just says, "if Biopython isn't installed, do the following instead:" and it defines a more generic fasta parser.
except Exception:

    def parse_fasta(path: str) -> Iterator[Tuple[str, str]]:
        """
        Simple FASTA parser that yields (header, sequence) for each entry.
        Header does not include the leading '>'.
        """
        print("Warning: Biopython not found, using fallback FASTA parser.", file=sys.stderr)
        header = None
        seq_parts = []
        with open(path, "r") as fh:
            for line in fh:
                line = line.rstrip("\n")
                if not line:
                    continue
                if line.startswith(">"):
                    if header is not None:
                        yield header, "".join(seq_parts)
                    header = line[1:].strip()
                    seq_parts = []
                else:
                    seq_parts.append(line.strip())
            if header is not None:
                yield header, "".join(seq_parts)


#Building the kmer table function
#function build_kmer_table takes two arguments, the fasta path and the kmer size (default is 3). It defines the kmer size as 3 by default if no other value is provided. It inherits the fasta path from the 
#main function at table = build_kmer_table(args.fasta, k=args.k) below where the first input is the fasta path specified by argparser variable "fasta" and the second input is the kmer size specified by argparser variable "k".
def build_kmer_table(fasta_path: str, k: int = 3) -> Dict:
    """
    Build a k-mer table from a FASTA file.
    """

    #bases allowed can only be A, C, G, or T. Non-standard bases are skipped when they occur inside a k-mer.
    allowed = set("ACGT")
   
    total = Counter() #variable total is a "Counter" object that will store the kmer counts as we find them. A counter is just a python Dectionary object that is specialized for counting things.
                         #In a normal Dictionary, you have to check if a key exists before incrementing it. A Counter object automatically initializes missing keys to 0 so you can just increment them directly.

    for _, seq in parse_fasta(fasta_path):  #The for-loop calls the parse-_fasta function above, which will read through the fasta and return header and sequence for each record. However, for "_," discards the header since the tuple contains both header and sequence, and we only need the sequence.
        seq = seq.upper() #convert the sequence to uppercase to standardize it.
        for i in range(len(seq) - k + 1): #reads through seq, where range generates the range of starting positions for kmers in the sequence. len(seq) - k + 1 ensures we don't go past the end of the sequence when extracting kmers.
            kmer = seq[i : i + k] #extract the string from position i to i+k, which is the kmer.
            if set(kmer) <= allowed: #if the kmer is allowed (i.e., it only contains A, C, G, T), then:
                total[kmer] += 1 #increment the count for that kmer in the total Counter object.
    return total #return the total Counter object containing kmer counts.


#print_kmer_table function to be used below to print the kmer table in a tabular format.
def write_kmer_table(counter: Counter, outfile: str): #takes an undefined Counter object as input and prints the kmer counts in a tabular format.
    """
    Print a k-mer table in a simple tabular format: kmer\tcount
    """
    with open(outfile, "w") as f: #open the output file for writing.
        for kmer, count in sorted(counter.items()): #unpacks each tuple in the counter object into kmer and count variables, sorts them alphabetically by kmer, and iterates through them.
            f.write(f"{kmer}\t{count}\n") #write the kmer and count separated by a tab character to the output file.

#main command. this block runs when the script is executed directly from the command line. It sets up argument parsing and calls the functions defined above.
#this syntax means "if this script is being run directly (not imported as a module), then execute the following code block:". If the script is imported as a module, 
# this block will not run but the functions can still be used as, for example, fasta_kmer_counter.build_kmer_table("my_sequences.fasta", k=3).
if __name__ == "__main__": #argument parser to handle command line arguments. It defines three arguments: fasta (positional), k (optional with default 3), and output (required).
    parser = argparse.ArgumentParser(description="Build k-mer table from a FASTA file.")
    parser.add_argument("fasta", help="Input FASTA file")
    parser.add_argument("--k", type=int, default=3, help="k-mer size (default: 3)")
    parser.add_argument("--output", "-o", required=True, help="Output file for k-mer table, TSV format") 
    args = parser.parse_args()

    table = build_kmer_table(args.fasta, k=args.k) #calls the build_kmer_table function and passes the fasta file path and kmer size to it, returning the table to the table variable.
    write_kmer_table(table,args.output) #once the kmer table is built and the variable table contains it, table is passed to write_kmer_table to print.