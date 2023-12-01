import tkinter as tk
from tkinter import messagebox
import mysql.connector

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")

        self.question_label = tk.Label(root, text="Question:")
        self.question_label.pack()

        self.options = []
        for i in range(4):
            option = tk.Radiobutton(root, text="", variable=tk.StringVar(), value=i+1)
            option.pack()
            self.options.append(option)

        self.next_button = tk.Button(root, text="Next", command=self.next_question)
        self.next_button.pack()

        # Connect to MySQL
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='finalquiz'
        )
        self.cursor = self.connection.cursor()

        self.current_question = 0
        self.load_question()

    
    def add_sample_questions(self):
        try:
            # Sample question data
            sample_questions = [
                {
                    'question_text': 'What is the capital of France?',
                    'option1': 'Berlin',
                    'option2': 'Paris',
                    'option3': 'London',
                    'option4': 'Madrid',
                    'correct_option': 2,
                },
                # Add more sample questions as needed
            ]

            # Insert sample questions into the database
            insert_query = """
            INSERT INTO questions (question_text, option1, option2, option3, option4, correct_option)
            VALUES (%(question_text)s, %(option1)s, %(option2)s, %(option3)s, %(option4)s, %(correct_option)s)
            """

            for question_data in sample_questions:
                self.cursor.execute(insert_query, question_data)

            # Commit the changes
            self.connection.commit()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while adding sample questions: {str(e)}")


    def load_question(self):
        self.cursor.execute("SELECT * FROM finalquiz.questions WHERE id = %s", (self.current_question + 1,))
        question_data = self.cursor.fetchone()

        if question_data:
            question_text = question_data[1]
            options = question_data[2:6]

            self.question_label.config(text=question_text)

            for i, option_text in enumerate(options):
                self.options[i].config(text=option_text)

        else:
            self.show_result()

    def next_question(self):
        selected_option = None
        for i, option in enumerate(self.options):
            if option.get():
                selected_option = i + 1

        if selected_option is not None:
            self.cursor.execute("SELECT correct_option FROM questions WHERE id = %s", (self.current_question + 1,))
            correct_option = self.cursor.fetchone()[0]

            if selected_option == correct_option:
                messagebox.showinfo("Correct", "Your answer is correct!")
            else:
                messagebox.showinfo("Incorrect", "Your answer is incorrect.")

            self.current_question += 1
            self.load_question()

        else:
            messagebox.showwarning("Warning", "Please select an option.")

    def show_result(self):
        messagebox.showinfo("Quiz Complete", "You have completed the quiz!")


        # Close the MySQL connection
        self.cursor.close()
        self.connection.close()

        # Close the Tkinter window
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
