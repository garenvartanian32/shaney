#!/usr/bin/python
import os, sys, random

# Markov chain word generator.

# Map each context to {word->frequency}.
def build(contexts, words, n):
    context = words[:n]
    for word in words[n:]:
        key = tuple(context)
        wordfreq = contexts.get(key, {})
        wordfreq[word] = wordfreq.get(word, 0) + 1
        contexts[key] = wordfreq
        context = context[1:] + [word]

# Generate semi-random output with formatting.
def generate(f, starters, contexts, n, words_per_paragraph=80):
    context = random.choice(starters)
    output_words = list(context)

    while True:
        key = tuple(context)
        wordfreq = contexts.get(key, {})
        if not wordfreq:
            break
        word = choose(wordfreq)
        output_words.append(word)
        context = context[1:] + [word]

    # Convert to lowercase
    output_words = [w.lower() for w in output_words]

    # Write paragraphs
    for i in range(0, len(output_words), words_per_paragraph):
        paragraph = output_words[i:i + words_per_paragraph]
        f.write(" ".join(paragraph) + "\n\n")

# Weighted random choice
def choose(wordfreq):
    total = sum(wordfreq.values())
    chosen = random.randint(1, total)

    sofar = 0
    for word, count in wordfreq.items():
        sofar += count
        if chosen <= sofar:
            return word

    assert 0

def main():
    data_dir = "data/"
    n = 2

    for arg in sys.argv[1:]:
        if arg.isnumeric():
            n = int(arg)
        else:
            data_dir = arg

    contexts = {}
    starters = []

    for filename in sorted(os.listdir(data_dir)):
        print("Reading " + data_dir + filename)
        with open(os.path.join(data_dir, filename), encoding="utf-8") as f:
            words = f.read().split()
            if len(words) >= n:
                starters.append(words[:n])
                build(contexts, words, n)

    out_file = "output.txt"
    print("Writing " + out_file)

    with open(out_file, "w") as f:
        generate(f, starters, contexts, n)

if __name__ == '__main__':
    main()