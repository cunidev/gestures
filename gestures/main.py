from gi.repository import Gtk, Gio, Gdk

import sys
from configfile import ConfigFileHandler
from gesture import Gesture
from __version__ import __version__

class ErrorDialog(Gtk.Dialog):
    def __init__(self,parent):
	    pass
    def showNotInstalledError(self,win):
        dialog = Gtk.MessageDialog(
            win, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Can't load libinput-gestures")
        dialog.format_secondary_text(
            "Make sure it is correctly installed. The configuration file has been saved anyway.")
        dialog.run()
        dialog.destroy()

class EditDialog(Gtk.Dialog):
    def __init__(self, parent, confFile, i=-1):
        self.lock = False
        self.confFile = confFile

        if (i == -1):
            title = "Add Gesture"
            self.curGesture = Gesture("swipe", "up", "echo \"Useless\"", 2)
        else:
            title = "Edit Gesture"
            self.curGesture = self.confFile.gestures[i]

        Gtk.Dialog.__init__(self, title, parent, 0, Gtk.ButtonsType.NONE)
        self.set_transient_for(parent)
        self.set_modal(True)
        self.set_default_size(480, 200)

        area = self.get_content_area()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                      spacing=15, margin=10)
        area.add(box)

        hbox = Gtk.Box(spacing=5)
        box.add(hbox)

        label = Gtk.Label()
        label.set_markup("<b>Type</b>")
        hbox.pack_start(label, False, False, 0)

        self.buttonTypeSwipe = Gtk.RadioButton.new_with_label_from_widget(
            None, "Swipe")
        hbox.pack_start(self.buttonTypeSwipe, False, False, 0)

        self.buttonTypePinch = Gtk.RadioButton.new_from_widget(
            self.buttonTypeSwipe)
        self.buttonTypePinch.set_label("Pinch")
        hbox.pack_start(self.buttonTypePinch, False, False, 0)

        self.buttonTypeSwipe.set_active((self.curGesture.type != "pinch"))
        self.buttonTypePinch.set_active((self.curGesture.type == "pinch"))

        directionBox = Gtk.Box(spacing=5)
        box.add(directionBox)

        label = Gtk.Label()
        label.set_markup("<b>Direction</b>")
        directionBox.pack_start(label, False, False, 0)

        self.buttonDirection1 = Gtk.RadioButton.new_with_label_from_widget(
            None, "Up")
        directionBox.pack_start(self.buttonDirection1, False, False, 0)

        self.buttonDirection2 = Gtk.RadioButton.new_from_widget(
            self.buttonDirection1)
        self.buttonDirection2.set_label("Down")
        directionBox.pack_start(self.buttonDirection2, False, False, 0)

        self.buttonDirection3 = Gtk.RadioButton.new_from_widget(
            self.buttonDirection1)
        self.buttonDirection3.set_label("Left")
        directionBox.pack_start(self.buttonDirection3, False, False, 0)

        self.buttonDirection4 = Gtk.RadioButton.new_from_widget(
            self.buttonDirection1)
        self.buttonDirection4.set_label("Right")
        directionBox.pack_start(self.buttonDirection4, False, False, 0)

        # 1: up/in 2: down/out 3: left/clockwise 4: right/anticlockwise
        self.buttonDirection1.set_active(
            (self.curGesture.direction == "up") or (self.curGesture.direction == "in"))
        self.buttonDirection2.set_active(
            (self.curGesture.direction == "down") or (self.curGesture.direction == "out"))
        self.buttonDirection3.set_active((self.curGesture.direction == "left") or (
            self.curGesture.direction == "clockwise"))
        self.buttonDirection4.set_active((self.curGesture.direction == "right") or (
            self.curGesture.direction == "anticlockwise"))

        hbox = Gtk.Box(spacing=5)
        box.add(hbox)

        label = Gtk.Label()
        label.set_markup("<b>Fingers</b>")
        hbox.pack_start(label, False, False, 0)

        self.buttonFinger2 = Gtk.RadioButton.new_with_label_from_widget(
            None, "Two")
        hbox.pack_start(self.buttonFinger2, False, False, 0)

        self.buttonFinger3 = Gtk.RadioButton.new_from_widget(
            self.buttonFinger2)
        self.buttonFinger3.set_label("Three")
        hbox.pack_start(self.buttonFinger3, False, False, 0)

        self.buttonFinger4 = Gtk.RadioButton.new_from_widget(
            self.buttonFinger2)
        self.buttonFinger4.set_label("Four")
        hbox.pack_start(self.buttonFinger4, False, False, 0)

        if (self.curGesture.fingers != 0):
            self.buttonFinger2.set_active((int(self.curGesture.fingers) == 2))
            self.buttonFinger3.set_active((int(self.curGesture.fingers) == 3))
            self.buttonFinger4.set_active((int(self.curGesture.fingers) == 4))

        hbox = Gtk.Box(spacing=5)
        box.add(hbox)

        label = Gtk.Label()
        label.set_markup("<b>Command</b>")
        hbox.pack_start(label, False, False, 0)

        self.commandInput = Gtk.Entry()
        self.commandInput.set_text(self.curGesture.command)
        hbox.pack_start(self.commandInput, True, True, 0)

        # header bar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(False)
        hb.props.title = title

        cancelButton = Gtk.Button("Cancel")
        cancelButton.modify_bg(Gtk.StateType.ACTIVE, Gdk.color_parse('red'))
        hb.pack_start(cancelButton)

        confirmButton = Gtk.Button("Confirm")
        confirmButton.modify_bg(Gtk.StateType.ACTIVE, Gdk.color_parse('teal'))
        hb.pack_end(confirmButton)
        self.set_titlebar(hb)

        # signals - declared at the end to avoid AttributeErrors on not-yet-existing objects

        self.buttonTypeSwipe.connect("toggled", self.onTypeToggle, i, "swipe")
        self.buttonTypePinch.connect("toggled", self.onTypeToggle, i, "pinch")

        self.buttonDirection1.connect("toggled", self.onDirectionToggle, 1)
        self.buttonDirection2.connect("toggled", self.onDirectionToggle, 2)
        self.buttonDirection3.connect("toggled", self.onDirectionToggle, 3)
        self.buttonDirection4.connect("toggled", self.onDirectionToggle, 4)

        self.buttonFinger2.connect("toggled", self.onFingerToggle, 2)
        self.buttonFinger3.connect("toggled", self.onFingerToggle, 3)
        self.buttonFinger4.connect("toggled", self.onFingerToggle, 4)
        self.commandInput.connect("changed", self.onCommandChange)

        confirmButton.connect("clicked", self.onConfirm, i)
        cancelButton.connect("clicked", self.onCancel)
        
        confirmButton.set_can_default(True)
        confirmButton.grab_default()
        
        self.show_all()
        
        # SET LABELS - after show_all because of set_visible()
        self.setFingerRadios(self.curGesture.type)
        self.setDirectionLabels(self.curGesture.type)


    def setDirectionLabels(self, type):
        if(type == "pinch"):
            self.buttonDirection1.set_label("In")
            self.buttonDirection2.set_label("Out")
            self.buttonDirection3.set_label("Clockwise")
            self.buttonDirection4.set_label("Anticlockwise")
        else:
            self.buttonDirection1.set_label("Up")
            self.buttonDirection2.set_label("Down")
            self.buttonDirection3.set_label("Left")
            self.buttonDirection4.set_label("Right")

    def onTypeToggle(self, widget, i, type):
        self.curGesture.type = type

        self.setDirectionLabels(type)  # needed after changing type
        self.setFingerRadios(type)
        self.correctDirections()

    def setFingerRadios(self, type):
        if(type == "pinch"):
            self.buttonFinger2.set_visible(True)
        else:
            if(self.buttonFinger2.get_active() == True):
                self.buttonFinger3.set_active(True)
			    
            self.buttonFinger2.set_visible(False)

    def correctDirections(self):
        if(self.buttonDirection2.get_active()):
            direction = 2
        elif(self.buttonDirection3.get_active()):
            direction = 3
        elif(self.buttonDirection4.get_active()):
            direction = 4
        else:
            direction = 1

        self.onDirectionToggle(None, direction)

    def onDirectionToggle(self, widget, direction):
        if(self.curGesture.type == "pinch"):
            if(direction == 2):
                self.curGesture.direction = "out"
            elif(direction == 3):
                self.curGesture.direction = "clockwise"
            elif(direction == 4):
                self.curGesture.direction = "anticlockwise"
            else:
                self.curGesture.direction = "in"  # first case as default
        else:
            if(direction == 2):
                self.curGesture.direction = "down"
            elif(direction == 3):
                self.curGesture.direction = "left"
            elif(direction == 4):
                self.curGesture.direction = "right"
            else:
                self.curGesture.direction = "up"  # first case as default

    def onFingerToggle(self, widget, finger):
        self.curGesture.fingers = finger

    def onCommandChange(self, widget):
        self.curGesture.command = widget.get_text()

    def onCancel(self, widget):
        self.response(Gtk.ResponseType.CANCEL)

    def onConfirm(self, widget, i):
        if(i != -1):
            self.confFile.gestures[i] = self.curGesture
        else:
            self.confFile.gestures.append(self.curGesture)
        self.confFile.save()
        try:
            self.confFile.reloadProcess()
        except:
            err = ErrorDialog(self)
            err.showNotInstalledError(win)
        
        self.response(Gtk.ResponseType.OK)


class MainWindow(Gtk.Window):

    def __init__(self):
        self.editMode = False
        # window
        Gtk.Window.__init__(self, title="Gestures")
        self.set_border_width(10)
        self.set_default_size(600, 400)

        # header bar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Gestures"
        self.set_titlebar(hb)

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_end(button)
        button.connect("clicked", self.showMenu)

        self.menuPopover = Gtk.Popover.new(button)
        self.menuPopover.set_size_request(200, 100)
        popoverBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin=15)
        label = Gtk.Label(margin=10)
        label.set_markup("<b>Gestures</b> " + __version__ + "")
        button = Gtk.Button("Restore backup configuration", margin=10)
        button.connect("clicked", self.restoreBackup)

        popoverBox.add(label)
        popoverBox.add(button)
        self.menuPopover.add(popoverBox)

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="list-add-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        button.connect("clicked", self.onAdd)
        hb.pack_start(button)

        button = Gtk.ToggleButton()
        icon = Gio.ThemedIcon(name="document-edit-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        button.connect("clicked", self.onEditMode)
        hb.pack_start(button)

        # contents

        self.box_outer = Gtk.ScrolledWindow()
        self.box_outer.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.add(self.box_outer)
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.box_outer.add(self.listbox)

    def onAdd(self, widget):
        editDialog = EditDialog(self, self.confFile)
        editDialog.run()
        editDialog.destroy()
        self.populate()

    def onEditMode(self, button):
        self.editMode = button.get_active()
        self.populate()

    def onEdit(self, widget, i):
        editDialog = EditDialog(self, self.confFile, i)
        editDialog.run()
        editDialog.destroy()
        self.populate()

    def restoreBackup(self, button):
        self.hide()
        dialog = Gtk.MessageDialog(win, 0, Gtk.MessageType.WARNING,
                                   Gtk.ButtonsType.OK_CANCEL, "Restore backup configuration?")
        dialog.format_secondary_text(
            "This operation can't be undone. The app will be closed after restoring, and all changes will be lost.")
        if(dialog.run() == Gtk.ResponseType.OK):
            if(self.confFile.restore()):

                dialog.destroy()
                dialog = Gtk.MessageDialog(
                    win, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Backup file restored.")
                dialog.format_secondary_text(
                    "Gestures will be closed. Please remember that re-opening this app will result in overwriting the configuration file.")
                dialog.set_modal(True)
                dialog.run()
                dialog.destroy()
                sys.exit(0)
            else:
                dialog.destroy()
                dialog = Gtk.MessageDialog(
                    win, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Can't restore backup file.")
                dialog.format_secondary_text("The file might not exist.")
                dialog.set_modal(True)
                dialog.run()
                dialog.destroy()
                self.show()
        else:
            dialog.destroy()
            self.show()

    def onDelete(self, widget, i):
        dialog = Gtk.MessageDialog(
            win, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, "Confirm deletion?")
        dialog.format_secondary_text("This operation can't be undone.")
        if(dialog.run() == Gtk.ResponseType.OK):
            del self.confFile.gestures[i]
            self.confFile.save()

            self.confFile.reloadProcess()

        dialog.destroy()
        self.populate()

    def showMenu(self, widget):
        if self.menuPopover.get_visible():
            self.menuPopover.hide()
        else:
            self.menuPopover.show_all()

    def setConfFile(self, confFile):
        self.confFile = confFile

    def populate(self):
        # redraw

        for child in self.listbox.get_children():
            child.destroy()

        if(len(self.confFile.gestures) == 0):
            label = Gtk.Label()
            label.set_markup("<big><big>No gestures.</big></big>")
            #box = Gtk.Box()
            box = Gtk.ListBoxRow(margin=150)
            box.add(label)
            # self.listbox.set_placeholder(box)
            self.listbox.add(box)

            # TODO: fix (ugly and temporary!)

        for i, gesture in enumerate(self.confFile.gestures):

            row = Gtk.ListBoxRow(margin=5)
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, margin=5)
            row.add(hbox)
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

            hbox.pack_start(vbox, True, True, 0)

            label1 = Gtk.Label(xalign=0)
            label1.set_markup("<b>" + gesture.type.title() + " " + gesture.direction +
                              "</b> <i>(" + str(gesture.fingers) + " fingers)</i>" + "")

            if len(gesture.command) > 74:
                cmd = gesture.command[:70] + "..."
            else:
                cmd = gesture.command

            label2 = Gtk.Label(cmd, xalign=0)
            vbox.pack_start(label1, True, True, 0)
            vbox.pack_start(label2, True, True, 0)

            if(self.editMode):
                deleteButton = Gtk.Button()
                icon = Gio.ThemedIcon(name="edit-delete-symbolic")
                image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
                deleteButton.add(image)

                editButton = Gtk.Button()
                icon = Gio.ThemedIcon(name="document-edit-symbolic")
                image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
                editButton.add(image)

                editButton.connect("clicked", self.onEdit, i)

                box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
                Gtk.StyleContext.add_class(box.get_style_context(), "linked")

                box.add(editButton)
                box.add(deleteButton)

                deleteButton.connect("clicked", self.onDelete, i)

                hbox.pack_start(box, False, True, 10)
            else:
                switch = Gtk.Switch()
                switch.props.active = gesture.enabled
                switch.props.valign = Gtk.Align.CENTER
                hbox.pack_start(switch, False, True, 0)
                switch.connect("state-set", self.setActive, i)

            self.listbox.add(row)

        self.listbox.show_all()

    def setActive(self, widget, enabled, i):
        self.confFile.gestures[i].enabled = enabled
        self.confFile.save()
        try:
            self.confFile.reloadProcess()
        except:
            err = ErrorDialog(self)
            err.showNotInstalledError(win)
            
    def showNotInstalledError(self,win):
        dialog = Gtk.MessageDialog(
                win, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Can't load libinput-gestures")
        dialog.format_secondary_text(
            "Make sure it is correctly installed. The configuration file has been saved anyway.")
        dialog.run()
        dialog.destroy()


class main():
    win = MainWindow()
    
    
    try:
        confFile = ConfigFileHandler(__version__)
        if(confFile.createFileIfNotExisting()):
            dialog = Gtk.MessageDialog(
                win, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Configuration file not found")
            dialog.format_secondary_text(
                "Don't panic: an empty configuration file has just been generated.")
            dialog.run()
            dialog.destroy()
    
        confFile.openFile()
        if not(confFile.isValid()):
            if (confFile.backup()):
                dialog = Gtk.MessageDialog(win, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
                                           "The current configuration file hasn't been created with this tool.")
                dialog.format_secondary_text("The old file has been backed up to " + confFile.backupPath +
                                             ", its contents will be extracted and the conf file has been overridden.")
                dialog.run()
                dialog.destroy()
                confFile.save()
            else:
                dialog = Gtk.MessageDialog(
                    win, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Invalid configuration file, can't backup!")
                dialog.format_secondary_text(
                    "Can't create backup file! For security reasons, this tool can't be run.")
                dialog.run()
                dialog.destroy()
                sys.exit(-1)
        else:
            pass
    
    except:
        dialog = Gtk.MessageDialog(
            win, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Can't open configuration file.")
        dialog.format_secondary_text(
            "The configuration file can't be opened or created, check permissions.")
        dialog.run()
        dialog.destroy()
        sys.exit(-1)

    # load file
    win.setConfFile(confFile)
    win.set_position(Gtk.WindowPosition.CENTER)
    win.populate()
    
    try:
        self.confFile.reloadProcess()
    except:
        err = ErrorDialog(win)
        err.showNotInstalledError(win)

    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
