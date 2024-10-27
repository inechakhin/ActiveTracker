import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.metrics import mean_squared_error, mean_absolute_error
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from keras.regularizers import l2

f_df = pd.read_csv("dataset/features.csv")
t_df = pd.read_csv("dataset/traits.csv")
df = pd.merge(f_df, t_df, on="id")
df.drop("id", axis=1, inplace=True)

X = df.iloc[:, :-5]
y = df.iloc[:, -5:]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

model = Sequential()
model.add(Dense(32, input_dim=X_train.shape[1], activation="relu", kernel_regularizer=l2(0.01)))
#model.add(Dense(16, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(5, activation="sigmoid"))

# model.compile(optimizer=Adam(learning_rate=0.001),loss="mean_squared_error",metrics=["mean_absolute_error"])
# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.compile(optimizer='adam',loss="mean_squared_error",metrics=["mean_absolute_error"])

early_stopping = EarlyStopping(monitor="mean_absolute_error", patience=10, restore_best_weights=True)

history = model.fit(
    X_train,
    y_train,
    epochs=100,
    batch_size=5,
    validation_data=(X_test, y_test),
    callbacks=[early_stopping],
)

model_json = model.to_json()
with open("info/model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("info/model.h5")



