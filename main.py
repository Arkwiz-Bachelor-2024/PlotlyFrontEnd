from app import app
import layout
import callbacks

layout.init_layout()

if __name__ == "__main__":
    app.run_server(debug=True)