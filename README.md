# TicketStoreProject
This was a project for a Defensive Programming class in 2020. The purpose was to create a mock ticket purchasing store that had specific, intentional vulnerabilities for the other classmates to find.

The first vulnerability was in the ticket search section. If a user selects to purchase the 3rd ticket option in the menu but cancels the purchase before it is completed, and then exits to the main menu, the program will crash. The reason for this bug is that initially, there is a numerical value passed in as a string. This numeric value is later used in a calculation and transformed into an integer. If the user backs out of the transaction, the int value is not transformed back into a string, and thus crashes the program when the integer value is concatenated with another string.

The second vulnerability is that the codes meant to redeem points can be reused. The program only keeps track of which code was used last, even though it states that it keeps track of all used over an account's lifetime. If a user wants to reuse a code, they would just need to cycle between two different codes.

