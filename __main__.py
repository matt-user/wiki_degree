import sys
import requests
import queue

def get_request(title):
    """Return the data for a request with title title"""
    session = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    PAGE_LIMIT = 500
    PARAMS = {
        "action": "query",
        "prop": "linkshere",
        "titles": title,
        "lhlimit": PAGE_LIMIT,
        "format": "json"
    }
    request = session.get(url=URL, params=PARAMS)
    return request.json()

def get_page_id(data):
    """Return the page id for the searched page."""
    for key, _ in data["query"]["pages"].items():
        return key

def get_adj_edges(title):
    """Return the links given the title of a page"""
    data = get_request(title)
    page_id = get_page_id(data)
    return data["query"]["pages"][page_id].setdefault("linkshere", [])


def find_page(graph, start_page, end_page):
    """Find the end page given a dictionary of initial links data."""
    link_q = queue.Queue()
    discovered = set(start_page)
    page_id = get_page_id(graph)
    root = graph["query"]["pages"][page_id]
    link_q.put(
        {
            "pageid": root["pageid"],
            "ns": root["ns"],
            "title": root["title"],
            "parent": None
        }
    )
    while not link_q.empty():
        cur_link = link_q.get()
        adj_links = get_adj_edges(cur_link["title"])
        if cur_link["title"] == end_page:
            return cur_link
        for link in adj_links:
            if link["title"] not in discovered:
                discovered.add(link["title"])
                link["parent"] = cur_link
                link_q.put(link)
    return "Path Not Found :("
        
def get_path(arr, end_link):
    """Appends all of the links in the path to arr."""
    arr.append(end_link["title"])
    if end_link["parent"] == None:
        return
    get_path(arr, end_link["parent"])

def print_link_path(end_link):
    """Given an end link it prints the path from the start."""
    links = []
    get_path(links, end_link)
    score = len(links) - 1
    print("Score: ", score)
    print("'start' -->", end=" ")
    for link in links[::-1]:
        print(f"{link} -->", end=" ")
    print("'end'")

    

def main(start_page, end_page):
    data = get_request(start_page)

    # get the link corresponding to the given end page
    # and print that link
    end_link = find_page(data, start_page, end_page)
    print(end_link)
    print("\n")
    print_link_path(end_link)



if __name__ == '__main__':

    main(sys.argv[1], sys.argv[2])