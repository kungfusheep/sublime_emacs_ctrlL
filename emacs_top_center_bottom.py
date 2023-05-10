import sublime
import sublime_plugin

class EmacsCenterTopBottomCommand(sublime_plugin.TextCommand):
    state = 0
    prev_cursor_position = None

    def run(self, edit):
        view = self.view
        cursor_position = view.sel()[0].begin()

        # Reset the state if the cursor line has moved
        if self.prev_cursor_position is not None and view.rowcol(cursor_position)[0] != view.rowcol(self.prev_cursor_position)[0]:
            EmacsCenterTopBottomCommand.state = 0

        layout_cursor_position = view.text_to_layout(cursor_position)

        if EmacsCenterTopBottomCommand.state == 0:
            view.show_at_center(cursor_position)
        elif EmacsCenterTopBottomCommand.state == 1:
            viewport_position = view.viewport_position()
            new_viewport_position = (viewport_position[0], layout_cursor_position[1] - view.line_height() - 30)
            view.set_viewport_position(new_viewport_position, True)
        elif EmacsCenterTopBottomCommand.state == 2:
            viewport_extents = view.viewport_extent()
            viewport_position = view.viewport_position()
            new_viewport_position = (viewport_position[0], layout_cursor_position[1] - viewport_extents[1] + view.line_height() + 30)
            view.set_viewport_position(new_viewport_position, True)

        EmacsCenterTopBottomCommand.state = (EmacsCenterTopBottomCommand.state + 1) % 3
        self.prev_cursor_position = cursor_position
