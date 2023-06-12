from timeit import default_timer as timer
from humanfriendly import format_timespan
from statistics import mean
import math


def word_tf_df(frequency, docs):
    '''
    :param frequency: passed explicitly so that you can increment existing frequencies if using in online mode
    :param docs:
    :return: updated frequency freq[0] = df, freq[1] = tf

    '''
    for doc in docs:
        doc_word = []
        for word in doc:
            if word not in frequency:
                frequency[word] = [0, 0]
            frequency[word][1] += 1
            if word not in doc_word:
                frequency[word][0] += 1
                doc_word.append(word)
    return frequency
    
def word_frequency(frequency, docs):
    '''
    :param frequency: passed explicitly so that you can increment existing frequencies if using in online mode
    :param docs:
    :return: updated frequency
    '''
    for doc in docs:
        for word in doc:
            if word in frequency:
                frequency[word] += 1
            else:
                frequency[word] = 1
    return frequency


def word_co_frequency2(frequency,docs):
    import numpy
    import itertools
    from collections import Counter
    
    document = docs
    
    # Get all of the unique entries you have
    varnames = tuple(sorted(set(itertools.chain(*document))))
    
    # Get a list of all of the combinations you have
    expanded = [tuple(itertools.combinations(d, 2)) for d in document]
    expanded = itertools.chain(*expanded)
    
    # Sort the combinations so that A,B and B,A are treated the same
    expanded = [tuple(sorted(d)) for d in expanded]
    
    # count the combinations
    c = Counter(expanded)
    
    # Create the table
    table = numpy.zeros((len(varnames), len(varnames)), dtype=int)
    
    for i, v1 in enumerate(varnames):
        for j, v2 in enumerate(varnames[i:]):
            j = j + i
            table[i, j] = c[v1, v2]
            table[j, i] = c[v1, v2]
    
    # Display the output
    for row in table:
        print(row)
        
    
def word_co_frequency(frequency, docs):
    round_turns = 0
    seconds_per_round = 0
    for doc in docs:
        start = timer()
        if round_turns % 1000 == 0:
            print(
                f"we are at doc {round_turns} of {len(docs)} time elapsed : {format_timespan(seconds_per_round)} ETA:{format_timespan(seconds_per_round * ((len(docs) - round_turns) / 1000))}")
            seconds_per_round = 0
        for i in range(0, len(doc) - 1):
            w1 = doc[i]
            for j in range(i + 1, len(doc)):
                w2 = doc[j]
                word_list = sorted([w1, w2])
                word_tup = tuple(word_list)
                if not word_tup in frequency:
                    frequency[word_tup] = 0
                frequency[word_tup] += 1
        end = timer()
        round_turns += 1
        seconds_passed = end - start
        seconds_per_round += seconds_passed
    return frequency


def npmi(topic, frequencies, cofrequencies):
    v = 0
    x = max(2, len(topic))
    print(x)
    count = 0
    for i in range(0, len(topic)):
        w_i = topic[i]
        p_i = 0
        if w_i in frequencies:
            p_i = frequencies[w_i]
        for j in range(i + 1, len(topic)):
            w_j = topic[j]
            p_j = 0
            if w_j in frequencies:
                p_j = frequencies[w_j]
            word_tup = tuple(sorted([w_i, w_j]))
            p_ij = 0
            print(word_tup,"wordtuple")
            if word_tup in cofrequencies:
                print(word_tup,"wordup")
                p_ij = cofrequencies[word_tup]
            if p_ij < 2:
                v -= 1
            else:
                raw = 6385292
                basic = 6265518
                stopwords = 3401802
                parlamint_stopwords = 305555290
                sizer = 1
                # sizer = 3584952
                # sizer = 305555290
                over = p_ij/sizer
                print(over,"over")
                under1 = p_i/sizer
                under2 = p_j/sizer
                under = under1*under2
                print(under,"under")
                #pmi = math.log((p_ij / sizer) / ((p_i / sizer) * (p_j / sizer)), 2)
                #denominator = -1 * math.log((p_ij / sizer), 2)
                pmi = math.log(p_ij / (p_i * p_j), 2)
                denominator = -1 * math.log(p_ij, 2)
                npmi = pmi / denominator
                print(pmi, denominator, npmi, word_tup, p_ij, p_i, p_j)
                v += pmi/denominator
                count += 1
    print(2 * v, "2v")
    print((x * (x - 1)), "x2")
    print(count * 2)
    return (2 * v) / (x * (x - 1))


def topic_npmis(T, frequencies, cofrequencies, k=20):
    npmis = []
    for topic in T:
        n = npmi(topic[:k], frequencies, cofrequencies)
        npmis.append(n)
        print(n, "n printed")
    return npmis


def topic_coherence(T, frequencies, cofrequencies, k=20):
    '''
    Computes the coherence of a topic set (average NPMI of topics)
    :param T:
    :param frequencies:
    :param cofrequencies:
    :param k: top-k words per topic to consider
    :return:
    '''
    npmis = topic_npmis(T, frequencies, cofrequencies, k)
    if len(npmis) > 0:
        print(npmis, "npmis")
        return mean(npmis)
    return 0


def topic_diversity(T, k):
    '''
    fraction of words in top-k words of each topic that are unique
    :param T:
    :param k: top k words per topic
    :return:
    '''
    top_words = []
    for topic in T:
        top_words.extend(topic[:k])
    unique_words = set(top_words)
    if len(top_words) > 0:
        return len(unique_words) / len(top_words)
    return 0


def compute_metrics(topics, freqs, cofreqs, k):
    coherence_score = topic_coherence(topics, freqs, cofreqs, k)
    diversity_score = topic_diversity(topics, k)
    return [coherence_score, diversity_score]


if __name__ == "__main__":
    #docs = [["hei","hei","hei","hei","du","loko","du","du"]]
    #docs = [["loko","du","loko","du","loko","du","loko","du"]]
    #docs = [["loko","loko","du","du"]]
    docs = [["loko","du","loko","du","loko","du"]]
    freqs = {}
    l = word_co_frequency(freqs,docs)
    print(l)
    not_freqs = {}
    r = word_frequency(not_freqs,docs)
    print(r)
    print(l)
    res = compute_metrics(topics=[["du","loko"]],freqs=r,cofreqs=l,k=10)
    
    
    """topics = [['trur', 'gjeld', 'noreg', 'seie', 'sjølvsagt', 'mogleg', 'veit', 'ønskjer', 'pengar',
               'treng', 'viktigaste', 'auka', 'leggje', 'høgre', 'saka',
               'verda', 'raudgrøne', 'legg', 'kommunar', 'kommunane', 'seia',
               'kristeleg', 'arbeidarpartiet', 'regjeringa', 'offentlege',
               'auke', 'veg', 'folkeretten', 'usa', 'tida', 'knytte', 'nato',
               'menneske', 'framtida', 'sivile', 'meldinga', 'iallfall',
               'fn', 'israel', 'demokrati', 'omrade', 'irak', 'russland', 'krig',
               'toget', 'parti', 'innstillinga', 'militære', 'forsvar', 'angrep']]
    
    # topics=[["representanten", "harald"]]
    from utils.filemanagement import load_word_frequencies
    
    data_type = "stopwords"
    folder_path_frequencies = r"preprocessed_data/stats"
    file_name_co_frequencies = f"{data_type}_co_freq"
    file_name_frequencies = f"{data_type}_freq"
    
    word_frequencies = load_word_frequencies(folder_path_frequencies, file_name_frequencies)
    
    from utils.filemanagement import load_zipped_word_co_frequencies
    
    word_co_frequencies = load_zipped_word_co_frequencies(folder_path_frequencies, file_name_co_frequencies)
    
    res = compute_metrics(topics, word_frequencies, word_co_frequencies, 10)
    print(res, "result")"""
