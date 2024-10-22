import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

file_path = '/home/trang/aiops/AI/demo/output_with_bands (1).csv' 
data = pd.read_csv(file_path)

data = data.dropna(subset=['SymbolID'])

data['SymbolID'] = data['SymbolID'].astype(int)
X = data[['LAT', 'LONG', 'B04', 'B05', 'B06']]  # Feature 
y = data['SymbolID']  # Target 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = XGBClassifier(objective='multi:softmax', num_class=5, eval_metric='mlogloss')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:')
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=[0, 1, 2, 3, 4], yticklabels=[0, 1, 2, 3, 4])
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show() 