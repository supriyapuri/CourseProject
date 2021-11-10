import sys
import time
import metapy
import pytoml
import math
from page_scraper import title_content, url, synopsis_content
from scipy.stats import rankdata

# custom score class

# class InL2Ranker(metapy.index.RankingFunction):
#     """
#     Create a new ranking function in Python that can be used in MeTA.
#     """
#
#     def __init__(self, some_param=1.0):
#         self.param = some_param
#
#         # You *must* call the base class constructor here!
#         super(InL2Ranker, self).__init__()
#
#     def score_one(self, sd):
#         """
#         You need to override this function to return a score for a single term.
#         For fields available in the score_data sd object,
#         @see https://meta-toolkit.org/doxygen/structmeta_1_1index_1_1score__data.html
#         """
#
#         tfn = sd.doc_term_count * math.log((1.0 + self.param * sd.avg_dl /
#                                             sd.doc_size), 2)
#
#         score = sd.query_term_weight * (tfn / (tfn + self.param)) * math.log(
#             ((sd.num_docs + 1.0) / (sd.corpus_term_count + 0.5)), 2)
#         return score


def load_ranker(cfg_file):
    """
    Use this function to return the Ranker object to evaluate,
    The parameter to this function, cfg_file, is the path to a
    configuration file used to load the index.
    """
    #return InL2Ranker(some_param= 5.0)
    return metapy.index.OkapiBM25(1.5, 5)
    # return metapy.index.JelinekMercer(5.0)


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
                print("{} {} {}".format((title_content[(results[i])[0]]),(url[(results[i])[0]]),synopsis_content[(results[i])[0]]))
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



def process_query(query_string):
    query = metapy.index.Document()
    query.content(query_string)
    top_k = 10  # maximum documents relevant to query
    cfg = 'config.toml'
    print('creating idx')
    idx = metapy.index.make_inverted_index(cfg)
    print('created idx.. now loading ranker')
    print(idx)
    ranker = load_ranker(cfg)
    print('loaded_ranker. now scoring...')
    print(ranker)
    results = ranker.score(idx, query, top_k)
    print('results received from  ranker.score.. now iterating')
    print(results)
    query_result = []
    for i in range(len(results)):
        query_result.append((title_content[(results[i])[0]], url[(results[i])[0]],
                                synopsis_content[(results[i])[0]]))
    return query_result


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)
    cfg = sys.argv[1]
    run(cfg)
