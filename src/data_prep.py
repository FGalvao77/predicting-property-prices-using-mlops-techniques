import pandas as pd
from sklearn.datasets import fetch_openml, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_prepare_data(test_size=0.2, random_state=42, descr:bool=False, selected_features=None):
    # Load the housing dataset from OpenML
    housing = fetch_openml(name='house_prices', as_frame=True)
    if descr == True:
        print('\n\tDataset Description:')
        print(housing.DESCR)

    X = pd.DataFrame(housing.data, columns=housing.feature_names)
    y = pd.Series(housing.target, name='target')

    # Remove 'Id' column if it exists
    if 'Id' in X.columns:
        X = X.drop(columns=['Id'])
    
    # Select only numeric columns
    X = X.select_dtypes(include=['number'])
    
    # Select specific features if provided, otherwise use all
    if selected_features is not None:
        X = X[selected_features]
    
    feature_names = X.columns.tolist()
    
    # Handle missing values
    X = X.fillna(X.mean())

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Standardize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train.values, y_test.values, feature_names

if __name__ == '__main__':
    X_train, X_test, y_train, y_test, feature_names = load_and_prepare_data(descr=True)
    print('=' * 50)
    print('Shapes:')
    print(f'X_train: {X_train.shape} | y_train: {y_train.shape}')
    print(f'X_test : {X_test.shape}  | y_test: {y_test.shape}')
    print(f'Features used: {len(feature_names)}')
    print('=' * 50)
    print('++++++++++ Data preparation complete!!! ++++++++++\n')