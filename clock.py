#!/usr/bin/env python3
import base64
import datetime
from io import BytesIO

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gdk, Gtk, GObject, GdkPixbuf, Gio, GLib

class ClockApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="net.korin.clock")
        GLib.set_application_name("Clock")


    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self, title="Clock")
        window.set_resizable(False)
        window.set_deletable(True)

        window.set_default_size(256,86)

        window.set_icon(self.load_icon())
        self.pixbuf = self.load_icon()

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        window.add(vbox)

        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_data(b"""
            label {
                font-size: 48px;
                font-family: "Matrix Sans Print SC", monospace;
            }
        """)

        self.label = Gtk.Label(label="05:09:47")
        self.label.set_xalign(0.5)
        self.label.get_style_context().add_provider(self.css_provider, 1)
        vbox.add(self.label)

        about_button = Gtk.Button(label="About")
        about_button.connect("clicked", self.show_about)
        vbox.add(about_button)

        self.setup_shortcuts(window)

        self.update()
        GLib.timeout_add_seconds(1, self.update)

        window.show_all()
        window.present()

    def load_icon(self):
        icon_data = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAASFJREFUWIXtV0uWhCAMrPTzWHA0s4gHc5GDZRY2DtK2Ak3jTL+ujc/wqaQMwcAAE8B6PxFwBblFDpABNgGACHpgZEbgY2b6VUDESoAliqI1ImIxn4jYbQQWjzoh5btNd2MpVBWqWrwu5RtqFXDOgYiwfI18NFOgFinf/82BWnwVeIsCRJQ9t7kCRFRUDw4VIKLDaMJ4Os97/zAWj8fvqQLDtGN8hjhS7/2DLQcp36YSnm3mnFsjUlV471dbjuPzPB/ngHPudMNAnkMcOx7mv3QKashTVJ+CPfIut2HI3r3Ia5SoUuBV2WMU50BLctQo0JIcH3UbnpXtZ/hzCpAANgKYOjUmYMaG76reMDQml/WGwYE1i0Sk7Ae/ETZp3NsJZqYf4rm/YXrWzTYAAAAASUVORK5CYII="
        try:
            icon_bytes = base64.b64decode(icon_data.strip())
            loader = GdkPixbuf.PixbufLoader()
            loader.write(icon_bytes)
            loader.close()
            pixbuf = loader.get_pixbuf()
            return pixbuf
        except Exception as e:
            print("K: we done fucked up.")
            print("Oops! An error has occurred!")
            print(e)
            return None

    def update(self):
        ct = datetime.datetime.now().strftime("%H:%M:%S")
        self.label.set_text(ct)
        return True

    def setup_shortcuts(self, window):
        accel_group = Gtk.AccelGroup()
        window.add_accel_group(accel_group)
        accel_group.connect(
            Gdk.KEY_F1,
            0,
            Gtk.AccelFlags.VISIBLE,
            lambda *args: self.show_about()
        )
        accel_group.connect(
            Gdk.KEY_Escape,
            0,
            Gtk.AccelFlags.VISIBLE,
            lambda *args: window.destroy(),
        )

    def show_about(self, *args):
        about = Gtk.AboutDialog()
        about.set_program_name("Clock")
        about.set_version("0.1")
        about.set_copyright("(c) Korin 2026")
        about.set_comments("A clock app.")
        about.set_authors(["Korin"])
        about.set_website("https://7d9.pages.dev/apps/clock")
        about.set_website_label("App Website")
        about.set_license_type(Gtk.License.GPL_3_0)

        about.set_logo(self.pixbuf)

        about.run()
        about.destroy()

app = ClockApp()
app.run()
