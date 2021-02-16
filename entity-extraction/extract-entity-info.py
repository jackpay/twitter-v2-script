from collections import defaultdict
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
    #     json.loads(json.dumps(row[indx]))
    # return [json.loads(json.dumps(row[indx])) for row in rows]
    return [json.loads(row[indx]) for row in rows]

def get_annotations(indx, rows):
    print(rows[2][indx])
    items = [[json.loads(anno) for anno in row[indx] if anno and len(anno) > 0] for row in rows]
    return [item for sublist in items for item in sublist]

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

if __name__ == "__main__":
    csv_file = "/Users/jp242/Documents/Projects/SHL/electric-vehicles/ev-tweets-2.csv"
    headers, docs = read_csv(csv_file)
    ent_indx = headers.index("entities")
    ant_indx = headers.index("context_annotations")
    # annotations = get_annotations(ant_indx,docs)
    entities = get_entities(ent_indx,docs)
    print (type(entities[0]))
    # coll_ents = collate_entities(entities)
    # coll_anns = collate_entities(annotations)
    pickle_data("/Users/jp242/Documents/Projects/SHL/electric-vehicles/twitter-data_ev-tweets-non-verified-dedupe-ann.p",coll_anns)
    pickle_data("/Users/jp242/Documents/Projects/SHL/electric-vehicles/twitter-data_ev-tweets-non-verified-dedupe-ent.p",coll_ents)


