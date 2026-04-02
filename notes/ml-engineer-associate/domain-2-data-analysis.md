# Domain 2: Exploratory Data Analysis

## 2.1: Sanitize and prepare data for modeling.

### Identify and handle missing data, corrupt data, and stop words

- **Missing Data:** Real-world datasets often have missing values. These can occur for
  various reasons, such as data entry errors, sensor malfunctions, or incomplete
  surveys. Handling missing data is essential to avoid bias and errors in your model.
  Common techniques include:
  - **Imputation:** Filling in missing values with estimated values. This can be done
    using simple methods like mean or median imputation, or more sophisticated
    techniques like k-nearest neighbors imputation or regression imputation.
  - **Removal:** Removing rows or columns with missing values. This is a simpler
    approach but can lead to loss of valuable data if missing values are prevalent.

- **Corrupt Data:** This refers to data that is inaccurate, inconsistent, or invalid. Examples
  include:
  - **Outliers:** Data points that are significantly different from the rest of the data.
  - **Inconsistent formatting:** Dates in different formats, inconsistent
    capitalization, etc.
  - **Duplicate records:** Identical or near-identical data entries.

Handling corrupt data involves identifying and correcting or removing these errors.
Techniques include:

- **Data validation:** Implementing checks to ensure data conforms to expected
  formats and ranges.
- **Outlier detection and removal:** Using statistical methods or visualization
  techniques to identify and remove outliers.
- **Deduplication:** Identifying and removing duplicate records.
- **Stop Words:** In natural language processing (NLP), stop words are common words
  that are often removed from text data because they don't carry much meaning.
  Examples include "the," "a," "is," and "are." Removing stop words can help to
  improve the efficiency and accuracy of NLP models.

### Format, normalize, augment, and scale data

- **Format:** This involves structuring the data into a consistent and usable format. This
  may include:
  - **Data type conversion:** Converting data to the appropriate data type (e.g.,
    numeric, categorical, date).
  - **Data transformation:** Restructuring data, such as pivoting tables or
    converting between wide and long formats.

- **Normalize:** Normalization is the process of scaling data to a standard range, typically
  between 0 and 1. This is important because features with larger values can dominate
  those with smaller values, which can negatively impact model performance.
  Common normalization techniques include:
  - **Min-Max scaling:** Scales data to a range between 0 and 1.
  - **Z-score standardization:** Scales data to have a mean of 0 and a standard
    deviation of 1.

- **Augment:** Data augmentation involves creating new data points from existing data by
  applying various transformations. This is particularly useful when you have limited
  data, as it can help to improve model generalization and prevent overfitting.
  Examples of data augmentation techniques include:
  - **Image augmentation:** Rotating, flipping, cropping, and adjusting the
    brightness of images.
  - **Text augmentation:** Back translation, synonym replacement, and random
    insertion.

- **Scale:** Scaling is a more general term that refers to transforming data to a different
  range or distribution. Normalization is a specific type of scaling. Other scaling
  techniques include:
  - **Robust scaling:** Scales data using the median and interquartile range, which is
    less sensitive to outliers.
  - **Log transformation:** Compresses the range of data by taking the logarithm of
    the values.

### Determine whether there is sufficient labeled data

- **Importance of Labeled Data:** Supervised learning algorithms rely on labeled data to
  learn patterns and make predictions. Labeled data means that each data point has a
  corresponding "answer" or "label" associated with it. For example, in an image
  classification task, labeled data would consist of images with labels indicating what
  objects are present in each image (e.g., "cat," "dog," "car").
- **Assessing Sufficiency:** Determining whether you have enough labeled data depends
  on several factors:
  - **Complexity of the problem:** More complex problems generally require more
    data.
  - **Complexity of the model:** More complex models (e.g., deep neural networks)
    typically need more data to train effectively.
  - **Variability in the data:** If your data has a lot of variability, you'll need more
    data to capture all the different patterns.

- **Consequences of Insufficient Data:** Insufficient labeled data can lead to:
  - **Underfitting:** The model is too simple to capture the underlying patterns in
    the data.
  - **Overfitting:** The model learns the training data too well, including noise and
    outliers, and performs poorly on new data.

### Mitigation strategies

If you determine that you don't have enough labeled data, several mitigation strategies can
be employed:

- **Data Augmentation:** Create new training data by applying transformations to existing
  data (e.g., rotating, cropping, or flipping images).
- **Transfer Learning:** Use a pre-trained model that has been trained on a large dataset
  and fine-tune it on your smaller dataset.
- **Active Learning:** Select the most informative data points to be labeled by a human,
  iteratively improving the model with less overall labeling effort.
- **Semi-Supervised Learning:** Combine a small amount of labeled data with a large
  amount of unlabeled data to train a model.
- **Synthetic Data Generation:** Generate synthetic data that resembles your real data
  using techniques like Generative Adversarial Networks (GANs).

### Use data labeling tools (for example, Amazon Mechanical Turk)

- **Data Labeling Tools:** These tools help streamline the process of labeling data. They
  provide interfaces for humans to label data points and can also automate some
  aspects of the labeling process.
- **Amazon Mechanical Turk (MTurk):** MTurk is a crowdsourcing marketplace that can
  be used to label data. It provides access to a large pool of human workers who can
  perform tasks like image annotation, text categorization, and data transcription.
- **Other AWS Labeling Services:**
  - **Amazon SageMaker Ground Truth:** A fully managed data labeling service that
    makes it easy to build highly accurate training datasets for machine learning. 1
    Ground Truth can use MTurk workers, your own private workforce, or vendor-
    managed workforces. It also supports automated labeling to reduce labeling
    costs.

## 2.2: Perform feature engineering.

### Identifying and Extracting Features from Various Data Sources:

- **Text:**
  - **Tokenization:** Breaking down text into individual words or phrases
    (tokens).
  - **Stop word removal:** Removing common words (e.g., "the," "a," "is")
    that don't carry much meaning.
  - **Stemming/Lemmatization:** Reducing words to their root form (e.g.,
    "running" to "run").
  - **TF-IDF:** Measuring the importance of words in a document relative to
    a collection of documents.
  - **Word embeddings (Word2Vec, GloVe):** Representing words as dense
    vectors that capture semantic relationships.

- **Speech:**
  - **Audio features:** Extracting features like Mel-Frequency Cepstral
    Coefficients (MFCCs), spectral features, and energy.
  - **Speech-to-text conversion:** Using services like Amazon Transcribe to
    convert speech to text and then applying text feature engineering
    techniques.

- **Images:**
  - **Pixel values:** Using raw pixel data as features.
  - **Edge detection:** Identifying edges and boundaries in images.
  - **Feature extraction using pre-trained models:** Leveraging models like
    ResNet or Inception to extract high-level features.

- **Public Datasets:**
  - **Understanding the structure and content of public datasets.**
  - **Identifying relevant features based on the problem you're trying to
    solve.**

### Feature Engineering Techniques:

- **Binning:** Grouping continuous values into discrete bins (e.g., age ranges).

- **One-Hot Encoding:** Converting categorical variables into numerical
  representations.
- **Handling Outliers:** Identifying and treating extreme values that can skew
  model training.
- **Creating Synthetic Features:** Generating new features by combining or
  transforming existing ones (e.g., creating interaction terms).
- **Reducing Data Dimensionality:** Techniques like Principal Component Analysis
  (PCA) to reduce the number of features while retaining important
  information.

### AWS Services for Feature Engineering

- **Amazon SageMaker:** Provides built-in algorithms and tools for feature engineering,
  including processing, transforming, and analyzing data.
- **AWS Glue:** A fully managed ETL (extract, transform, load) service that can be used for
  data preparation and feature engineering.
- **Amazon Athena:** An interactive query service that makes it easy to analyze data in
  Amazon S3 using SQL, which can be used for feature exploration and creation.

### Analyze and evaluate feature engineering concepts (for example, binning, tokenization,

outliers, synthetic features, one-hot encoding, reducing dimensionality of data).

#### 1. Binning

- **Concept:** Binning, also known as discretization or bucketing, is the process of
  converting continuous numerical features into discrete categorical features by
  grouping values into bins or intervals.
- **Use Cases:**
  - Handling outliers by grouping extreme values into a single bin.
  - Capturing non-linear relationships between features and the target variable.
  - Simplifying complex models by reducing the number of distinct values.
- **Example:** Converting age into age groups (e.g., 0-18, 19-35, 36-50, 50+).

#### 2. Tokenization

- **Concept:** Tokenization is the process of breaking down text data into individual units
  called tokens. Tokens can be words, phrases, characters, or subwords.
- **Use Cases:**
  - Preparing text data for natural language processing (NLP) tasks like text
    classification, sentiment analysis, and machine translation.
  - Creating a vocabulary of unique tokens for representing text data numerically.
- **Example:** Tokenizing the sentence "The quick brown fox" into the tokens "The",
  "quick", "brown", and "fox".

#### 3. Outliers

- **Concept:** Outliers are data points that significantly deviate from the rest of the data.
  They can be caused by errors in data collection, rare events, or genuine extreme
  values.
- **Handling Outliers:**
  - **Detection:** Visualizing data (e.g., box plots, scatter plots) or using statistical
    methods (e.g., Z-score, IQR).
  - **Treatment:** Removing outliers, capping them at a certain value, or using
    robust statistical methods that are less sensitive to outliers.
- **Impact:** Outliers can negatively impact the performance of some machine learning
  models by skewing the data distribution and affecting model training.

#### 4. Synthetic Features

- **Concept:** Synthetic features are new features created from existing features using
  mathematical operations or domain knowledge.
- **Use Cases:**
  - Capturing complex relationships between features.
  - Improving model accuracy by providing additional information.
- **Example:** Creating a feature "BMI" (Body Mass Index) from "weight" and "height"
  features.

#### 5. One-Hot Encoding

- **Concept:** One-hot encoding is a technique for converting categorical features into
  numerical features. Each category is represented by a binary vector, where only one
  element is 1 (hot) and the rest are 0.
- **Use Cases:**
  - Preparing categorical data for machine learning models that require
    numerical input.
  - Avoiding giving artificial ordinal relationships to categories.
- **Example:** Encoding the colors "red", "green", and "blue" as [1, 0, 0], [0, 1, 0], and [0,
  0, 1], respectively.

#### 6. Reducing Dimensionality of Data

- **Concept:** Dimensionality reduction is the process of reducing the number of features
  in a dataset while retaining important information.
- **Use Cases:**
  - Improving model performance by reducing overfitting and computational
    complexity.
  - Visualizing high-dimensional data in lower dimensions.
- **Techniques:**
  - **Feature Selection:** Selecting a subset of the most relevant features.
  - **Feature Extraction:** Creating new features that are combinations of the
    original features (e.g., Principal Component Analysis (PCA)).

## 2.3: Analyze and visualize data for ML.

### Create Graphs

- **Why Graphs Matter:** Graphs help you quickly grasp patterns, relationships, and
  anomalies in your data that might be hard to spot in raw numbers.
- **Types of Graphs**
  - **Scatter Plots:** Show the relationship between two continuous variables.
    Useful for identifying correlations. - **Example:** Plotting advertising spend vs. sales revenue.
- **Time Series:** Display data points collected over time. Essential for forecasting
  and trend analysis. - **Example:** Website traffic over the past year.
- **Histograms:** Show the distribution of a single numerical variable by grouping
  data into bins. - **Example:** Distribution of customer ages.
- **Box Plots:** Display the distribution of a numerical variable through quartiles,
  highlighting the median, potential outliers, and spread. - **Example:** Comparing the distribution of test scores across different
  classes.

### Interpret Descriptive Statistics

Descriptive statistics provide a numerical summary of your data's key features.

- **Correlation**
  - Measures the strength and direction of a linear relationship between two
    variables. - **Range:** -1 (perfect negative correlation) to +1 (perfect positive
    correlation). 0 means no linear correlation. - **Example:** A correlation of 0.8 between study time and exam scores
    suggests a strong positive relationship.

- **Summary Statistics**
  - Provide a concise overview of your data's distribution and central tendency. - **Mean:** The average value. - **Median:** The middle value when data is ordered. - **Mode:** The most frequent value. - **Standard Deviation:** Measures the spread or dispersion of data
    around the mean. - **Variance:** The average of the squared differences from the mean.

- **P-value**

- In hypothesis testing, the p-value helps determine the statistical significance
  of results. - It indicates the probability of observing the results (or more extreme
  results) if there were actually no effect (the null hypothesis is true). - A small p-value (typically ≤ 0.05) suggests strong evidence against the
  null hypothesis. - **Example:** In an A/B test, a p-value of 0.03 for the difference in
  conversion rates indicates that the difference is statistically significant.

### Perform cluster analysis

Cluster analysis is an unsupervised learning technique used to group similar data points
together. The exam focuses on understanding and applying different clustering algorithms:

- **Hierarchical Clustering:** This method builds a hierarchy of clusters.
  - **Agglomerative (bottom-up):** Starts with each data point as its own cluster
    and successively merges the closest clusters.
  - **Divisive (top-down):** Starts with one cluster containing all data points and
    recursively splits it into smaller clusters.
  - **Dendrogram:** A tree-like diagram that visualizes the hierarchy of clusters. It
    helps in understanding the relationships between clusters and choosing the
    number of clusters.

- **k-means Clustering:** This algorithm aims to partition n observations into k clusters in
  which each observation belongs to the cluster with the nearest mean (cluster 1
  center).
  - **Diagnosis:** Assessing the quality of the clusters formed. This can involve
    analyzing cluster sizes, distances between cluster centers, and using metrics
    like silhouette score.
  - **Elbow Plot:** A technique to determine the optimal number of clusters (k) in k-
    means. It plots the within-cluster sum of squares (WCSS) against different
    values of k. The "elbow point" of the plot, where the rate of decrease in WCSS
    sharply changes, suggests a good value for k.

- **Cluster Size:** Analyzing the number of data points in each cluster. This can reveal
  insights about the data, such as the presence of dominant groups or outliers.
