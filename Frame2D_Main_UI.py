from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objs as go
import sys, os
from qt_material import apply_stylesheet
extra = {
    # Density Scale
    'density_scale': '-2',
    'PyQt6': True,
    'windows': True
}


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the ui
        self.setWindowTitle("StruQLab Frame 2D")
        ui_file = QFile(self.resource_path("Frame2D_GUI.ui"))
        loader = QUiLoader()
        self.uic = loader.load(ui_file)

        # Create a Plotly figure
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 3, 5])])
        fig.update_layout(title="Sample Plotly Chart")
        fig.update_layout(template='plotly_dark')

        # Convert figure to HTML string
        html_content = fig.to_html(include_plotlyjs='cdn')
        web_view = self.uic.findChild(QWebEngineView, "webEngineView")

        if web_view is None:
            raise RuntimeError("QWebEngineView not found")

        web_view.setHtml(html_content)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_cyan.xml', extra = extra, css_file='custom.css')
    UIWindow = UI()
    UIWindow.uic.show()
    sys.exit(app.exec())
