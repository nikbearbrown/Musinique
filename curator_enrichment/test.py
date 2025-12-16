from langsmith import Client
import json
import os 
from dotenv import load_dotenv
load_dotenv()

client = Client()
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
trace_id = "019b2436-4ab0-7991-98dd-37ece4f132d2"

runs = list(client.list_runs(trace_id=trace_id))

trace_data = {
    "trace_id": trace_id,
    "runs": [r.dict() for r in runs]
}

with open("full_trace.json", "w") as f:
    json.dump(trace_data, f, indent=2 , default=str)
