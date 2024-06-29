import streamlit as st


def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    words = sorted(set(line.strip().lower() for line in lines))
    return words


def levenshteinFullMatrix(str1, str2):
    m = len(str1)
    n = len(str2)
 
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
 
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
 
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])
 
    return dp[m][n]

def main():
    st.title('Word Correction using Levenshtein Distance')

    # Input
    src_word = st.text_input('Input a word:')

    # Load vocab
    vocabs = load_vocab('vocab.txt')

    # Compute
    if st.button('Compute'):
        # Compute distance
        lev_dis_dict = dict()
        for vocab in vocabs:
            lev_dis_dict[vocab] = levenshtein_distance(src_word, vocab)

        # Find the minimum distance
        lev_dis_dict = dict(sorted(
            lev_dis_dict.items(),
            key=lambda item: item[1]
        ))
        lev_dis_lst = [[key, value] for key, value in lev_dis_dict.items()]
        res = []
        for item in lev_dis_lst:
            if (item[1] == lev_dis_lst[0][1]):
                res.append(item[0])

        # Show result
        st.write('Correct word(s): ', res)

        col1, col2 = st.columns(2)
        col1.write('Top 10: ')
        col1.write(lev_dis_lst[0:10])

        col2.write('Top 10-20: ')
        col2.write(lev_dis_lst[10:21])


if __name__ == "__main__":
    main()
