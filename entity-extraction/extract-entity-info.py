from collections import defaultdict, Counter
import csv,json,pickle,ast

def read_csv(csv_path):
    with open(csv_path,'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        rows = [row for row in reader]
    return headers, rows

def get_entities(indx, rows):
    # for row in rows:
    #     print(row[indx])
    #     print(type(json.loads(json.loads(json.dumps(row[indx])))))
    return [json.loads(json.loads(json.dumps(row[indx]))) for row in rows if row[indx]]
    # return [json.loads(row[indx]) for row in rows]

def get_annotations(indx, rows):
    # print(rows[2][indx])
    for row in rows:
        print(row[indx])

    # items = [[json.loads(json.loads(json.dumps(anno))) for anno in row[indx] if anno] for row in rows]
    # return [item for sublist in items for item in sublist]

def get_counter(dicts, key):
    return Counter([dic[key] for dic in dicts if key in dic]).most_common()

def collate_entities(dicts):
    entites = defaultdict(list)
    for dict in dicts:
        for key in dict.keys():
            entites[key].append(dict[key])
    return entites

def get_key_info(dic):
    for key in dic.keys():
        print(key)
        print(type(dic[key][0]))

def pickle_data(output_path, data):
    with open(output_path,'wb') as outputfile:
        pickle.dump(data,outputfile)

def tuple_list_to_csv(output_path, tuples,headers=["text","count"]):
    with open(output_path,'w') as outputcsv:
        writer = csv.writer(outputcsv)
        writer.writerow(headers)
        for tup in tuples:
            writer.writerow([tup[0],tup[1]])



if __name__ == "__main__":
    csv_file = ""
    # headers, docs = read_csv(csv_file)
    # ent_indx = headers.index("entities")
    # ant_indx = headers.index("context_annotations")
    # annotations = get_entities(ant_indx,docs)
    # annotations = [item for sublist in annotations for item in sublist]
    # entities = get_entities(ent_indx,docs)
    # print (type(entities[0]))
    # coll_ents = collate_entities(entities)
    # coll_anns = collate_entities(annotations)
    # print(coll_ents)
    # pickle_data(csv_file.replace(".csv","-ann.p"),coll_anns)
    # pickle_data(csv_file.replace(".csv","-ent.p"),coll_ents)


    collans = csv_file.replace(".csv","-ann.p")
    collents = csv_file.replace(".csv","-ent.p")
    common_usernames = csv_file.replace(".csv","-ent-users.p")
    common_annotations = csv_file.replace(".csv","-anno-mentions.p")
    common_annotations_doms = csv_file.replace(".csv","-anno-domain.p")
    common_annotations_desc = csv_file.replace(".csv","-anno-desc.p")

    # #
    # with open(collans,'rb') as entities:
    #     ents = pickle.load(entities)
    #     print(ents['domain'])

    # with open(collans, 'rb') as entities:
    #     ents = pickle.load(entities)
    #     # # print(ents)
    #     # ents = [item for sublist in ents['mentions'] for item in sublist]
    #     # keys = set()
    #     # for dic in ents:
    #     #     keys.update(dic.keys())
    # #     # print(keys)
    # #     # print(type(ents[0]))
    # #     # print(ents)
    # #     # print()
    #     print(get_counter(ents["domain"], "description"))
    #     pickle_data(common_annotations_desc,get_counter(ents["domain"], "description"))

    pathname = common_annotations_desc
    with open(pathname,'rb') as openfile:
        tups = pickle.load(openfile)
        tuple_list_to_csv(pathname.replace(".p",".csv"),tups)


