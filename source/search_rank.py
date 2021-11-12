import sys
import time
import metapy
import pytoml

from scipy.stats import rankdata

def load_ranker(cfg_file):
    """
    Use this function to return the Ranker object to evaluate,
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    
    # DirichletPrior best mu parameter = 0.1
    # return metapy.index.DirichletPrior(.1)
    
    # JelinekMercer best alpha parameter = 10
    # return metapy.index.JelinekMercer(10)
    
    # OkapiBM25 best parameters = k1=.3, b=.2
    return metapy.index.OkapiBM25(k1=.3, b = .2)

def run(cfg):
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    print(idx)
    ranker = load_ranker(cfg)
    ev = metapy.index.IREval(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    start_time = time.time()
    top_k = 10 # maximum documents relevant to query
    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)
    query = metapy.index.Document()

    print('Running queries')
    rank_list = []
    avg_p_list = []
    with open(query_path) as query_file:

        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            rank_score = []
            doc_num = []

            results = ranker.score(idx, query, top_k)

            # ranking from highest rank to lowest
            print("Query: ", query_num + 1, " ",  line)
            for i in range(len(results)):
                rank_score.append((results[i])[1])
                # print("{} {}".format((title_content[(results[i])[0]]),(url[(results[i])[0]])))
                doc_num.append((results[i])[0] + 1)
            rank = list(rankdata(rank_score))


            for j in range(len(doc_num)):
                line = "{} {} {}".format(query_num + 1, doc_num[j], rank[j])
                rank_list.append(line)

            write_lst(rank_list, 'data/rank_result.txt')

            #avg precision
            avg_p = ev.avg_p(results, query_start + query_num, top_k)
            #print("Query {} average precision: {}".format(query_num + 1, avg_p))
            avg_p_list.append(avg_p)

            write_lst(avg_p_list, 'data/avg_p.txt')

        print("Mean average precision: {}".format(ev.map()))
        print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))


def write_lst(lst, file_):
    with open(file_, 'w') as f:
        for l in lst:
            f.write(str(l))
            f.write('\n')


def fetch_results(query):
    # TODO Pass the query to the ranker and fetch results and populate below array
    results = [("Nomadland", "https://www.rottentomatoes.com/m/nomadland", "96%",  "About the movie")]
    return results

#Open txt file with urls, titles, synopsis, rating
with open("data/movie_urls.txt") as f:
    url = f.readlines()

with open("data/titles.txt") as f:
    title_content = f.readlines()

with open("data/synopsis.txt") as f:
    synopsis_content = f.readlines()

with open("data/ratings.txt") as f:
    ratings = f.readlines()

def initialize():
    cfg = 'config.toml'
    print('creating idx')
    idx = metapy.index.make_inverted_index(cfg)
    print('now loading ranker')

    return idx, load_ranker(cfg)

idx, ranker = initialize()

def process_query(query_string):

    print("Processing : " + query_string)
    query = metapy.index.Document()
    query.content(query_string)

    top_k = 10  # maximum documents relevant to query
    print('Now scoring...')

    results = ranker.score(idx, query, top_k) #problem
    print('results received from  ranker.score.. now iterating')
    print(results)
    query_result = []
    for i in range(len(results)):
        query_result.append((title_content[(results[i])[0]], url[(results[i])[0]],
                             synopsis_content[(results[i])[0]], ratings[(results[i])[0]] ))
    # title = [("Nomadland", "https://www.rottentomatoes.com/m/nomadland"), ("Judas and the Black Messiah", "https://www.rottentomatoes.com/m/judas_and_the_black_m# query_result = []
    # for i in range(2):
    #     query_result.append(title[i])

    return query_result

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)
    cfg = sys.argv[1]
    run(cfg)
