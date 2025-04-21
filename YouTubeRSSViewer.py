import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font as tkFont
import feedparser
import webbrowser
from datetime import datetime
import time
import json
import os
from threading import Thread

# --- Configuration Files (MODIFIED) ---
FEEDS_FILE = "feeds.json"
VIEWED_FILE = "viewed.json"
CONFIG_FILE = "config.json" # New config file

# --- Default Settings ---
DEFAULT_VIDEOS_PER_CHANNEL = 15 # Default limit


# --- Dark Theme Colors ---
COLOR_DARK_BG = "#2e2e2e"
COLOR_WIDGET_BG = "#3c3c3c"
COLOR_TEXT = "#e0e0e0"
COLOR_TEXT_DIM = "#a0a0a0"
COLOR_LINK = "#66b3ff"
COLOR_SELECT_BG = "#555555" # Used for Listbox selection
COLOR_SELECT_FG = "#ffffff" # Used for Listbox selection text
COLOR_BORDER = "#4f4f4f"

# --- Font Configuration ---
FONT_SIZE_BASE = 11
FONT_SIZE_TITLE = 12
FONT_SIZE_INFO = 9

# --- Data Loading/Saving (MODIFIED for JSON) ---

# --- *** NEW Config Loading/Saving *** ---

def load_config():
    """Loads configuration from config.json."""
    defaults = {"videos_per_channel": DEFAULT_VIDEOS_PER_CHANNEL}
    if not os.path.exists(CONFIG_FILE):
        return defaults # Return defaults if file doesn't exist
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            # Ensure the specific key exists, otherwise use default
            if "videos_per_channel" not in config_data or not isinstance(config_data["videos_per_channel"], int):
                 config_data["videos_per_channel"] = DEFAULT_VIDEOS_PER_CHANNEL
            # You could load other settings here in the future
            # Merge loaded data with defaults to ensure all keys exist
            defaults.update(config_data)
            return defaults
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"Warning: Error reading {CONFIG_FILE} or file not found. Using default settings.")
        return defaults # Return defaults on error
    except Exception as e:
        print(f"Error loading config data: {e}")
        return defaults


def save_config(config_data):
    """Saves configuration data to config.json."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)
    except Exception as e:
        print(f"Error saving config data: {e}")




def load_feeds():
    """Loads feed data (list of dicts) from the JSON file."""
    if not os.path.exists(FEEDS_FILE):
        return [] # Return empty list if file doesn't exist
    try:
        with open(FEEDS_FILE, 'r', encoding='utf-8') as f:
            feeds_data = json.load(f)
            # Basic validation: ensure it's a list
            if isinstance(feeds_data, list):
                # Further validation: check if items are dicts with 'url' (optional)
                return [item for item in feeds_data if isinstance(item, dict) and 'url' in item]
            else:
                print(f"Warning: {FEEDS_FILE} does not contain a valid list. Starting fresh.")
                return []
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"Warning: Error reading {FEEDS_FILE} or file not found. Starting fresh.")
        return [] # Return empty list on error or if file is empty/corrupt
    except Exception as e:
        print(f"Error loading feeds data: {e}")
        return []

def save_feeds(feeds_data):
    """Saves feed data (list of dicts) to the JSON file."""
    try:
        with open(FEEDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(feeds_data, f, indent=4) # Save list of dicts with indentation
    except Exception as e:
        print(f"Error saving feeds data: {e}")

# --- Core Feed Parsing Logic (fetch_single_feed - Unchanged) ---
# ... (keep the fetch_single_feed function exactly as before) ...


def load_viewed():
    """Loads viewed video IDs from the JSON file."""
    if not os.path.exists(VIEWED_FILE):
        return {}
    try:
        with open(VIEWED_FILE, 'r', encoding='utf-8') as f: # Specify encoding
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}
    except Exception as e:
        print(f"Error loading viewed status: {e}")
        return {}

def save_viewed(viewed_dict):
    """Saves viewed video IDs to the JSON file."""
    try:
        with open(VIEWED_FILE, 'w', encoding='utf-8') as f: # Specify encoding
            json.dump(viewed_dict, f, indent=4)
    except Exception as e:
        print(f"Error saving viewed status: {e}")



# --- GUI Application Class ---
# <<< Keep all imports and helper functions from the previous version here >>>
# (load_feeds, save_feeds, load_viewed, save_viewed, fetch_single_feed)
# Also keep the Color and Font constants.

# --- GUI Application Class ---

# --- GUI Application Class ---


class YouTubeRSSViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube RSS Feed Viewer")
        self.root.geometry("900x700")
        self.root.config(bg=COLOR_DARK_BG)

        self.font_base = tkFont.Font(family="TkDefaultFont", size=FONT_SIZE_BASE)
        self.font_title = tkFont.Font(family="TkDefaultFont", size=FONT_SIZE_TITLE, weight="bold")
        self.font_info = tkFont.Font(family="TkDefaultFont", size=FONT_SIZE_INFO)

        self.setup_style()

        # --- MODIFIED: Load feed data (list of dicts) ---
        self.feeds_data = load_feeds() # Renamed from self.feeds
        self.viewed_videos = load_viewed()
        # --- *** Load Config and Setup Variable *** ---
        self.config = load_config()
        self.videos_per_channel_var = tk.IntVar(value=self.config.get("videos_per_channel", DEFAULT_VIDEOS_PER_CHANNEL))

        self.all_videos = []
        self.checkbox_vars = {}
        self.feeds_list_window = None
        self.feed_listbox_widget = None # Added missing init here

        self.setup_ui()
        # Refresh feeds using the new self.feeds_data
        self.refresh_feeds()

    # --- setup_style method (Unchanged) ---
    def setup_style(self):
        """Configures the ttk style for the dark theme and fonts."""
        style = ttk.Style(self.root)
        available_themes = style.theme_names()
        if 'clam' in available_themes: style.theme_use('clam')
        elif 'alt' in available_themes: style.theme_use('alt')

        style.configure('.', background=COLOR_DARK_BG, foreground=COLOR_TEXT, font=self.font_base, fieldbackground=COLOR_WIDGET_BG, borderwidth=1, focuscolor=COLOR_LINK)
        style.map('.', background=[('active', COLOR_WIDGET_BG)], foreground=[('disabled', COLOR_TEXT_DIM)])
        style.configure('TFrame', background=COLOR_DARK_BG)
        style.configure('TLabel', background=COLOR_DARK_BG, foreground=COLOR_TEXT)
        style.configure('TButton', background=COLOR_WIDGET_BG, foreground=COLOR_TEXT, padding=5)
        style.map('TButton', background=[('active', COLOR_SELECT_BG), ('pressed', COLOR_SELECT_BG)], foreground=[('active', COLOR_TEXT)])
        style.configure('TEntry', insertcolor=COLOR_TEXT)
        style.configure('TCheckbutton', background=COLOR_DARK_BG, foreground=COLOR_TEXT)
        style.map('TCheckbutton', foreground=[('active', COLOR_LINK)], indicatorcolor=[('selected', COLOR_LINK), ('active', COLOR_WIDGET_BG)])
        style.configure('Vertical.TScrollbar', background=COLOR_WIDGET_BG, troughcolor=COLOR_DARK_BG, bordercolor=COLOR_BORDER, arrowcolor=COLOR_TEXT)
        style.map('Vertical.TScrollbar', background=[('active', COLOR_SELECT_BG)])
        style.configure('Link.TLabel', foreground=COLOR_LINK, background=COLOR_DARK_BG, font=self.font_title)
        style.configure('Info.TLabel', foreground=COLOR_TEXT_DIM, background=COLOR_DARK_BG, font=self.font_info)
        style.configure('Item.TFrame', background=COLOR_DARK_BG, bordercolor=COLOR_BORDER, relief=tk.GROOVE, borderwidth=1)


    # --- setup_ui method (MODIFIED - added Spinbox) ---
    def setup_ui(self):
        # --- Top Frame: Add Feed (Unchanged) ---
        top_frame = ttk.Frame(self.root, padding="5")
        top_frame.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(top_frame, text="Add YouTube RSS Feed URL:").pack(side=tk.LEFT, padx=(0, 5))
        self.feed_url_entry = ttk.Entry(top_frame, width=60)
        self.feed_url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        # Store ref to button if needed later (e.g. for disabling during add)
        self.add_button_widget = ttk.Button(top_frame, text="Add Feed", command=self.add_feed, style='TButton')
        self.add_button_widget.pack(side=tk.LEFT, padx=(5, 0))


        # --- Middle Frame: Video List (Scrollable) (Unchanged) ---
        list_container = ttk.Frame(self.root, padding="5")
        list_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(list_container, bg=COLOR_DARK_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=canvas.yview, style='Vertical.TScrollbar')
        self.scrollable_frame = ttk.Frame(canvas, style='TFrame')
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        def _on_mousewheel(event):
            if event.num == 4: delta = -1
            elif event.num == 5: delta = 1
            else: delta = -1 * int(event.delta / 120)
            if canvas.winfo_exists(): canvas.yview_scroll(delta, "units")
        self.root.bind_all("<MouseWheel>", _on_mousewheel)
        self.root.bind_all("<Button-4>", _on_mousewheel)
        self.root.bind_all("<Button-5>", _on_mousewheel)


        # --- Bottom Frame: Actions & Status (MODIFIED) ---
        bottom_frame = ttk.Frame(self.root, padding="5")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        refresh_button = ttk.Button(bottom_frame, text="Refresh Feeds", command=self.refresh_feeds, style='TButton')
        refresh_button.pack(side=tk.LEFT, padx=(0, 5))

        view_feeds_button = ttk.Button(bottom_frame, text="View Feeds", command=self.show_feeds_list, style='TButton')
        view_feeds_button.pack(side=tk.LEFT, padx=(0, 15)) # Added more padding

        # *** ADDED Videos per Channel Limit Controls ***
        limit_label = ttk.Label(bottom_frame, text="Videos per Channel:")
        limit_label.pack(side=tk.LEFT, padx=(0, 2))

        limit_spinbox = ttk.Spinbox(
            bottom_frame,
            from_=1,  # Minimum 1 video
            to=50,    # Sensible maximum (feeds rarely offer more usable items)
            textvariable=self.videos_per_channel_var, # Link to IntVar
            width=5,  # Make it compact
            command=self.save_current_config # Save when value changes via arrows/typing+enter
        )
        # Also save when focus leaves the spinbox after potential manual typing
        limit_spinbox.bind("<FocusOut>", lambda e: self.save_current_config())
        limit_spinbox.bind("<Return>", lambda e: self.save_current_config()) # Save on Enter key
        limit_spinbox.pack(side=tk.LEFT)
        # ---

        self.status_label = ttk.Label(bottom_frame, text="Status: Idle")
        self.status_label.pack(side=tk.RIGHT) # Status label pushed to the right


    # --- *** NEW Method: save_current_config *** ---
    def save_current_config(self):
        """Saves the current configuration settings."""
        try:
            # Update the config dictionary from the UI variable
            self.config["videos_per_channel"] = self.videos_per_channel_var.get()
            # Add other settings here if needed in the future
            save_config(self.config)
            # print(f"Config saved: Videos per channel = {self.config['videos_per_channel']}") # Optional debug print
        except tk.TclError:
             print("Warning: Could not read value from spinbox yet.") # May happen during init
        except Exception as e:
             print(f"Error saving config: {e}")

    # --- fetch_single_feed (MODIFIED - Now a method, applies limit) ---
    def fetch_single_feed(self, rss_url):
        """
        Fetches and parses a single RSS feed, limiting entries.
        Returns a dictionary with feed details and entries, or None on error.
        """
        print(f"Fetching: {rss_url}")
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...'} # Keep User-Agent
            feed = feedparser.parse(rss_url, agent=headers['User-Agent'])

            # --- Get the limit from the instance variable ---
            try:
                 limit = self.videos_per_channel_var.get()
            except tk.TclError: # Handle case where variable might not be fully ready
                 limit = DEFAULT_VIDEOS_PER_CHANNEL
                 print(f"Warning: Using default limit ({limit}) as UI variable wasn't ready.")
            # ---

            if feed.bozo:
                 bozo_msg = feed.get('bozo_exception', 'Unknown issue')
                 print(f"Warning: Feedparser issues with {rss_url}. Bozo: {bozo_msg}")

            http_status = feed.get("status")
            if http_status and http_status != 200:
                print(f"HTTP Error {http_status} for feed: {rss_url}")
                return {"Feed Title": f"HTTP Error {http_status}", "posts": [], "Feed Link": rss_url, "status": "error"}
            elif not feed.entries and not feed.feed:
                 print(f"Error: Feed seems empty or parsing failed for {rss_url}.")
                 return {"Feed Title": f"Empty/Failed Parse {rss_url}", "posts": [], "Feed Link": rss_url, "status": "error"}

            feed_title = feed.feed.get("title", "Unknown Channel")
            feed_link = feed.feed.get("link", rss_url)
            posts_details = {"Feed Title": feed_title, "Feed Link": feed_link, "status": "ok"}
            processed_entries = []

            # --- Apply the limit by slicing the entries ---
            entries_to_process = feed.entries[:limit]
            # ---

            # print(f"Processing {len(entries_to_process)} entries (limit: {limit}) for {feed_title}") # Debugging

            for entry in entries_to_process: # Iterate through the limited list
                published_dt = None; published_str = "Unknown date"
                published_parsed = entry.get('published_parsed')
                if published_parsed:
                    try:
                        published_dt = datetime.fromtimestamp(time.mktime(published_parsed))
                        published_str = published_dt.strftime('%Y-%m-%d %H:%M:%S')
                    except Exception as date_e: print(f"Date error: {date_e}")
                elif 'published' in entry: published_str = entry.published

                video_id = entry.get("id", entry.get("link"))
                if not video_id: continue # Skip if no ID

                processed_entries.append({
                    "title": entry.get("title", "No Title"), "link": entry.get("link", "#"),
                    "id": video_id, "published_str": published_str, "published_dt": published_dt,
                    "channel_title": feed_title # This will be overwritten later by stored name
                })

            posts_details["posts"] = processed_entries
            return posts_details

        except Exception as e:
            import traceback
            print(f"Critical Error fetching/parsing feed {rss_url}: {e}")
            traceback.print_exc()
            return {"Feed Title": f"Error Parsing {rss_url}", "posts": [], "Feed Link": rss_url, "status": "error"}




    # --- add_feed method (MODIFIED - calls self.fetch_single_feed) ---
    def add_feed(self):
        # ... (URL validation - unchanged) ...
        new_url = self.feed_url_entry.get().strip()
        # ... (validation checks ...)
        if any(feed_info['url'] == new_url for feed_info in self.feeds_data):
             messagebox.showinfo("Duplicate Feed", "This feed URL is already in the list.")
             return

        self.status_label.config(text=f"Status: Fetching title for {new_url}...")
        self.root.update_idletasks()

        # --- MODIFIED Call ---
        feed_details = self.fetch_single_feed(new_url) # Call the METHOD now

        self.status_label.config(text="Status: Idle")

        if feed_details and feed_details.get("status") == "ok":
            channel_name = feed_details.get("Feed Title", f"Unknown ({new_url})")
            new_feed_info = {"url": new_url, "name": channel_name}
            self.feeds_data.append(new_feed_info)
            save_feeds(self.feeds_data)
            self.feed_url_entry.delete(0, tk.END)
            print(f"Added feed: {channel_name} - {new_url}")
            self.refresh_feeds()
        else:
            err_msg = feed_details.get("Feed Title", "Unknown Error") if feed_details else "Unknown Error"
            messagebox.showerror("Feed Error", f"Could not fetch feed details for:\n{new_url}\n\nError: {err_msg}\n\nPlease check the URL.")
            self.status_label.config(text="Status: Feed add failed")


    # --- fetch_all_videos_thread (MODIFIED - calls self.fetch_single_feed) ---
    def fetch_all_videos_thread(self):
        self.status_label.config(text="Status: Fetching feeds...")
        self.root.update_idletasks()
        local_feeds_data = list(self.feeds_data)
        feed_urls_to_fetch = [fi['url'] for fi in local_feeds_data if 'url' in fi]
        all_videos_fetched = []
        errors = 0

        for url in feed_urls_to_fetch:
            # --- MODIFIED Call ---
            feed_data = self.fetch_single_feed(url) # Call the METHOD now

            original_name = "Unknown Channel"
            for item in local_feeds_data: # Find original stored name
                 if item.get('url') == url: original_name = item.get('name', original_name); break

            if feed_data and feed_data.get("status") == "ok":
                valid_entries = []
                for post in feed_data.get("posts", []):
                    if post.get("id"):
                         post['channel_title'] = original_name # Use stored name
                         valid_entries.append(post)
                all_videos_fetched.extend(valid_entries)
            # ... (error handling unchanged) ...
            elif feed_data and feed_data.get("status") == "error":
                 errors += 1; print(f"Failed to process feed: {url} - {feed_data.get('Feed Title')}")
            else:
                 errors += 1; print(f"Failed to process feed (unknown error): {url}")

        # ... (sorting and calling update_video_list unchanged) ...
        try: all_videos_fetched.sort(key=lambda x: x.get('published_dt', datetime.min), reverse=True)
        except TypeError as e: print(f"Sorting error: {e}")
        self.root.after(0, self.update_video_list, all_videos_fetched, errors)



    # --- refresh_feeds method (Unchanged) ---
    def refresh_feeds(self):
        for widget in self.scrollable_frame.winfo_children(): widget.destroy()
        self.checkbox_vars.clear()
        thread = Thread(target=self.fetch_all_videos_thread, daemon=True); thread.start()

    # --- update_video_list method (Unchanged from previous version) ---
    def update_video_list(self, fetched_videos, error_count):
        self.all_videos = fetched_videos
        current_viewed_dict = load_viewed()
        current_fetched_ids = {video['id'] for video in self.all_videos if video.get('id')}
        viewed_ids_from_file = set(current_viewed_dict.keys())
        valid_viewed_ids = viewed_ids_from_file.intersection(current_fetched_ids)
        pruned_viewed_videos = {vid_id: True for vid_id in valid_viewed_ids}
        if set(pruned_viewed_videos.keys()) != viewed_ids_from_file:
             print(f"Pruning viewed list: Removed {len(viewed_ids_from_file - valid_viewed_ids)} old entries.")
             save_viewed(pruned_viewed_videos)
             self.viewed_videos = pruned_viewed_videos
        else:
             self.viewed_videos = current_viewed_dict
        videos_to_display = [v for v in self.all_videos if v.get('id') and v['id'] not in self.viewed_videos]
        for widget in self.scrollable_frame.winfo_children(): widget.destroy()
        self.checkbox_vars.clear()
        if not videos_to_display:
            message = "No new videos found."
            if error_count > 0: message += f"\n({error_count} feed errors occurred - check console)."
            elif not self.all_videos and error_count == 0: message = "No videos found in feeds. Add RSS feed URLs."
            elif self.all_videos: message = "All fetched videos have been marked as viewed."
            ttk.Label(self.scrollable_frame, text=message, wraplength=700).pack(pady=20, padx=10) # Use wraplength approx
        else:
            for video in videos_to_display:
                video_id = video.get("id")
                item_frame = ttk.Frame(self.scrollable_frame, padding=(5, 3), style='Item.TFrame')
                item_frame.pack(fill=tk.X, pady=(0, 5), padx=3)
                var = tk.BooleanVar(value=False)
                self.checkbox_vars[video_id] = var
                chk = ttk.Checkbutton(item_frame, variable=var, command=lambda v_id=video_id: self.toggle_viewed(v_id), style='TCheckbutton')
                chk.pack(side=tk.LEFT, padx=(0, 8))
                text_frame = ttk.Frame(item_frame); text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
                title_label = ttk.Label(text_frame, text=video.get('title', 'No Title'), style='Link.TLabel', cursor="hand2", wraplength=700, justify=tk.LEFT)
                title_label.pack(anchor="w", fill=tk.X, pady=(0, 2))
                title_label.bind("<Button-1>", lambda e, link=video.get('link', '#'): self.open_link(link))
                info_text = f"Channel: {video.get('channel_title', 'Unknown')} | Published: {video.get('published_str', 'Unknown')}"
                info_label = ttk.Label(text_frame, text=info_text, style='Info.TLabel', wraplength=700, justify=tk.LEFT)
                info_label.pack(anchor="w", fill=tk.X)
        status_text = f"Status: Displaying {len(videos_to_display)} new videos."
        if error_count > 0: status_text += f" ({error_count} feed errors)"
        self.status_label.config(text=status_text)
        self.root.after(100, self.update_scroll_region)

    # --- update_scroll_region method (Unchanged) ---
    def update_scroll_region(self):
        canvas = self.scrollable_frame.master
        if canvas and canvas.winfo_exists():
             canvas.configure(scrollregion=canvas.bbox("all"))

    # --- open_link method (Unchanged) ---
    def open_link(self, url):
        if url and url != "#":
            try: webbrowser.open_new_tab(url)
            except Exception as e: messagebox.showerror("Error", f"Could not open link:\n{url}\nError: {e}")
        else: messagebox.showwarning("No Link", "This video entry does not have a valid link.")

    # --- toggle_viewed method (Unchanged) ---
    def toggle_viewed(self, video_id):
        if not video_id: print("Warning: Toggle view without ID."); return
        if video_id in self.checkbox_vars:
            if self.checkbox_vars[video_id].get(): # If checked
                if video_id not in self.viewed_videos:
                    self.viewed_videos[video_id] = True
                    save_viewed(self.viewed_videos)
                    print(f"Marked as viewed: {video_id}")
            # Else (unchecked) - do nothing in this workflow
        else: print(f"Error: Checkbox variable not found for video ID {video_id}")

    # --- show_feeds_list method (MODIFIED - display name & URL) ---
    def show_feeds_list(self):
        """Displays the list of feed names and URLs with delete functionality."""
        if self.feeds_list_window and self.feeds_list_window.winfo_exists():
            self.feeds_list_window.lift()
            return

        self.feeds_list_window = tk.Toplevel(self.root)
        self.feeds_list_window.title("Current Feeds") # Renamed title
        self.feeds_list_window.geometry("750x450") # Wider for longer text
        self.feeds_list_window.config(bg=COLOR_DARK_BG)
        self.feeds_list_window.transient(self.root)

        list_frame = tk.Frame(self.feeds_list_window, bg=COLOR_DARK_BG)
        list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        listbox_scrollbar_y = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        listbox_scrollbar_x = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL) # Added horizontal scrollbar

        feed_listbox = tk.Listbox(list_frame,
                                  yscrollcommand=listbox_scrollbar_y.set,
                                  xscrollcommand=listbox_scrollbar_x.set, # Link horizontal scrollbar
                                  bg=COLOR_WIDGET_BG, fg=COLOR_TEXT,
                                  selectbackground=COLOR_SELECT_BG,
                                  selectforeground=COLOR_SELECT_FG,
                                  borderwidth=1, relief=tk.SOLID,
                                  highlightthickness=1,
                                  highlightbackground=COLOR_BORDER,
                                  highlightcolor=COLOR_LINK,
                                  font=self.font_base,
                                  selectmode=tk.SINGLE)

        listbox_scrollbar_y.config(command=feed_listbox.yview, bg=COLOR_WIDGET_BG, troughcolor=COLOR_DARK_BG, activebackground=COLOR_SELECT_BG)
        listbox_scrollbar_x.config(command=feed_listbox.xview, bg=COLOR_WIDGET_BG, troughcolor=COLOR_DARK_BG, activebackground=COLOR_SELECT_BG) # Config horizontal

        listbox_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        listbox_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X) # Pack horizontal at bottom
        feed_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.feed_listbox_widget = feed_listbox # Store reference

        # --- Populate listbox with formatted strings ---
        if self.feeds_data:
            for feed_info in self.feeds_data:
                display_text = f"{feed_info.get('name', 'Unknown Name')}  —  {feed_info.get('url', 'Unknown URL')}"
                feed_listbox.insert(tk.END, display_text)
        else:
            feed_listbox.insert(tk.END, "No feeds added yet.")
            feed_listbox.config(state=tk.DISABLED)

        button_frame = ttk.Frame(self.feeds_list_window, style='TFrame')
        button_frame.pack(pady=(0, 10))

        delete_button = ttk.Button(button_frame, text="Delete Selected", command=lambda lb=feed_listbox: self.delete_selected_feed(lb), style='TButton')
        delete_button.pack(side=tk.LEFT, padx=5)
        if not self.feeds_data: delete_button.config(state=tk.DISABLED)

        close_button = ttk.Button(button_frame, text="Close", command=self.close_feeds_window, style='TButton')
        close_button.pack(side=tk.LEFT, padx=5)

        self.feeds_list_window.protocol("WM_DELETE_WINDOW", self.close_feeds_window)
        self.feeds_list_window.grab_set()
        self.feeds_list_window.focus_set()
        self.feeds_list_window.wait_window()

    # --- delete_selected_feed method (MODIFIED - uses index) ---
    def delete_selected_feed(self, listbox_widget):
        """Deletes the selected feed using its index."""
        selected_indices = listbox_widget.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select a feed from the list to delete.", parent=self.feeds_list_window)
            return

        selected_index = selected_indices[0]

        # Get the corresponding dictionary from our data using the index
        if 0 <= selected_index < len(self.feeds_data):
            feed_to_delete = self.feeds_data[selected_index]
            url_to_delete = feed_to_delete.get('url', 'N/A')
            name_to_delete = feed_to_delete.get('name', 'N/A')
        else:
            messagebox.showerror("Error", "Selected index out of range.", parent=self.feeds_list_window)
            return

        # Use retrieved details in confirmation
        confirm = messagebox.askyesno("Confirm Deletion",
                                      f"Are you sure you want to delete this feed?\n\nName: {name_to_delete}\nURL: {url_to_delete}",
                                      parent=self.feeds_list_window)

        if confirm:
            try:
                # Remove from the internal list self.feeds_data using index
                del self.feeds_data[selected_index]
                print(f"Removed feed: {name_to_delete} - {url_to_delete}")

                # Remove from the listbox visually using index
                listbox_widget.delete(selected_index)

                # Save the updated list to the file
                save_feeds(self.feeds_data)

                # Disable delete button if list becomes empty
                if not self.feeds_data:
                     try:
                          button_frame = listbox_widget.master.master.children['!ttkframe']
                          delete_button = button_frame.children['!ttkbutton']
                          delete_button.config(state=tk.DISABLED)
                          listbox_widget.config(state=tk.DISABLED) # Also disable listbox
                          listbox_widget.insert(tk.END, "No feeds remaining.") # Add placeholder text
                     except Exception as e: print(f"Could not disable delete button/listbox: {e}")

            except Exception as e:
                 messagebox.showerror("Error", f"Failed to delete feed:\n{e}", parent=self.feeds_list_window)
                 print(f"Error deleting feed {url_to_delete}: {e}")


    # --- *** NEW METHOD: close_feeds_window *** ---
    def close_feeds_window(self):
        """Helper method to destroy the feeds list window and reset the tracker."""
        if self.feeds_list_window and self.feeds_list_window.winfo_exists():
            self.feeds_list_window.destroy()
        self.feeds_list_window = None # Reset the tracker


# --- Main Execution (Keep the exact same block from the dark theme version) ---
if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeRSSViewerApp(root)
    root.mainloop()
