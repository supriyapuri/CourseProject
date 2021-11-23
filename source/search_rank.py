import sys
import time
import metapy
import pytoml

from scipy.stats import rankdata

# Open txt file with urls, titles, synopsis, rating
with open("data/movie_urls.txt") as f:
    url = f.readlines()

with open("data/titles.txt") as f:
    title_content = f.readlines()

with open("data/synopsis.txt") as f:
    synopsis_content = f.readlines()

with open("data/ratings.txt") as f:
    ratings = f.readlines()


def load_ranker(cfg_file):
    """
    Use this function to return the Ranker object to evaluate,
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """

    # DirichletPrior best mu parameter = 0.1
    # return metapy.index.DirichletPrior(.1)

    # JelinekMercer best alpha parameter = 20
    # return metapy.index.JelinekMercer(20)

    # OkapiBM25 best parameters = k1=1.2, b=0
    return metapy.index.OkapiBM25(k1=1.2, b=0)


def initialize():
    cfg = 'config.toml'
    print('creating idx')
    idx = metapy.index.make_inverted_index(cfg)
    print('now loading ranker')

    return idx, load_ranker(cfg)


idx, ranker = initialize()
top_k = 10  # maximum documents relevant to query
query = metapy.index.Document()


def run(cfg):
    print('Building or loading index...')
    ev = metapy.index.IREval(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    start_time = time.time()

    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)
    print('Running queries')
    rank_list = []
    avg_p_list = []
    ndcg = 0.0
    num_queries = 0

    with open(query_path) as query_file:

        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            rank_score = []
            doc_num = []

            results = ranker.score(idx, query, top_k)

            # ranking from highest rank to lowest

            for i in range(len(results)):
                rank_score.append((results[i])[1])
                # print("{} {}".format((title_content[(results[i])[0]]),(url[(results[i])[0]])))
                doc_num.append((results[i])[0] + 1)
            rank = list(rankdata(rank_score))

            for j in range(len(doc_num)):
                content = "{} {} {}".format(query_num + 1, doc_num[j], rank[j])
                rank_list.append(content)

            write_lst(rank_list, 'data/rank_result.txt')

            # avg precision
            avg_p = ev.avg_p(results, query_start + query_num, top_k)
            # print("Query {} average precision: {}".format(query_num + 1, avg_p))
            avg_p_list.append(avg_p)

            #ndcg
            ndcg += ev.ndcg(results, query_start + query_num, top_k)
            num_queries+=1

            write_lst(avg_p_list, 'data/avg_p.txt')
            print("Query: ", query_num + 1, " ", line)
            print("Average Precision :{}".format(avg_p),'\n')


        print("Mean average precision: {}".format(ev.map()))
        # print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))

    ndcg= ndcg / num_queries
    print("NDCG@{}: {}".format(top_k, ndcg))

    with open("data/ndcg.txt", "w") as text_file:
        text_file.write("NDCG@{}: {}".format(top_k, ndcg))


def write_lst(lst, file_):
    with open(file_, 'w') as f:
        for l in lst:
            f.write(str(l))
            f.write('\n')


def process_query(query_string):
    print("Processing : " + query_string)
    query.content(query_string)
    print('Now scoring...')

    results = ranker.score(idx, query, top_k)  # problem
    print('results received from  ranker.score.. now iterating')
    print(results)
    query_result = []
    for i in range(len(results)):
        query_result.append((title_content[(results[i])[0]], url[(results[i])[0]],
                             synopsis_content[(results[i])[0]], ratings[(results[i])[0]]))

    return query_result


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)
    cfg = sys.argv[1]
    run(cfg)
