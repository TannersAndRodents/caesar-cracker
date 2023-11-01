# window.py
#
# Copyright 2023 Nathan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from .decryptor import encrypt_text, decrypt_text

@Gtk.Template(resource_path='/org/gnome/Example/window.ui')
class CaesarcrackerWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CaesarcrackerWindow'

    main_text_view = Gtk.Template.Child()
    open_button = Gtk.Template.Child()
    encrypt_button = Gtk.Template.Child()
    decrypt_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        open_action = Gio.SimpleAction(name="open")
        open_action.connect("activate", self.open_file_dialog)
        self.add_action(open_action)

        encrypt_action = Gio.SimpleAction(name="encrypt")
        encrypt_action.connect("activate", self.encrypt_text)
        self.add_action(encrypt_action)

        decrypt_action = Gio.SimpleAction(name="decrypt")
        decrypt_action.connect("activate", self.decrypt_text)
        self.add_action(decrypt_action)

    def open_file_dialog(self, action, _):
        self._native = Gtk.FileChooserNative(
            title="Open File",
            transient_for=self,
            action=Gtk.FileChooserAction.OPEN,
            accept_label="_Open",
            cancel_label="_Cancel",
        )

        self._native.connect("response", self.on_open_resource)

        self._native.show()

    def on_open_resource(self, diaglog, response):

        if response == Gtk.ResponseType.ACCEPT:
            self.open_file(diaglog.get_file())
        self._native = None

    def open_file(self, file):
        file.load_contents_async(None, self.open_file_complete)

    def open_file_complete(self, file, result):
        contents = file.load_contents_finish(result)

        info = file.query_info("standard::display-name", Gio.FileQueryInfoFlags.NONE)
        if info:
            display_name = info.get_attribute_string("standard::display-name")
        else:
            display_name = file.get_basename()

        if not contents[0]:
            path = file.peek_path()
            print(f"Unable to open {path}: {contents[1]}")
            return

        try:
            text = contents[1].decode('utf-8')
        except UnicodeError as err:
            path = file.peek_path()
            print(f"Unable to load the contents of {path}: the file is not encoded with UTF-8")
            return

        buffer = self.main_text_view.get_buffer()
        buffer.set_text(text)
        start = buffer.get_start_iter()
        buffer.place_cursor(start)

        self.set_title(display_name)

    def encrypt_text(self, action, _):

        buffer = self.main_text_view.get_buffer()
        buffer_start = buffer.get_start_iter()
        buffer_end = buffer.get_end_iter()
        INCLUDE_HIDDEN_CHARS = True
        text = buffer.get_text(buffer_start, buffer_end, INCLUDE_HIDDEN_CHARS)

        OFFSET = 1
        encrypted_text = encrypt_text(text, OFFSET)

        buffer.set_text(encrypted_text)
        return

    def decrypt_text(self, action, _):

        buffer = self.main_text_view.get_buffer()
        buffer_start = buffer.get_start_iter()
        buffer_end = buffer.get_end_iter()
        INCLUDE_HIDDEN_CHARS = True
        text = buffer.get_text(buffer_start, buffer_end, INCLUDE_HIDDEN_CHARS)

        decrypted_text = decrypt_text(text)

        buffer.set_text(decrypted_text)
        return
