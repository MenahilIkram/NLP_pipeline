# NLP Assignment 04 — 50-PDF Corpus Pipeline

Complete NLP pipeline: PDF extraction → cleaning → n-grams → Word2Vec
(CBOW/Skip-gram) next-word prediction → text classification (Naive Bayes,
Logistic Regression, K-Means).

## Requirements

```
pip install pandas numpy matplotlib seaborn nltk gensim scikit-learn pymupdf reportlab
```

> Note: the PDF library is installed as `pymupdf` but imported as `fitz`.

## Folder Structure (required before running)

```
project/
├── Assignment04_NLP_Pipeline.ipynb
└── data/
    └── pdfs/
        ├── Sports/        (10 PDFs)
        ├── Technology/     (10 PDFs)
        ├── Health/         (10 PDFs)
        ├── Finance/        (10 PDFs)
        └── Education/      (10 PDFs)
```

Folder names = category labels. ~50 PDFs total, any category names/counts
work as long as each folder has real, text-based PDFs (not scanned images).


## What Each Section Produces

| Section | Output |
|---|---|
| PDF extraction | `df` with `file_name, category, raw_text` |
| Cleaning | `df["cleaned_text"]`, saved to `data/corpus.csv` |
| N-grams | `df["unigrams"]`, `df["bigrams"]`, `df["trigrams"]` |
| Frequency graphs | Top-word, unigram, bigram, trigram bar charts |
| Part A (Word2Vec) | CBOW + Skip-gram models, next-word predictions, comparison chart |
| Part B (Classification) | Naive Bayes & Logistic Regression on unigram/bigram/trigram TF-IDF, `results_df` |
| Confusion matrix | For the best-performing model in `results_df` |
| K-Means | Cluster labels, ARI/NMI vs true categories, PCA scatter plot |

## Viewing the Clean Corpus

After the cleaning cell runs, display it anytime with:
```python
df_out = df[["file_name", "category", "raw_text", "cleaned_text"]]
df_out
```

## Saving Graphs / Results (optional)

- To save a specific graph as PNG: add `plt.savefig("name.png", dpi=200, bbox_inches="tight")` **directly before** that graph's `plt.show()` line. Do this per-graph — do not globally override `plt.show`.
- To export the classification comparison table: `results_df.to_csv("classification_comparison.csv", index=False)`
- To export the CBOW vs Skip-gram comparison: `cmp_df.to_csv("cbow_vs_skipgram.csv", index=False)`

## Troubleshooting

| Error | Fix |
|---|---|
| `No module named 'fitz'` | `pip install pymupdf` (not `pip install fitz`) |
| `FileNotFoundError: data/pdfs` | Check notebook's working directory with `os.getcwd()`; make sure `data/pdfs/` exists relative to it |
| `RecursionError` on `plt.show()` | Some earlier cell overrode `plt.show`. Restart the kernel and remove any cell containing `plt.show = ...` |
| Hundreds of duplicate PNGs | Caused by re-running a `plt.savefig(...)` cell many times without a fixed filename. Always use a fixed, unique filename per graph |
