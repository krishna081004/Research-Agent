# Research Agent

A Python-based research assistant that uses the SerpAPI Google Search API to find job listings based on a company and role.

## Features
- Search for job listings for any company and job title.
- Outputs results in JSON format for easy processing.
- Uses SerpAPI for reliable Google Search results.

## Requirements
- Python 3.10+
- A valid SerpAPI API key

## Installation

1. **Clone the repository** (or create a project folder):
```bash
git clone <your-repo-url>
cd research_agent
```

2. **Create a virtual environment**:
```bash
python -m venv venv
```

3. **Activate the virtual environment**:
- **Windows**:
```bash
venv\Scripts\activate
```
- **macOS/Linux**:
```bash
source venv/bin/activate
```

4. **Install dependencies**:
```bash
pip install requests
```

## Usage

1. **Set your SERPAPI_KEY environment variable**:
- **Windows**:
```bash
set SERPAPI_KEY="your_api_key_here"
```
- **macOS/Linux**:
```bash
export SERPAPI_KEY="your_api_key_here"
```

2. **Run the script**:
```bash
python research_agent.py "Company Name" "Job Title"
```
Example:
```bash
python research_agent.py "NVIDIA" "Deep Learning Engineer"
```

## Example Output
```json
[
    {
        "title": "Deep Learning Engineer - NVIDIA",
        "link": "https://www.example.com/job1",
        "snippet": "Job description here..."
    },
    {
        "title": "Senior Deep Learning Engineer - NVIDIA",
        "link": "https://www.example.com/job2",
        "snippet": "Job description here..."
    }
]
```

## License
MIT License
