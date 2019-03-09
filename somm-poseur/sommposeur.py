import numpy as np

def get_reviews_text(file_path):
    # First row is header; all other lines are reviews
    raw_data = open(file_path, encoding='utf8').read()
    raw_reviews  = raw_data.splitlines()
    del(raw_reviews[0])

    # Description is in quotations--but a few reviews are missing "\"""
    reviews = []
    for raw_review in raw_reviews:
        parsed = raw_review.split("\"")
        if len(parsed) > 1:
            reviews.append(parsed[1])
    
    return reviews


def get_word_pairs(reviews):
    for review in reviews:
        review_split = review.split(" ")
        for i in range(len(review_split) - 1):
            yield (review_split[i], review_split[i + 1])


def get_markov_chain(reviews):
    word_pairs = get_word_pairs(reviews)
    word_dict = {}

    for word1, word2 in word_pairs:
        if word1 in word_dict.keys():
            word_dict[word1].append(word2)
        else:
            word_dict[word1] = [word2]
    
    return word_dict


def get_random_starting_word(reviews):
    # Grab a random review and then grab a random word
    # until we find upppercase which is probably a new sentence
    first_word = "nil"
    while first_word.islower():
        random_review = np.random.choice(reviews)
        first_word    = np.random.choice(random_review.split())
    
    return first_word


def get_generated_review(starting_word, markov_chain, review_length):
    next_word = starting_word
    review_chain = [next_word]

    for i in range(review_length):
        # Terminal word
        if next_word not in markov_chain:
            break

        sub_chain = markov_chain[next_word]
        next_word = np.random.choice(markov_chain[next_word])
        review_chain.append(next_word)

    return " ".join(review_chain)


reviews       = get_reviews_text("../data/winemag-data-130k-v2.csv")
starting_word = get_random_starting_word(reviews)
markov_chain  = get_markov_chain(reviews)
rando_review  = get_generated_review(starting_word, markov_chain, 50)

print(rando_review)
