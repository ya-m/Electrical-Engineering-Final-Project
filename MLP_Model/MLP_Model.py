import pandas_datareader as web
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split, GridSearchCV
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

RANDOM_SEED = 123
N_SAMPLES = 3_000


def plot_predictions(data, predictions):
    train = data[:4_500]
    valid = data[4_500:]
    valid['Predictions'] = predictions
    # Visualize the data
    plt.figure(figsize=(16, 8))
    plt.title('Model')
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Close Price USD ($)', fontsize=18)
    plt.plot(train['Close'])
    plt.plot(valid[['Close', 'Predictions']])
    plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
    plt.show()


def plot_loss_curve(loss_values):
    plt.figure(figsize=(18, 8))
    plt.title('Loss Curve Of The Model')
    plt.plot(loss_values)
    plt.xlabel('Iteration', fontsize=18)
    plt.ylabel('Loss value', fontsize=18)
    plt.show()


def main():
    df = web.DataReader('AAPL', data_source='yahoo', start='2000-01-01', end='2019-12-19')
    rate_of_increase_in_vol = [0]
    rate_of_increase_in_adj_close = [0]
    for i in range(1, len(df)):
        rate_of_increase_in_vol.append(df.iloc[i]['Volume'] - df.iloc[i - 1]['Volume'])
        rate_of_increase_in_adj_close.append(df.iloc[i]['Adj Close'] - df.iloc[i - 1]['Adj Close'])
    df['Increase_in_vol'] = rate_of_increase_in_vol
    df['Increase_in_adj_close'] = rate_of_increase_in_adj_close
    print(df.head(5))
    y = df['Close']
    dataset = y.values
    X = df.drop(['Close'], axis=1)
    # X, y = resample(X, y, n_samples=N_SAMPLES, random_state=RANDOM_SEED)
    # Scale the all of the data to be values between 0 and 1
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(y.values.reshape(-1, 1))
    X = StandardScaler().fit_transform(X)
    # x_train, x_test, y_train, y_test = train_test_split(X, scaled_data, test_size=0.3)
    x_train = X[:4_500]
    y_train = scaled_data[:4_500]
    x_test = X[4_500:]
    y_test = y[4_500:]
    best_model, gcv = search_best_model(x_train, y_train)
    print(f'{gcv.best_params_=}')
    # model.fit(x_train, y_train)
    # print(f'{model.loss=},{model.best_loss_=}')
    pred = best_model.predict(x_test)
    ys = scaler.inverse_transform(pred.reshape(-1, 1))
    plot_loss_curve(best_model.loss_curve_)
    plot_predictions(df.filter(['Close']), ys)
    print(f'{mean_absolute_error(y_test,ys)=}')
    print(f'Mean absolute error percentage: {(mean_absolute_error(y_test, ys)) * 100}')
    print(f'Validation over training percentage: {(1 - (mean_absolute_error(y_test, ys))) * 100}')
    print(f'{mean_squared_error(y_test,ys)=}')
    print(f'Prediction: {ys[len(ys) - 1]}')
    print(f'closing price: {dataset[len(dataset) - 1]}')
    print('done')


def search_best_model(x_train, y_train):
    model = MLPRegressor(random_state=RANDOM_SEED)
    params = {
        'hidden_layer_sizes': [(10, 5, 3)],
        'activation': ['relu'],
        'solver': ['adam'],
        'learning_rate_init': [.01],
        'max_iter': [200]
    }
    gcv = GridSearchCV(model, params, scoring='neg_mean_squared_error', cv=5, verbose=4, n_jobs=4)
    gcv.fit(x_train, y_train.flatten())
    best_model = gcv.best_estimator_
    return best_model, gcv


if __name__ == '__main__':
    main()

# 'hidden_layer_sizes': [(7, 5, 3), (10, 5, 3)],
# 'activation': ['relu', 'tanh'],
# 'solver': ['sgd', 'adam', 'lbfgs'],
# 'learning_rate_init': [.01, .001, .0001],
# 'max_iter': [200, 500, 700]
