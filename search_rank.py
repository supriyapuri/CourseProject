import sys
import metapy
import pytoml
from scipy.stats import rankdata
# from page_scraper import title_content


def load_ranker(cfg_file):
    """
    Use this function to return the Ranker object to evaluate,
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """

    return metapy.index.OkapiBM25(1.5, .75)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)

    cfg = sys.argv[1]
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    print(idx)
    ranker = load_ranker(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    top_k = 50
    query_path = query_cfg.get('query-path', 'queries.txt')
    query = metapy.index.Document()

    print('Running queries')
    with open(query_path) as query_file:

        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            rank_score = []
            doc_num = []

            results = ranker.score(idx, query, top_k)


            for i in range(len(results)):
                rank_score.append((results[i])[1])
                doc_num.append((results[i])[0])
            rank = list(rankdata(rank_score))


            print(query_num)
            print("-------------")
            #print(len(rank_score))
            print(doc_num)
            print("-------------")
            print(rank)
            print("********")


            # for i in range(len(results)):
            #     print("Title:", (title_content[(results[i])[0]]))
            #     print("\nRanker score: ", (results[i])[1], "\n")
