import os
import argparse
from serpapi import GoogleSearch
from dotenv import load_dotenv

def get_company_info(api_key, company_name):
    """
    Performs a Google search to get a company overview and latest news.
    """
    print(f"[*] Searching for information on {company_name}...")
    search_params = {
        "engine": "google",
        "q": f"{company_name} overview",
        "api_key": api_key,
    }

    search = GoogleSearch(search_params)
    results = search.get_dict()

    # --- Extracting a better, more reliable description ---
    description = "No company description found."
    if results.get("knowledge_graph"):
        description = results["knowledge_graph"].get("description", description)
    elif results.get("organic_results"):
        description = results["organic_results"][0].get("snippet", description)

    # --- Performing a more focused search for news ---
    news_results = results.get("news_results", [])
    if not news_results: # If the first search didn't bring news, try a dedicated news search
        print("[*] Initial search had no news, running a dedicated news search...")
        news_search_params = {
            "engine": "google",
            "q": f"{company_name} latest news",
            "tbm": "nws", # tbm="nws" specifies a News search
            "api_key": api_key,
        }
        news_search = GoogleSearch(news_search_params)
        news_results = news_search.get_dict().get("news_results", [])

    news_summary = "\n".join([f"- {news['title']}. [Source: {news['source']}]" for news in news_results[:3]])
    if not news_summary:
        news_summary = "No recent news found."

    return {"description": description, "news": news_summary}


def get_job_role_requirements(api_key, company_name, job_role):
    """
    Searches for a specific job role using the Google Jobs engine for reliable data.
    """
    print(f"[*] Searching for the role: {job_role} at {company_name} using the Google Jobs engine...")
    search_params = {
        "engine": "google_jobs",
        "q": f'{job_role} {company_name}',
        "api_key": api_key,
    }
    search = GoogleSearch(search_params)
    results = search.get_dict()

    if "error" in results:
        return {"summary": results["error"], "salary": "Not found"}
    
    if not results.get("jobs_results"):
        return {"summary": "Could not find any job postings for this role.", "salary": "Not found"}

    # --- We now get structured data, no more manual scraping! ---
    first_job_result = results["jobs_results"][0]
    
    # The description is usually clean and well-formatted
    summary = first_job_result.get("description", "No description found.")
    
    # Look for salary information in the detected_extensions
    salary = "Not specified"
    if "detected_extensions" in first_job_result and "salary" in first_job_result["detected_extensions"]:
        salary = first_job_result["detected_extensions"]["salary"]

    return {"summary": summary, "salary": salary}


def main():
    load_dotenv() 
    
    parser = argparse.ArgumentParser(description="A research agent to find company and job role information.")
    parser.add_argument("company_name", type=str, help="The name of the company to research.")
    parser.add_argument("job_role", type=str, help="The job role to look for.")
    args = parser.parse_args()
    
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        print("Error: SERPAPI_KEY not found. Make sure you have created a .env file with your API key.")
        return

    company_info = get_company_info(api_key, args.company_name)
    role_info = get_job_role_requirements(api_key, args.company_name, args.job_role)

    # --- Print the final report ---
    print("\n" + "="*50)
    print(f"Research Report: {args.company_name} - {args.job_role}")
    print("="*50 + "\n")

    print("--- Company Overview ---")
    print(company_info["description"])
    print("\n--- Latest News ---")
    print(company_info["news"])

    print("\n" + "="*50 + "\n")

    print("--- Role-Specific Requirements (from first job found) ---")
    print("\nSALARY: ", role_info["salary"])
    print("\nJOB DESCRIPTION SUMMARY:\n")
    # Print first 1500 characters of the description for readability
    print(role_info["summary"][:1500] + "...")
    print("\n" + "="*50)


if __name__ == "__main__":
    main()