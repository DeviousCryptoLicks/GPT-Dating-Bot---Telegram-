 
### Key Features:
1. **Bot Start (`/start` command)**:
   - Initializes the bot and displays the main menu with different options like generating Tinder profiles, creating opener messages, starting a conversation, etc.

2. **GPT Chat (`/gpt` command)**:
   - Engages in a GPT chat session where the user can ask questions, and the bot responds using GPT.

3. **Date Simulation (`/date` command)**:
   - Simulates a conversation where the user can "invite" celebrities such as Ariana Grande, Margot Robbie, Zendaya, Ryan Gosling, or Tom Hardy on a date. GPT generates responses based on this interaction.

4. **Message Generation (`/message` command)**:
   - Helps the user create a sequence of messages, providing options to continue the conversation or invite the recipient on a date.

5. **Handling Messages**:
   - If the user sends a message unrelated to a command, the bot checks its mode (whether it’s in GPT, date, or message mode) and acts accordingly. If none of these apply, the bot responds with a default "Hello" message and a prompt.

6. **Callback Query Handlers**:
   - Handles button interactions, for instance, confirming the choice of a date or generating a new message sequence.

7. **Running the Bot**:
   - The bot runs in polling mode, continuously checking for new messages and user interactions.

TG- @DeviousCryptoLicks
