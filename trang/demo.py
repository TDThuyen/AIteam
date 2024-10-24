# chatGPT
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

file_path = '/home/trang/aiops/AI/demo/output_with_bands (1).csv' 
data = pd.read_csv(file_path)

# Drop rows with NaN in 'SymbolID'
data = data.dropna(subset=['SymbolID'])

# Ensure 'SymbolID' is treated as integer
data['SymbolID'] = data['SymbolID'].astype(int)

# Features and target variable
X = data[['LAT', 'LONG', 'B04', 'B05', 'B06']]  # Features 
y = data['SymbolID']  # Target 

# Check class distribution
print("Class distribution:\n", y.value_counts())

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Initialize the model with regularization parameters
model = XGBClassifier(
    objective='multi:softmax',
    num_class=5,
    eval_metric='mlogloss',
    max_depth=3,           # limit tree depth
    min_child_weight=1,    # minimum sum of instance weight needed in a child
    subsample=0.8,         # subsample ratio of training instances
    colsample_bytree=0.8   # subsample ratio of columns when constructing each tree
)

# Perform cross-validation
cv_scores = cross_val_score(model, X, y, cv=5)  # 5-fold cross-validation
print(f'Cross-Validation Accuracy: {cv_scores.mean():.2f} ± {cv_scores.std():.2f}')

# Fit the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:')
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

# Plot Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=np.unique(y), yticklabels=np.unique(y))
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

# Function to plot learning curves
def plot_learning_curve(model, X, y):
    train_sizes = np.linspace(0.1, 1.0, 5)
    train_scores = []
    test_scores = []

    for train_size in train_sizes:
        X_train, X_val, y_train, y_val = train_test_split(X, y, train_size=train_size, stratify=y)
        model.fit(X_train, y_train)
        train_scores.append(model.score(X_train, y_train))
        test_scores.append(model.score(X_val, y_val))

    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_scores, label='Training Accuracy', marker='o')
    plt.plot(train_sizes, test_scores, label='Validation Accuracy', marker='o')
    plt.title('Learning Curves')
    plt.xlabel('Training Set Size')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid()
    plt.show()

# Plot learning curves
plot_learning_curve(model, X, y)
