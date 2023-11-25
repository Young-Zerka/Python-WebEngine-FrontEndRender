import wx
import wx.html2
import os
import json

class MyHtmlFrame(wx.Frame):
    def __init__(self, parent, title, icon_path):
        wx.Frame.__init__(
            self,
            parent,
            -1,
            title,
            size=(700, 400)
        )

        self.SetIcon(wx.Icon(icon_path, wx.BITMAP_TYPE_ICO))  

        self.webview = wx.html2.WebView.New(self)

        json_file_path = "config.json"

        try:
            with open(json_file_path, "r") as json_content:
                config_data = json.load(json_content)

                base_dir = config_data.get("base_dir", "")
                html_file_path = os.path.join(base_dir, config_data.get("html_file", ""))
                self.webview.LoadURL("file://" + html_file_path)

                js_files = config_data.get("js_files", [])
                for js_file in js_files:
                    js_file_path = os.path.join(base_dir, js_file)
                    with open(js_file_path, "r") as js_content:
                        js_code = js_content.read()
                        self.webview.RunScript(js_code)

                css_files = config_data.get("css_files", [])
                for css_file in css_files:
                    css_file_path = os.path.join(base_dir, css_file)
                    try:
                        with open(css_file_path, "r") as css_content:
                            css_code = "<style>{}</style>".format(css_content.read())
                            self.webview.RunScript(css_code)
                    except FileNotFoundError:
                        print(f"CSS file not found: {css_file_path}")

        except FileNotFoundError:
            print(f"JSON file not found: {json_file_path}")

app = wx.App()
json_file_path = "config.json"
icon_path = "" 
frame_title = ""

try:
    with open(json_file_path, "r") as json_content:
        config_data = json.load(json_content)
        base_dir = config_data.get("base_dir", "")
        icon_path = os.path.join(base_dir, config_data.get("icon_file", ""))
        frame_title = config_data.get("frame_title", "")
except FileNotFoundError:
    print(f"JSON file not found: {json_file_path}")

frm = MyHtmlFrame(None, frame_title, icon_path)
frm.Show()
app.MainLoop()