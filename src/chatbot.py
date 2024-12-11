import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random
import pandas as pd
import json

from database_manager import InventoryDatabase
from text_processor import TextProcessor


class InventoryBot:
    def __init__(self):
        print("Loading InventoryBot...")
        self.inventory = InventoryDatabase()
        self.processor = TextProcessor()
        self.small_talk_responses = self.load_json('data/small_talk_responses.json')
        self.intents = self.load_json('data/intents.json')
        self.running = True
        self.continued = False # for continued conversation
        self.user = User()

    def load_json(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def start(self):
        user_name = input("Hi, I'm your handy kitchen chatbot, Gordon.\nWhat's your name?\n").capitalize()
        user_name = self.naming(user_name)
        self.user.set_name(user_name)
        print(f"Nice to meet you, {user_name}!")
        self.main_loop()

    def main_loop(self):
        openers = ["How can I help you today?", "What can I do for you?", "What do you need help with?", "How can I assist you?"]
        continuers = [f"What else can I help you with, {self.user.get_name()}?", f"Is there anything else you need, {self.user.get_name()}?", f"What else can I do for you, {self.user.get_name()}?"]
        while self.running:
            if self.continued:
                user_input = input(random.choice(continuers) + "\n").strip().lower()
            else:
                user_input = input(random.choice(openers) + "\n").strip().lower()
            self.handle_input(user_input)

    def handle_input(self, user_input):
        small_talk = list(self.small_talk_responses.keys())
        intent_list = list(self.intents.keys())
        while True:

            # Process user input
            tokenized_input = self.processor.tokenize(user_input)
            processed_input = self.processor.process_text(user_input) # removes stopwords also
            lemmatized_input = ' '.join(self.processor.lemmatize(tokenized_input))
            simple_input = ' '.join(self.processor.lemmatize(processed_input)) # used for intent transactions
            print(lemmatized_input)

            # Get the index of the most similar small talk response and its similarity
            index, similarity = self.processor.tfidf_cosim(small_talk, user_input)
            print(similarity)
            if similarity > 0.91:
                key = small_talk[index]
                closers = ['bye', 'goodbye', 'see you later', 'stop', 'no', 'nothing']
                # check if the user wants to end the conversation
                if (key or user_input) in closers:
                    print(random.choice(self.small_talk_responses[key]).replace("{user_name}", self.user.get_name()))
                    self.running = False
                    return

                else:
                    response = self.small_talk_responses[key]
                    print(random.choice(response).replace("{user_name}", self.user.get_name()))
                    self.continued = True
                    return

            # Question Answering section
            else:
                filepath = 'COMP3074-CW1-Dataset.csv'
                data = pd.read_csv(filepath)
                qa_dict = dict(zip(data['Question'], data['Answer']))
                questions = list(qa_dict.keys())
                processed_questions = [self.processor.tokenize(question) for question in questions]
                lemmatized_questions = [' '.join(self.processor.lemmatize(question)) for question in processed_questions]
                index, similarity = self.processor.tfidf_cosim(lemmatized_questions, lemmatized_input)
                print(similarity)

                if similarity > 0.73:
                    key = questions[index]
                    print(qa_dict[key])
                    self.continued = True
                    return

                else:
                    # Intent Commands
                    # 101: Check inventory, 102: List all inventory, 103: Low stock items
                    # 201: Add/Update Inventory, 202: Batch add items, 203: Update item quantity
                    # 301: Remove items, 302: Delete item from inventory
                    # 501: Show recent changes, 502: Generate usage report, 503: Inventory valuation
                    # 601: Help
                    intent_overview = {
                        101: "Check specific item",
                        102: "List all inventory items",
                        103: "Show Low stock items",
                        201: "Add/Update Inventory",
                        202: "Batch add items",
                        203: "Update item quantity",
                        301: "Remove items",
                        302: "Delete item from inventory",
                        501: "Show recent changes",
                        502: "Generate usage report",
                        503: "Show Inventory valuation",
                        601: "Get Help"
                    }

                    # Process intent_data
                    processed_intent_data = [self.processor.tokenize(intent) for intent in intent_list]
                    lemmatized_intent_data = [' '.join(self.processor.lemmatize(intent)) for intent in processed_intent_data]

                    # Pass the processed data into the model
                    index, similarity = self.processor.tfidf_cosim(lemmatized_intent_data, lemmatized_input)
                    print(similarity)

                    if similarity < 0.73:
                        print("I'm sorry, I didn't understand that. Could you please rephrase?")
                        user_input = input().strip().lower()
                    else:
                        key = intent_list[index]
                        intent = self.intents[key]
                        if input(f"Did you mean you want me to '{intent_overview[intent]}'? (yes/no)\n").lower() == 'yes':
                            self.execute_intent(intent, lemmatized_input)
                            self.continued = True
                            break
                        else:
                            print("Okay, let's try again. Could you please rephrase?")
                            user_input = input().strip().lower()


    def execute_intent(self, intent, user_input):
        if intent == 101:
            return self.get_item(user_input)
        elif intent == 102:
            return self.get_all_items()
        elif intent == 201:
            return self.add_item(user_input)
        elif intent == 203:
            return self.update_item(user_input)
        elif intent == 301:
            return self.remove_item(user_input)
        elif intent == 302:
            return self.delete_item(user_input)
        elif intent == 501:
            return self.show_recent_changes()
        elif intent == 502:
            return self.generate_usage_report()
        elif intent == 503:
            return self.inventory_valuation()
        elif intent == 601:
            return self.help()

    # def add_item(self, user_input):
    #
    #
    # def remove_item(self, user_input):
    #
    # def update_item(self, user_input):
    #
    def get_item(self, user_input):
        all_items = self.inventory.get_all_items()
        for item in all_items:
            for word in word_tokenize(user_input):
                if word in item[0].lower():
                    print(f"{item[0]}: {item[1]}")
                    return


    def get_all_items(self):
        all_items = self.inventory.get_all_items()
        print("Here are all the items in your inventory:\nName : Quantity")
        for item in all_items:
            print(f"{item[0]}: {item[1]}")

    # def get_item_by_id(self, user_input):

    def help(self):
        print("**Help Menu:**\nHere are some things you can ask me:\n1. **Inventory Check**\n   - \"How much of [item] do we have?\"\n   - \"List all inventory items.\"\n   - \"What items are running low?\"\n\n2. **Add/Update Inventory**\n   - \"Add 10 apples to inventory.\"\n   - \"Set oranges quantity to 20.\"\n   - \"Add these items: apples, bananas, oranges.\"\n\n3. **Remove Items**\n   - \"Remove 5 apples from inventory.\"\n   - \"Delete bananas from inventory.\"\n\n4. **Expiration and Restocking**\n   - \"Set expiration date for milk to 2024-11-30.\"\n   - \"Show me expired items.\"\n   - \"What items need restocking?\"\n\n5. **Reports**\n   - \"Show recent inventory changes.\"\n   - \"Generate usage report for last month.\"\n   - \"What’s the total inventory value?\"\n\n6. **Settings**\n   - \"Set restock threshold for apples to 5.\"\n   - \"Turn on restock notifications.\"\n\nLet me know what you’d like to do! 😊\n\n")


    def naming(self, name):
        keywords = ['my name is', 'call me', 'name is', 'change my name to', 'change name to', 'hi my name is', 'i am']
        for keyword in keywords:
            if keyword in name:
                return next(word for word in name.split() if word not in keyword.split())
        return name


class User:
    def __init__(self, name=None, age=None):
        self.name = name
        self.age = age

    def set_name(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age


if __name__ == '__main__':
    chatbot = InventoryBot()
    chatbot.start()

