import unittest
import pymarkdownsplitter
import os
import shutil

TEST_RESOURCES = "test/test_resources/"
TMP_WORK_DIR = "tmp_outdir/"


class PyMarkdownSplitterTest(unittest.TestCase):

    def setUp(self):
        if os.path.isdir(TMP_WORK_DIR):
            shutil.rmtree(TMP_WORK_DIR)

    def assertFileExistsAndContainsTest(self, filename, text):
        self.assertTrue(os.path.isfile(filename))
        with open(filename, 'r') as f:
            self.assertTrue(text in f.read())

    def testComprehensiveFile(self):
        """Test a comprensive file; creates two sub-section files, creates index file; converts local links to global links"""
        pymarkdownsplitter.work(TEST_RESOURCES + "manual_comprehensive.md", TMP_WORK_DIR)

        MANUAL_FILE = TMP_WORK_DIR + "manual.md"
        INSERT_AND_UPDATE_FILE = TMP_WORK_DIR + "insert-and-update.md"
        FIND_AND_QUERY_FILE = TMP_WORK_DIR + "find-and-query.md"

        # Test Index File
        self.assertFileExistsAndContainsTest(MANUAL_FILE, "[Find and Query](http://find-and-query.html)")
        self.assertFileExistsAndContainsTest(MANUAL_FILE, "[Insert and Update](http://insert-and-update.html)")
        # Test correct heading for sub-section files
        self.assertFileExistsAndContainsTest(INSERT_AND_UPDATE_FILE, "% Insert and Update")
        # Test local link to global link conversion
        self.assertFileExistsAndContainsTest(FIND_AND_QUERY_FILE, "[local link](http://insert-and-update.html)")
        self.assertFileExistsAndContainsTest(FIND_AND_QUERY_FILE, "[local link](http://blub-and-update.html)")


if __name__ == '__main__':
    unittest.main()
