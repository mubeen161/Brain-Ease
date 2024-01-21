import streamlit as st
from datetime import datetime
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import json
import os

class Journal:
    def __init__(self, journal_type):
        self.journal_type = journal_type
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

    def view_entries(self):
        st.header("Journal Entries")
        for index, entry in enumerate(self.entries, start=1):
            timestamp = entry["timestamp"]
            entry_text = entry["entry_text"]
            st.write(f"{index}. {timestamp}\n{entry_text}\n")

    def search_entries(self, keyword):
        st.header("Matching Entries")
        matching_entries = [entry for entry in self.entries if keyword.lower() in entry["entry_text"].lower()]
        if matching_entries:
            for index, entry in enumerate(matching_entries, start=1):
                timestamp = entry["timestamp"]
                entry_text = entry["entry_text"]
                st.write(f"{index}. {timestamp}\n{entry_text}\n")
        else:
            st.write("No matching entries found.")

    def view_entries(self):
        st.header("Journal Entries")
        for index, entry in enumerate(self.entries, start=1):
            timestamp = entry["timestamp"]
            entry_text = entry["entry_text"]
            st.write(f"{index}. {timestamp}\n{entry_text}\n")

    def delete_entry(self, index):
        if 0 <= index < len(self.entries):
            deleted_entry = self.entries.pop(index)
            st.write("Entry deleted:")
            st.write(deleted_entry)
        else:
            st.write("Invalid entry index.")

    def sentiment_analysis(self):
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        for entry in self.entries:
            entry_text = entry["entry_text"]
            blob = TextBlob(entry_text)
            polarity = blob.sentiment.polarity

            if polarity > 0.2:
                positive_count += 1
            elif polarity < -0.2:
                negative_count += 1
            else:
                neutral_count += 1
        
        return positive_count, negative_count, neutral_count

    def generate_word_cloud(self):
        all_text = " ".join([entry["entry_text"] for entry in self.entries])
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title("Word Cloud of Journal Entries")
        st.pyplot()

    def save_entries(self):
        data = {
            "journal_type": self.journal_type,
            "entries": self.entries
        }
        filename = f"{self.journal_type}_journal.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        st.write("Entries saved!")

    def load_entries(self):
        filename = f"{self.journal_type}_journal.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
                self.entries = data["entries"]
                st.write("Entries loaded!")
        else:
            st.write("No journal entries found.")


class DashboardUI:
    @staticmethod
    def display_visualizations(journal):
        st.header("Visualizations")

        # Sentiment Analysis Visualization
        positive_count, negative_count, neutral_count = journal.sentiment_analysis()
        st.subheader("Sentiment Analysis")
        st.write(f"Positive entries: {positive_count}")
        st.write(f"Negative entries: {negative_count}")
        st.write(f"Neutral entries: {neutral_count}")

        # Tag Distribution Visualization
        tag_counts = {}
        for entry in journal.entries:
            tags = entry.get("tags", [])
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        tag_df = pd.DataFrame.from_dict(tag_counts, orient="index", columns=["Count"])
        st.subheader("Tag Distribution")
        st.bar_chart(tag_df)

        # Rating Distribution Visualization
        ratings = [entry.get("rating", 0) for entry in journal.entries]
        rating_df = pd.DataFrame(ratings, columns=["Rating"])
        st.subheader("Rating Distribution")
        st.bar_chart(rating_df["Rating"].value_counts().sort_index())

        # Word Cloud Visualization
        st.subheader("Word Cloud of Journal Entries")
        journal.generate_word_cloud()


# Main function for Streamlit app
def main():
    st.title("Your Digital Journaling System")
    journal_type = st.selectbox("Select journal type", ["mood", "thought"], key="journal_type_selectbox")

    journal = Journal(journal_type)
    choice_options = [
        "Add entry", "View entries", "Search entries", "Edit entry", "Delete entry",
        "Sentiment analysis", "Generate word cloud", "Save entries", "Load entries", "Exit"
    ]

    while True:
        choice = st.sidebar.selectbox(
            "Menu",
            choice_options,
            key="menu_selectbox"
        )

        if choice == "Add entry":
            entry_text = st.text_area("Enter your journal entry:")
            if st.button("Add Entry"):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                entry = {"timestamp": timestamp, "entry_text": entry_text}
                if journal_type == "mood":
                    positive_mood = st.text_input("Enter your positive mood:")
                    negative_mood = st.text_input("Enter your negative mood:")
                    entry["positive_mood"] = positive_mood
                    entry["negative_mood"] = negative_mood
                journal.add_entry(entry)
                st.success("Entry added!")

        elif choice == "View entries":
            journal.view_entries()

        elif choice == "Search entries":
            keyword = st.text_input("Enter keyword to search:")
            if st.button("Search"):
                journal.search_entries(keyword)

        elif choice == "Edit entry":
            index = st.number_input("Enter the index of the entry to edit:", min_value=1, max_value=len(journal.entries))
            new_text = st.text_area("Enter the new text:")
            if st.button("Edit Entry"):
                journal.edit_entry(index - 1, new_text)
            
        elif choice == "Delete entry":
            index = st.number_input("Enter the index of the entry to delete:", min_value=1, max_value=len(journal.entries))
            if st.button("Delete Entry"):
                journal.delete_entry(index - 1)
            
        elif choice == "Sentiment analysis":
            DashboardUI.display_visualizations(journal)

        elif choice == "Generate word cloud":
            journal.generate_word_cloud()

        elif choice == "Save entries":
            journal.save_entries()

        elif choice == "Load entries":
            journal.load_entries()

        elif choice == "Exit":
            st.write("Exiting...")
            break


if __name__ == "__main__":
    main()
