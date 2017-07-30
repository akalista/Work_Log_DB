import Database
import os
import re

from Errors import Error

db = Database
error = Error()


# Clear Screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Main Menu function
def main_menu():
    input("Press enter to return to the main menu!")


# Strips the headers off the delete_list
def strip(delete_list):
    # Slice indexes are specific to headers
    employee_str, task_str, time_str = delete_list[0], delete_list[1], delete_list[2]
    notes_str, date_str = delete_list[3], delete_list[4]
    employee_str, task_str, time_str, notes_str, date_str = employee_str[10:], task_str[11:], time_str[12:], notes_str[18:], date_str[15:]
    delete_list2 = [employee_str, task_str, time_str, notes_str, date_str]
    return delete_list2


# Creates a more pleasant display for the iteration menu
def display(list_of_lists, header_list):
    print(list_of_lists)
    print(header_list)
    # For loops combine list_of_lists and header_list into a readable list to display
    for entries in list_of_lists:
        count = 0
        for variables in entries:
            variables1 = header_list[count] + variables
            entries[count] = variables1
            count += 1
    return list_of_lists


# Iteration menu for browsing entries
def iteration_menu(list_object):
    '''
    The iteration menu function provides a way for the user of the program to
    scroll through the options they are given in a more pleasant visual way. Each
    Entry that the user scrolls through will be able to be deleted and edited. The
    menu runs off several while loops and a couple of indexes that keep track of
    the users place in the incoming lists.
    '''

    # Set incoming list length, loop to True, headers list, and create the display for the menu
    list_length, running = len(list_object), True
    headers = ['Employee: ', 'Task Name: ', 'Time Spent: ', 'Additional Notes: ', 'Date of Entry: ']
    display(list_object, headers)

    # First running loop
    while running:

        # If there are no matches break loop and go to main menu
        if list_length == 0:
            print("Looks like your search found no matches, sorry!\n")
            main_menu()
            break

        # Set indexes, second while loop to True, and print the first item in the list
        # REGEX if list chars run over 60, newline starts
        run1, index, back_index = True, 1, -1
        print(re.sub("(.{60})", "\\1\n", ('\n'.join(list_object[0])), 0))

        while run1:

            # If list length is 1, special menu presented with no options to scroll, if to correct for mistakes
            if list_length == 1:
                user_in = input("\nWould you like to go [B]ack, [E]dit the entry, or [D]elete the entry?\n>>")
                if user_in.upper() not in ['B', 'E', 'D']:
                    print("Only one entry available, choose from the given options!")
                    continue
            # If list length is greater than 1, other menu appears, all options preset
            else:
                user_in = input("\nWould you like to see the [N]ext object, [P]revious object, go [B]ack,\n"
                                "[E]dit the entry, or [D]elete the entry?\n>>")
            clear_screen()

            # If user selects 'N", and proper conditions met, the entry at 'index' is shown
            if user_in.upper() == "N":
                if 0 <= index < list_length:
                    print(re.sub("(.{60})", "\\1\n", '\n'.join(list_object[index]), 0))
                    # Index and back_index += 1 after print
                    index += 1
                    back_index += 1
                # Message shown if no more entries
                else:
                    print("There are no more entries to browse through!\n")
                    continue

            # If user selects 'P' and proper conditions met, entry at 'back_index' is shown
            elif user_in.upper() == "P":
                if back_index >= 0:
                    print(re.sub("(.{60})", "\\1\n", '\n'.join(list_object[back_index]), 0))
                    # Index and back_index +=1 after print
                    index -= 1
                    back_index -= 1
                # Message shown if no more entries
                else:
                    print("There are no more entries, look at the next entry or go back to the main menu.\n")
                    continue

            # If user selects 'B' both loops set to false and main menu presented
            elif user_in.upper() == "B":
                run1 = False
                running = False
                main_menu()

            # If user selects 'D' the list at index - 1 is stripped of the header
            elif user_in.upper() == "D":
                delete_item = strip(list_object[index - 1])
                db.delete_entry(delete_item)
                print("Item has been deleted!")
                main_menu()
                running = False
                break

            # If user selects 'E', the list at index - 1 is stripped of the header
            elif user_in.upper() == "E":
                # Options appear for the list edit, verify list option with error check
                print("What would you like to edit:\n1: Date of Task\n2: Task Name"
                      "\n3: Time Spent\n4: Additional Notes")
                to_edit = error.int_error(1, 5)
                edit_item = strip(list_object[index - 1])
                db.edit_entry(edit_item, to_edit)
                print("Item has been edited!")
                main_menu()
                running = False
                break


# Main loop
def work_loop():

    run = True

    while run:
        # Print work log menu with options, check for errors and clear screen
        print("Welcome to the work log! Options are listed below!")
        print("1: Add new entry\n2: Lookup previous entry\n3: Exit the program")

        main_choice = error.int_error(1, 4)

        # DONE NEEDS COMMENTS
        if main_choice == 1:
            clear_screen()
            db.add_entry()
            print("New entry created!")
            main_menu()
            clear_screen()

        # LOOK UP ENTRY
        elif main_choice == 2:
            clear_screen()
            # Print menu of choices to look up by, check for errors
            print("Would you like to look up pattern by:\n1: Date\n2: Time Spent\n"
                  "3: Exact Search\n4: Employee\n5: Date Range")

            user_input1 = error.int_error(1, 6)

            # DONE NEEDS COMMENTS
            if user_input1 == 1:
                clear_screen()
                dates = db.pull_dates()
                print("Available dates are:")
                for date in dates:
                    print(date)
                print()
                # GET USER INPUT AND CHECK FOR ERROR
                date_input = error.time_error()
                # MENU
                clear_screen()
                iteration_menu(db.pull_dates1(date_input))
                clear_screen()

            # DONE NEEDS COMMENTS
            elif user_input1 == 2:
                clear_screen()
                time_input = error.time_spent_error()
                clear_screen()
                iteration_menu(db.pull_time_spent(time_input))
                clear_screen()

            # DONE NEEDS COMMENTS
            elif user_input1 == 3:
                clear_screen()
                string_input = error.empty_search_error()
                clear_screen()
                iteration_menu(db.pull_string(string_input))
                clear_screen()

            # DONE NEEDS COMMENTS
            elif user_input1 == 4:
                clear_screen()
                employees = db.pull_names()
                print("Available employees with entries are:")
                for employee in employees:
                    print(employee)
                print()
                employee_input = error.empty_string_error()
                clear_screen()
                iteration_menu(db.pull_name(employee_input))
                clear_screen()

            # DONE NEEDS COMMENTS
            elif user_input1 == 5:
                clear_screen()
                date1_input = error.time_error2('start')
                date2_input = error.time_error2('end')
                clear_screen()
                iteration_menu(db.pull_date_range(date1_input, date2_input))
                clear_screen()

        # DONE NEEDS COMMENTS
        elif main_choice == 3:
            print("Goodbye!")
            run = False


if __name__ == '__main__':
    db.initialize()
    work_loop()
    db.close()

