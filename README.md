# Data preprocessing:
    - The datasets are already tokenised. 
    - All words are changed to lower case.

### Training the models:

    * Used `defaultdict` as translation probability table to improve training time and space, where each entry takes key-value pairs in the following format: tef([hindi_word, english_word]) = translation_probability. Using this only relevant pairs of words are looked at. 
    * For each hindi word in each hindi sentence the corresponding english translated sentence's words are made pairs with.
    * The EM algorithm is run i.e. the model is trained for `16 epochs`.
    * The HMM model uses a very similar EM based approach to try and compute the alignments and is again run for 16 epochs. 

### Results:
    - t(Ahead|ढोंकों)                      1.0
    - t(remove|0.1)                        1.0
    - t(mood|मूड)                          1.0
    - t(Delhi|दिल्ली)                      1.0
    - t(skin|त्वचा)                        1.0
    - t(or|या)                             1.0
    - t(Shah|शाह)                          1.0
    - t(oil|तेल)                           1.0
    - t(Manali|मनाली)                     0.99
    - t(list|लिस्ट)                       0.99
    - t(24|24)                            0.99
    - t(Kalimpong|कालिमपौंग)                0.99
    - t(20|20)                            0.99
    - t(and|एवं)                          0.99
    - t(chest|छाती)                       0.99
    - t(with|विद)                         0.99
    - t(and|व)                            0.99
    - t(water|पानी)                       0.99
    - t(green|हरी)                        0.99
    - t(milk|दूध)                         0.99
