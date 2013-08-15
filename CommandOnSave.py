from __future__ import print_function
import sublime
import sublime_plugin
import subprocess
import threading
import os

class CommandRunner(threading.Thread):
    def __init__(self, command):
        threading.Thread.__init__(self)
        self.command = command

    def run(self):
        # Fix this.
        print("Executing \"" + self.command + "\" ... ", end='')
        
        p = subprocess.Popen([self.command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, errors) = p.communicate()
        
        print('done.')

        if len(output) > 0:
            print('Output:')
            print(output)
        	
        if len(output) > 0 and len(errors) > 0:
		    print('')
        
        if len(errors) > 0:
            print('Errors:')
            print(errors)

class CommandOnSave(sublime_plugin.EventListener):
    def on_post_save(self, view):
        settings = view.settings()
        commands = settings.get("commands")
        current_filename = view.file_name()

        for entry in commands:
            if current_filename.endswith(entry.get("extension")):
                (base_filename, extension) = os.path.splitext(current_filename)

                command = entry.get("command")
                command = command.replace("$filename$", current_filename)
                command = command.replace("$filename_no_ext$", base_filename)
                
                t = CommandRunner(command)
                t.start()