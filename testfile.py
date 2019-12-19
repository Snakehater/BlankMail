class TestFile():

    def __init__(self):
        import os
        import errno

        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY

        try:
            file_handle = os.open('logins.json', flags)
        except OSError as e:
            if e.errno == errno.EEXIST:  # Failed as the file already exists.
                savedJson = open('logins.json', "r").read()
                if savedJson == '':
                    with open('logins.json', 'w') as outfile:
                        outfile.write('[]')
            else:  # Something unexpected went wrong so reraise the exception.
                raise
        else:  # No exception, so the file must have been created successfully.
            with os.fdopen(file_handle, 'w') as file_obj:
                # Using `os.fdopen` converts the handle to an object that acts like a
                # regular Python file object, and the `with` context manager means the
                # file will be automatically closed when we're done with it.
                file_obj.write("[]")
