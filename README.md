Functionality:

- Detects Offline UNVR Devices (Outdated):** The code used to periodically check your UniFi dashboard for offline UNVR devices using Selenium. However, due to website changes, this functionality no longer works reliably.
- Sends Alerts to Microsoft Teams : When it identified offline devices , the code would send notifications to a specified Teams chat using Selenium and web automation.
- Schedules Alerts:** It is used to alert you at 6 AM daily with a device status update and send additional alerts during operating hours (6 AM to 8 PM) for device offline/online events.

Key Limitations:

- Outdated and Inoperable Due to changes in the UniFi dashboard structure, the code cannot accurately detect offline devices and is currently not functional.
- Requires Updates for Compatibility To function again, significant updates to the code, particularly the `get_offline_devices()` function, would be needed to match the current UniFi dashboard structure.

Instructions for Use (if it were functional):

Note: These instructions are provided for informational purposes only, as the code is currently not functional.

1. Install Python and Libraries Ensure you have Python and the required libraries (`selenium`, `webdriver_manager`, and optionally `pytz`) installed.
2. Fill in Credentials Replace the placeholders with your UniFi portal username, password, Teams email, password, and the ID of the Teams chat for receiving alerts.
3. Run the Script Execute the Python script to initiate the (now outdated) monitoring process.

Considerations:

- Troubleshooting (if applicable):** If you attempt to use the code and encounter errors, carefully examine the Selenium interactions and web automation aspects for potential issues.
- Maintenance (if applicable):** Keeping Selenium-based scripts functional often requires maintenance as websites evolve.
- Alternative Approaches Consider using alternative methods like the UniFi Network mobile app or API integration for monitoring device status, as maintaining this code is likely not feasible due to its outdated nature.

1. Import Libraries
   - Import the necessary libraries: `time`, `selenium`, and `datetime`.

2. `get_offline_devices` Function:
   - Print a starting message.
   - Set Chrome options for headless mode.
   - Open a Chrome browser and navigate to the UniFi dashboard.
   - Wait for the login elements to be ready.
   - Find the email and password input fields and input your credentials.
   - Click the sign-in button.
   - Wait for the dashboard to load.
   - Extract offline device information (outdated method).
   - Close the browser.
   - Print a closing message and return a set of offline device names.

3. `login_to_teams` Function:
   - Set Chrome options for headless mode.
   - Open a Chrome browser and navigate to the Microsoft Teams login page.
   - Wait for the email field to be ready.
   - Input your Teams email and click "Next".
   - Wait for the password field to be ready.
   - Input your Teams password and click sign-in using JavaScript.
   - Wait for the chat to load and return the browser instance.

4. `send_message_to_teams` Function (Requires Login via `login_to_teams`):
   - Find the chat category button and click it.
   - Implement the logic to send a message in Teams chat.
