# Spam Email Detection using Machine Learning

This project classifies an email as **spam** or **ham (not spam)** using:

- TF-IDF vectorization: converts email text into numeric importance scores.
- Multinomial Naive Bayes: predicts whether the text is spam or ham.

## Run the project

Open a terminal in this folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python train.py
streamlit run app.py
```

The browser page will open automatically. Paste a message and select **Detect**.

## Dataset format

`data/spam.csv` must have exactly these headers:

```csv
label,message
ham,Are we still meeting at 4 pm?
spam,You have won a free prize. Click now!
```

The included data is only a starter sample. For meaningful accuracy, replace it with a large labeled spam dataset while preserving the `label,message` columns.
