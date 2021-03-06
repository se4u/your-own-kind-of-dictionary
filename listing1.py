# vim: set expandtab ts=4 sw=4 filetype=python:

import unittest

class TestTaskAsString(unittest.TestCase):
    """
    This one is going to raise ERRORs because self.Task isn't defined.
    """

    def test_as_str_when_empty(self):
        """
        Convert an empty TaskDict to a string.
        """

        td = self.Task()
        s = str(td)

        assert s == 'Empty task', \
        """Expected 'Empty task', got %s!""" % s


    def test_as_str_with_data(self):

        """
        Convert a Task with stuff inside it into a string.
        """

        td = self.Task(title='Waterproof basement',
            expected_cost_range=[3000, 8000])

        s = str(td)

        expected_results = """\
Waterproof basement
===================

Attributes
----------

expected_cost_range            : [3000, 8000]
"""

        assert s == expected_results, \
        "Got %s, expected something different!" % s



class BogusTask(object):
    def __init__(self, *args, **kwargs):
        pass


class TestBogusTaskAsString(TestTaskAsString):
    """
    This one should fail, but not raise an error.
    """

    def setUp(self):
        self.Task = BogusTask

class UglyTask(dict):
    """
    Just like a dictionary, but with a modified __str__ method.
    """

    def __str__(self):
        if not self:
            return "Empty task"

        else:

            return "\n".join(
                [
                    self['title'],
                    "="*len(self['title']),
                    "",
                    "Attributes",
                    "-"*len("Attributes"),
                    ""]
                + [
                    "%-31s: %s" % (k, v)
                    for k, v in self.items()
                    if k != 'title']
                + [""]
                )


class TestUglyTaskAsString(TestTaskAsString):

    """
    This one should pass.
    """

    def setUp(self):
        self.Task = UglyTask



class RefactoredTask(UglyTask):

    newline = '\n'
    do_not_display_these_attributes = ['title']
    empty_display = 'Empty task'

    attributes_subtitle = "Attributes\n----------\n\n"

    @property
    def display_title(self):

        """
        Returns a string like

        <My Title>
        ==========

        But <My title> is this instance's title.
        """

        title = self['title']
        equalsigns = "=" * len(title)

        return "".join([title, self.newline, equalsigns, self.newline])


    @property
    def display_attributes(self):

        """
        Returns a string like

        Attributes
        ----------

        key1          : value for key1
        key2          : value for key2

        """

        attributes = ''.join(
            [self.display_single_attribute(k) for k in sorted(self)
                if k not in self.do_not_display_these_attributes])

        return ''.join([self.attributes_subtitle, attributes])

    def display_single_attribute(self, k):
        """
        Return a single string like

        k                 : value for k

        for key k.

        >>> t = RefactoredTask(title='bogus task', temperature=19)
        >>> t.display_single_attribute('temperature')
        'temperature                    : 19\n'
        """

        return '%-31s: %s\n' % (k, self[k])

    def __str__(self):

        if not self:
            return self.empty_display

        else:

            return ''.join([
                self.display_title,
                self.newline,
                self.display_attributes])


class TestRefactoredTaskAsString(TestTaskAsString):
    """
    This one should pass, and it verifies that when I rewrote the Task
    class __str__ method, I didn't break anything.
    """

    def setUp(self):
        self.Task = RefactoredTask


if __name__ == '__main__':
    unittest.main()
