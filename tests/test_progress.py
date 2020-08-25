import unittest
from test.support import captured_stdout
from janome.progress import SimpleProgressIndicator


class TestProgress(unittest.TestCase):
    def test_simple_progress_indicator(self):
        total = 22
        desc = "Test loop"

        # create SimpleProgressIndicator, print once in 10 times update
        progress_indicator = SimpleProgressIndicator(update_frequency=0.1)

        # initialize
        progress_indicator.on_start(
            total=total,
            desc=desc)

        self.assertEqual(total, progress_indicator.total)
        self.assertEqual(0, progress_indicator.value)
        self.assertEqual(desc, progress_indicator.desc)

        # progress 1 / total 22
        with captured_stdout() as stdout:
            progress_indicator.on_progress()
            print("")
            # progress to 1 but nothing printed (frequency=0.1)
            self.assertEqual(1, progress_indicator.value)
            self.assertEqual("", stdout.getvalue().strip())

        with captured_stdout() as stdout:
            progress_indicator.on_progress(8)
            print("")
            # progress to 9 but still nothing printed
            self.assertEqual(9, progress_indicator.value)
            self.assertEqual("", stdout.getvalue().strip())

        with captured_stdout() as stdout:
            progress_indicator.on_progress(1)
            print("")
            # progress to 10 and printed (frequency=0.1)
            self.assertEqual(10, progress_indicator.value)
            stdout_value = stdout.getvalue()
            self.assertIn(desc, stdout_value)
            self.assertIn("10/22", stdout_value)

        with captured_stdout() as stdout:
            progress_indicator.on_progress(10)
            print("")
            # progress to 20 and printed
            self.assertEqual(20, progress_indicator.value)
            stdout_value = stdout.getvalue()
            self.assertIn(desc, stdout_value)
            self.assertIn("20/22", stdout_value)

        with captured_stdout() as stdout:
            progress_indicator.on_progress(2)
            print("")
            # progress to 22 but nothing printed
            self.assertEqual(22, progress_indicator.value)
            self.assertEqual("", stdout.getvalue().strip())

        with captured_stdout() as stdout:
            progress_indicator.on_complete()
            stdout_value = stdout.getvalue()
            # printed after on_complete regardless of frequency
            self.assertIn(desc, stdout_value)
            self.assertIn("22/22", stdout_value)
            self.assertIn("100.0%", stdout_value)
