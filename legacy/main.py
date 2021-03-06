from dataLoader import Corpus
from perceptron import perceptron
from config import config
from tqdm import tqdm


def train(trainSet, pct):
    N = len(trainSet)
    with tqdm(total=N) as bar:
        for xs, ys in trainSet:
            pct.train(xs, ys)
            bar.update()

def test(testSet, pct):
    N = len(testSet)
    total = 0
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    with tqdm(total=N) as bar:
        for xs, ys in testSet:
            preds = (pct.pred(xs) > 1)
            ys = (ys > 1)
            total += len(preds)
            tp += (preds * ys).sum()
            fp += (preds * (1-ys)).sum()
            tn += ((1-preds) * (1-ys)).sum()
            fn += ((1-preds) * ys).sum()
            bar.update()
    assert total == tp + fp + tn + fn
    print('true positive: %d' % tp)
    print('true negative: %d' % tn)
    print('false positive: %d' % fp)
    print('false negative: %d' % fn)
    f1 = ((2 * tp)/(2*tp+fn+fp))
    print('f1 socre: %.4f' % f1)
    print('acc: %.4f' % ((tp+tn)/total))
    return f1


def search_for_parameter():
    n_bis = [ 100000, 200000, 500000]
    steps = [ 5e-2, 1e-1, 5e-1, 1]
    n_epoch = 5

    for n_bi in n_bis:
        for step in steps:
            print('-'*20)
            print(n_bi, ' ', step)
            config['n_bigram'] = n_bi
            config['smooth'] = step
            corpus = Corpus(config['data_dir'])
            pct = perceptron()
            for cnt in range(n_epoch):
                train(corpus.trainSet, pct)
            test(corpus.testSet, pct)

if __name__ == '__main__':
    #search_for_parameter()
    pct = perceptron()
    corpus = Corpus(config['data_dir'])
    n_epoch = 5
    while True:
        for cnt in range(n_epoch):
            print('Happy training!')
            train(corpus.trainSet, pct)
        print('\nHappy testing!')
        test(corpus.testSet, pct)
        config['smooth'] /= 10
        if config['smooth'] < 1.01e-10:
            break

