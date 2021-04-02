import sys, re, os, json

rx_name = re.compile(r'NAME\s+(.+)')
rx_entry = re.compile(r'ENTRY\s+(\w+)')
rx_description = re.compile(r'DESCRIPTION\s+(.+)')
rx_category = re.compile(r'CATEGORY\s+(.+)')
rx_pathogen = re.compile(r'PATHOGEN\s+(.+)')
rx_drug = re.compile(r'DRUG\s+(.+)')

rx_pathogen_detail = re.compile(r'(.+)\[GN:(\w+)\]')
rx_drug_detail = re.compile(r'(.+)\[DR:(\w+)\]')

top_folder = sys.argv[1]


disease = {}

drug = {}

pathogen = {}

drug_disease_connections = set()

pathogen_disease_connections = set()

with open("disease.csv", "a") as output:
    output.write(",".join(["ko", "name", "description", "disease_category"]) + "\n")

with open("drug.csv", "a") as output:
    output.write(",".join(["ko", "name",]) + "\n")

with open("pathogen_tmp.csv", "a") as output:
    output.write(",".join(["ko", "name", "taxonomy"]) + "\n")

with open("drug_disease.csv", "a") as output:
    output.write(",".join(["from", "to"]) + "\n")

with open("pathogen_disease.csv", "a") as output:
    output.write(",".join(["from", "to"]) + "\n")

for (head, dirs, files) in os.walk(top_folder):
    for file in files:
        current_file_path = os.path.abspath(os.path.dirname(os.path.join(head, file)))
        with_name = os.path.join(current_file_path, file)

        disease_entry = ""
        disease_name = ""
        disease_description = ""
        disease_category = ""

        is_pathogen = False
        is_drug = False

        for line in open(with_name, 'r'):
            search_entry = rx_entry.search(line)
            search_name = rx_name.search(line)
            search_description = rx_description.search(line)
            search_category = rx_category.search(line)
            search_pathogen = rx_pathogen.search(line)
            search_drug = rx_drug.search(line)
            
            if not line.startswith(" "):
                is_pathogen = False
                is_drug = False

            if search_entry:
                disease_entry = search_entry.group(1)
            
            elif search_name:
                disease_name = search_name.group(1)

                if disease_name.endswith(";"):
                    disease_name = disease_name[:-1]
            
            elif search_description:
                disease_description = search_description.group(1).replace('"', "'")
            
            elif search_category:
                disease_category = search_category.group(1)

            elif search_pathogen:
                pathogen_item = search_pathogen.group(1)

                search_pathogen_detail = rx_pathogen_detail.search(pathogen_item)

                if search_pathogen_detail:
                    pathogen_name = search_pathogen_detail.group(1).strip()
                    pathogen_ko = search_pathogen_detail.group(2).strip()

                    if pathogen_ko not in pathogen:
                        pathogen[pathogen_ko] = ",".join([f'"{pathogen_ko}"', f'"{pathogen_name}"'])

                    pathogen_disease_connections.add(",".join([f'"{pathogen_ko}"', f'"{disease_entry}"']))
                    #with open("kegg.csv", "a") as output:
                    #    output.write(",".join([f'"{pathogen_ko}"', f'"{pathogen_name}"', '""', '"pathogen"', '""']) + "\n")
                    #pathogen.append([pathogen_name, pathogen_ko])
                    
                    #with open("connections.csv", "a") as output:
                    #    output.write(",".join([f'"{pathogen_ko}"', f'"{disease_entry}"']) + "\n")

                is_pathogen = True
            
            elif is_pathogen == True and line.startswith(" "):
                pathogen_item = line.strip()

                search_pathogen_detail = rx_pathogen_detail.search(pathogen_item)

                if search_pathogen_detail:
                    pathogen_name = search_pathogen_detail.group(1).strip()
                    pathogen_ko = search_pathogen_detail.group(2).strip()

                    if pathogen_ko not in pathogen:
                        pathogen[pathogen_ko] = ",".join([f'"{pathogen_ko}"', f'"{pathogen_name}"'])
                    #with open("kegg.csv", "a") as output:
                    #    output.write(",".join([f'"{pathogen_ko}"', f'"{pathogen_name}"', '""', '"pathogen"', '""']) + "\n")
                    #pathogen.append([pathogen_name, pathogen_ko])

                    pathogen_disease_connections.add(",".join([f'"{pathogen_ko}"', f'"{disease_entry}"']))
                    #with open("connections.csv", "a") as output:
                    #    output.write(",".join([f'"{pathogen_ko}"', f'"{disease_entry}"']) + "\n")

            elif search_drug:
                drug_item = search_drug.group(1)

                search_drug_detail = rx_drug_detail.search(drug_item)

                if search_drug_detail:
                    drug_name = search_drug_detail.group(1).strip()

                    drug_ko = search_drug_detail.group(2)

                    if drug_ko not in drug:
                        drug[drug_ko] = ",".join([f'"{drug_ko}"', f'"{drug_name}"'])

                    #with open("kegg.csv", "a") as output:
                    #    output.write(",".join([f'"{drug_ko}"', f'"{drug_name}"', '""', '"drug"', '""']) + "\n")
                    #drug.append([drug_name, drug_ko])

                    drug_disease_connections.add(",".join([f'"{drug_ko}"', f'"{disease_entry}"']))
                    #with open("connections.csv", "a") as output:
                    #    output.write(",".join([f'"{drug_ko}"', f'"{disease_entry}"']) + "\n")

                is_drug = True
            
            elif is_drug == True and line.startswith(" "):
                drug_item = line.strip()

                search_drug_detail = rx_drug_detail.search(drug_item)

                if search_drug_detail:
                    drug_name = search_drug_detail.group(1).strip()

                    drug_ko = search_drug_detail.group(2)

                    if drug_ko not in drug:
                        drug[drug_ko] = ",".join([f'"{drug_ko}"', f'"{drug_name}"'])

                    #with open("kegg.csv", "a") as output:
                    #    output.write(",".join([f'"{drug_ko}"', f'"{drug_name}"', '""', '"drug"', '""']) + "\n")

                    drug_disease_connections.add(",".join([f'"{drug_ko}"', f'"{disease_entry}"']))
                    #with open("connections.csv", "a") as output:
                    #    output.write(",".join([f'"{drug_ko}"', f'"{disease_entry}"']) + "\n")
                    #drug.append([drug_name, drug_ko])

        if disease_entry:
            if disease_entry not in disease:
                disease[disease_entry] = ",".join([f'"{disease_entry}"', f'"{disease_name}"', f'"{disease_description}"', f'"{disease_category}"']) 
            #with open("kegg.csv", "a") as output:
                #output.write(",".join([f'"{disease_entry}"', f'"{disease_name}"', f'"{disease_description}"', '"disease"', f'"{disease_category}"']) + "\n")

            
for node in disease:
    with open("disease.csv", "a") as output:
        output.write(disease[node] + "\n")

for node in drug:
    with open("drug.csv", "a") as output:
        output.write(drug[node] + "\n")

for node in pathogen:
    with open("pathogen_tmp.csv", "a") as output:
        output.write(pathogen[node] + "\n")

for c in pathogen_disease_connections:
    with open("pathogen_disease.csv", "a") as output:
        output.write(c + "\n")

for c in drug_disease_connections:
    with open("drug_disease.csv", "a") as output:
        output.write(c + "\n")