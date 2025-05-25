"""
Script to run the Wikipedia Word-Frequency Dictionary API.
"""

import uvicorn
import argparse
import webbrowser
import time
import threading


def open_browser(port):
    """Open the browser after a short delay."""
    time.sleep(2)
    url = f"http://localhost:{port}/docs"
    print(f"Opening API documentation in browser: {url}")
    webbrowser.open(url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the Wikipedia Word-Frequency Dictionary API server."
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind the server to"
    )
    parser.add_argument(
        "--no-browser", action="store_true", help="Don't open the browser automatically"
    )
    parser.add_argument(
        "--no-reload", action="store_true", help="Disable auto-reload on code changes"
    )

    args = parser.parse_args()

    print(f"Starting server at http://{args.host}:{args.port}")
    print(f"API documentation available at http://{args.host}:{args.port}/docs")
    print("Press Ctrl+C to stop the server")

    # Open a browser in a separate thread
    if not args.no_browser:
        threading.Thread(target=open_browser, args=(args.port,), daemon=True).start()

    # Run the server
    uvicorn.run(
        "wiki_word_freq.main:app",
        host=args.host,
        port=args.port,
        reload=not args.no_reload,
    )
