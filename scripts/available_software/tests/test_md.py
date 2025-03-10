from mdutils.mdutils import MdUtils
from available_software import get_unique_software_names, modules_eessi, generate_table_data, generate_module_table
from available_software import generate_detail_pages
import os
import filecmp
import shutil


class TestMarkdown:
    # ---------------------------
    # Class level setup/teardown
    # ---------------------------

    path = os.path.dirname(os.path.realpath(__file__))

    @classmethod
    def setup_class(cls):
        os.environ["TESTS_PATH"] = cls.path
        os.environ["LMOD_CMD"] = cls.path + "/data/lmod_mock.sh"
        os.environ["MOCK_FILE_SWAP"] = cls.path + "/data/data_swap_TARGET.txt"
        os.environ["MOCK_FILE_AVAIL_TARGET"] = cls.path + "/data/data_avail_target_simple.txt"

    @classmethod
    def teardown_class(cls):
        if os.path.exists("test_simple.md"):
            os.remove("test_simple.md")
        if os.path.exists("detailed_md"):
            shutil.rmtree("detailed_md")

    # ---------------------------
    # Markdown tests
    # ---------------------------

    def test_table_generate_simple(self):
        simple_data = get_unique_software_names(modules_eessi())
        table_data, col, row = generate_table_data(simple_data)
        assert col == 3
        assert row == 5
        assert len(table_data) == 15

    def test_md_simple(self):
        md_file = MdUtils(file_name='test_simple', title='Overview Modules')
        simple_data = get_unique_software_names(modules_eessi())
        generate_module_table(simple_data, md_file)
        md_file.create_md_file()
        assert os.path.exists("test_simple.md")
        assert filecmp.cmp(self.path + "/data/test_md_simple_sol.md", "test_simple.md")

    def test_md_detailed_template(self):
        os.environ["TIME_GENERATED_TEMPLATE"] = "{{ generated_date }}"
        os.mkdir('detailed_md')
        generate_detail_pages(self.path + "/data/test_json_simple_sol_detail.json", 'detailed_md')
        del os.environ["TIME_GENERATED_TEMPLATE"]
        assert os.path.exists("detailed_md/science.md")
        assert filecmp.cmp(self.path + "/data/test_md_template_detailed_science_sol.md", "detailed_md/science.md")
