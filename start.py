#!/usr/bin/env python3
"""
Startup script for Railway deployment
Handles PORT environment variable properly
"""

import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
