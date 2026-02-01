from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
import json

app = FastAPI()

# 🔐 SOURCE API (HIDDEN SERVER SIDE)
SOURCE_API = "https://ravan-lookup.vercel.app/api?key=Ravan&type=mobile&term="

HEADER_TEXT = "💾 HiTeckGroop.in"
VALID_KEYS = ["chut", "Paid"]

@app.get("/get_data")
def get_data(
    mobile: str = Query(..., min_length=10, max_length=10),
    key: str = Query(...)
):
    # 🔑 KEY VALIDATION
    if key not in VALID_KEYS:
        return JSONResponse(
            status_code=403,
            content={"error": "Invalid API key"}
        )

    try:
        # 🔒 CALL SOURCE API (NO LEAK)
        r = requests.get(
            SOURCE_API + mobile,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }
        )

        r.raise_for_status()
        raw = r.text.strip()

        if not raw:
            return JSONResponse(content={
                "header": HEADER_TEXT,
                "total_records": 0,
                "data": []
            })

        try:
            api_data = json.loads(raw)
        except:
            api_data = raw

        # 🧹 REMOVE UNWANTED KEYS
        def clean_data(obj):
            if isinstance(obj, dict):
                obj.pop("developer", None)
                obj.pop("credit", None)
                obj.pop("source", None)
                for v in obj.values():
                    clean_data(v)
            elif isinstance(obj, list):
                for i in obj:
                    clean_data(i)
            return obj

        api_data = clean_data(api_data)

        total = len(api_data) if isinstance(api_data, list) else 1

        return JSONResponse(content={
            "header": HEADER_TEXT,
            "total_records": total,
            "data": api_data
        })

    except Exception:
        # ❌ NO SOURCE / NO REAL ERROR LEAK
        return JSONResponse(
            status_code=500,
            content={
                "header": HEADER_TEXT,
                "total_records": 0,
                "data": [],
                "error": "Service temporarily unavailable"
            }
        )