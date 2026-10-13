"""Small local preview server with clean guest-name URLs such as /udin."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


class InvitationHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        request = urlsplit(self.path)
        route = request.path.strip("/")
        requested_file = Path(self.translate_path(request.path))

        if route and "/" not in route and request.path.endswith("/") and not requested_file.exists():
            location = request.path.rstrip("/")
            if request.query:
                location += "?" + request.query
            self.send_response(301)
            self.send_header("Location", location)
            self.end_headers()
            return

        # Let real files and directories (including assets) be served normally.
        # Unknown one-part paths are guest links, so serve the invitation app.
        if route and "/" not in route and not requested_file.exists():
            self.path = "/index.html"
            if request.query:
                self.path += "?" + request.query

        super().do_GET()


if __name__ == "__main__":
    address = ("127.0.0.1", 8000)
    print(f"Undangan berjalan di http://{address[0]}:{address[1]}/")
    ThreadingHTTPServer(address, InvitationHandler).serve_forever()
