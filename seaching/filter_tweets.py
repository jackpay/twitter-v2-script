from collections import defaultdict
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import csv,json,os,string
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
stemmer = SnowballStemmer("english", ignore_stopwords=True)
lemmatizer = WordNetLemmatizer()


# entity:London place:London -bio:news

desc_filter = ["news", "source", "advice", "post", "trend", "inform", "journalist", "edit"]

def filter_tweets(user_info,tweets,verified="false"):
    user_dic, usr_headers = get_wanted_users(user_info)
    with open(tweets,'r') as tweetsfile:
        reader = csv.reader(tweetsfile)
        headers = next(reader)
        textindx = headers.index("text")
        tweetid = headers.index("id")
        headers[tweetid] = "tweet_id"
        headers += ["stemmed_text", "unstemmed_text"]
        tweet_metrics = headers.index("public_metrics")
        headers[tweet_metrics] = "tweet_public_metrics"
        authindx = headers.index("author_id")
        # attach_index = headers.index("attachments")
        ents = headers.index("entities")
        # headers = [row for row in headers if not row == "attachments"]
        print(headers)

        # headers[ents] = "tweet_entities"
        # veriindx = usr_headers.index('verified') + len(headers)
        # rows = [row[:2] + [clean_text(row[textindx])] for row in reader if row[authindx] in user_dic]
        rows = [row + [clean_text(row[textindx], True), clean_text(row[textindx], False)] for row in reader
                if row[authindx] in user_dic
                and not hasLinks(row,ents)]
        # rows = [row for row in reader
        #         if row[authindx] in user_dic]
        print(len(headers))
        # print(len(rows[232]))
    with open(user_info.replace(".csv","-filtered.csv"),'w') as filteredcsv:
        writer = csv.writer(filteredcsv)
        writer.writerow(headers)
        writer.writerows(rows)

def clean_text(text_str, stem=False):
    tokens = [tok.lower().translate(str.maketrans('', '', string.punctuation)) for tok in word_tokenize(text_str)]
    return " ".join([lemmatizer.lemmatize(tok) if stem else tok for tok in tokens if
                     not tok in stopwords and
                     tok.isalpha() and
                     "amp" not in tok])

def createRow(headers, tweet):
    return [json.dumps(tweet[head]) if head in tweet else None for head in headers]

def hasLinks(row,entitiesindx):
    if not row[entitiesindx]:
        return False
    entities = json.loads(row[entitiesindx])
    if "urls" in entities:
        return True
    return False

def hasText(row,descindx, tokens):
    for tok in tokens:
        if tok in row[descindx]:
            return True
    return False

def get_wanted_users(userspath,followers=1000):
    user_dic = defaultdict(list)
    i = 0
    exists = True
    while exists:
        with open(userspath.replace("-users.csv",str(i)+"-users.csv"),'r') as userscsv:
            print(userspath.replace("-users.csv",str(i)+"-users.csv"))
            reader = csv.reader(userscsv)
            headers = next(reader)
            met_indx = headers.index('public_metrics')
            ents_indx = headers.index('entities')
            idindx = headers.index('id')
            veriindx = headers.index('verified')
            descindx = headers.index('description')
            ##
            for row in reader:
                metrics = json.loads(row[met_indx])
                # print(metrics)
                if(metrics['followers_count'] < followers and row[veriindx] == 'false' and not hasLinks(row,ents_indx) and not hasText(row,descindx,desc_filter)):
                    user_dic[row[idindx]] = row
        i += 1
        exists = os.path.exists(userspath.replace("-users.csv",str(i)+"-users.csv"))
    return user_dic,headers

if __name__ == "__main__":
    usercsv = ""
    tweets = ""
    filter_tweets(usercsv,tweets)