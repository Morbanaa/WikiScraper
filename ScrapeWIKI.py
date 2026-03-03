# Wiki Scraper
# Morbanaa Studios
# By Teddy Rodd

import wikipedia
import mysql.connector
import platform
import os

import warnings
from bs4 import GuessedAtParserWarning

warnings.filterwarnings("ignore", category=GuessedAtParserWarning)  # Stops warning from beautiful soup


# ============================================================
# main()
# ------------------------------------------------------------
# Program entry point.
# Establishes database connection and displays the main menu.
# Uses a loop to continuously prompt the user for actions
# until they choose to exit. Calls the appropriate function
# based on user input.
# ============================================================
def main():

    # Connect to database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="mydb"
    )

    view_header = False

    while True:

        # Get user choice
        print("Would you like to:")
        print("(1) Search for a article on wiki:")
        print("(2) Add a article to your database:")
        print("(3) Delete an article from your database:")
        print("(4) View an article from your database:")
        print("(5) Show list of articles on your database:")
        print("(6) Exit Program:")

        choice = input("Choose: ").upper()

        clear_screen()

        # Activates function based on user input
        match choice:
            case "1":
                search_wiki(conn)
            case "2":
                add_row(conn)
            case "3":
                view_header = False
                delete_row(conn, view_header)
            case "4":
                view_header = False
                view_selected_content(conn, view_header)
            case "5":
                view_header = True
                view_page_headers(conn, view_header)
            case "6":
                break
            case _:
                continue


# ============================================================
# search_wiki(conn)
# ------------------------------------------------------------
# Prompts the user for a search term and queries Wikipedia
# using the wikipedia.search() function.
# Displays a list of matching article titles.
# Handles general API exceptions gracefully.
# ============================================================
def search_wiki(conn):

    while True:

        print()
        choice = input("Please enter an article to search for (Enter (Q) to Quit): ")

        if choice.upper() == "Q" or choice == "q":
            break

        try:
            results = wikipedia.search(choice)

            if not results:
                print("No results found.\n")
            else:
                print("\nResults:\n---------")
                for result in results:
                    print(result)
                print()

        except Exception as e:
            print("\nWikipedia API failed.")
            print("This is likely a package/API issue.")
            print("Error:", e)

    clear_screen()


# ============================================================
# add_row(conn)
# ------------------------------------------------------------
# Prompts the user for an article title.
# Retrieves the full Wikipedia page (without auto-suggest).
# Extracts title, URL, and summary.
# Inserts the data into the MySQL table "wiki_stuff".
# Handles DisambiguationError when the term is ambiguous.
# ============================================================
def add_row(conn):

    while True:

        print()
        choice = input("Enter the name of the article you would like to add to your database (Enter (Q) to Quit): ")

        if choice == "Q" or choice == "q":
            break
        else:

            cursor = conn.cursor()  # Opens connection

            try:
                page = wikipedia.page(choice, auto_suggest=False)

                print("We added the closest match to your search")

                data = []
                data.append(page.title)
                data.append(page.url)
                data.append(page.summary)

                query = "insert into wiki_stuff (title,url,summary) values (%s,%s,%s)"
                cursor.execute(query, data)
                conn.commit()

                data.clear()

            except wikipedia.exceptions.DisambiguationError as e:
                print("\nThat term is ambiguous. Did you mean:\n")

                for option in e.options[:5]:
                    print("-", option)

                print("\nPlease try again with a more specific title.\n")

            cursor.close()  # Closes connection

        print()

    clear_screen()


# ============================================================
# delete_row(conn, view_header)
# ------------------------------------------------------------
# Displays current stored article headers.
# Prompts the user to select an article by ID.
# Deletes the selected row from the MySQL database.
# ============================================================
def delete_row(conn, view_header):

    while True:

        print()
        cursor = conn.cursor()  # Open connection

        view_page_headers(conn, view_header)

        selection = []
        choice = input("Enter the id of the article to remove from your database (Enter (Q) to Quit):")

        clear_screen()

        if choice == "Q" or choice == "q":
            break

        selection.append(choice)

        query = "delete from wiki_stuff where id = (%s)"
        cursor.execute(query, selection)
        conn.commit()

        selection.clear()

        cursor.close()  # Close connection

    clear_screen()


# ============================================================
# view_selected_content(conn, view_header)
# ------------------------------------------------------------
# Displays stored article headers.
# Prompts the user to select an article by ID.
# Retrieves the full row from the database and prints
# the stored title, URL, and summary.
# ============================================================
def view_selected_content(conn, view_header):

    while True:

        print()
        cursor = conn.cursor()  # Open connection

        view_page_headers(conn, view_header)

        selection = []
        choice = input("Enter the id of the article you would like to view (Enter (Q) to Quit): ")

        clear_screen()

        if choice == "Q" or choice == "q":
            break

        selection.append(choice)

        query = "select * from wiki_stuff where id = (%s)"
        cursor.execute(query, selection)
        results = cursor.fetchall()

        print("Selected Article:")
        print("-----------------")

        for result in results:
            for row in result:
                print(row)

        print()

        selection.clear()
        cursor.close()


# ============================================================
# view_page_headers(conn, view_header)
# ------------------------------------------------------------
# Retrieves and displays a list of all stored article IDs
# and titles from the database.
# If view_header is True, waits for user input before
# returning to the main menu.
# ============================================================
def view_page_headers(conn, view_header):

    cursor = conn.cursor()  # Opens connection

    query = "select id,title from wiki_stuff"
    cursor.execute(query)
    results = cursor.fetchall()

    print("\nYour Articles:")
    print("-------------")

    for result in results:
        for stuff in result:
            print(stuff, end=" ")
        print()

    print()

    if view_header == True:
        input("Press enter to return to menu: ")
        clear_screen()

    cursor.close()


# ============================================================
# clear_screen()
# ------------------------------------------------------------
# Clears the terminal screen.
# Uses "cls" for Windows and "clear" for other OS systems.
# ============================================================
def clear_screen():

    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


# ============================================================
# Program Point Of Entry
# ============================================================
if __name__ == "__main__":
    main()

    # Last Message
    print("\nDon't have a good day, have a great day : )\n")