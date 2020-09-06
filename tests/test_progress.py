import unittest
from janome.progress import SimpleProgressIndicator, logger as p_logger


class TestProgress(unittest.TestCase):
    def test_simple_progress_indicator(self):
        total = 22
        desc = 'Test loop'

        # create SimpleProgressIndicator, print once in 10 times update
        progress_indicator = SimpleProgressIndicator(update_frequency=0.1)

        # initialize
        progress_indicator.on_start(
            total=total,
            desc=desc)

        self.assertEqual(total, progress_indicator.total)
        self.assertEqual(0, progress_indicator.value)
        self.assertEqual(desc, progress_indicator.desc)

        with self.assertLogs(logger=p_logger) as cm:
            # progress to 1 but no outputs (frequency=0.1)
            progress_indicator.on_progress()
            self.assertEqual(1, progress_indicator.value)
            self.assertEqual(0, len(cm.output))

            # progress to 9 but still no outputs
            progress_indicator.on_progress(8)
            self.assertEqual(9, progress_indicator.value)
            self.assertEqual(0, len(cm.output))

            # progress to 10 then 1 output (frequency=0.1)
            progress_indicator.on_progress(1)
            self.assertEqual(10, progress_indicator.value)
            self.assertEqual(1, len(cm.output))
            self.assertIn(desc, cm.output[0])
            self.assertIn('10/22', cm.output[0])

            # progress to 20, 2 outputs
            progress_indicator.on_progress(10)
            self.assertEqual(20, progress_indicator.value)
            self.assertEqual(2, len(cm.output))
            self.assertIn(desc, cm.output[1])
            self.assertIn('20/22', cm.output[1])

            # progress to end but no additinonal outputs
            progress_indicator.on_progress(2)
            self.assertEqual(22, progress_indicator.value)
            self.assertEqual(2, len(cm.output))

            # output after on_complete regardless of frequency
            progress_indicator.on_complete()
            self.assertIsNone(progress_indicator.value)  # value reset after complete
            self.assertEqual(3, len(cm.output))
            self.assertIn(desc, cm.output[2])
            self.assertIn('22/22', cm.output[2])
            self.assertIn('100.0%', cm.output[2])
