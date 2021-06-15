from searchtweets import ResultStream, gen_request_parameters, load_credentials
import csv,sys,json

headers = ["id","text", "created_at" , "geo", "in_reply_to_user_id" , "lang", "author_id", "conversation_id", "public_metrics", "entities", "context_annotations"]
user_headers = ["id","description","location","name","username","public_metrics","verified","withheld","protected","url","entities"]
media_headers = ["media"]

def search(queryString, outputpath, api_key_yaml,startTime="2016-01-01",endTime="2021-03-15", lang="en"):

    search_args = load_credentials(api_key_yaml,
                                   yaml_key="search_tweets_v2",
                                   env_overwrite=False)

    print("Should be 1024, but it:")
    print(len(queryString + " -is:nullcast -is:retweet -is:verified -is:quote " + "lang:"+lang))

    #,created_at,geo,in_reply_to_user_id,lang,author_id,conversation_id,public_metrics,entities,context_annotations
    query = gen_request_parameters(query=queryString.strip() + " -is:nullcast -is:retweet -is:verified -is:quote " + "lang:"+lang, media_fields="media_key,type",user_fields="id,description,location,name,entities,url,username,public_metrics,verified,withheld,protected",tweet_fields="id,text,created_at,geo,in_reply_to_user_id,lang,author_id,conversation_id,public_metrics,entities,context_annotations,attachments",start_time=startTime,end_time=endTime, stringify=False, expansions="author_id,attachments.media_keys",results_per_call=500)

    rs = ResultStream(request_parameters=query, max_tweets=sys.maxsize, max_requests=sys.maxsize, **search_args)
    i = 0
    with open(outputpath, 'w') as outputcsv:
        writer = csv.writer(outputcsv)
        writer.writerow(headers)
        for tweet in rs.stream():
            # print(tweet)
            if "id" in tweet:
                writer.writerow(createRow(headers, tweet))
            if "users" in tweet:
                print("parsing users")
                dump_users_info(tweet,outputpath.replace(".csv",str(i) +"-users.csv"))
                i+=1

def createRow(headers, tweet):
    return [json.dumps(tweet[head]) if head in tweet else None for head in headers]

def dump_users_info(users_tweet,outputpath):
    with open(outputpath,'w') as outputcsv:
        writer = csv.writer(outputcsv)
        writer.writerow(user_headers)
        for user in users_tweet["users"]:
            writer.writerow(createRow(user_headers,user))

def many_followers(tweet,threshold=800):
    return int(tweet["public_metrics"]["followers_count"]) > threshold


if __name__ == "__main__":
    query = sys.argv[1]
    outputpath = sys.argv[2]
    credentials = sys.argv[3]
    lang = sys.argv[4]
    search(query,outputpath,credentials, lang=lang)


