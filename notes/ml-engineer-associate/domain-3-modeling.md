# Domain 3: Modeling

## 3.1: Frame business problems as ML problems.

### Determine when to use and when not to use ML.

- **When to use ML:**
  - Complex problems with no clear rules: ML excels at tasks where traditional
    programming is difficult, like image recognition, natural language processing,
    and fraud detection.
  - Large datasets: ML algorithms thrive on data, finding patterns and insights
    that humans might miss.
  - Need for predictions or insights: ML can forecast future trends, classify data,
    and provide recommendations.
  - Continuous improvement: ML models can learn and adapt as new data
    becomes available.

- **When not to use ML:**
  - Simple problems with clear rules: If a problem can be solved with a
    straightforward rule-based system, ML might be overkill.
  - Small datasets: ML models need sufficient data to train effectively.
  - Need for explainability: Some ML models (like deep neural networks) are
    "black boxes," making it hard to understand their decision-making process. If
    explainability is crucial, simpler models or rule-based systems might be better.
  - Real-time, low-latency requirements: Training and deploying complex ML
    models can introduce latency, which might be unacceptable for certain
    applications.

### Know the difference between supervised and unsupervised learning.

- **Supervised learning:**
  - The algorithm learns from labeled data, where the input and the desired
    output are provided.
  - Examples:
    - Classification: Predicting a category (e.g., spam or not spam).
    - Regression: Predicting a continuous value (e.g., house prices).
  - Common algorithms: Linear Regression, Logistic Regression, Decision Trees,
    Random Forests, Support Vector Machines, Neural Networks.

- **Unsupervised learning:**
  - The algorithm learns from unlabeled data, finding patterns and structures on
    its own.
  - Examples: - Clustering: Grouping similar data points together (e.g., customer
    segmentation). - Dimensionality reduction: Reducing the number of variables while
    preserving important information.
  - Common algorithms: K-Means Clustering, Principal Component Analysis
    (PCA).

### Select from among classification, regression, forecasting, clustering, recommendation, and foundation models.

- **Classification:** Predicting a category or class.
  - Example: Identifying whether an email is spam or not.
  - Algorithms: Logistic Regression, Support Vector Machines, Decision Trees,
    Random Forests, Naive Bayes.

- **Regression:** Predicting a continuous numerical value.
  - Example: Predicting house prices based on features like size and location.
  - Algorithms: Linear Regression, Polynomial Regression, Support Vector
    Regression.

- **Forecasting:** Predicting future values based on historical time-series data.
  - Example: Predicting sales for the next quarter.
  - Algorithms: ARIMA, Prophet.

- **Clustering:** Grouping similar data points together.
  - Example: Segmenting customers based on their purchasing behavior.
  - Algorithms: K-Means Clustering, DBSCAN.

- **Recommendation:** Suggesting items or content to users based on their preferences.
  - Example: Recommending products to customers on an e-commerce website.
  - Algorithms: Collaborative Filtering, Content-Based Filtering.

- **Foundation Models:** Large, pre-trained models that can be adapted to a wide range
  of tasks.
  - Example: Using a large language model for text generation, translation, or
    question answering.
  - Examples: BERT, GPT, Gemini.

## 3.2: Select the appropriate model(s) for a given ML problem.

### Regression Models (Predicting Continuous Values):

- **Linear Regression:** Used for predicting a continuous target variable based on
  a linear relationship with predictor variables. Simple, interpretable, but
  assumes linearity. Suitable for problems where a linear relationship is
  expected, like predicting house prices based on size.
- **XGBoost (Extreme Gradient Boosting):** A powerful ensemble method that
  combines multiple decision trees. Handles complex relationships, missing
  data, and is robust to outliers. Often used for tabular data in classification and
  regression tasks where high accuracy is important.

### Classification Models (Predicting Categories):

- **Logistic Regression:** Used for binary classification problems (two classes).
  Predicts the probability of belonging to a certain class. Simple and
  interpretable, but assumes a linear decision boundary. Suitable for problems
  like spam detection.
- **Decision Trees:** Tree-like structures that make decisions based on a series of
  if-else conditions. Easy to understand and visualize, but prone to overfitting.
  Can be used for both classification and regression.
- **Random Forests:** An ensemble method that combines multiple decision
  trees. Reduces overfitting and improves accuracy compared to single decision
  trees. Effective for various classification and regression tasks.
- **XGBoost (also used for classification):** As mentioned earlier, XGBoost is very
  versatile and performs well in classification tasks, often outperforming
  Random Forests.

### Clustering Models (Grouping Similar Data Points):

- **K-means:** Partitions data into k clusters based on distance to cluster centers.
  Simple and efficient, but requires specifying the number of clusters (k)
  beforehand. Suitable for tasks like customer segmentation.

### Neural Networks (Complex Models for Various Tasks):

- **RNN (Recurrent Neural Networks):** Designed for sequential data, such as
  time series or text. Have memory of past inputs, making them suitable for
  natural language processing (NLP) and time series forecasting.

- **CNN (Convolutional Neural Networks):** Primarily used for image recognition
  and computer vision tasks. Utilize convolutional layers to extract features
  from images. Also used in NLP for tasks like text classification.

### Advanced Techniques:

- **Ensemble Methods:** Combine multiple models to improve performance.
  Examples include Random Forests, XGBoost, and stacking.
- **Transfer Learning:** Reusing a pre-trained model on a new task with similar
  characteristics. Saves training time and resources, particularly useful when
  limited data is available. Common in image classification and NLP.
- **Large Language Models (LLMs):** Very large neural networks trained on
  massive text datasets. Capable of generating human-like text, translating
  languages, writing different kinds of creative content, and answering your
  questions in an informative way.

### Intuition Behind Models:

Understanding the intuition behind the models is crucial for effective model selection. Here
are some key intuitive explanations:

- **Linear Regression:** Imagine trying to fit a straight line through a set of data points.
  Linear regression finds the line that minimizes the sum of squared errors between
  the line and the points.
- **Logistic Regression:** Instead of fitting a line, logistic regression fits an "S"-shaped
  curve (sigmoid function) to the data. This curve represents the probability of
  belonging to a certain class.
- **Decision Trees:** Imagine asking a series of questions to classify an object. Each
  question corresponds to a node in the tree, and the answers lead to different
  branches.
- **Random Forests:** Imagine having multiple decision trees, each trained on a random
  subset of the data and features. The final prediction is made by aggregating the
  predictions of all trees. This reduces overfitting and improves accuracy.
- **K-means:** Imagine placing k random points (centroids) in the data space. Then, each
  data point is assigned to the nearest centroid. The centroids are then recalculated as
  the mean of the assigned points. This process is repeated until the centroids no
  longer move significantly.
- **RNN:** Imagine a loop that allows information to persist from one step to the next.
  This loop allows the network to remember past inputs and use them to process
  current inputs.
- **CNN:** Imagine sliding a small window (filter) over an image. This window extracts
  features from the image, such as edges and textures. Multiple filters are used to
  extract different features.
- **Transfer Learning:** Imagine learning to ride a motorcycle after already knowing how
  to ride a bicycle. You can transfer your knowledge of balance and steering to the new
  task.

### Key Considerations for Model Selection:

- Type of Data: Numerical, categorical, text, images, time series.
- Problem Type: Regression, classification, clustering.
- Data Size: Small datasets may benefit from simpler models or transfer learning. Large
  datasets can support more complex models.
- Interpretability: Some models (e.g., linear regression, decision trees) are easier to
  interpret than others (e.g., neural networks).
- Performance Metrics: Accuracy, precision, recall, F1-score, RMSE, etc.
- Computational Resources: Some models require more computational resources than
  others.

## 3.3: Train ML models.

### Split data between training and validation (for example, cross-validation)

- Data Splitting: In machine learning, you typically split your dataset into three
  parts:
  - Training set: Used to train the model.
  - Validation set: Used to tune hyperparameters and evaluate the
    model's performance during training.
  - Test set: Used to provide a final, unbiased evaluation of the model's
    performance after training.
- Cross-validation: A technique used to assess how well a model generalizes to
  independent data. It helps to avoid overfitting and provides a more robust
  estimate of model performance. Common types include:
  - k-fold cross-validation: The dataset is divided into k subsets (folds).
    The model is trained k times, each time using a different fold as the
    validation set and the remaining k-1 folds as the training set.
  - Stratified k-fold cross-validation: Similar to k-fold, but ensures that
    each fold has the same proportion of target classes as the original
    dataset. This is important for imbalanced datasets.

### Understand optimization techniques for ML training (for example, gradient descent, loss functions, convergence)

- Loss functions: A loss function measures how well the model is performing
  on the training data. It quantifies the difference between the predicted values
  and the actual values. Common loss functions include:
  - Mean Squared Error (MSE): Used for regression problems.
  - Binary Cross-Entropy: Used for binary classification problems.
  - Categorical Cross-Entropy: Used for multi-class classification
    problems.

- Gradient descent: An iterative optimization algorithm used to find the
  minimum of a function (in this case, the loss function). It works by repeatedly
  adjusting the model's parameters in the direction of the steepest descent of
  the loss function.
  - Learning rate: A hyperparameter that controls the step size in each
    iteration of gradient descent.
  - Batch size: The number of training examples used in each iteration of
    gradient descent.
- Convergence: Refers to the point where the model's performance on the
  training data stops improving significantly. It indicates that the optimization
  algorithm has found a minimum of the loss function.

### AWS Services and Considerations

When working with AWS for machine learning model training, you'll likely use services like:

- Amazon SageMaker: A fully managed service that provides tools for building,
  training, and deploying machine learning models. It supports various training
  options, including distributed training and hyperparameter tuning.
- AWS Deep Learning AMIs: Amazon Machine Images that are pre-configured with
  popular deep learning frameworks like TensorFlow and PyTorch.
- Amazon EC2: Provides virtual servers for training models, giving you more control
  over the hardware and software environment.

### Choosing Appropriate Compute Resources

The choice of compute resources significantly impacts training time and cost. Here's a
breakdown:

- **CPU vs. GPU:**
  - CPUs (Central Processing Units): General-purpose processors suitable for a
    wide range of tasks. They are cost-effective for smaller datasets, simpler
    models, and tasks that don't involve heavy matrix operations.
  - GPUs (Graphics Processing Units): Specialized processors designed for
    parallel processing, particularly effective for matrix operations common in
    deep learning. GPUs significantly accelerate training for complex models and
    large datasets.

- **Distributed vs. Non-Distributed:**
  - Non-Distributed (Single Instance): Training happens on a single machine. This
    is suitable for smaller datasets and models that fit in the memory of a single
    instance.
  - Distributed (Multiple Instances): Training is distributed across multiple
    machines working together. This is essential for very large datasets and
    complex models that require more memory and processing power than a

single instance can provide. Frameworks like TensorFlow and PyTorch support
distributed training.

### Choosing Appropriate Compute Platforms

AWS offers various platforms for machine learning. The choice depends on the scale and
complexity of your project:

- **Non-Spark Platforms (e.g., Amazon SageMaker):**
  - Amazon SageMaker: A fully managed machine learning service. It provides
    tools for building, training, and deploying ML models. SageMaker supports
    various instance types (CPU and GPU) and offers features like automatic
    model tuning, distributed training, and model monitoring. It's a good choice
    for most ML projects, especially those that benefit from a managed
    environment.

- **Spark Platforms (e.g., Amazon EMR):**
  - Amazon EMR (Elastic MapReduce): A managed Hadoop framework that can
    be used for large-scale data processing and machine learning. Apache Spark,
    a popular distributed computing framework, runs on EMR. Spark is well-
    suited for processing and transforming very large datasets before training ML
    models. It also has its own MLlib library for machine learning. Use EMR when
    you need to process massive datasets or already have a Spark-based data
    processing pipeline.

### Updating and Retraining Models

Models need to be retrained periodically to maintain accuracy as new data becomes
available or data patterns change. There are two main retraining strategies:

- **Batch Retraining:**
  - The model is retrained on a batch of new data, typically at scheduled intervals
    (e.g., daily, weekly). This is simpler to implement but may not be suitable for
    applications that require immediate updates. The provided code example
    demonstrates a basic batch retraining scenario.

- **Real-time/Online Retraining:**
  - The model is updated continuously as new data arrives. This is more complex
    to implement but allows the model to adapt quickly to changing conditions.
    This approach is suitable for applications where data changes rapidly and
    timely updates are crucial.

## 3.4: Perform hyperparameter optimization.

### Perform Regularization

Regularization is a technique used to prevent overfitting in machine learning models.
Overfitting occurs when a model learns the training data too well, including its noise and
outliers, leading to poor performance on new, unseen data. Regularization methods add a

penalty to the model's complexity, encouraging it to learn simpler, more generalizable
patterns.

Here are two common regularization techniques:

- **Dropout:** This technique is primarily used in neural networks. During training,
  dropout randomly "drops out" (ignores) a fraction of neurons in a layer. This prevents
  the network from relying too heavily on any single neuron and encourages it to learn
  more robust features. Dropout can be seen as training multiple networks with
  different architectures simultaneously.
- **L1/L2 Regularization:** These techniques add a penalty term to the loss function that
  the model tries to minimize during training.
  - L1 Regularization (Lasso): Adds the sum of the absolute values of the model's
    weights to the loss function. This encourages the model to have sparse
    weights, meaning some weights become exactly zero. This effectively
    performs feature selection, as features with zero weights are effectively
    ignored by the model.
  - L2 Regularization (Ridge): Adds the sum of the squares of the model's
    weights to the loss function. This encourages the model to have small
    weights, but not necessarily zero. This helps to prevent any single feature
    from having too much influence on the model.

### Perform Cross-Validation

Cross-validation is a technique used to evaluate the performance of a machine learning
model on unseen data. It helps to assess how well the model generalizes to new data and to
avoid overfitting.

Here's how it works:

1. The data is divided into k subsets or "folds" of roughly equal size.
2. The model is trained k times. In each iteration, one fold is held out as the validation
   set, and the remaining k-1 folds are used for training.
3. The performance of the model is evaluated on the validation set in each iteration.
4. The average performance across all k iterations is calculated to give an overall
   estimate of the model's performance.

A common type of cross-validation is k-fold cross-validation, where k is typically 5 or 10.
Cross-validation helps to:

- Get a more reliable estimate of model performance than a single train-test split.
- Detect overfitting.
- Tune hyperparameters.

### Initialize Models

Initializing a model refers to setting the initial values of its parameters (e.g., weights in a
neural network) before training begins. Proper initialization is crucial for effective training, as
it can affect the model's convergence speed and final performance.

Here are some common initialization techniques:

- **Zero Initialization:** Setting all parameters to zero. This is generally not a good idea,
  especially in neural networks, as it can lead to symmetry issues where all neurons in
  a layer learn the same thing.
- **Random Initialization:** Setting parameters to small random values. This helps to
  break symmetry and allows different neurons to learn different features.
- **Xavier/Glorot Initialization:** This method sets the initial weights based on the
  number of input and output neurons in a layer. It aims to keep the variance of the
  activations consistent across layers, which can help with training deep networks.
- **He Initialization:** This is a variant of Xavier initialization that is specifically designed
  for ReLU activation functions.

### Neural Network Architecture

- **Layers and Nodes:**
  - Layers: Neural networks consist of interconnected layers of nodes (neurons).
    The main types of layers are: - Input Layer: Receives the initial data. - Hidden Layers: Perform computations on the input data. A network
    can have multiple hidden layers (deep learning). - Output Layer: Produces the final result.
  - Nodes: Each node in a layer receives input from the nodes in the previous
    layer, applies a weight to each input, sums them up, adds a bias, and then
    passes the result through an activation function.

- **Learning Rate:**
  - The learning rate is a hyperparameter that controls the step size during the
    optimization process. It determines how much the weights of the network are
    adjusted in response to the error calculated during training.
  - A high learning rate can lead to overshooting the optimal solution, while a
    low learning rate can result in slow convergence.

- **Activation Functions:**
  - Activation functions introduce non-linearity to the network, allowing it to
    learn complex patterns. Common activation functions include: - Sigmoid: Outputs values between 0 and 1. - ReLU (Rectified Linear Unit): Outputs 0 for negative inputs and the
    input value for positive inputs. - Tanh (Hyperbolic Tangent): Outputs values between -1 and 1.

### Tree-Based Models

- **Number of Trees:**
  - Tree-based models like Random Forests and Gradient Boosting Machines
    (GBMs) use an ensemble of decision trees.
  - Increasing the number of trees generally improves the model's accuracy, but
    also increases computational cost and can lead to overfitting.

- **Number of Levels (Tree Depth):**
  - The depth of a decision tree determines the complexity of the model.
  - A deeper tree can capture more intricate relationships in the data but is also
    more prone to overfitting.
  - Limiting the tree depth can help to prevent overfitting and improve
    generalization.

### Linear Models

- **Learning Rate:**
  - Linear models, such as linear regression and logistic regression, also use a
    learning rate during the optimization process (e.g., gradient descent).
  - Similar to neural networks, the learning rate in linear models controls the
    step size taken towards the optimal solution.
  - Choosing an appropriate learning rate is crucial for efficient convergence and
    avoiding oscillations or slow progress.

## 3.5: Evaluate ML models.

### Avoid Overfitting or Underfitting

- **Overfitting:** This occurs when a model learns the training data too well, capturing
  noise and specific details that don't generalize. It's like memorizing answers to a test
  instead of understanding the underlying concepts. Overfit models have high variance
  and low bias.
  - Symptoms: High accuracy on training data, low accuracy on validation/test
    data. Complex models (e.g., deep decision trees) are more prone to
    overfitting.
  - Detection: Observing a significant gap between training and validation/test
    performance.
  - Handling: - Regularization: Techniques like L1 (LASSO) and L2 (Ridge)
    regularization add penalties to the model's complexity, discouraging it
    from fitting noise.

  - Cross-validation: Techniques like k-fold cross-validation provide more

robust performance estimates by training and evaluating the model
on multiple subsets of the data. - Pruning (for decision trees): Reducing the size of the tree by removing
branches that don't contribute significantly to performance. - Data augmentation: Increasing the size and diversity of the training
data by applying transformations (e.g., rotations, flips) to existing
data. - Early stopping: Halting the training process before the model starts to
overfit, based on performance on a validation set.

- **Underfitting:** This happens when a model is too simple to capture the underlying
  patterns in the data. It's like trying to fit a straight line to a highly curved dataset.
  Underfit models have high bias and low variance.
  - Symptoms: Low accuracy on both training and validation/test data. Simple
    models (e.g., linear regression on complex data) are more prone to
    underfitting.
  - Detection: Consistently poor performance across all datasets.
  - Handling: - Using a more complex model: Switching to a more powerful
    algorithm (e.g., from linear regression to a neural network). - Feature engineering: Creating new features that better represent the
    data. - Removing constraints on the model: For example, allowing a decision
    tree to grow deeper.

### Detect and Handle Bias and Variance

- **Bias:** Represents the error introduced by approximating a real-world problem, which
  may be complex, by a simplified model. High bias implies strong assumptions about
  the data. A high-bias model is more likely to underfit.
- **Variance:** Represents the model's sensitivity to small fluctuations in the training data.
  High variance means the model is learning noise in the training data. A high-variance
  model is more likely to overfit.
- **Bias-Variance Tradeoff:** The goal is to find a balance between bias and variance.
  Reducing bias often increases variance, and vice-versa. The optimal model minimizes
  the total error, which is the sum of bias, variance, and irreducible error (inherent
  noise in the data).

### Evaluate Metrics

Choosing the right evaluation metric depends on the specific problem and the type of
machine learning task (classification, regression, etc.).

- **Classification Metrics:**

- Accuracy: The overall proportion of correctly classified instances. Can be
  misleading with imbalanced datasets (where one class has many more
  instances than others).
- Precision: Out of all the instances predicted as positive, how many were
  actually positive? (True Positives / (True Positives + False Positives)).
  Important when minimizing false positives is crucial.
- Recall (Sensitivity): Out of all the actual positive instances, how many were
  correctly predicted? (True Positives / (True Positives + False Negatives)).
  Important when minimizing false negatives is crucial.
- F1 Score: The harmonic mean of precision and recall. Provides a balance
  between precision and recall, especially useful for imbalanced datasets. F1 =
  2 _ (Precision _ Recall) / (Precision + Recall)
- AUC-ROC (Area Under the Receiver Operating Characteristic Curve): The
  ROC curve plots the true positive rate (recall) against the false positive rate at
  various threshold settings. AUC measures the ability of the classifier to
  distinguish between classes. A higher AUC (closer to 1) indicates better
  performance.

- **Regression Metrics:**
  - Root Mean Square Error (RMSE): The square root of the average of the
    squared differences between predicted and actual values. Sensitive to
    outliers.
  - Mean Absolute Error (MAE): The average of the absolute differences
    between predicted and actual values. Less sensitive to outliers than RMSE.
  - R-squared (Coefficient of Determination): Represents the proportion of
    variance in the dependent variable that is predictable from the independent
    variables. A higher R-squared (closer to 1) indicates a better fit.

### Confusion Matrices

A confusion matrix is a table that visualizes the performance of a classification model by
summarizing the counts of correct and incorrect predictions. It helps you understand where
the model is making mistakes and provides insights beyond simple accuracy metrics.

Key elements of a confusion matrix:

- True Positive (TP): The model correctly predicts the positive class.
- True Negative (TN): The model correctly predicts the negative class.
- False Positive (FP): The model incorrectly predicts the positive class (Type I error).
- False Negative (FN): The model incorrectly predicts the negative class (Type II error).

### Example:

Consider a binary classification model that predicts whether an email is spam or not. A
confusion matrix might look like this:

|                  | Predicted: Spam | Predicted: Not Spam |
| ---------------- | --------------- | ------------------- |
| Actual: Spam     | TP = 100        | FN = 20             |
| Actual: Not Spam | FP = 10         | TN = 970            |

Export to Sheets

Metrics derived from the confusion matrix:

- Accuracy: The overall correctness of the model's predictions. Calculated as (TP + TN)
  / (TP + TN + FP + FN).
- Precision: The proportion of true positives among all predicted positives. Calculated
  as TP / (TP + FP).
- Recall (Sensitivity): The proportion of true positives among all actual positives.
  Calculated as TP / (TP + FN).
- F1-score: The harmonic mean of precision and recall, balancing both metrics.
  Calculated as 2 _ (Precision _ Recall) / (Precision + Recall).

Interpreting the confusion matrix and these metrics helps you understand the specific
strengths and weaknesses of your model, such as whether it tends to produce more false
positives or false negatives.

### Offline Model Evaluation

Offline evaluation involves assessing the model's performance on a held-out dataset that
was not used during training. This provides an estimate of how the model is likely to perform
on unseen data.

Common offline evaluation techniques:

- Train/Test Split: Divide the data into training and testing sets. Train the model on the
  training set and evaluate its performance on the testing set.
- K-Fold Cross-Validation: Divide the data into k equal folds. Train the model k times,
  each time using a different fold as the testing set and the remaining folds as the
  training set. Average the performance across all folds to get a more robust estimate.

Key offline evaluation metrics:

- For classification: Accuracy, precision, recall, F1-score, AUC-ROC.
- For regression: Mean Squared Error (MSE), Root Mean Squared Error (RMSE), Mean
  Absolute Error (MAE).

### Online Model Evaluation (A/B Testing)

Online evaluation assesses the model's performance in a real-world production environment
by deploying it and observing its impact on actual users or systems. A/B testing is a common
technique for online evaluation.

### A/B testing:

- Create two versions of your system or application: one with the new model (version
  B) and one with the existing model or no model at all (version A).
- Divide your users or traffic into two groups and expose each group to one of the
  versions.
- Measure and compare the performance of the two versions based on relevant
  metrics, such as conversion rates, click-through rates, or user engagement.
- Use statistical analysis to determine if there is a significant difference between the
  two versions.

### Benefits of online evaluation:

- Provides a more realistic assessment of the model's performance in real-world
  conditions.
- Captures user behavior and feedback, which may not be reflected in offline
  evaluation.
- Allows you to measure the actual business impact of the model.

### Considerations for online evaluation:

- Requires careful experimental design and statistical analysis.
- May be more complex and time-consuming than offline evaluation.
- Need to consider potential risks and impact on users during the experiment.

### Comparing Models Using Metrics

When you train multiple machine learning models on the same dataset, you need a way to
compare their performance and select the best one. This is where metrics come in. Different
metrics are suitable for different types of machine learning problems. Here's a breakdown of
common metrics and considerations:

- **Time to Train a Model:** This metric measures the computational time required to
  train a model. It's crucial in scenarios where rapid model development or frequent
  retraining is necessary. Complex models or large datasets can lead to longer training
  times.
- **Quality of Model (Performance Metrics):** This is the core of model evaluation. The
  specific metrics used depend on the type of machine learning task:
  - Regression (predicting continuous values): - Mean Squared Error (MSE): Average of the squared differences
    between predicted and actual values. Lower MSE indicates better
    performance. Sensitive to outliers. - Root Mean Squared Error (RMSE): Square root of MSE. Easier to
    interpret as it's in the same units as the target variable. - Mean Absolute Error (MAE): Average of the absolute differences
    between predicted and actual values. Less sensitive to outliers than
    MSE. - R-squared (Coefficient of Determination): Measures the proportion
    of variance in the dependent variable that is predictable from the
    independent variables. Higher R-squared (closer to 1) indicates a
    better fit.
  - Classification (predicting categories):

  - Accuracy: Proportion of correctly classified instances. Can be

misleading with imbalanced datasets. - Precision: Proportion of true positives among all predicted positives.
Measures how many of the predicted positive cases were actually
positive. - Recall (Sensitivity): Proportion of true positives among all actual
positives. Measures how many of the actual positive cases were
correctly identified. - F1-score: Harmonic mean of precision and recall. Balances precision
and recall, especially useful with imbalanced datasets. - Area Under the ROC Curve (AUC): Measures the ability of the model
to distinguish between classes. Higher AUC (closer to 1) indicates
better performance. - Confusion Matrix: A table that summarizes the performance of a
classification model by showing the counts of true positives, true
negatives, false positives, and false negatives.

- **Engineering Costs:** This includes factors like:
  - Model Complexity: More complex models may require more computational
    resources for training and inference.
  - Deployment Costs: Deploying large models can be more expensive due to
    infrastructure requirements.
  - Maintenance Costs: Complex models may be harder to maintain and debug.
  - Inference Time (Latency): The time it takes for a model to make a prediction.
    This is critical for real-time applications.

### Example Comparison:

Imagine you're building a fraud detection system. You train two models:

- Model A: High accuracy (99%), but low recall (50%). This means it correctly classifies
  most legitimate transactions but misses many fraudulent ones.
- Model B: Lower accuracy (95%), but high recall (90%). This means it catches most
  fraudulent transactions but also flags some legitimate ones as suspicious (false
  positives).

Depending on the cost of false positives (e.g., customer inconvenience), you might choose
Model B despite its lower accuracy because catching fraud is the priority.

### Performing Cross-Validation

Cross-validation is a technique used to assess how well a model generalizes to unseen data.
It helps prevent overfitting, where a model performs well on the training data but poorly on
new data. The most common type is k-fold cross-validation:

1. Divide the dataset: Split the dataset into k equal-sized folds.
2. Iterate: For each fold:

- Use the current fold as the validation set.
- Use the remaining k-1 folds as the training set.
- Train the model on the training set.
- Evaluate the model on the validation set and record the performance metrics.

3. Average: Calculate the average of the performance metrics across all k folds.

This provides a more robust estimate of the model's performance than a single train-test
split. Common values for k are 5 or 10.

### Benefits of Cross-Validation:

- Reduced overfitting: Provides a more realistic estimate of model performance on
  unseen data.
- Better use of data: Uses all data for both training and validation.
- More robust performance estimate: Averaging results across multiple folds reduces
  the impact of random data splits.
