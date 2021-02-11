from searchtweets import ResultStream, gen_request_parameters, load_credentials,convert_utc_time
import csv,sys

headers = ["id","text"]

def search(queryString, outputpath, api_key_yaml,startTime="2016-01-01",endTime="2021-02-11"):

    search_args = load_credentials(api_key_yaml,
                                   yaml_key="search_tweets_v2",
                                   env_overwrite=False)

    query = gen_request_parameters(query=queryString + " -is:retweet",start_time=startTime,end_time=endTime,stringify=False, results_per_call=500)

    rs = ResultStream(request_parameters=query, max_tweets=sys.maxsize, max_requests=sys.maxsize, **search_args)

    with open(outputpath, 'w') as outputcsv:
        writer = csv.writer(outputcsv)
        writer.writerow(headers)
        for tweet in rs.stream():
            if "id" in tweet:
                writer.writerow(createRow(headers, tweet))

def createRow(headers, tweet):
    print(tweet)
    return [tweet[header] for header in headers]

if __name__ == "__main__":
    query = sys.argv[1]
    outputpath = sys.argv[2]
    credentials = sys.argv[3]
    search(query,outputpath,credentials)


