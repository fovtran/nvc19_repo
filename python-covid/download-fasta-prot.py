import sys
from Bio import Entrez

# *Always* tell NCBI who you are
Entrez.email = "vivenentitan@hotmail.com"

def retrieve_annotation(id_list):
    request = Entrez.epost("gene",id=",".join(id_list))
    try:
        result = Entrez.read(request)
    except RuntimeError as e:
        #FIXME: How generate NAs instead of causing an error with invalid IDs?
        print ("An error occurred while retrieving the annotations.")
        print ("The error returned was %s" % e)
        sys.exit(-1)

    webEnv = result["WebEnv"]
    queryKey = result["QueryKey"]
    data = Entrez.esummary(db="gene", webenv=webEnv, query_key =
            queryKey)
    annotations = Entrez.read(data)

    print ("Retrieved %d annotations for %d genes" % (len(annotations), len(id_list)))

    return annotations

def print_data(annotation):
    for gene_data in annotation:
        gene_id = gene_data["Id"]
        gene_symbol = gene_data["NomenclatureSymbol"]
        gene_name = gene_data["Description"]
        print ("ID: %s - Gene Symbol: %s - Gene Name: %s" % (gene_id, gene_symbol, gene_name))

#??????
retrieve_annotation( [sys.argv[1]] )
