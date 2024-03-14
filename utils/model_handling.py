from tensorflow import keras


def initialize_model(input_shape, output_shape):
    """Initialize the model with the input and output shapes."""
    model = keras.Sequential([
        keras.layers.Dense(8, activation='relu', input_shape=(input_shape,)),
        keras.layers.Dense(8, activation='relu'),
        keras.layers.Dense(output_shape, activation='softmax')
    ])
    # TODO: Add some logging
    return model


def train_model(model, training, output, epochs=1000, batch_size=8):
    """Train the model with the provided training and output data."""
    # TODO: Add some logging
    # model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])  # TODO: refactor
    model.fit(training, output, epochs=epochs, batch_size=batch_size)
    save_model(model)
    # TODO: Add some logging


def save_model(model, filename="ai_chat_bot_model.keras"):
    """Save the model to a file."""
    model.save(filename)
    # TODO: Add some logging


def load_model(filename="ai_chat_bot_model.keras"):
    """Load a model from a file."""
    model = keras.models.load_model(filename)
    # TODO: Add some logging
    return model


def set_model(training_data, output_data):
    model = initialize_model(input_shape=len(training_data[0]), output_shape=len(output_data[0]))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    try:
        model = load_model()
    except:
        train_model(model, training_data, output_data)

    return model
