# YouTube-RSS-Feed-Viewer
simple python app to view YouTube channels RSS feeds

made with Gemini Pro 2.5 (experimental) free.

Run this in it's own folder it will create some files for persistance. Add RSS links to the feed list it will get the last 15 videos (adjustable) from the channel and list all the videos from the channel list sorted by most recent, clicking the title will open the video in your default browser, checking the box next to the title will stop the video from showing on the list when it's updated.

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
