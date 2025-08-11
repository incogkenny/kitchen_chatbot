
# **Gordon – Kitchen Inventory Chatbot**

**Gordon** is a Python-based chatbot designed to streamline kitchen inventory management through natural language interaction. It enables users to add, update, check, and remove inventory items, while also offering helpful features like small talk, guidance prompts, and intelligent error handling.

The system is built to demonstrate strong software engineering practices, combining **Natural Language Processing (NLP)**, database integration, and conversational design principles.

There is also a scientific report for this project [here](Chatbot_Report.pdf).

---

## **Key Features**

* **Inventory Management**

  * Check quantities of specific items or view the full inventory.
  * Add or update items, including batch additions.
  * Remove specific quantities or delete items entirely.

* **Conversational Interface**

  * Small talk responses for a friendly, human-like experience.
  * Help prompts to guide first-time users.
  * Confirmation system (implicit & explicit) to reduce user errors.

* **Error Handling**

  * Handles ambiguous or incomplete inputs gracefully.
  * Suggests alternative commands when confidence is low.

---

## **Technical Stack**

* **Python 3.9+** – Core programming language.
* **NLTK** – Natural Language Processing for tokenisation and intent detection.
* **scikit-learn** – TF-IDF and cosine similarity for intent matching.
* **SQLite3** – Local database for persistent inventory storage.

---

## **System Architecture**

The chatbot follows a modular design, consisting of:

1. **Intent Matching Module** – Classifies user inputs into predefined intents using TF-IDF vectorisation and cosine similarity.
2. **Response Generator** – Produces responses based on matched intent, confidence score, and conversation context.
3. **Database Layer** – Handles CRUD operations on the SQLite database.
4. **Interface Layer** – Provides a terminal-based interface for interaction.

---

## **Installation**
Make sure you have python 3.12 or higher installed.

1. Clone the repository
```bash
git clone https://github.com/incogkenny/kitchen_chatbot.git
```

2. Install dependencies
```bash
pip install -r requirements.txt
```


## **Usage**

Run the chatbot:

```bash
python chatbot.py
```

Example interaction:

```
> Hello
Hi there! How can I help you today?

> Add 5 apples
5 apples have been added to your inventory.

> How much milk do I have?
You have 2 cartons of milk in stock.

> Help
[Displays a list of available commands with examples]
```

---

## **Evaluation Summary**

* **Task Completion Rate:** 90%
* **Intent Detection Accuracy:** 88%
* **Error Recovery Success:** 85%
* Positive feedback on **help command** usability and **confirmation prompts**.

---

## **Future Enhancements**

* Advanced NLP with spaCy or transformer models for improved intent recognition.
* Voice command support for hands-free operation.
* Meal planning and grocery list integration.
* Expiration alerts for better food management.

---

## **License**

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
