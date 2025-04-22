# YouTube RSS Feed Viewer

A simple desktop application built with Python and Tkinter to aggregate and view the latest videos from your favorite YouTube channels using their RSS feeds. Keep track of new uploads chronologically without relying on YouTube's main feed or subscriptions.

![Screenshot Placeholder - Consider adding a screenshot of the app here!]

## Features

* **Aggregate Feeds:** Monitor multiple YouTube channel RSS feeds in one place.
* **Chronological View:** Displays the latest videos from all monitored channels, sorted by publication date (most recent first).
* **Direct Video Links:** Click video titles to open them directly in your default web browser.
* **View Tracking:** Mark videos as "viewed" using checkboxes; viewed videos are hidden on subsequent refreshes.
* **Feed Management:**
    * Add new channel RSS feeds via the UI.
    * View the list of currently monitored channels/feeds.
    * Delete feeds you no longer want to follow.
* **Configurable Video Limit:** Set the maximum number of recent videos to fetch and display per channel (default is 15).
* **Persistence:** Your list of feeds, viewed video status, and video limit setting are saved locally in JSON files (`feeds.json`, `viewed.json`, `config.json`).
* **Simple Interface:** Uses Python's built-in Tkinter library with a clean dark theme.

## Getting Started

There are two ways to run the application:

**1. Using the Executable (Recommended for most users)**

* [*(Link to Releases page)*](https://github.com/jpmiii/YouTube-RSS-Feed-Viewer/releases/tag/v1.0.0)
* Download the latest pre-built executable for your operating system (Windows `.exe`, macOS `.app`, Linux) from the **Releases** page of this repository (if available).
* Place the executable in its own folder.
* Run the executable.
* On the first run, it will create the necessary data files (`feeds.json`, `viewed.json`, `config.json`) in the same folder.

**2. Running from Source (For developers or if no executable is available)**

* **Prerequisites:**
    * Python 3.x installed.
    * `pip` (Python package installer).
* **Setup:**
    1.  Clone or download this repository:
        ```bash
        git clone [https://docs.github.com/repositories/creating-and-managing-repositories/about-repositories](https://docs.github.com/repositories/creating-and-managing-repositories/about-repositories)
        cd [repository folder name]
        ```
    2.  **(Recommended)** Create and activate a virtual environment:
        ```bash
        # Windows
        python -m venv venv
        .\venv\Scripts\activate

        # macOS / Linux
        python3 -m venv venv
        source venv/bin/activate
        ```
    3.  Install the required dependencies:
        ```bash
        pip install -r requirements.txt
        ```
        *(Note: You need to create a `requirements.txt` file containing `feedparser`)*
    4.  Run the application:
        ```bash
        python YouTubeRSSViewer.py
        ```

## Usage

1.  **Finding YouTube Channel RSS Feeds:**
    * This is the trickiest part, as YouTube doesn't make it obvious. The standard URL format is:
        `https://googleusercontent.com/youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID`
    * To find the `CHANNEL_ID`:
        * Go to the main page of the YouTube channel you want to add.
        * Right-click on the page and select "View Page Source" (or similar option in your browser).
        * Search the source code (Ctrl+F or Cmd+F) for `"channelId"` or `"externalId"`.
        * Copy the long string of letters and numbers associated with it (e.g., `UCxxxxxxxxxxxxxxxxxxxxxx`). This is the `CHANNEL_ID`.
        * Replace `CHANNEL_ID` in the URL template above with the ID you found.

2.  **Adding a Feed:**
    * Paste the full RSS feed URL (obtained above) into the input field at the top of the application.
    * Click "Add Feed". The application will attempt to fetch the channel name and add it to your list.

3.  **Viewing Videos:**
    * The main panel lists videos sorted by date.
    * Click "Refresh Feeds" to fetch the latest videos.
    * Click any video title to open it in your web browser.

4.  **Marking Videos as Viewed:**
    * Check the box next to a video title.
    * The next time you click "Refresh Feeds", that video will no longer appear in the list (unless you manually edit the `viewed.json` file).

5.  **Managing Feeds:**
    * Click the "View Feeds" button. A new window will show your current list of feeds (Channel Name — URL).
    * Select a feed in the list.
    * Click "Delete Selected" and confirm to remove it.

6.  **Setting Video Limit:**
    * Use the small spinbox at the bottom labeled "Videos per Channel:" to set the maximum number of recent videos fetched from *each* feed during a refresh.
    * Your setting is saved automatically.

## Configuration & Data Files

The application automatically creates and manages these files in the same directory where it runs:

* `feeds.json`: Stores the list of channels you've added (name and URL).
* `viewed.json`: Stores the IDs of videos you've marked as viewed.
* `config.json`: Stores application settings, currently just `videos_per_channel`.

## Dependencies

* [feedparser](https://pypi.org/project/feedparser/): For parsing RSS feeds.
* Python 3 Standard Library (Tkinter, json, os, sys, datetime, time, webbrowser, threading).

## Building from Source

If you want to create your own executable:

1.  Make sure you are in your activated virtual environment.
2.  Install PyInstaller: `pip install pyinstaller`
3.  Ensure you have modified the script to correctly handle data file paths (using the `get_base_path()` function as described in executable creation guides).
4.  Run PyInstaller (example for a single-file executable):
    ```bash
    pyinstaller --onefile --windowed --name YouTubeRSSViewer --icon=your_icon.ico ytrss.py
    ```
    *(Adjust options, name, icon, and script name as needed)*
5.  Find the output in the `dist` folder.

## License

*(Choose a license - MIT is common and permissive)*
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

* Built using Python and the Tkinter GUI library.
* Uses the excellent `feedparser` library for RSS handling.
* *Optional: Initial structure and feature implementation assisted by Google Gemini.*

# How to get a RSS feed link from YouTube


You can definitely get an RSS feed link from a YouTube channel using Chrome, and yes, you can do it with a plugin! Here are a few methods:

**1. Using a Chrome Extension (Plugin):**

This is generally the easiest method. Several Chrome extensions are designed to automatically detect and provide the RSS feed link for a YouTube channel. Here are a couple of options:

* **YouTube RSS Getter:** This extension aims to simplify the process of extracting RSS links from YouTube channels. It often places an RSS button on the channel page for easy access. You can find it in the Chrome Web Store.
* **RSS Feed Reader:** While primarily an RSS reader, some extensions like "RSS Feed Reader" can also help you discover feeds on websites, including YouTube channels. Look for options within the extension's interface to subscribe to a page's RSS feed.

To find these or other similar extensions:

1.  Open the Chrome Web Store.
2.  In the search bar, type "YouTube RSS feed" or "RSS feed finder."
3.  Browse the results and install a reputable extension.
4.  Once installed, navigate to the YouTube channel you're interested in and look for a button or option provided by the extension to get the RSS feed link.

**2. Manually Finding the RSS Feed Link (Without an Extension):**

While YouTube doesn't directly display an RSS feed link on the channel page anymore, you can often find it in the page's source code:

1.  Open the YouTube channel page in Chrome.
2.  **Right-click** anywhere on the page and select **"View page source"** (or press `Ctrl + U` on Windows/Linux or `Command + Option + U` on macOS).
3.  A new tab will open with the HTML source code of the page.
4.  Press `Ctrl + F` (Windows/Linux) or `Command + F` (macOS) to open the search bar.
5.  Type in either `<link rel="alternate"` or `rss+xml` and press Enter.
6.  Look for a line that looks similar to this:

    ```html
    <link rel="alternate" type="application/rss+xml" title="RSS" href="https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID">
    ```

7.  The URL within the `href` attribute is the RSS feed link for that channel. The `CHANNEL_ID` is a unique identifier for the YouTube channel.

**3. Constructing the RSS Feed URL Manually (If you know the Channel ID):**

If you know the Channel ID of the YouTube channel, you can construct the RSS feed URL directly. Here's the general format:

```
https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID
```

**How to find the Channel ID:**

* **Check the URL:** Sometimes, the Channel ID is visible in the channel's URL after `/channel/`. It will be a string of letters and numbers (e.g., `UCxxxxxxxxxxxxxxxxx`).
* **View Page Source (as described above):** You can also find the `CHANNEL_ID` by searching for `"channelId"` in the page source.

**In summary, using a Chrome extension is the most user-friendly way to get an RSS feed link from a YouTube channel. However, you can also manually extract it from the page source or construct it if you know the Channel ID.**
