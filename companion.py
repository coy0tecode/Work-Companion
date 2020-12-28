# -*- coding: utf-8 -*-

import os
import re
import threading
import glob
import win32api
import webbrowser
import winsound
import wx
import wx.adv
import wx.lib.agw.genericmessagedialog as GMD
from datetime import datetime
from datetime import timedelta
from random import randint
from functools import partial



# Create profile directory if not already exists
profile_directory = os.getcwd() + '/Profiles'
if not os.path.exists(profile_directory):
    os.makedirs(profile_directory)
    
    
# Set image directory
image_directory = os.getcwd() + '/Images'
    
    
# Set music directory
music_directory = os.getcwd() + '/Music'


# Set profile_directory as cwd
os.chdir(profile_directory)



# Create the registration panel
class RegPanel(wx.Panel):
    
    def __init__(self, *args, **kwargs):
        super(RegPanel, self).__init__(*args, **kwargs)
        
        
        # Companion image dictionary
        # For companion images in hbox4
        self.companion_images = {'Default' : image_directory + '/default0.png',
                                'Butler' : image_directory + '/butler0.png',
                                'Bro' : image_directory + '/bro0.png',
                                'Goon' : image_directory + '/goon0.png',
                                'Vassal' : image_directory + '/vassal0.png',
                                'BFF' : image_directory + '/bff0.png',
                                'Secretary' : image_directory + '/secretary0.png',
                                'Dog' : image_directory + '/dog0.png'}


        # Set font style        
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(12)
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Name entry
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        name_text = wx.StaticText(self, label='Name')
        name_text.SetFont(font)
        hbox1.Add(name_text, flag=wx.RIGHT, border=8)
        self.name_entry = wx.TextCtrl(self)
        self.Bind(wx.EVT_TEXT, self.onName, self.name_entry)
        hbox1.Add(self.name_entry, proportion=1)
        self.vbox.Add(hbox1, flag=wx.EXPAND|wx.RIGHT|wx.LEFT|wx.TOP, border=20)
        
        self.vbox.Add((-1, 10))
        
        # Birthday entry
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        bday_text = wx.StaticText(self, label='Birthday')
        bday_text.SetFont(font)
        hbox2.Add(bday_text, flag=wx.RIGHT, border=8)
        self.bday_entry = wx.adv.DatePickerCtrl(self)
        hbox2.Add(self.bday_entry, proportion=1)
        self.vbox.Add(hbox2, flag=wx.EXPAND|wx.RIGHT|wx.LEFT|wx.TOP, border=20)
        
        self.vbox.Add((-1, 10))
        
        # Companion Choice
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        comp_text = wx.StaticText(self, label='Choose Companion Style')
        comp_text.SetFont(font)
        hbox3.Add(comp_text, flag=wx.RIGHT, border = 8)
        self.comp_choice = wx.Choice(self, choices=['Default', 'Butler', 'Bro',
                                               'Goon', 'Vassal', 'BFF',
                                               'Secretary', 'Dog'])
        self.Bind(wx.EVT_CHOICE, self.compSelect, self.comp_choice)
        hbox3.Add(self.comp_choice, proportion=1)
        self.vbox.Add(hbox3, flag=wx.RIGHT|wx.LEFT|wx.TOP, border=20)
        
        self.vbox.Add((-1, 50))
        
        # Companion Image (changes accordingly with companion choice)
        self.hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        # Set initial companion to default
        self.companion = 'Default'
        self.comp_image = wx.Image(name=self.companion_images[self.companion],
                                   type=wx.BITMAP_TYPE_PNG)
        self.final_image = self.comp_image.ConvertToBitmap()
        self.image_holder = wx.StaticBitmap(self, bitmap=self.final_image)
        self.hbox4.Add(self.image_holder, flag=wx.ALIGN_LEFT|wx.ALL, border=10)
        self.vbox.Add(self.hbox4, flag=wx.ALIGN_LEFT|wx.ALL, border=10)
        
        # Register Button
        self.hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.reg_button = wx.Button(self, label='Register', size=(100, 40))
        self.Bind(wx.EVT_BUTTON, self.onReg, self.reg_button)
        self.hbox5.Add(self.reg_button, flag=wx.ALL|wx.ALIGN_BOTTOM, border=20)
        self.vbox.Add((0.0), 1, wx.ALL|wx.EXPAND, 5)
        self.vbox.Add(self.hbox5, flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM, border=20)
        
        # Bind size event
        self.Bind(wx.EVT_SIZE, self.onSize)
        
        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        
    # Bound to 'comp_choice'. Changes companion image when a companion
    # style is selected from the drop down list
    def compSelect(self, e):
        os.chdir(image_directory)
        self.companion = self.comp_choice.GetCurrentSelection()
        self.companion = self.comp_choice.GetString(self.companion)
        self.comp_image = wx.Image(name=self.companion_images[self.companion],
                                   type=wx.BITMAP_TYPE_PNG)
        self.final_image = self.comp_image.ConvertToBitmap()
        self.hbox4.Detach(self.image_holder)
        self.image_holder.Destroy()
        self.image_holder = wx.StaticBitmap(self, bitmap=self.final_image)
        self.vbox.Detach(self.hbox4)
        self.hbox4.Destroy()
        self.hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox4.Add(self.image_holder, flag=wx.ALIGN_LEFT|wx.ALL, border=10)
        self.vbox.Add(self.hbox4, flag=wx.ALIGN_LEFT|wx.ALL, border=10)
        self.vbox.Detach(self.hbox5)
        self.vbox.Add(self.hbox5, flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM, border=20)
        self.Layout()
        self.Refresh()
    
    # Bound to 'Register'. Checks if Name is not in registered profiles,
    # adds profile information to registered profiles and changes app to
    # home screen.
    def onReg(self, e):
        if self.name_entry.GetLineText(0):
            if os.path.exists(profile_directory + '/' + self.pend_name):
                wx.MessageBox('Profile name is already taken',
                              'Error: Invalid profile name', wx.OK|wx.ICON_ERROR)
            else:
                self.bday = self.bday_entry.GetValue()
                self.bday = str(self.bday)
                os.makedirs(profile_directory + '/' + self.pend_name)
                global current_profile_dir
                current_profile_dir = profile_directory + '/' + self.pend_name
                os.chdir(current_profile_dir)
                bday_file = open('birthday.txt', 'w')
                bday_file.write(self.bday)
                bday_file.close()
                companion_file = open('companion.txt', 'w')
                companion_file.write(self.companion)
                companion_file.close()
                global notes_path
                notes_path = os.getcwd() + '/Notes'
                os.makedirs(notes_path)
                global break_path
                break_path = os.getcwd() + '/Breaks'
                os.makedirs(break_path)
                wx.MessageBox('Your profile has been created. Please click ok to '
                              'reach the home screen', 'Registration Successful!',
                              wx.OK)
                
                # Prepare to check if it is profile's birthday
                self.current = datetime.now()
                self.current = self.current.strftime("%b%d")
                self.bday = datetime.strptime(self.bday, 
                                              "%a %b %d %H:%M:%S %Y")
                self.bday = self.bday.strftime("%b%d")
                
                main_panel.updateCompanion()
                self.Hide()
                main_panel.Show()
                main_panel.PostSizeEvent()
                app_window.PostSizeEvent()
                if self.current == self.bday:
                    main_panel.birthdayShow(self.pend_name, self.companion)
        else:
            wx.MessageBox('Profile name must have at least 1 character',
                          'Error: Invalid profile name', wx.OK|wx.ICON_ERROR)
        
    # Bound to 'Name entry field'. Gets value from name_entry for use in the
    # onReg function
    def onName(self, e):
        self.pend_name = self.name_entry.GetLineText(0)
        
        
    # Size event function
    def onSize(self, e):
        self.Refresh()
        self.Layout()
        
        
        
# Create the main panel
class MainPanel(wx.Panel):
    
    def __init__(self, *args, **kwargs):
        super(MainPanel, self).__init__(*args, **kwargs)
        
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        
        # Create dummy object(s) for sizing
        self.dummy1 = wx.StaticText(self, label='')
                
        
        # hbox2 (dummy1, break panel)
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.break_button = wx.Button(self, label='Break Panel', size=(100, 50))
        self.Bind(wx.EVT_BUTTON, self.breakShow, self.break_button)
        self.hbox2.Add(self.dummy1, 1, flag=wx.ALL, border=20)
        self.hbox2.Add(self.break_button, 1, flag=wx.ALIGN_RIGHT|wx.ALL, border=10)
        
        # Add hbox2 to vbox
        self.vbox.Add(self.hbox2, 1, flag=wx.ALIGN_RIGHT|wx.ALL, border=10)
        
        
        # hbox3 (notes panel)
        self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.notes_button = wx.Button(self, label='Notes Panel', size=(100, 50))
        self.Bind(wx.EVT_BUTTON, self.noteShow, self.notes_button)
        self.hbox3.Add(self.notes_button, 1, flag=wx.ALIGN_RIGHT|wx.ALL, border=10)
        
        # Add hbox3 to vbox
        self.vbox.Add(self.hbox3, 1, flag=wx.ALIGN_RIGHT|wx.ALL, border=10)
        
        
        # hbox4 (companion image)
        # Companion image dictionary
        # For companion images in hbox4
        self.companion_images = {'Default' : image_directory + '/default0.png',
                                'Butler' : image_directory + '/butler0.png',
                                'Bro' : image_directory + '/bro0.png',
                                'Goon' : image_directory + '/goon0.png',
                                'Vassal' : image_directory + '/vassal0.png',
                                'BFF' : image_directory + '/bff0.png',
                                'Secretary' : image_directory + '/secretary0.png',
                                'Dog' : image_directory + '/dog0.png'}


        self.hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        try:
            global current_profile_dir
            os.chdir(current_profile_dir)
            companion_file = open('companion.txt', 'r')
            self.companion = companion_file.readline()
            companion_file.close()
        except:
            self.companion = 'Default'
        os.chdir(image_directory)
        self.comp_image = wx.Image(name=self.companion_images[self.companion],
                                   type=wx.BITMAP_TYPE_PNG)
        self.final_image = self.comp_image.ConvertToBitmap()
        self.image_holder = wx.StaticBitmap(self, bitmap=self.final_image)
        self.hbox4.Add(self.image_holder, flag=wx.ALIGN_LEFT|wx.ALL, border=10)
        self.vbox.Add(self.hbox4, flag=wx.ALIGN_LEFT|wx.ALL, border=10)
        
        # Bind size event
        self.Bind(wx.EVT_SIZE, self.onSize)
        
        # Set sizer and fit
        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        

        
    # Function to update companion image
    def updateCompanion(self):
        
        try:
            global current_profile_dir
            os.chdir(current_profile_dir)
            companion_file = open('companion.txt', 'r')
            self.companion = companion_file.readline()
            companion_file.close()
        except:
            self.companion = 'Default'

        os.chdir(image_directory)
        self.comp_image = wx.Image(name=self.companion_images[self.companion],
                                   type=wx.BITMAP_TYPE_PNG)
        self.final_image = self.comp_image.ConvertToBitmap()
        self.image_holder.SetBitmap(self.final_image)
        self.vbox.Detach(self.hbox4)
        self.hbox4.Destroy()
        self.hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox4.Add(self.image_holder, flag=wx.ALIGN_LEFT|wx.ALL, border=10)
        self.vbox.Add(self.hbox4, flag=wx.ALIGN_LEFT|wx.ALL, border=10)
        self.Layout()
        self.Refresh()
        
    
    # Bound to 'Break Panel' button
    def breakShow(self, e):
        self.Hide()
        break_panel.populateBreaks()
        break_panel.Show()
        break_panel.PostSizeEvent()
        app_window.PostSizeEvent()
    
    
    # Bound to 'Notes Panel' button
    def noteShow(self, e):
        self.Hide()
        notes_panel.updatePath()
        notes_panel.Show()
        notes_panel.PostSizeEvent()
        app_window.PostSizeEvent()
        
        
    # Size event function
    def onSize(self, e):
        self.Refresh()
        self.Layout()
        
        
    # Called from profile popup if datetime.now matches birthday
    def birthdayShow(self, name='User', companion='Default'):
        self.bday_object = birthdayDialog(self)
        self.bday_object.SetLabel(f'HAPPY BIRTHDAY {name}!!!')
        self.bday_object.updateBdayComp(companion)
        self.bday_object.ShowModal()
        


# Create birthday dialog
class birthdayDialog(wx.Dialog):
    
    def __init__(self, *args, **kwargs):
        super(birthdayDialog, self).__init__(*args, **kwargs)
        
        
        
        # Birthday companion dictionary
        self.bday_companions = {'Default' : image_directory + '/defaultB.png',
                                'Butler' : image_directory + '/butlerB.png',
                                'Bro' : image_directory + '/broB.png',
                                'Goon' : image_directory + '/goonB.png',
                                'Vassal' : image_directory + '/vassalB.png',
                                'BFF' : image_directory + '/bffB.png',
                                'Secretary' : image_directory + '/secretaryB.png',
                                'Dog' : image_directory + '/dogB.png'}
        
        # Birthday image dictionary
        self.bday_pictures = {1 : image_directory + '/cake.png',
                              2 : image_directory + '/balloons.png',
                              3 : image_directory + '/phat.png'}
        
        # Roll for bday_image
        self.bday_roll = randint(1, 3)
        
        
        # Set font style and size
        self.font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        self.font.SetPointSize(18)
        
        # Create vbox
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Create hbox (bday companion image, birthday image)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        # Create image holder for bday companion (bro0 used as default)
        self.bday_companion = wx.Image(image_directory + '/bro0.png',
                                       type=wx.BITMAP_TYPE_PNG)
        self.companion_final = self.bday_companion.ConvertToBitmap()
        self.companion_holder = wx.StaticBitmap(self, bitmap=self.companion_final)
        
        # Add self.companion_holder to hbox
        self.hbox.Add(self.companion_holder, flag=wx.ALL|wx.EXPAND, border=50)
        
        # Create image holder for bday image
        self.bday_image = wx.Image(self.bday_pictures[self.bday_roll],
                                   type=wx.BITMAP_TYPE_PNG)
        self.bday_final = self.bday_image.ConvertToBitmap()
        self.bday_holder = wx.StaticBitmap(self, bitmap=self.bday_final)
        
        # Add self.bday_holder to hbox
        self.hbox.Add(self.bday_holder, flag=wx.ALL|wx.EXPAND, border=50)
        
        # Add hbox to vbox
        self.vbox.Add(self.hbox, flag=wx.ALL|wx.EXPAND, border=5)
        
        # Bind close event
        self.Bind(wx.EVT_CLOSE, self.onX)
        
        # Set sizer and fit
        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        
        
    # Function to update bday_companion image
    def updateBdayComp(self, companion='Default'):
        
        # Detach and destroy companion_holder
        self.hbox.Detach(self.companion_holder)
        self.companion_holder.Destroy()
        self.bday_companion = wx.Image(self.bday_companions[companion],
                                       type=wx.BITMAP_TYPE_PNG)
        self.companion_final = self.bday_companion.ConvertToBitmap()
        self.companion_holder = wx.StaticBitmap(self, bitmap=self.companion_final)
        
        # Detach bday_holder from hbox
        self.hbox.Detach(self.bday_holder)
        
        # Detach hbox from vbox
        self.vbox.Detach(self.hbox)
        
        # Add back image holders to hbox
        self.hbox.Add(self.companion_holder, flag=wx.ALL|wx.EXPAND, border=50)
        self.hbox.Add(self.bday_holder, flag=wx.ALL|wx.EXPAND, border=50)
        
        # Add hbox back to vbox
        self.vbox.Add(self.hbox, flag=wx.ALL|wx.EXPAND, border=5)
        
        # Set sizer and fit
        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        
    
    # Bound to 'X' on top right of Dialog
    def onX(self, e):
        self.EndModal(1)
    
        
        
        
# Create the break panel
class BreakPanel(wx.Panel):
    
    def __init__(self, *args, **kwargs):
        super(BreakPanel, self).__init__(*args, **kwargs)
        
        
        # Set label font
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(12)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # hbox1 (descriptive text for saved breaks, break options)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Dummy text panels for additional spacing
        dummy = wx.StaticText(self, label='')
        dummy2 = wx.StaticText(self, label='')
        
        # Saved breaks text
        saved_text = wx.StaticText(self, label='Saved Breaks')
        saved_text.SetFont(font)
        hbox1.Add(dummy2, 0, flag=wx.RIGHT, border=7)
        hbox1.Add(saved_text, 0, flag=wx.ALL, border=15)
        hbox1.Add(dummy, 0, flag=wx.LEFT, border=15)
        
        # Dummy text panels for additional spacing
        dummy3 = wx.StaticText(self, label='')
        dummy4 = wx.StaticText(self, label='')
        
        # Break type text
        break_type_text = wx.StaticText(self, label='Break Type')
        break_type_text.SetFont(font)
        hbox1.Add(dummy4, 0, flag=wx.RIGHT, border=8)
        hbox1.Add(break_type_text, 0, flag=wx.ALL, border=15)
        hbox1.Add(dummy3, 0, flag=wx.LEFT, border=28)
        
        # Break length text
        break_length_text = wx.StaticText(self, label='Break Length')
        break_length_text.SetFont(font)
        hbox1.Add(break_length_text, 0, flag=wx.ALL, border=15)
        
        # Dummy text panels for additional spacing
        dummy5 = wx.StaticText(self, label='')
        dummy6 = wx.StaticText(self, label='')
        
        # Interval text
        interval_text = wx.StaticText(self, label='Interval')
        interval_text.SetFont(font)
        hbox1.Add(dummy5, 0, flag=wx.RIGHT, border=40)
        hbox1.Add(interval_text, 0, flag=wx.ALL, border=15)
        hbox1.Add(dummy6, 0, flag=wx.LEFT, border=65)
        
        # Music choice text
        music_text = wx.StaticText(self, label='Music')
        music_text.SetFont(font)
        hbox1.Add(music_text, 0, flag=wx.ALL, border=15)
        
        
        # Add hbox1 to vbox
        vbox.Add(hbox1, 1, flag=wx.ALL|wx.EXPAND, border=10)
        
        
        # hbox2 (drop down menus for all listed options)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Saved breaks drop down menu
        self.saved_breaks = wx.Choice(self, choices=[])
        self.Bind(wx.EVT_CHOICE, self.breakChoice, self.saved_breaks)
        hbox2.Add(self.saved_breaks, 1, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM,
                  border=15)
        
        # Break type drop down menu
        self.break_type = wx.Choice(self, choices=['Take a Walk', 'Stretch',
                                                   'Phone Time', 'Snack Time',
                                                   'Meditate'])
        self.break_type.SetSelection(0)
        hbox2.Add(self.break_type, 1, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM,
                  border=15)
        
        # Break length drop down menu
        self.break_length = wx.Choice(self, choices=['2 minutes', '5 minutes',
                                                     '7 minutes', '10 minutes'])
        self.break_length.SetSelection(0)
        hbox2.Add(self.break_length, 1, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM,
                  border=15)
        
        # Interval drop down menu
        self.interval_choice = wx.Choice(self, 
                                         choices=['0.5 hours', '1 hour',
                                                  '1.5 hours', '2 hours',
                                                  '2.5 hours', '3 hours',
                                                  '4 hours'])
        self.interval_choice.SetSelection(0)
        hbox2.Add(self.interval_choice, 1, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM,
                  border=15)
        
        # Music drop down menu
        self.music_choice = wx.Choice(self, choices=['None', 'Elegy For Argus',
                                                     'Sphere',
                                                     'A Christmas Adventure',
                                                     'Binary Code'])
        self.music_choice.SetSelection(0)
        hbox2.Add(self.music_choice, 1, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM,
                  border=15)
        
        # Add hbox2 to vbox
        vbox.Add(hbox2, 1, flag=wx.ALL|wx.EXPAND, border=10)
        
        
        # hbox3 (buttons)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Save break button
        self.save_break = wx.Button(self, label='Save Break', size=(100,50))
        self.Bind(wx.EVT_BUTTON, self.onSave, self.save_break)
        hbox3.Add(self.save_break, 1, flag=wx.ALL, border=10)
        
        # Delete break button
        self.delete_break = wx.Button(self, label='Delete Selected Break',
                                      size=(140,50))
        self.Bind(wx.EVT_BUTTON, self.onDelete, self.delete_break)
        hbox3.Add(self.delete_break, 1, flag=wx.ALL, border=10)
        
        # Break now button
        self.break_now = wx.Button(self, label='Break Now', size=(100,50))
        self.Bind(wx.EVT_BUTTON, self.onNow, self.break_now)
        hbox3.Add(self.break_now, 1, flag=wx.ALL, border=10)
        
        # Add hbox3 to vbox
        vbox.Add(hbox3, 1, flag=wx.ALL, border=5)
        
        
        # Additional vbox space
        vbox.Add((-1, 10))
        
        
        # hbox4 (main menu button)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Main menu button
        self.main_menu = wx.Button(self, label='Main Menu', size=(100,70))
        self.Bind(wx.EVT_BUTTON, self.onMenu, self.main_menu)
        hbox4.Add(self.main_menu, 0, flag=wx.ALL|wx.ALIGN_BOTTOM, 
                  border=15)
        
        # Add hbox4 to vbox
        vbox.Add(hbox4, 0, flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM, border=15)
        
        # Bind size event
        self.Bind(wx.EVT_SIZE, self.onSize)
        
            
        # Set sizer and fit
        self.SetSizer(vbox)
        vbox.Fit(self)
        
        
        
    # Bound to 'Saved Breaks' choice menu
    def breakChoice(self, e):
        selected_break = self.saved_breaks.GetCurrentSelection()
        self.loaded_break = self.saved_breaks.GetString(selected_break)
        global break_path
        os.chdir(break_path)
        try:
            with open(self.loaded_break, 'r') as file:
                for i, line in enumerate(file):
                    if i == 2:
                        global interval_timer
                        interval_timer = float(re.search(r'\d+\.*\d*', line).group())
                    else:
                        pass
            now = datetime.now()
            run_at = now + timedelta(hours=interval_timer)
            delay = (run_at - now).total_seconds()
            threading.Timer(delay, self.breakFunction).start()
        except:
            wx.MessageBox('Break file could not be found. Please restart the app',
                          'Error: File not found', wx.OK|wx.ICON_ERROR)

    
    # Bound to 'Save Break' button
    def onSave(self, e):
        save_popup = wx.TextEntryDialog(self, 'Enter Filename',
                                       caption='Save Break',
                                       style=wx.OK|wx.CANCEL)
        save_choice = save_popup.ShowModal()
        if save_choice == wx.ID_OK:
            global break_path
            os.chdir(break_path)
            self.break_title = save_popup.GetValue() + '.txt'
            b_type = self.break_type.GetString(self.break_type.GetCurrentSelection())
            b_length = self.break_length.GetString(
                self.break_length.GetCurrentSelection())
            i_choice = self.interval_choice.GetString(
                self.interval_choice.GetCurrentSelection())
            m_choice = self.music_choice.GetString(
                self.music_choice.GetCurrentSelection())
            self.break_file = open(self.break_title, 'w')
            self.break_file.write(b_type + '\n')
            self.break_file.write(b_length + '\n')
            self.break_file.write(i_choice + '\n')
            self.break_file.write(m_choice)
            self.saved_breaks.AppendItems(self.break_title)
            self.break_file.close()
        else:
            pass
            
        
    
    # Bound to 'Delete Selected Break' button
    def onDelete(self, e):
        selected_break = self.saved_breaks.GetCurrentSelection()
        if selected_break == -1:
            wx.MessageBox('Please select a break', 'Error: No break selected',
                          wx.OK|wx.ICON_ERROR)
        else:
            delete_pUp = wx.MessageDialog(self,
                                         'Do you really want to delete this break?',
                                         caption='WARNING',
                                         style=wx.YES_NO|wx.NO_DEFAULT|wx.ICON_WARNING)
            delete_choice = delete_pUp.ShowModal()
            if delete_choice == wx.ID_YES:
                global break_path
                break_name = self.saved_breaks.GetString(selected_break)
                self.saved_breaks.Delete(selected_break)
                delete_path = break_path + '/' + break_name
                os.remove(delete_path)
            else:
                pass
                
            
    
    # Bound to 'Break Now' button
    def onNow(self, e):
        selected_break = self.saved_breaks.GetCurrentSelection()
        if selected_break == -1:
            wx.MessageBox('Please select a break', 'Error: No break selected',
                          wx.OK|wx.ICON_ERROR)
        else:
            self.breakFunction()
                
    
    # Bound to 'Main Menu' button
    def onMenu(self, e):
        self.Hide()
        main_panel.Show()
        main_panel.PostSizeEvent()
        app_window.PostSizeEvent()
        
        
    # Size event function
    def onSize(self, e):
        self.Refresh()
        self.Layout()
        
        
    # Function to populate saved breaks from user's Breaks folder
    def populateBreaks(self):
        global break_path
        os.chdir(break_path)
        self.saved_breaks.Clear()
        self.break_files = glob.glob(break_path + '/*.txt')
        for path in (self.break_files):
            self.saved_breaks.AppendItems(os.path.basename(path))
            
            
    # Function that runs the selected break at the appropriate time
    def breakFunction(self):
        global break_path
        global current_profile_dir
        os.chdir(break_path)
        try:
            break_open = open(self.loaded_break, 'r')
            break_name = break_open.readline().rstrip('\n')
            break_duration = break_open.readline().rstrip('\n')
            break_duration = int(re.search(r'\d+', break_duration).group())
            break_open.readline()
            break_music = break_open.readline().rstrip('\n')
            self.break_object = BreakDialog(self)
            break_open.close()
            os.chdir(current_profile_dir)
            companion_open = open('companion.txt', 'r')
            break_companion = companion_open.readline().rstrip('\n')
            companion_open.close()
            self.break_object.updateImages(break_name, break_companion)
            self.break_object.playMusic(break_music)
            self.break_object.timeStart(break_duration)
            self.break_object.ShowModal()
            pass
        except:
            wx.MessageBox('Break file could not be found. Please restart the app',
                          'Error: File not found', wx.OK|wx.ICON_ERROR)
            return
        pass
        
    
    
# Create the break popup dialog
class BreakDialog(wx.Dialog):
    
    def __init__(self, *args, **kwargs):
        super(BreakDialog, self).__init__(*args, **kwargs)
        
        
        # Companion activity image dictionaries
        self.walk_companions = {'Default' : image_directory + '/default1.png',
                                'Butler' : image_directory + '/butler1.png',
                                'Bro' : image_directory + '/bro1.png',
                                'Goon' : image_directory + '/goon1.png',
                                'Vassal' : image_directory + '/vassal1.png',
                                'BFF' : image_directory + '/bff1.png',
                                'Secretary' : image_directory + '/secretary1.png',
                                'Dog' : image_directory + '/dog1.png'}
        
        self.stretch_companions = {'Default' : image_directory + '/default2.png',
                                   'Butler' : image_directory + '/butler2.png',
                                   'Bro' : image_directory + '/bro2.png',
                                   'Goon' : image_directory + '/goon2.png',
                                   'Vassal' : image_directory + '/vassal2.png',
                                   'BFF' : image_directory + '/bff2.png',
                                   'Secretary' : image_directory + '/secretary2.png',
                                   'Dog' : image_directory + '/dog2.png'}
        
        self.phone_companions = {'Default' : image_directory + '/default3.png',
                                 'Butler' : image_directory + '/butler3.png',
                                 'Bro' : image_directory + '/bro3.png',
                                 'Goon' : image_directory + '/goon3.png',
                                 'Vassal' : image_directory + '/vassal3.png',
                                 'BFF' : image_directory + '/bff3.png',
                                 'Secretary' : image_directory + '/secretary3.png',
                                 'Dog' : image_directory + '/dog3.png'}
        
        self.snack_companions = {'Default' : image_directory + '/default4.png',
                                 'Butler' : image_directory + '/butler4.png',
                                 'Bro' : image_directory + '/bro4.png',
                                 'Goon' : image_directory + '/goon4.png',
                                 'Vassal' : image_directory + '/vassal4.png',
                                 'BFF' : image_directory + '/bff4.png',
                                 'Secretary' : image_directory + '/secretary4.png',
                                 'Dog' : image_directory + '/dog4.png'}
        
        self.meditate_companions = {'Default' : image_directory + '/default5.png',
                                    'Butler' : image_directory + '/butler5.png',
                                    'Bro' : image_directory + '/bro5.png',
                                    'Goon' : image_directory + '/goon5.png',
                                    'Vassal' : image_directory + '/vassal5.png',
                                    'BFF' : image_directory + '/bff5.png',
                                    'Secretary' : image_directory + '/secretary5.png',
                                    'Dog' : image_directory + '/dog5.png'}
        
        # Dictionary of companion activity dictionaries
        self.master_dictionary = {'Take a Walk' : self.walk_companions,
                                  'Stretch' : self.stretch_companions,
                                  'Phone Time' : self.phone_companions,
                                  'Snack Time' : self.snack_companions,
                                  'Meditate' : self.meditate_companions}
        
        # Activity image dictionary
        self.activity_images = {'Take a Walk' : image_directory + '/walk.png',
                                'Stretch' : image_directory + '/stretch.png',
                                'Phone Time' : image_directory + '/phone.png',
                                'Snack Time' : image_directory + '/snack.png',
                                'Meditate' : image_directory + '/meditate.png'}
        
        
        
        
        # Set font style and size
        self.font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        self.font.SetPointSize(18)
        
        # Setup vbox
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        
        # hbox1 (countdown timer, picture of activity)
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Countdown timer text
        # Label gets updated by a function before Dialog is shown
        self.countdown_timer = wx.StaticText(self, label='00:00')
        self.countdown_timer.SetFont(self.font)
        
        # Timer object
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.countdownUpdate, self.timer)
        
        self.hbox1.Add(self.countdown_timer, 
                       flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,
                       border=40)
        
        # Activity picture (USING BRO PICTURE AS TEST/PLACEHOLDER)
        # NOTE: may need a dummy text panel for sizing
        self.activity_picture = wx.Image(image_directory + '/bro0.png',
                                         type=wx.BITMAP_TYPE_PNG)
        self.activity_final = self.activity_picture.ConvertToBitmap()
        self.activity_holder = wx.StaticBitmap(self, bitmap=self.activity_final)
        
        self.hbox1.Add(self.activity_holder,
                       flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,
                       border=20)
        
        # Add hbox1 to vbox
        self.vbox.Add(self.hbox1, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        
        
        # hbox2 (companion image, dismiss button)
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Companion activity image (USING BRO PICTURE AS TEST/PLACEHOLDER)
        # Image gets updated by a function before the Dialog is shown
        self.activity_companion = wx.Image(image_directory + '/bro0.png',
                                           type=wx.BITMAP_TYPE_PNG)
        self.companion_final = self.activity_companion.ConvertToBitmap()
        self.companion_holder = wx.StaticBitmap(self, 
                                                bitmap=self.companion_final)
        
        self.hbox2.Add(self.companion_holder, flag=wx.ALIGN_LEFT|wx.ALL, 
                       border=20)
        
        
        # Dismiss button
        self.dismiss_button = wx.Button(self, label='Dismiss', size=(100, 50))
        self.Bind(wx.EVT_BUTTON, self.onDismiss, self.dismiss_button)
        
        self.hbox2.Add(self.dismiss_button, flag=wx.ALIGN_RIGHT|wx.ALL,
                       border = 20)
        
        # Add hbox2 to vbox
        self.vbox.Add(self.hbox2, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        

        # Bind close event
        self.Bind(wx.EVT_CLOSE, self.onX)
        
        
        # Set sizer and fit
        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        
    
    
    # Function to update companion and activity images
    def updateImages(self, activity='Take a Walk', companion='Default'):
        
        
        # Set activity label
        self.SetLabel(activity)
        
        
        # Detach, destroy, and re-create contents of hbox1
        self.hbox1.Detach(self.countdown_timer)
        self.countdown_timer.Destroy()
        self.countdown_timer = wx.StaticText(self, label='00:00')
        self.countdown_timer.SetFont(self.font)
        
        self.hbox1.Detach(self.activity_holder)
        self.activity_holder.Destroy()
        self.activity_picture = wx.Image(self.activity_images[activity],
                                         type=wx.BITMAP_TYPE_PNG)
        self.activity_final = self.activity_picture.ConvertToBitmap()
        self.activity_holder = wx.StaticBitmap(self, bitmap=self.activity_final)
        
        # Detach, destroy and re-create hbox1
        self.vbox.Detach(self.hbox1)
        self.hbox1.Destroy()
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Re-add contents to hbox1
        self.hbox1.Add(self.countdown_timer, 
                       flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,
                       border=40)
        self.hbox1.Add(self.activity_holder,
                       flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,
                       border=20)
        
        # Re-add hbox1 to vbox
        self.vbox.Add(self.hbox1, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        
        
        # Detach, destroy, and re-create self.companion_holder
        self.hbox2.Detach(self.companion_holder)
        self.companion_holder.Destroy()
        self.activity_companion = wx.Image(self.master_dictionary[activity][companion],
                                           type=wx.BITMAP_TYPE_PNG)
        self.companion_final = self.activity_companion.ConvertToBitmap()
        self.companion_holder = wx.StaticBitmap(self, 
                                                bitmap=self.companion_final)
        
        # Detach, destroy, and re-create self.dismiss_button
        self.hbox2.Detach(self.dismiss_button)
        
        
        # Detach, destroy, and re-create hbox2
        self.vbox.Detach(self.hbox2)
        
        # Re-add contents back to hbox2
        self.hbox2.Add(self.companion_holder, flag=wx.ALIGN_LEFT|wx.ALL, 
                       border=20)
        self.hbox2.Add(self.dismiss_button, flag=wx.ALIGN_RIGHT|wx.ALL,
                       border = 20)
        
        # Re-add hbox2 to vbox
        self.vbox.Add(self.hbox2, flag=wx.ALIGN_CENTER|wx.ALL, border=5)
        
        # Set sizer and fit
        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        
        self.Layout()
        self.Refresh()
        
        
    # Function to play selected music
    def playMusic(self, music):
        winsound.PlaySound(music_directory + '/' + music, winsound.SND_ASYNC)
    
    
    # Function to stop selected music when Dialog is dismissed
    def stopMusic(self):
        winsound.PlaySound(None, winsound.SND_PURGE)
    
    
    # Function to start 'self.timer'
    def timeStart(self, number):
        self.decrement = timedelta(seconds=1)
        self.break_clock = timedelta(minutes=number)
        self.countdown_timer.SetLabel(str(self.break_clock))
        self.timer.Start(milliseconds=1000)
        
    
    # Bound to 'self.timer'
    def countdownUpdate(self, e):
        if self.break_clock.total_seconds() == 0:
            self.stopMusic()
            self.EndModal(1)
        self.break_clock -= self.decrement
        self.countdown_timer.SetLabel(str(self.break_clock))
    
    
    # Bound to 'Dismiss button'
    def onDismiss(self, e):
       self.stopMusic()
       self.EndModal(1)
       
       
    # Bound to 'X' on top right of Dialog
    def onX(self, e):
        self.stopMusic()
        self.EndModal(1)
    
    
        
# Create the notes panel
class NotesPanel(wx.Panel):
    
    def __init__(self, *args, **kwargs):
        super(NotesPanel, self).__init__(*args, **kwargs)
        
        
        # Set label font
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(12)
       
        
        # Working directory will be set to current_profile/Notes when clicking
        # the Notes button from the MainPanel
        self.notes_path = os.getcwd()
            
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        
        
        # Dummy text panel for additional spacing
        self.dummy1 = wx.StaticText(self, label='')
        
        
        # hbox1 (note entry and note explorer)
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Note entry
        self.note_entry = wx.TextCtrl(self, name='Note Entry',
                                      style=wx.TE_NO_VSCROLL|wx.TE_MULTILINE)
        self.hbox1.Add(self.note_entry, 1, 
                  flag=wx.ALIGN_LEFT|wx.LEFT|wx.TOP|wx.RIGHT|wx.EXPAND,
                  border=10)
        
        # Add dummy1 for spacing
        self.hbox1.Add(self.dummy1, 0, flag=wx.LEFT|wx.EXPAND, border=20)
        
        
        # Note explorer
        # NEEDS UPDATED AFTER global notes_path created
        self.note_explorer = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.note_explorer.InsertColumn(0, 'Filename')
        self.notes_files = glob.glob(self.notes_path + '/*.txt')
        for index, path in enumerate(self.notes_files):
            self.note_explorer.InsertItem(index,
                                          os.path.basename(path))
        self.hbox1.Add(self.note_explorer, 1,
                  flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.TOP|wx.EXPAND,
                  border=10)
        
        
        # Add hbox1 to the vbox
        self.vbox.Add(self.hbox1, 1, flag=wx.EXPAND, border=15)
        
        
        # hbox2 (clear button, save button, delete button, read button)
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        
        
        # Dummy text panels for additional spacing
        dummy2 = wx.StaticText(self, label='')
        
        
        # Clear button
        self.clear_button = wx.Button(self, label='Clear Text', size=(100, 50))
        self.Bind(wx.EVT_BUTTON, self.onClear, self.clear_button)
        self.hbox2.Add(self.clear_button, 0, flag=wx.LEFT|wx.TOP|wx.RIGHT,
                  border=10)
        
        # Save button
        self.save_button = wx.Button(self, label='Save Note', size=(100,50))
        self.Bind(wx.EVT_BUTTON, self.onSave, self.save_button)
        self.hbox2.Add(self.save_button, 0, flag=wx.TOP|wx.LEFT, border=10)
        
        
        # Add dummy2 for spacing
        self.hbox2.Add(dummy2, 0, flag=wx.LEFT|wx.EXPAND, border=30)
        
        
        # Delete button
        self.delete_button = wx.Button(self, label='Delete Note', size=(100,50))
        self.Bind(wx.EVT_BUTTON, self.onDelete, self.delete_button)
        self.hbox2.Add(self.delete_button, 0, flag=wx.TOP|wx.RIGHT, border=10)
        
        # Read button
        self.read_button = wx.Button(self, label='Read Note', size=(100,50))
        self.Bind(wx.EVT_BUTTON, self.onRead, self.read_button)
        self.hbox2.Add(self.read_button, 0, flag=wx.LEFT|wx.TOP|wx.RIGHT, border=10)
        
        
        # Add self.hbox2 to vbox
        self.vbox.Add(self.hbox2, 1, flag=wx.ALL|wx.SHAPED, border=5)
        
        
        # Additional spacing
        self.vbox.Add((-1, 20))
        
                 
        
        # hbox3 (main menu button)
        self.hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Main menu button
        self.menu_button = wx.Button(self, label='Main Menu', size=(100,70))
        self.Bind(wx.EVT_BUTTON, self.onMenu, self.menu_button)
        self.hbox3.Add(self.menu_button, 0, 
                  flag=wx.ALL|wx.ALIGN_BOTTOM|wx.SHAPED, border=10)
        
        
        # Add hbox3 to vbox
        self.vbox.Add(self.hbox3, 0, flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM, border=10)
        
        
        # Bind size event
        self.Bind(wx.EVT_SIZE, self.onSize)
        
        
        # Set sizer and fit
        self.SetSizer(self.vbox)
        self.vbox.Fit(self)
        
     
    # Bound to 'Clear Text' button
    def onClear(self, e):
        self.note_entry.SetValue('')
        
    # Bound to 'Save Note' button
    def onSave(self, e):
       save_popup = wx.TextEntryDialog(self, 'Enter Filename',
                                       caption='Save Note',
                                       style=wx.OK|wx.CANCEL)
       save_choice = save_popup.ShowModal()
       if save_choice == wx.ID_OK:
           global notes_path
           os.chdir(notes_path)
           self.note_title = save_popup.GetValue() + '.txt'
           self.note_entry.SaveFile(filename=self.note_title)
           self.note_explorer.DeleteAllItems()
           self.notes_files = glob.glob(notes_path + '/*.txt')
           for index, path in enumerate(self.notes_files):
               self.note_explorer.InsertItem(index,
                                             os.path.basename(path))
           self.note_entry.SetValue('')
       else:
           pass
   
    # Bound to 'Delete Note' button
    def onDelete(self, e):
        selected_note = self.note_explorer.GetFirstSelected()
        if selected_note == -1:
            wx.MessageBox('Please select a note', 'Error: No note selected',
                          wx.OK|wx.ICON_ERROR)
        else:
            delete_pUp = wx.MessageDialog(self,
                                          'Do you really want to delete this note?',
                                          caption='WARNING',
                                          style=wx.YES_NO|wx.NO_DEFAULT|wx.ICON_WARNING)
            delete_choice = delete_pUp.ShowModal()
            if delete_choice == wx.ID_YES:
                global notes_path
                delete_item = self.note_explorer.GetItemText(selected_note)
                delete_path = notes_path + '/' + delete_item
                os.remove(delete_path)
                self.note_explorer.DeleteAllItems()
                self.notes_files = glob.glob(notes_path + '/*.txt')
                for index, path in enumerate(self.notes_files):
                    self.note_explorer.InsertItem(index,
                                                  os.path.basename(path))
            else:
                pass
    
    # Bound to 'Read Note' button
    def onRead(self, e):
        selected_note = self.note_explorer.GetFirstSelected()
        if selected_note == -1:
            wx.MessageBox('Please select a note', 'Error: No note selected',
                          wx.OK|wx.ICON_ERROR)
        else:
            global notes_path
            read_item = self.note_explorer.GetItemText(selected_note)
            read_path = notes_path + '/' + read_item
            open_note = open(read_path, 'r')
            note_contents = open_note.read()
            reading_note = GMD.GenericMessageDialog(self, note_contents,
                                                    read_item,
                                                    agwStyle=wx.ICON_INFORMATION|wx.OK)
            reading_note.ShowModal()
            open_note.close()
            
     
    # Size event function
    def onSize(self, e):
        self.Refresh()
        self.Layout()
            
            
    # Function to update the self.notes_path with global notes_path
    # and update self.note_explorer
    def updatePath(self):
        try:
            global notes_path
            os.chdir(notes_path)
            
            # Detach, destroy, and re-create items in self.hbox1
            self.hbox1.Detach(self.note_entry)
            self.note_entry.Destroy()
            self.note_entry = wx.TextCtrl(self, name='Note Entry',
                                          style=wx.TE_NO_VSCROLL|wx.TE_MULTILINE)
            self.hbox1.Detach(self.dummy1)
            self.dummy1.Destroy()
            self.dummy1 = wx.StaticText(self, label='')
            self.hbox1.Detach(self.note_explorer)
            self.note_explorer.Destroy()
            self.note_explorer = wx.ListCtrl(self, style=wx.LC_REPORT)
            self.note_explorer.InsertColumn(0, 'Filename')
            self.notes_files = glob.glob(notes_path + '/*.txt')
            for index, path in enumerate(self.notes_files):
                self.note_explorer.InsertItem(index,
                                              os.path.basename(path))
            
            # Detach, destroy, and re-create self.hbox1
            self.vbox.Detach(self.hbox1)
            self.hbox1.Destroy()
            self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
            # Add items back to hbox1
            self.hbox1.Add(self.note_entry, 1, 
                  flag=wx.ALIGN_LEFT|wx.LEFT|wx.TOP|wx.RIGHT|wx.EXPAND,
                  border=10)
            self.hbox1.Add(self.dummy1, 0, flag=wx.LEFT|wx.EXPAND, border=20)
            self.hbox1.Add(self.note_explorer, 1,
                      flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.TOP|wx.EXPAND,
                      border=10)
            self.vbox.Add(self.hbox1, 1, flag=wx.EXPAND, border=15)
            
            # Detach and re-attach the remaining hboxes to maintain layout
            self.vbox.Detach(self.hbox2)
            self.vbox.Add(self.hbox2, 1, flag=wx.ALL|wx.SHAPED, border=5)
            self.vbox.Detach(self.hbox3)
            self.vbox.Add(self.hbox3, 0, flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM, 
                          border=10)
            
            self.Layout()
            self.Refresh()
        except:
            print("It didn't work. Fix it")
            
            
    
    # Bound to 'Main Menu' button
    def onMenu(self, e):
        self.Hide()
        main_panel.Show()
        main_panel.PostSizeEvent()
        app_window.PostSizeEvent()
    
    
# Create the profile pop up Window
class ProfilePopup(wx.PopupTransientWindow):
    
    def __init__(self, *args, **kwargs):
        super(ProfilePopup, self).__init__(*args, **kwargs)
        
        
        # Get display size
        self.d_size = wx.GetDisplaySize()
        
        # Get width and height divided by appropriate floats
        self.x_size = self.d_size[0] / 4.2
        self.y_size = self.d_size[1] / 3
        
        # Create wx.Point variable
        self.true_size = wx.Point(self.x_size, self.y_size)
        
        
        # Set size of popup
        self.SetSize((300, 300))
        
        
        # Set position of popup
        self.SetPosition(self.true_size)
        
        
        # Create vbox
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # hbox1 (ListCtrl showing available profiles)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Profile list
        self.profile_explorer = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.profile_explorer.InsertColumn(0, 'Profile Name')
        self.profiles = [x.name for x in os.scandir(profile_directory) if x.is_dir()]
        for index, profile in enumerate(self.profiles):
            self.profile_explorer.InsertItem(index, profile)
            
            
        
        # Add self.profile_explorer to hbox1
        hbox1.Add(self.profile_explorer, 1, flag=wx.ALL|wx.EXPAND, border=10)
        
        
        # Add hbox1 to vbox
        vbox.Add(hbox1, 1, flag=wx.ALL|wx.EXPAND, border=10)
        
        
        #hbox2 (Ok button)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        
        # Ok button
        self.ok_button = wx.Button(self, label='OK', size=(80,40))
        self.Bind(wx.EVT_BUTTON, self.onOk, self.ok_button)
        
        # Add OK button to hbox2
        hbox2.Add(self.ok_button, flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM, 
                  border=10)
        
        
        # Add hbox2 to vbox
        vbox.Add(hbox2, flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM|wx.ALL, border=10)
        
        # Set sizer and fit
        self.SetSizer(vbox)
        self.Layout()
        
        
    # Bound to 'OK' button
    def onOk(self, e):
        profile_choice = self.profile_explorer.GetFirstSelected()
        if self.profile_explorer.GetItemCount() == 0:
            self.Dismiss()
            reg_panel.Hide()
            break_panel.Hide()
            notes_panel.Hide()
            main_panel.updateCompanion()
            main_panel.Show()
            main_panel.PostSizeEvent()
            app_window.PostSizeEvent()
        elif profile_choice == -1:
            wx.MessageBox('Please select a profile', 'Error: No profile selected',
                          wx.OK|wx.ICON_ERROR)
        else:
            global profile_directory
            self.profile_selected = self.profile_explorer.GetItemText(profile_choice)
            global current_profile_dir
            current_profile_dir = profile_directory + '/' + self.profile_selected
            os.chdir(current_profile_dir)
            global notes_path
            notes_path = current_profile_dir + '/Notes'
            if not os.path.exists(notes_path):
                os.makedirs(notes_path)
            global break_path
            break_path = current_profile_dir + '/Breaks'
            if not os.path.exists(break_path):
                os.makedirs(break_path)
                
            # Set background color according to profile if able
            try:
                with open('color.txt', 'r') as color_file:
                    bg_color = color_file.read().rstrip('\n')
                for child in app_window.Children:
                    child.SetBackgroundColour((240, 240, 240))
                    child.Refresh()
                app_window.SetBackgroundColour(app_window.color_dict[bg_color])
                app_window.Refresh()
            except:
                pass
                
            # Prepare to check if it is profile's birthday
            self.current = datetime.now()
            self.current = self.current.strftime("%b%d")
            with open('birthday.txt', 'r') as bf:
                self.bday_value = bf.read()
            with open('companion.txt', 'r') as cf:
                self.companion = cf.read().rstrip('\n')
            self.bday_value = datetime.strptime(self.bday_value, 
                                                "%a %b %d %H:%M:%S %Y")
            self.bday_value = self.bday_value.strftime("%b%d")
            
            # Dismiss self, update and show main_panel
            self.Dismiss()
            reg_panel.Hide()
            break_panel.Hide()
            notes_panel.Hide()
            main_panel.updateCompanion()
            main_panel.Show()
            main_panel.PostSizeEvent()
            app_window.PostSizeEvent()
            if self.current == self.bday_value:
                main_panel.birthdayShow(self.profile_selected, self.companion)
            




# Create the main app window/frame
class MainFrame(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
        
        self.InitUI()
        
        
    def InitUI(self):
        
        # Set icon
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap(image_directory + '/icon.png',
                                           wx.BITMAP_TYPE_PNG))
        self.SetIcon(self.icon)

        
        menubar = wx.MenuBar()
        
        # Add main menu and companion submenu
        mainMenu = wx.Menu()
        changeProfile = wx.Menu()
        select = changeProfile.Append(wx.ID_ANY, 'Select Profile')
        self.Bind(wx.EVT_MENU, self.onSelect, select)
        register = changeProfile.Append(wx.ID_ANY, 'Register New Profile')
        self.Bind(wx.EVT_MENU, self.onRegister, register)
        mainMenu.AppendSubMenu(changeProfile, 'Change Profile')
        
        compStyle = wx.Menu()
        default = compStyle.Append(wx.ID_ANY, 'Default')
        self.Bind(wx.EVT_MENU,
                  partial(self.onCompanion, default.GetItemLabelText()), default)
        butler = compStyle.Append(wx.ID_ANY, 'Butler')
        self.Bind(wx.EVT_MENU,
                  partial(self.onCompanion, butler.GetItemLabelText()), butler)
        bro = compStyle.Append(wx.ID_ANY, 'Bro')
        self.Bind(wx.EVT_MENU,
                  partial(self.onCompanion, bro.GetItemLabelText()), bro)
        goon = compStyle.Append(wx.ID_ANY, 'Goon')
        self.Bind(wx.EVT_MENU,
                  partial(self.onCompanion, goon.GetItemLabelText()), goon)
        vassal = compStyle.Append(wx.ID_ANY, 'Vassal')
        self.Bind(wx.EVT_MENU,
                  partial(self.onCompanion, vassal.GetItemLabelText()), vassal)
        bff = compStyle.Append(wx.ID_ANY, 'BFF')
        self.Bind(wx.EVT_MENU,
                  partial(self.onCompanion, bff.GetItemLabelText()), bff)
        sec = compStyle.Append(wx.ID_ANY, 'Secretary')
        self.Bind(wx.EVT_MENU,
                  partial(self.onCompanion, sec.GetItemLabelText()), sec)
        dog = compStyle.Append(wx.ID_ANY, 'Dog')
        self.Bind(wx.EVT_MENU,
                  partial(self.onCompanion, dog.GetItemLabelText()), dog)
        mainMenu.AppendSubMenu(compStyle, 'Companion Style')
        
        
        # Create color database object
        self.cd = wx.ColourDatabase()
        
        # Create custom colors
        standard_cust = wx.Colour(170, 170, 170)
        dark_red_cust = wx.Colour(170, 30, 30)
        goldenrod_cust = wx.Colour(215, 190, 100)
        
        # Create the color dictionary
        self.color_dict = {'Standard' : standard_cust,
                           'Steel Blue' : self.cd.Find('STEEL BLUE'),
                           'Dark Red' : dark_red_cust,
                           'Forest Green' : self.cd.Find('FOREST GREEN'),
                           'Sea Green' : self.cd.Find('SEA GREEN'),
                           'Goldenrod' : goldenrod_cust,
                           'Maroon' : self.cd.Find('MAROON'),
                           'Tan' : self.cd.Find('TAN'),
                           'Black' : self.cd.Find('BLACK')}
        
        # Create key and value lists for self.color_dict
        self.key_list = list(self.color_dict.keys())
        self.value_list = list(self.color_dict.values())
        
        # Add 'Color' submenu
        backColor = wx.Menu()
        standard = backColor.Append(wx.ID_ANY, 'Standard')
        steel_blue = backColor.Append(wx.ID_ANY, 'Steel Blue')
        dark_red = backColor.Append(wx.ID_ANY, 'Dark Red')
        forest_green = backColor.Append(wx.ID_ANY, 'Forest Green')
        sea_green = backColor.Append(wx.ID_ANY, 'Sea Green')
        goldenrod = backColor.Append(wx.ID_ANY, 'Goldenrod')
        maroon = backColor.Append(wx.ID_ANY, 'Maroon')
        tan = backColor.Append(wx.ID_ANY, 'Tan')
        black = backColor.Append(wx.ID_ANY, 'Black')
        mainMenu.AppendSubMenu(backColor, 'Background Color')
        self.Bind(wx.EVT_MENU,
                  partial(self.onColor, self.color_dict['Standard']), standard)
        self.Bind(wx.EVT_MENU,
                  partial(self.onColor, self.color_dict['Steel Blue']), steel_blue)
        self.Bind(wx.EVT_MENU,
                  partial(self.onColor, self.color_dict['Dark Red']), dark_red)
        self.Bind(wx.EVT_MENU,
                  partial(self.onColor, self.color_dict['Forest Green']), forest_green)
        self.Bind(wx.EVT_MENU,
                  partial(self.onColor, self.color_dict['Sea Green']), sea_green)
        self.Bind(wx.EVT_MENU,
                  partial(self.onColor, self.color_dict['Goldenrod']), goldenrod)
        self.Bind(wx.EVT_MENU,
                  partial(self.onColor, self.color_dict['Maroon']), maroon)
        self.Bind(wx.EVT_MENU,
                  partial(self.onColor, self.color_dict['Tan']), tan)
        self.Bind(wx.EVT_MENU,
                  partial(self.onColor, self.color_dict['Black']), black)
        
        mainMenu.AppendSeparator()
        
        menuItem3 = mainMenu.Append(wx.ID_EXIT, 'Quit')
        self.Bind(wx.EVT_MENU, self.onQuit, menuItem3)
        
        menubar.Append(mainMenu, 'Menu')
        
        
        # Add 'Help' menu
        helpMenu = wx.Menu()
        
        documentation = helpMenu.Append(wx.ID_ANY, 'Documentation')
        self.Bind(wx.EVT_MENU, self.onDoc, documentation)
        problem = helpMenu.Append(wx.ID_ANY, 'Report a Problem')
        self.Bind(wx.EVT_MENU, self.onProblem, problem)
        helpMenu.AppendSeparator()
        about = helpMenu.Append(wx.ID_ANY, 'About')
        self.Bind(wx.EVT_MENU, self.onAbout, about)
        
        menubar.Append(helpMenu, 'Help')
        
        self.SetMenuBar(menubar)
        
        # Bind size event
        self.Bind(wx.EVT_SIZE, self.onSize)
        
        # Bind close event
        self.Bind(wx.EVT_CLOSE, self.onX)
        
        
        
        self.SetInitialSize((400, 400))
        self.SetTitle('Work Companion (Beta)')
        self.Centre()
        
        # Create layout sizer
        self.layout_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Opening expand
        self.layout_sizer.Add((0,0), 1, wx.EXPAND)
        
        
        global profile_select
        profile_select = ProfilePopup(self)
        
        global reg_panel
        reg_panel = RegPanel(self)
        self.layout_sizer.Add(reg_panel, 0, wx.CENTER)
        
        global profile_directory
        if len(os.listdir(profile_directory)) == 0:
            reg_panel.Layout()
            reg_panel.Refresh()
            reg_panel.Show()
        else:
            profile_select.Show()
            reg_panel.Hide()
            
        global break_panel
        break_panel = BreakPanel(self)
        break_panel.Hide()
        self.layout_sizer.Add(break_panel, 0, wx.CENTER)
        break_panel.Layout()
        
        global notes_panel
        notes_panel = NotesPanel(self)
        notes_panel.Hide()
        self.layout_sizer.Add(notes_panel, 0, wx.CENTER)
        notes_panel.Layout()
        
        global main_panel
        main_panel = MainPanel(self)
        main_panel.Hide()
        self.layout_sizer.Add(main_panel, 0, wx.CENTER)
        main_panel.Layout()
        
        
        # Closing expand
        self.layout_sizer.Add((0,0), 1, wx.EXPAND)
        
        
        # Set sizer and fit for MainFrame
        self.SetSizer(self.layout_sizer)
        self.layout_sizer.Fit(self)
        
    
    # Bound to 'Select Profile' under 'Change Profile'. Lets user change 
    # profile if there are multiple profiles available
    def onSelect(self, e):
        if len(os.listdir(profile_directory)) == 0:
            wx.MessageBox('No profiles found. Please register a profile')
        else:
            profile_select.Show()
    
    
    # Bound to 'Register New Profile' under 'Change Profile'. Opens the
    # 'Registration' frame
    def onRegister(self, e):
        break_panel.Hide()
        notes_panel.Hide()
        main_panel.Hide()
        reg_panel.name_entry.SetValue('')
        reg_panel.bday_entry.SetValue(wx.DateTime.Now())
        reg_panel.Show()
        reg_panel.PostSizeEvent()
        self.PostSizeEvent()
        
    
    # Bound to all items in 'Companion Style'
    def onCompanion(self, comp, e):
        global current_profile_dir
        os.chdir(current_profile_dir)
        with open('companion.txt', 'w') as cmp:
            cmp.write(comp)
        main_panel.updateCompanion()
        
        
    # Bound to all items in 'Color'
    def onColor(self, color, e):
        for child in self.Children:
            child.SetBackgroundColour((240, 240, 240))
            child.Refresh()
        self.SetBackgroundColour(color)
        self.Refresh()
        try:
            global current_profile_dir
            os.chdir(current_profile_dir)
            with open('color.txt', 'w') as color_file:
                color_file.write(self.key_list[self.value_list.index(color)])
        except:
            pass
        
        
    # Size event
    def onSize(self, e):
        self.size = e.GetSize()
        self.SetSize((self.size.width, self.size.height))
        self.Refresh()
        self.Layout()
        
    
    # Bound to 'Quit' under 'Menu'. Exits the application
    def onQuit(self, e):
        self.DestroyChildren()
        self.Destroy()
    
    
    # Bound to 'Documentation' under 'Help'. Opens web browser to doc page.
    def onDoc(self, e):
        webbrowser.open('https://github.com/coy0tecode/Work-Companion/blob/main/documentation.txt')
    
    
    # Bound to 'Report a Problem' under 'Help'. Opens default mail application
    # with "to" field filled in with email specific to app
    def onProblem(self, e):
        win32api.ShellExecute(0, 'open', 'mailto: mjt5224@gmail.com', 
                              None, None, 0)
    
    
    # Bound to 'About' under 'Help'. Opens a pop up window with the app's
    # most up to date information
    def onAbout(self, e):
        app_info = GMD.GenericMessageDialog(self, 'Version: 0.2\n'
                                            'Author: coy0tecode\n'
                                            'License: MIT License\n'
                                            'Supported OS: Windows 10\n',
                                            'About Work Companion',
                                            agwStyle=wx.ICON_INFORMATION
                                            | wx.OK)
        app_info.ShowModal()
        
    
    
    # Bound to wx.EVT_CLOSE
    def onX(self, e):
        dial = wx.MessageDialog(None, 'Quit Work Companion?', 'Exit Program?',
                                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = dial.ShowModal()
        if ret == wx.ID_YES:
            self.DestroyChildren()
            self.Destroy()
        else:
            e.Veto()
    
    
        
        
def main():
    app = wx.App()
    global app_window
    app_window = MainFrame(None)
    app_window.Show()
    app.MainLoop()
    
if __name__ == "__main__":
    main()
        
