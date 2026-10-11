# big photos use a lot of memory, so we only keep the last few steps
MAX_HISTORY = 10


class History:
    """Keeps earlier versions of the image so the user can undo and redo changes."""

    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    # call this before the image is changed
    def save(self, image):
        if image is None:
            return

        self.undo_stack.append(image)
        if len(self.undo_stack) > MAX_HISTORY:
            self.undo_stack.pop(0)

        # a new change makes the old redo steps invalid
        self.redo_stack.clear()

    # returns the previous image, or None if there is nothing to undo
    def undo(self, current_image):
        if not self.undo_stack:
            return None

        self.redo_stack.append(current_image)
        return self.undo_stack.pop()

    # returns the next image, or None if there is nothing to redo
    def redo(self, current_image):
        if not self.redo_stack:
            return None

        self.undo_stack.append(current_image)
        return self.redo_stack.pop()

    def clear(self):
        self.undo_stack.clear()
        self.redo_stack.clear()
