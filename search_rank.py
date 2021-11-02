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

    return metapy.index.OkapiBM25(1.5, 5.0)


def run(cfg):
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

    top_k = 10
    query_path = query_cfg.get('query-path', 'queries.txt')
    query = metapy.index.Document()

    print('Running queries')
    file_writer_list = []
    with open(query_path) as query_file:

        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            rank_score = []
            doc_num = []

            results = ranker.score(idx, query, top_k)

            for i in range(len(results)):
                rank_score.append((results[i])[1])
                doc_num.append((results[i])[0] + 1)
            rank = list(rankdata(rank_score))

            print("Query, Document, Rank")
            for j in range(len(doc_num)):
                line = "{} {} {}".format(query_num + 1, doc_num[j], rank[j])
                print(line)

                file_writer_list.append(line)

            write_lst(file_writer_list, 'data/rank_result.txt')


def write_lst(lst, file_):
    with open(file_, 'w') as f:
        for l in lst:
            f.write(l)
            f.write('\n')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)
    cfg = sys.argv[1]
    run(cfg)
