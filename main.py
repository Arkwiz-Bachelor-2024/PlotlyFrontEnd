from dashboard.app import app
import dashboard.layout as layout
import dashboard.callbacks as callbacks

layout.init_layout()

if __name__ == "__main__":
    app.run_server(debug=True)