import subprocess
import tempfile
from training import utils

class IngredientParser:
    def __init__(self, model_path):
        self.model_path = model_path

    def parse_file(self, ingredient_file):
        # Convert the ingredient file to the correct input, stored in a temp file
        _, tmp_file = tempfile.mkstemp()
        with open(ingredient_file, "r") as infile, open(tmp_file, "w") as outfile:
            outfile.write(utils.export_data(infile.readlines()))
        # Run the CRF model on the temp file input
        crf_result = subprocess.run(["crf_test", "-v", "1", "-m", "{}".format(self.model_path), "{}".format(tmp_file)], stdout=subprocess.PIPE, universal_newlines=True, check=True)
        # Remove the temp file
        subprocess.run(["rm", tmp_file], check=True)
        # No error, so let's take the result and transform it
        result_lines = [""]
        for char in crf_result.stdout:
            result_lines[-1] += char
            if char == "\n":
                result_lines.append("")
        return utils.import_data(result_lines)

