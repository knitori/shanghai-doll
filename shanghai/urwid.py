
# source from:
# https://gist.github.com/ksamuel/1521153

import sys
import logging

import urwid
from urwid import MetaSignals


class ExtendedListBox(urwid.ListBox):
    """
        Listbow widget with embeded autoscroll
    """

    __metaclass__ = urwid.MetaSignals
    signals = ["set_auto_scroll"]

    def set_auto_scroll(self, switch):
        if type(switch) != bool:
            return
        self._auto_scroll = switch
        urwid.emit_signal(self, "set_auto_scroll", switch)

    auto_scroll = property(lambda self: self._auto_scroll, set_auto_scroll)

    def __init__(self, body):
        urwid.ListBox.__init__(self, body)
        self.auto_scroll = True

    def switch_body(self, body):
        if self.body:
            urwid.disconnect_signal(body, "modified", self._invalidate)

        self.body = body
        self._invalidate()

        urwid.connect_signal(body, "modified", self._invalidate)

    def keypress(self, size, key):
        urwid.ListBox.keypress(self, size, key)

        if key in ("page up", "page down"):
            logging.debug("focus = {}, len = {}".format(
                self.get_focus()[1], len(self.body)))
            if self.get_focus()[1] == len(self.body)-1:
                self.auto_scroll = True
            else:
                self.auto_scroll = False
            logging.debug("auto_scroll = {}".format(self.auto_scroll))

    def scroll_to_bottom(self):
        logging.debug("current_focus = {}, len(self.body) = {}".format(
            self.get_focus()[1], len(self.body)))

        if self.auto_scroll:
            # at bottom -> scroll down
            self.set_focus(len(self.body)-1)


class MainWindow(object):

    __metaclass__ = MetaSignals
    signals = ["quit", "keypress"]

    _palette = [
            ('divider', 'black', 'dark cyan', 'standout'),
            ('text', 'light gray', 'default'),
            ('bold_text', 'light gray', 'default', 'bold'),
            ("body", "text"),
            ("footer", "text"),
            ("header", "text"),
        ]

    for type, bg in (
            ("div_fg_", "dark cyan"),
            ("", "default")):
        for name, color in (
                ("red", "dark red"),
                ("blue", "dark blue"),
                ("green", "dark green"),
                ("yellow", "yellow"),
                ("magenta", "dark magenta"),
                ("gray", "light gray"),
                ("white", "white"),
                ("black", "black")):
            _palette.append((type + name, color, bg))

    def __init__(self, sender="1234567890", event_loop=None):
        self.shall_quit = False
        self.sender = sender
        self.event_loop = event_loop
        self.size = 80, 24
        self.ui = None
        self.main_loop = None

    def main(self):
        """
            Entry point to start UI
        """

        self.ui = urwid.raw_display.Screen()
        self.ui.register_palette(self._palette)
        self.build_interface()
        self.ui.run_wrapper(self.run)

    def input_cb(self, key):
        if self.shall_quit:
            raise urwid.ExitMainLoop
        self.keypress(self.size, key)

    def run(self):
        """
            Setup input handler, invalidate handler to
            automatically redraw the interface if needed.
            Start mainloop.
        """

        self.size = self.ui.get_cols_rows()
        self.main_loop = urwid.MainLoop(
                self.context,
                screen=self.ui,
                handle_mouse=False,
                unhandled_input=self.input_cb,
                event_loop=self.event_loop,
            )

        try:
            self.main_loop.run()
        except KeyboardInterrupt:
            self.quit()

    def quit(self, exit=True):
        """
            Stops the ui, exits the application (if exit=True)
        """
        urwid.emit_signal(self, "quit")

        self.shall_quit = True

        if exit:
            sys.exit(0)

    def build_interface(self):
        """
            Call the widget methods to build the UI
        """

        self.header = urwid.Text("Chat")
        self.footer = urwid.Edit("> ")
        self.divider = urwid.Text("Initializing.")

        self.generic_output_walker = urwid.SimpleListWalker([])
        self.body = ExtendedListBox(
            self.generic_output_walker)

        self.header = urwid.AttrWrap(self.header, "divider")
        self.footer = urwid.AttrWrap(self.footer, "footer")
        self.divider = urwid.AttrWrap(self.divider, "divider")
        self.body = urwid.AttrWrap(self.body, "body")

        self.footer.set_wrap_mode("space")

        main_frame = urwid.Frame(self.body,
                                 header=self.header,
                                 footer=self.divider)

        self.context = urwid.Frame(main_frame, footer=self.footer)

        self.divider.set_text(("divider",
                               ("Send message:")))

        self.context.set_focus("footer")

    def draw_interface(self):
        self.main_loop.draw_screen()

    def keypress(self, size, key):
        """
            Handle user inputs

            :type size (int, int)
            :type key str
        """

        urwid.emit_signal(self, "keypress", size, key)

        # scroll the top panel
        if key in ("page up", "page down"):
            self.body.keypress(size, key)

        # resize the main windows
        elif key == "window resize":
            self.size = self.ui.get_cols_rows()

        elif key in ("ctrl d", 'ctrl c'):
            self.quit()

        elif key == "enter":
            # Parse data or (if parse failed)
            # send it to the current world
            text = self.footer.get_edit_text()

            self.footer.set_edit_text(" "*len(text))
            self.footer.set_edit_text("")

            if text in ('quit', 'q'):
                self.quit()

            if text.strip():
                self.print_sent_message(text)
                self.print_received_message('Answer')
        else:
            self.context.keypress(size, key)

    def print_sent_message(self, text):
        """
            Print a received message

            :type text str|urwid.Text
        """
        self.print_text(text)

    def print_received_message(self, text):
        """
            Print a sent message

            :type text str|urwid.Text
        """
        self.print_text(text)

    def print_text(self, text):
        """
            Print the given text in the _current_ window
            and scroll to the bottom.
            You can pass a Text object or a string

            :type text str|urwid.Text
        """
        walker = self.generic_output_walker
        if not isinstance(text, urwid.Text):
            text = urwid.Text(text)
        walker.append(text)
        self.body.scroll_to_bottom()
