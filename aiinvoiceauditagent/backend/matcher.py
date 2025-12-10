import numpy as np

DOC_THRESHOLD = 0.55

def cosine_sim(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    return np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))


def find_best_po_match(invoice_item, invoice_vector, po_vectors):

    best = None
    score = 0

    for po in po_vectors:

        s = cosine_sim(invoice_vector, po["embedding"])

        if s > score:
            best = po
            score = s

    if score < DOC_THRESHOLD:
        return None, score

    return best, score
