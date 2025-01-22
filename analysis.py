# This script reads crawled_data.json and computes statistics about the URLs and keywords.

import json
import re
import matplotlib.pyplot as plt

def analyze_crawled_data(json_file="crawled_data.json"):
    # Counters
    total_urls = 0
    cs_count = 0               # URLs containing "cs"
    tilde_count = 0            # URLs containing "~"
    
    # domain counters
    cc_subdomain_count = 0     # URLs within *.cc.gatech.edu

    sites_subdomain_count = 0  # URLs within sites.gatech.edu
    faculty_subdomain_count = 0 # URLs within faculty.gatech.edu
    support_subdomain_count = 0 # URLs within support.cc.gatech.edu
    www_subdomain_count = 0     # URLs within www.cc.gatech.edu
    other_subdomain_count = 0   # URLs within other subdomains
    urls = []

    # Load from JSON
    with open(json_file, "r") as f:
        data = json.load(f)

    # data is dictionaries with url and keyword
    for item in data:
        url = item.get("url", "")
        urls.append(url)
        total_urls += 1
        
        # Classify based on substrings
        if re.search(r'cs\d{4}', url):
            cs_count += 1
        if "~" in url:
            tilde_count += 1
        if "cc.gatech.edu" in url:
            cc_subdomain_count += 1

        if "sites.cc.gatech.edu" in url:
            sites_subdomain_count += 1
        elif "faculty.cc.gatech.edu" in url:
            faculty_subdomain_count += 1
        elif "support.cc.gatech.edu" in url:
            support_subdomain_count += 1
        elif "www.cc.gatech.edu" in url:
            www_subdomain_count += 1
        else:
            other_subdomain_count += 1
        

    subdomain_total = sites_subdomain_count + faculty_subdomain_count + support_subdomain_count + www_subdomain_count + other_subdomain_count

    if total_urls == 0:
        print("No data found in crawled_data.json.")
        return
    if subdomain_total == 0:
        print("No URLs found, cannot calculate percentages.")
        return

    cs_percent = (cs_count / total_urls) * 100
    tilde_percent = (tilde_count / total_urls) * 100
    cc_subdomain_percent = (cc_subdomain_count / total_urls) * 100

    # subdomians
    sites_subdomain_percent = (sites_subdomain_count / subdomain_total) * 100
    faculty_subdomain_percent = (faculty_subdomain_count / subdomain_total) * 100
    support_subdomain_percent = (support_subdomain_count / subdomain_total) * 100
    www_subdomain_percent = (www_subdomain_count / subdomain_total) * 100
    other_subdomain_percent = (other_subdomain_count / subdomain_total) * 100

    print("Analysis of crawled_data.json")
    print("--------------------------------")
    print(f"Total URLs: {total_urls}")
    print(f"URLs containing 'cs': {cs_count} ({cs_percent:.2f}%)")
    print(f"URLs containing '~': {tilde_count} ({tilde_percent:.2f}%)")
    print(f"URLs under *.cc.gatech.edu: {cc_subdomain_count} ({cc_subdomain_percent:.2f}%)")
    print(f"sites.gatech.edu: {sites_subdomain_count} ({sites_subdomain_percent:.2f}%)")
    print(f"faculty.gatech.edu: {faculty_subdomain_count} ({faculty_subdomain_percent:.2f}%)")
    print(f"support.cc.gatech.edu: {support_subdomain_count} ({support_subdomain_percent:.2f}%)")
    print(f"www.cc.gatech.edu: {www_subdomain_count} ({www_subdomain_percent:.2f}%)")
    print(f"Other Subdomains: {other_subdomain_count} ({other_subdomain_percent:.2f}%)")

    #print("\nCategories above 10% occurrence:")
    #if cs_percent > 10:
    #    print(" - URLs containing 'cs'")
    #if tilde_percent > 10:
    #    print(" - Faculty pages (~)")
    #if cc_subdomain_percent > 10:
    #    print(" - cc.gatech.edu subdomain")

    # Prepare data for the pie chart
    subdomains = ["sites.gatech.edu", "faculty.gatech.edu", "support.cc.gatech.edu", "www.cc.gatech.edu", "Other Subdomains"]

    subdomain_counts = [sites_subdomain_count, faculty_subdomain_count, support_subdomain_count, www_subdomain_count, other_subdomain_count]

    # https://htmlcolorcodes.com/
    colors = ['#66b3ff','#99ff99','#ff9999','#ffcc99','#c2c2f0']

    plt.figure(figsize=(8, 8))
    plt.pie(subdomain_counts, labels=subdomains, autopct='%1.1f%%', startangle=140, colors=colors, shadow=True )
    plt.title("Distribution of URLs Across Subdomains")
    plt.axis('equal')  # Ensures pie chart is circular
    plt.tight_layout(); plt.savefig("subdomains_pie_chart.png"); plt.show()


if __name__ == "__main__":
    analyze_crawled_data("crawled_data.json")