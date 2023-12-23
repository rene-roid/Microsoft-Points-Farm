# 🚀 Bing Rewards Bot 🤖

This is a Python bot that automates the process of earning Bing rewards.

## 🛠️ Setup

1. Clone this repository to your local machine.
2. Install the required Python packages:

    ```sh
    pip install selenium
    pip install requests
    pip install python-dotenv
    pip install webdriver_manager
    ```

    Note: You might need to use `pip3` instead of `pip` if you're using Python 3. Also, you might need to add `--user` at the end of each command if you're installing the packages for a single user.

3. Download the `msedgedriver.exe` from the [Microsoft Edge Driver website](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) and place it in the project root directory.

4. Create a `.env` file in the project root directory and add your Bing account credentials:

    ```env
    USERNAME=your_username
    PASSWORD=your_password
    ```

5. Run the `main.py` script to start earning rewards:

    ```sh
    python main.py
    ```

Enjoy your automated Bing rewards! 🎉