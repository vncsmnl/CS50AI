import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    pages = dict()
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )
    return pages


def transition_model(corpus, page, damping_factor):
    prob_dist = {}
    pages = corpus.keys()
    linked_pages = corpus[page]

    if linked_pages:
        for p in pages:
            prob_dist[p] = (1 - damping_factor) / len(pages)
        for link in linked_pages:
            prob_dist[link] += damping_factor / len(linked_pages)
    else:
        for p in pages:
            prob_dist[p] = 1 / len(pages)

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    pagerank = {page: 0 for page in corpus}
    page = random.choice(list(corpus.keys()))
    for _ in range(n):
        pagerank[page] += 1
        model = transition_model(corpus, page, damping_factor)
        page = random.choices(list(model.keys()), list(model.values()))[0]
    pagerank = {page: rank / n for page, rank in pagerank.items()}
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    N = len(corpus)
    pagerank = {page: 1 / N for page in corpus}
    new_pagerank = pagerank.copy()
    converged = False

    while not converged:
        converged = True
        for page in corpus:
            total = (1 - damping_factor) / N
            for p in corpus:
                if page in corpus[p]:
                    total += damping_factor * pagerank[p] / len(corpus[p])
                if not corpus[p]:
                    total += damping_factor * pagerank[p] / N
            new_pagerank[page] = total
        for page in pagerank:
            if abs(new_pagerank[page] - pagerank[page]) > 0.001:
                converged = False
        pagerank = new_pagerank.copy()

    return pagerank


if __name__ == "__main__":
    main()
