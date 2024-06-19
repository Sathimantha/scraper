import http.server
import socketserver

# Define the port you want to serve on
PORT = 8000

# Create a simple handler
Handler = http.server.SimpleHTTPRequestHandler

# Create an HTTP server instance
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving HTTP on port {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

httpd.server_close()
print("Server stopped.")
