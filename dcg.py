from sklearn.metrics import ndcg_score, dcg_score
import numpy as np
# Relevance scores in Ideal order
true_relevance = np.asarray([[5, 5, 5, 5, 3, 3, 3, 3, 3, 3]])

# Relevance scores in output order
relevance_score = np.asarray([[5, 5, 3, 3, 5, 5, 2, 3, 3, 3]])

dcg = dcg_score(true_relevance, relevance_score)
print("DCG score : ", dcg)

# IDCG score
idcg = dcg_score(true_relevance, true_relevance)
print("IDCG score : ", idcg)

# Normalized DCG score
ndcg = dcg / idcg
print("nDCG score : ", ndcg)