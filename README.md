# Sequence Analyzer

This is my code to analyse sanger sequencing results from .abi files. This is specialized to my current needs, which is mainly confirming antibody cloning results.

`abi_analysis.py` has several functions that are used in succession to analyze the sequencing files. The general workflow is listed below:
* `list_of_abi_files = get_seq_files(directory, key = None)`
* `seqs_dict = create_dna_seqs_dict(list_of_abi_files, reverse = True)`
* `trimmed_dna_seqs = trim_dna_seqs(seqs_dict, starting_seq = string_of_dna, length = int_length)`
* `pro_seqs_df = create_protein_seqs(trimmed_dna_seqs)`

`get_seq_files` retrieves all the .abi files from the input `directory`.

`create_dna_seqs_dict` creates a dictionary of sequences within the .abi files using BioPython to get the information. The `reverse` flag is set to `True` when a reverse primer was used in the sequencing reaction. The resulting sequences will be reverse complemented to account for this.

`trim_dna_seqs` interates through all the sequences and searches for `starting_seq`, which is ~10bp of DNA prior to the 3' cut site used for cloning, and removes all bases after `length`, usually set to however many bp from the `starting_seq` through to the other cutsite on the 5' end. It is useful to make sure `starting_seq` is in-frame with your protein-of-interest and `length` is a multiple of 3.

`create_protein_seqs` translates the sequences into protein sequence and creates a dataframe of the results with one column per amino acid. 

I usually save the dataframe to excel and check for correct sequences there.
