# AI-Voice-Assistant


The project consists of three main files:

1. **`intents.json`**: Contains predefined user intents, patterns (phrases that the user might say), and associated responses.
2. **`main.py`**: The main script to run the chatbot, handling user input, loading intents, and responding with appropriate replies.
3. **`train.py`**: A script used to train the machine learning model for intent classification.

---

## File Descriptions

### 1. **intents.json**
This file stores the dataset of the chatbot's intents. Each intent has:
- **Tag**: A label for the intent, e.g., `services`, `jokes`, `random_fact`.
- **Patterns**: Phrases or questions that users might say to trigger that intent.
- **Responses**: Predefined responses that the bot will reply with if the user's input matches the intent's pattern.

For example:
- **Tag**: `jokes`
  - **Patterns**: "joke", "tell me a joke"
  - **Responses**: "Why don't scientists trust atoms? Because they make up everything!"

### 2. **main.py**
This script likely serves as the core of the chatbot system. It is responsible for:
- Loading and processing the intents from `intents.json`.
- Capturing user input and identifying which intent (if any) the input matches.
- Responding with a relevant response based on the matched intent.

### 3. **train.py**
This script is used to train a machine learning model that classifies user inputs into intents. It might involve:
- Tokenizing and vectorizing the user patterns in `intents.json`.
- Training a classification model (such as a neural network or SVM) to predict which intent a user input matches.
- Saving the trained model to be used in `main.py` for real-time predictions.

---

## Usage Instructions

### Requirements
To run the chatbot, ensure the following Python libraries are installed:
- `tensorflow` or `keras` (for training the model)
- `numpy`
- `json`

You can install them using the following command:
```bash
pip install tensorflow numpy
```

### Running the Chatbot

1. **Training the Model**
   Before running the chatbot, you may need to train the intent classification model by executing `train.py`:
 
   python train.py
 
   This will process the `intents.json` file and train the model based on the defined patterns.

2. **Running the Bot**
   After training, you can run the chatbot by executing `main.py`:
 
   python main.py


The bot will now be able to process user inputs, match them to an intent, and respond with appropriate replies.



## Extending the Project

- **Adding New Intents**: To add more functionality, simply update `intents.json` with new tags, patterns, and responses.
- **Improving Responses**: You can improve or modify the responses in `intents.json` to make the chatbot more engaging.
- **Model Improvement**: To increase the accuracy of intent detection, you can tweak the model architecture in `train.py` or add more training data.



 Example Interactions

- **User**: "Tell me a joke"
- **Bot**: "Why don't scientists trust atoms? Because they make up everything!"

- **User**: "Give me a random fact"
- **Bot**: "The world's largest snowflake on record was 15 inches wide and 8 inches thick."



 License

ALi Altrkbi



