import unittest
import pymarkdownsplitter
import os
import shutil

TEST_RESOURCES = "test/test_resources/"
TMP_WORK_DIR = "tmp_outdir/"

MANUAL_FILE = TMP_WORK_DIR + "manual.md"
INSERT_AND_UPDATE_FILE = TMP_WORK_DIR + "insert-and-update.md"
FIND_AND_QUERY_FILE = TMP_WORK_DIR + "find-and-query.md"
ENTITY_ADAPTER_AND_DESCRIPTOR_FILE = TMP_WORK_DIR + "entity-adapter-and-descriptor.md"


class PyMarkdownSplitterTest(unittest.TestCase):

    def setUp(self):
        if os.path.isdir(TMP_WORK_DIR):
            shutil.rmtree(TMP_WORK_DIR)

    def assertFileContainsText(self, filename, text):
        with open(filename, 'r') as f:
            self.assertTrue(text in f.read())

    def assertFileExistsAndContainsText(self, filename, text):
        self.assertTrue(os.path.isfile(filename))
        self.assertFileContainsText(filename, text)

    def testComprehensiveFile(self):
        """Test a comprensive file"""
        pymarkdownsplitter.work(TEST_RESOURCES + "manual_comprehensive.md", TMP_WORK_DIR)

        # Test Index File
        self.assertFileExistsAndContainsText(MANUAL_FILE, "[Find and Query](find-and-query.html)")
        self.assertFileExistsAndContainsText(MANUAL_FILE, "[Insert and Update](insert-and-update.html)")
        self.assertFileExistsAndContainsText(MANUAL_FILE, "[Entity, Adapter, and Descriptor](entity-adapter-and-descriptor.html)")
        # Test correct heading for sub-section files
        self.assertFileExistsAndContainsText(INSERT_AND_UPDATE_FILE, "% Insert and Update")
        # Test local link to global link conversion
        self.assertFileExistsAndContainsText(FIND_AND_QUERY_FILE, "[local link](insert-and-update.html)")
        self.assertFileExistsAndContainsText(FIND_AND_QUERY_FILE, "[local link](entity-adapter-and-descriptor.html)")

        # Test for correct section links
        self.assertFileContainsText(FIND_AND_QUERY_FILE, "[&uarr; Index](manual.html)")
        self.assertFileContainsText(FIND_AND_QUERY_FILE, "[Next Section &rarr;](insert-and-update.html)")

        self.assertFileContainsText(INSERT_AND_UPDATE_FILE, "[&larr; Previous Section](find-and-query.html)")
        self.assertFileContainsText(INSERT_AND_UPDATE_FILE, "[Next Section &rarr;](entity-adapter-and-descriptor.html)")

        self.assertFileExistsAndContainsText(ENTITY_ADAPTER_AND_DESCRIPTOR_FILE, "[&larr; Previous Section](insert-and-update.html)")


if __name__ == '__main__':
    unittest.main()
