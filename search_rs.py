#-*- coding:utf8 -*-
import subprocess
import tempfile
import os

def sorted_rsid_file(rsid_file):
    rsid_l = []
    with open(rsid_file) as F:
        for i in F:
            if i.startswith("rs") or i.startswith("RS"):
                rsid_l.append(int(i[2:].strip()))
    sorted_rsid_l = sorted(rsid_l)
    f = generate_rsid_file(sorted_rsid_l)
    return f, rsid_l

def generate_rsid_file(sorted_rsid_l):
    f = tempfile.NamedTemporaryFile(mode="w", delete=False)
    for i in sorted_rsid_l:
        f.write("rs\t%s\n"%(i))
    f.close()
    return f 

def search_rs_process(ref_file, rsids, tabix_path="tabix"):
    #query_result = {}
    rsid_l = []
    for rsid in rsids:
        rsid = rsid.strip()
        if rsid[:2] == "rs" or rsid[:2] == "RS":
            rsid_l.append(int(rsid[2:]))
        sorted_rsid_l = sorted(rsid_l)

    result_l = []
    if sorted_rsid_l:
        rsid_file_trans = generate_rsid_file(sorted_rsid_l)
        process = subprocess.run(f"{tabix_path} -R {rsid_file_trans.name} {ref_file}", shell=True, capture_output=True, check=True, text=True)
        os.remove(rsid_file_trans.name)
        for i in process.stdout.split("\n"):
            if i:
                items = i.strip().split("\t")
                result_l.append(
                    {
                        "rsid":"rs%s"%(items[1]),
                        "chrom":items[2],
                        "position":items[3],
                        "ref":items[4],
                        "alt":items[5]
                    }
                )
    return result_l

#print(search_rs_process("/data/users/liteng/my_project/optimal_wgs_genotype_search/dbsnp_155_5cols_format_sorted.txt.gz",
#                        ["rs3","rs21", "rs33"], "tabix"))