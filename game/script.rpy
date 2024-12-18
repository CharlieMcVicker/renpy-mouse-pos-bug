init python:
    from pygame import MOUSEMOTION

    class DebugCursor(renpy.Displayable):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.child = Text("waiting for mouse event")

            self.mx = None
            self.my = None

        def render(self, width, height, st, at):
            if self.mx is not None and self.my is not None:
                self.child = Text("mouse: "+str(self.mx)+", "+str(self.my))
            
            child_render = renpy.render(self.child, width, height, st, at)
            self.width, self.height = child_render.get_size()

            render = renpy.Render(self.width, self.height)
            render.blit(child_render, (0, 0))
            # show the size of the render (self.width, self.height)
            render.fill((255, 0, 0, 125))

            return render

        def event(self, ev, x, y, st):
            if ev.type == MOUSEMOTION:
                self.mx = x
                self.my = y
                
                renpy.redraw(self, 0)

                # log width and height to compare with mouse positions at boundaries of rendered item
                print(x, y, self.width, self.height)
            
            return self.child.event(ev, x, y, st)

        def visit(self):
            return [ self.child ]

    def debug_tag(tag, argument, contents):
        return [(renpy.TEXT_DISPLAYABLE, DebugCursor())]

    config.custom_text_tags["debug"] = debug_tag


label start:
    # contrast of filler background helps see textbox
    show bg some_image
    """{debug}{/debug}"""

    """Some offset to the left {debug}{/debug}"""

    """Some offset above
    \n
    {debug}{/debug}"""

    return