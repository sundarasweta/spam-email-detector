"""Dependency-free TF-IDF + Multinomial Naive Bayes utilities."""

from collections import Counter
import math
import re


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", str(text).lower())


def vectorize(tokens: list[str], idf: dict[str, float]) -> dict[str, float]:
    counts = Counter(token for token in tokens if token in idf)
    total = sum(counts.values())
    if not total:
        return {}
    return {word: (count / total) * idf[word] for word, count in counts.items()}


def predict_spam_probability(message: str, model: dict) -> float:
    features = vectorize(tokenize(message), model["idf"])
    vocabulary_size = len(model["idf"])
    alpha = model["alpha"]
    scores = {}
    for label in ("ham", "spam"):
        score = math.log(model["class_priors"][label])
        denominator = model["feature_totals"][label] + alpha * vocabulary_size
        weights = model["feature_weights"][label]
        for word, value in features.items():
            score += value * math.log((weights.get(word, 0.0) + alpha) / denominator)
        scores[label] = score
    maximum = max(scores.values())
    ham_score = math.exp(scores["ham"] - maximum)
    spam_score = math.exp(scores["spam"] - maximum)
    return spam_score / (ham_score + spam_score)
