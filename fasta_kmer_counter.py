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
    def parse_fasta(path: str) -> Iterator[Tuple[str, str]]:         
                                                                
        """
        FASTA parser using Biopython SeqIO. Header is the full description (no leading '>').
        Yields (header, sequence) pairs.
        """
        for rec in SeqIO.parse(path, "fasta"):
            yield rec.description, str(rec.seq)

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
   
    total = Counter() 
    
    for _, seq in parse_fasta(fasta_path):  
        seq = seq.upper() 
        for i in range(len(seq) - k + 1): 
            kmer = seq[i : i + k] 
            if set(kmer) <= allowed: 
                total[kmer] += 1 
    return total #return the total Counter object containing kmer counts.


#print_kmer_table function to be used below to print the kmer table in a tabular format.
def write_kmer_table(counter: Counter, outfile: str): #takes an undefined Counter object as input and prints the kmer counts in a tabular format.
    """
    Print a k-mer table in a simple tabular format: kmer\tcount
    """
    with open(outfile, "w") as f: #open the output file for writing.
        for kmer, count in sorted(counter.items()): #unpacks each tuple in the counter object into kmer and count variables, sorts them alphabetically by kmer, and iterates through them.
            f.write(f"{kmer}\t{count}\n") #write the kmer and count separated by a tab character to the output file.


if __name__ == "__main__": #parser defines three arguments: fasta (positional), k (optional with default 3), and output (required).
    parser = argparse.ArgumentParser(description="Build k-mer table from a FASTA file.")
    parser.add_argument("fasta", help="Input FASTA file")
    parser.add_argument("--k", type=int, default=3, help="k-mer size (default: 3)")
    parser.add_argument("--output", "-o", required=True, help="Output file for k-mer table, TSV format") 
    args = parser.parse_args()

    table = build_kmer_table(args.fasta, k=args.k) #calls the build_kmer_table function and passes the fasta file path and kmer size to it, returning the table to the table variable.
    write_kmer_table(table,args.output) #once the kmer table is built and the variable table contains it, table is passed to write_kmer_table to print.
