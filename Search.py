import tkinter as tk
import requests
import webbrowser

def search_reddit(query):
    headers = {'User-Agent': 'Mozilla/5.0'}
    reddit_url = f'https://www.reddit.com/search.json?q={query}&limit=5'
    response = requests.get(reddit_url, headers=headers)
    
    if response.status_code == 200:
        results = response.json()['data']['children']
        return [f"Reddit: {result['data']['title']} ({result['data']['url']})" for result in results]
    return []

def search_wikipedia(query):
    wiki_url = f'https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=5&format=json'
    response = requests.get(wiki_url)
    
    if response.status_code == 200:
        results = response.json()[1]
        urls = response.json()[3]
        return [f"Wikipedia: {title} ({url})" for title, url in zip(results, urls)]
    return []

def open_link(url):
    webbrowser.open(url)

def perform_search():
    query = search_entry.get()
    
    for widget in results_frame.winfo_children():
        widget.destroy()
    
    reddit_results = search_reddit(query)
    wiki_results = search_wikipedia(query)
    
    if reddit_results:
        for result in reddit_results:
            title, url = result.split(" (")
            url = url[:-1]
            result_label = tk.Label(results_frame, text=title, fg="blue", cursor="hand2", font=("Arial", 12, "bold"))
            result_label.pack(anchor="w", padx=10, pady=5)
            result_label.bind("<Button-1>", lambda e, u=url: open_link(u))
    
    if wiki_results:
        for result in wiki_results:
            title, url = result.split(" (")
            url = url[:-1]
            result_label = tk.Label(results_frame, text=title, fg="blue", cursor="hand2", font=("Arial", 12, "bold"))
            result_label.pack(anchor="w", padx=10, pady=5)
            result_label.bind("<Button-1>", lambda e, u=url: open_link(u))
    
    if not reddit_results and not wiki_results:
        no_results_label = tk.Label(results_frame, text="No results found.", font=("Arial", 12, "italic"))
        no_results_label.pack(anchor="w", padx=10, pady=5)

root = tk.Tk()
root.title("Search Engine (Reddit & Wikipedia)")

search_label = tk.Label(root, text="Enter search query:", font=("Arial", 14))
search_label.pack(pady=10)

search_entry = tk.Entry(root, width=50, font=("Arial", 14))
search_entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=perform_search, font=("Arial", 14))
search_button.pack(pady=10)

results_frame = tk.Frame(root)
results_frame.pack(pady=10)

root.mainloop()
